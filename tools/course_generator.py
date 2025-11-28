#!/usr/bin/env python3
"""
Course batch generator - orchestrates end-to-end course generation.

Implements Phase 3A: `/generate-course` command
- Pre-flight validation (syllabus, research availability)
- Batch generation loop (all weeks)
- Phase 2 validation integration (flag checking)
- Slide export (Decision 3A - always export)
- Progress tracking with recovery support (Decision 1A)
- Skip failed weeks, continue (Decision 2B)
- Final report generation
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime

from .core_structures import (
    GenerationConfig,
    GenerationProgress,
    GenerationResult,
    GenerationReport,
    SkippedWeek,
    ValidationResult
)
from .progress_tracker import ProgressTracker
from .recovery_manager import RecoveryManager
from .content_generators import (
    LectureGenerator,
    TutorialGenerator,
    TutorNotesGenerator
)


class CourseGenerator:
    """Main orchestrator for batch course generation."""

    def __init__(self, course_code: str, course_path: Path):
        """
        Initialize course generator.

        Args:
            course_code: Course code (e.g., "BCI2AU")
            course_path: Path to course directory
        """
        self.course_code = course_code
        self.course_path = Path(course_path)
        self.config: Optional[GenerationConfig] = None
        self.tracker: Optional[ProgressTracker] = None
        self.completed_weeks: List[int] = []
        self.skipped_weeks: List[SkippedWeek] = []
        self.week_results: Dict[int, GenerationResult] = {}

    def run(self) -> GenerationReport:
        """
        Run batch course generation.

        Returns:
            GenerationReport with summary and any skipped weeks
        """
        print("=" * 65)
        print("BATCH COURSE GENERATION")
        print("=" * 65)
        print(f"Course: {self.course_code}")
        print(f"Path: {self.course_path}")
        print()

        # Step 1: Check for interrupted generation
        interrupted_progress = RecoveryManager.detect_interrupted_generation(self.course_path)

        if interrupted_progress:
            # Recovery mode
            print(RecoveryManager.format_recovery_prompt(interrupted_progress))

            # Ask user confirmation
            response = input("\nResume from interrupted generation? [Y/n]: ").strip().lower()
            if response in ['n', 'no']:
                print("\nStarting fresh generation...")
                RecoveryManager.cleanup_progress(self.course_path)
                interrupted_progress = None
            else:
                # Validate recovery
                should_resume, reason = RecoveryManager.should_resume(interrupted_progress)
                if not should_resume:
                    print(f"\n✗ Cannot resume: {reason}")
                    print("Starting fresh generation...")
                    RecoveryManager.cleanup_progress(self.course_path)
                    interrupted_progress = None
                else:
                    print(f"\n✓ {reason}")
                    print(RecoveryManager.format_recovery_confirmation())

        # Step 2: Pre-flight validation
        total_weeks = self.validate_and_configure(interrupted_progress)

        if total_weeks == 0:
            print("\n✗ Pre-flight validation failed. Cannot proceed.")
            sys.exit(1)

        # Step 3: Initialize progress tracker
        self.tracker = ProgressTracker(total_weeks=total_weeks, course_code=self.course_code)

        # If recovering, restore completed weeks
        if interrupted_progress:
            self.completed_weeks = interrupted_progress.completed_weeks.copy()
            self.tracker.completed = len(interrupted_progress.completed_weeks)
            self.tracker.week_times = interrupted_progress.week_times.copy()

        # Step 4: Determine weeks to generate
        weeks_to_generate = RecoveryManager.get_weeks_to_generate(interrupted_progress, total_weeks)

        print(f"\n{'Resuming' if interrupted_progress else 'Starting'} generation for {len(weeks_to_generate)} weeks...")
        print()

        # Step 5: Main generation loop
        for week_num in weeks_to_generate:
            try:
                # Check if this is the interrupted week (Decision 1A)
                is_interrupted_week = (interrupted_progress and
                                      week_num == interrupted_progress.current_week)

                result = self.generate_week(week_num, is_interrupted_week)

                if result.success:
                    self.completed_weeks.append(week_num)
                else:
                    # Decision 2B: Skip and continue
                    skipped = SkippedWeek(
                        week_number=week_num,
                        topic=result.topic or f"Week {week_num}",
                        reason="Validation failed" if result.validation_failed else "Generation failed",
                        errors=result.errors.copy(),
                        fix_instructions=self._generate_fix_instructions(result)
                    )
                    self.skipped_weeks.append(skipped)

                self.week_results[week_num] = result

                # Save progress after each week
                self._save_progress(week_num + 1)  # Next week to process

            except KeyboardInterrupt:
                print("\n\nGeneration interrupted by user.")
                print(f"Progress saved. Completed weeks: {self.completed_weeks}")
                print(f"Run `/generate-course {self.course_code}` to resume.")
                return self._create_partial_report("Interrupted by user")

            except Exception as e:
                print(f"\n✗ Unexpected error generating Week {week_num}: {e}")
                # Decision 2B: Skip and continue
                result = GenerationResult(
                    week_number=week_num,
                    success=False,
                    topic=f"Week {week_num}"
                )
                result.add_error(f"Unexpected error: {str(e)}")

                skipped = SkippedWeek(
                    week_number=week_num,
                    topic=f"Week {week_num}",
                    reason="Unexpected error",
                    errors=[str(e)],
                    fix_instructions="Check logs and try regenerating this week individually."
                )
                self.skipped_weeks.append(skipped)
                self.week_results[week_num] = result

        # Step 6: Cleanup and generate report
        RecoveryManager.cleanup_progress(self.course_path)

        # Display completion message
        print(self.tracker.display_completion_message())

        # Create final report
        report = self._create_final_report()

        # Save report
        report_path = self.course_path / "generation-report.md"
        report.save(report_path)
        print(f"\n✓ Report saved: {report_path}")

        return report

    def validate_and_configure(self, recovery_progress: Optional[GenerationProgress]) -> int:
        """
        Pre-flight validation and configuration.

        Args:
            recovery_progress: Optional recovery progress

        Returns:
            Total weeks to generate (0 if validation failed)
        """
        print("Pre-flight validation...")
        print()

        # Check syllabus exists
        syllabus_path = self.course_path / "syllabus.md"
        if not syllabus_path.exists():
            print(f"✗ Syllabus not found: {syllabus_path}")
            print("  Please run `/generate-syllabus` first.")
            return 0

        print(f"✓ Syllabus found: {syllabus_path}")

        # Count weeks from syllabus
        total_weeks = self._count_weeks_from_syllabus(syllabus_path)
        if total_weeks == 0:
            print("✗ Could not determine number of weeks from syllabus.")
            return 0

        print(f"✓ Course has {total_weeks} weeks")

        # Check research availability
        research_status = self._check_research_availability(total_weeks)

        if research_status["missing"]:
            print(f"\n⚠ Missing research for weeks: {', '.join(map(str, research_status['missing']))}")
            print("  These weeks will fail validation unless research is added.")

            response = input("\nContinue anyway? [y/N]: ").strip().lower()
            if response not in ['y', 'yes']:
                return 0

        # Create configuration
        if recovery_progress:
            # Use recovery config (Decision 1A)
            original_config = GenerationConfig(
                course_code=self.course_code,
                course_path=self.course_path,
                total_weeks=total_weeks
            )
            self.config = RecoveryManager.create_recovery_config(recovery_progress, original_config)
        else:
            # Fresh config
            self.config = GenerationConfig(
                course_code=self.course_code,
                course_path=self.course_path,
                total_weeks=total_weeks,
                export_slides=True,  # Decision 3A
                skip_on_validation_failure=True,  # Decision 2B
                regenerate_interrupted_week=True  # Decision 1A
            )

        return total_weeks

    def generate_week(self, week_num: int, is_interrupted_week: bool = False) -> GenerationResult:
        """
        Generate content for a single week.

        Args:
            week_num: Week number to generate
            is_interrupted_week: Whether this week was interrupted (Decision 1A)

        Returns:
            GenerationResult with success status and details
        """
        # Get topic from syllabus
        topic = self._get_week_topic(week_num)

        result = GenerationResult(
            week_number=week_num,
            success=False,
            topic=topic
        )

        # Display week header
        print(self.tracker.display_week_header(week_num, topic))

        if is_interrupted_week:
            from .recovery_manager import format_interrupted_week_message
            print(format_interrupted_week_message(week_num))

        self.tracker.start_week(week_num)

        # Step 1: Check/validate research (Phase 2 integration)
        print(self.tracker.display_step_progress(1, 7, "Checking research"))

        validation = self._check_and_validate_research(week_num)
        result.validation_result = validation

        if not validation.passed:
            result.add_error(f"Research validation failed: {validation.message}")
            result.validation_failed = True
            self.tracker.complete_week(week_num, success=False)
            print(f"\n✗ Week {week_num} skipped: Research validation failed")
            print(f"  Reason: {validation.message}")
            return result

        print(f"✓ Research validation passed")

        # Step 2: Generate lecture content
        print(self.tracker.display_step_progress(2, 7, "Generating lecture"))

        lecture_success, lecture_error = self._generate_lecture(week_num, topic)
        if not lecture_success:
            result.add_error(f"Lecture generation failed: {lecture_error}")
            self.tracker.complete_week(week_num, success=False)
            return result

        result.files_generated.append(f"lecture-content.md")
        print(f"✓ Lecture generated")

        # Step 3: Generate tutorial content
        print(self.tracker.display_step_progress(3, 7, "Generating tutorial"))

        tutorial_success, tutorial_error = self._generate_tutorial(week_num, topic)
        if not tutorial_success:
            result.add_error(f"Tutorial generation failed: {tutorial_error}")
            self.tracker.complete_week(week_num, success=False)
            return result

        result.files_generated.append(f"tutorial-content.md")
        print(f"✓ Tutorial generated")

        # Step 4: Generate tutor notes
        print(self.tracker.display_step_progress(4, 7, "Generating tutor notes"))

        notes_success, notes_error = self._generate_tutor_notes(week_num)
        if not notes_success:
            result.add_error(f"Tutor notes generation failed: {notes_error}")
            self.tracker.complete_week(week_num, success=False)
            return result

        result.files_generated.append(f"tutorial-tutor-notes.md")
        print(f"✓ Tutor notes generated")

        # Step 5: Export quiz
        print(self.tracker.display_step_progress(5, 7, "Exporting quiz"))

        quiz_success, quiz_error = self._export_quiz(week_num)
        if not quiz_success:
            result.add_warning(f"Quiz export failed: {quiz_error}")
        else:
            result.files_generated.append(f"week-{week_num}-quiz.gift")
            print(f"✓ Quiz exported")

        # Step 6: Export slides (Decision 3A - always export)
        print(self.tracker.display_step_progress(6, 7, "Exporting slides"))

        slides_success, slides_error = self._export_slides(week_num)
        if not slides_success:
            result.add_warning(f"Slide export failed: {slides_error}")
        else:
            result.files_generated.append(f"slides.html")
            print(f"✓ Slides exported")

        # Step 7: Complete
        print(self.tracker.display_step_progress(7, 7, "Finalizing"))

        elapsed = self.tracker.complete_week(week_num, success=True)
        result.success = True
        result.generation_time_minutes = elapsed

        print(f"\n✓ Week {week_num} complete ({elapsed:.1f} minutes)")
        print()

        return result

    def _count_weeks_from_syllabus(self, syllabus_path: Path) -> int:
        """Count total weeks from syllabus."""
        try:
            content = syllabus_path.read_text(encoding='utf-8')

            # Look for week markers in course calendar
            # Pattern: **Week 1**, **Week 2**, etc.
            import re
            week_matches = re.findall(r'\*\*Week (\d+)[:\-]', content)

            if week_matches:
                return max(int(w) for w in week_matches)

            # Fallback: count "Week N:" patterns
            week_patterns = re.findall(r'Week (\d+):', content)
            if week_patterns:
                return max(int(w) for w in week_patterns)

            return 0

        except Exception as e:
            print(f"Error reading syllabus: {e}")
            return 0

    def _get_week_topic(self, week_num: int) -> str:
        """Get week topic from syllabus."""
        try:
            syllabus_path = self.course_path / "syllabus.md"
            content = syllabus_path.read_text(encoding='utf-8')

            import re
            # Pattern: **Week N: Topic**
            pattern = rf'\*\*Week {week_num}[:\-]\s*(.+?)\*\*'
            match = re.search(pattern, content)

            if match:
                return match.group(1).strip()

            return f"Week {week_num}"

        except Exception:
            return f"Week {week_num}"

    def _check_research_availability(self, total_weeks: int) -> Dict[str, List[int]]:
        """
        Check which weeks have research available.

        Returns:
            Dict with 'available', 'missing', and 'flagged' week lists
        """
        working_dir = self.course_path / ".working" / "research"
        available = []
        missing = []
        flagged = []

        for week_num in range(1, total_weeks + 1):
            # Check for validation flag (Phase 2)
            flag_file = working_dir / f".week-{week_num}-ready"
            if flag_file.exists():
                flagged.append(week_num)
                available.append(week_num)
                continue

            # Check for research file
            research_file = working_dir / "article-research-summary.md"

            if research_file.exists():
                # File exists, check if it contains this week
                try:
                    content = research_file.read_text(encoding='utf-8')
                    if f"Week {week_num}" in content or f"week {week_num}" in content.lower():
                        available.append(week_num)
                    else:
                        missing.append(week_num)
                except Exception:
                    missing.append(week_num)
            else:
                missing.append(week_num)

        return {
            "available": available,
            "missing": missing,
            "flagged": flagged
        }

    def _check_and_validate_research(self, week_num: int) -> ValidationResult:
        """
        Check and validate research for a week (Phase 2 integration).

        This replicates Step 0.0 from /generate-week command.

        Args:
            week_num: Week number

        Returns:
            ValidationResult with pass/fail and message
        """
        working_dir = self.course_path / ".working" / "research"
        flag_file = working_dir / f".week-{week_num}-ready"

        # Check for validation flag
        if not flag_file.exists():
            # No flag - assume research is in file or will be read from syllabus
            return ValidationResult(
                passed=True,
                message="No validation flag - assuming research available"
            )

        # Flag exists - validate research
        research_file = working_dir / "article-research-summary.md"

        if not research_file.exists():
            return ValidationResult(
                passed=False,
                message=f"Flag exists but research file not found: {research_file}"
            )

        try:
            content = research_file.read_text(encoding='utf-8')

            # Basic validation checks (simplified from /import-research)

            # 1. Check format markers
            if "=== START RESEARCH OUTPUT ===" not in content:
                return ValidationResult(
                    passed=False,
                    message="Missing START marker in research file"
                )

            # 2. Check for this week's content
            week_marker = f"Week {week_num}"
            if week_marker not in content:
                return ValidationResult(
                    passed=False,
                    message=f"Research file does not contain content for Week {week_num}"
                )

            # 3. Check for required sections
            required_sections = [
                "## Required Concepts Coverage",
                "## Final Selections"
            ]

            for section in required_sections:
                if section not in content:
                    return ValidationResult(
                        passed=False,
                        message=f"Missing required section: {section}"
                    )

            # 4. Check for checkmarks (indicates concept coverage)
            if content.count("✓") < 2:  # At least 2 checkmarks expected
                return ValidationResult(
                    passed=False,
                    message="Insufficient concept coverage checkmarks found"
                )

            # All checks passed - delete flag
            flag_file.unlink()

            return ValidationResult(
                passed=True,
                message="Research validation passed"
            )

        except Exception as e:
            return ValidationResult(
                passed=False,
                message=f"Error validating research: {str(e)}"
            )

    def _generate_lecture(self, week_num: int, topic: str) -> Tuple[bool, str]:
        """
        Generate lecture content for a week.

        Returns:
            (success, error_message)
        """
        generator = LectureGenerator(self.course_path, week_num)
        return generator.generate()

    def _generate_tutorial(self, week_num: int, topic: str) -> Tuple[bool, str]:
        """
        Generate tutorial content for a week.

        Returns:
            (success, error_message)
        """
        generator = TutorialGenerator(self.course_path, week_num)
        return generator.generate()

    def _generate_tutor_notes(self, week_num: int) -> Tuple[bool, str]:
        """
        Generate tutor notes for a week.

        Returns:
            (success, error_message)
        """
        generator = TutorNotesGenerator(self.course_path, week_num)
        return generator.generate()

    def _export_quiz(self, week_num: int) -> Tuple[bool, str]:
        """
        Export quiz to GIFT format.

        Returns:
            (success, error_message)
        """
        week_dir = self.course_path / "weeks" / f"week-{week_num:02d}"

        # Check if tool exists
        tool_path = Path(__file__).parent / "export_quiz_to_gift.py"
        if not tool_path.exists():
            return (False, "Quiz export tool not found")

        # Run export tool
        import subprocess

        try:
            result = subprocess.run(
                [sys.executable, str(tool_path), str(week_dir)],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return (True, "")
            else:
                return (False, result.stderr or "Quiz export failed")

        except subprocess.TimeoutExpired:
            return (False, "Quiz export timed out")
        except Exception as e:
            return (False, str(e))

    def _export_slides(self, week_num: int) -> Tuple[bool, str]:
        """
        Export slides to HTML (Decision 3A).

        Returns:
            (success, error_message)
        """
        week_dir = self.course_path / "weeks" / f"week-{week_num:02d}"
        lecture_file = week_dir / "lecture-content.md"
        slides_file = week_dir / "slides.html"

        if not lecture_file.exists():
            return (False, "Lecture file not found")

        # Check if converter exists
        converter_path = Path(__file__).parent / "convert_lecture_to_slides.py"
        if not converter_path.exists():
            return (False, "Slide converter not found")

        # Run converter
        import subprocess

        try:
            result = subprocess.run(
                [sys.executable, str(converter_path), str(lecture_file), str(slides_file)],
                capture_output=True,
                text=True,
                timeout=60
            )

            if result.returncode == 0:
                return (True, "")
            else:
                return (False, result.stderr or "Slide export failed")

        except subprocess.TimeoutExpired:
            return (False, "Slide export timed out")
        except Exception as e:
            return (False, str(e))

    def _save_progress(self, next_week: int) -> None:
        """Save progress to file for recovery."""
        if not self.tracker or not self.config:
            return

        progress = self.tracker.to_generation_progress(
            completed_weeks=self.completed_weeks.copy(),
            skipped_weeks=[s.week_number for s in self.skipped_weeks]
        )
        progress.current_week = next_week

        RecoveryManager.save_progress(self.course_path, progress)

    def _generate_fix_instructions(self, result: GenerationResult) -> str:
        """Generate fix instructions for a failed week."""
        if result.validation_failed:
            return (
                "1. Fix research issues using `/import-research` or regenerate research in Claude Desktop\n"
                "2. Ensure all required concepts are covered\n"
                "3. Regenerate this week individually using `/generate-week`"
            )
        else:
            return (
                "1. Review error messages above\n"
                "2. Fix any issues with course structure or templates\n"
                "3. Regenerate this week individually using `/generate-week`"
            )

    def _create_final_report(self) -> GenerationReport:
        """Create final generation report."""
        total_time = (time.time() - self.tracker.start_time) / 3600  # hours

        return GenerationReport(
            course_code=self.course_code,
            total_weeks=self.config.total_weeks,
            completed_weeks=self.completed_weeks.copy(),
            skipped_weeks=self.skipped_weeks.copy(),
            total_files=sum(len(r.files_generated) for r in self.week_results.values() if r.success),
            total_time_hours=round(total_time, 2)
        )

    def _create_partial_report(self, reason: str) -> GenerationReport:
        """Create partial report for interrupted generation."""
        total_time = (time.time() - self.tracker.start_time) / 3600 if self.tracker else 0

        report = GenerationReport(
            course_code=self.course_code,
            total_weeks=self.config.total_weeks if self.config else 0,
            completed_weeks=self.completed_weeks.copy(),
            skipped_weeks=self.skipped_weeks.copy(),
            total_files=sum(len(r.files_generated) for r in self.week_results.values() if r.success),
            total_time_hours=round(total_time, 2)
        )

        return report


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 2:
        print("Usage: python course_generator.py <course-code>")
        print("Example: python course_generator.py BCI2AU")
        sys.exit(1)

    course_code = sys.argv[1]

    # Find course directory
    courses_dir = Path(__file__).parent.parent / "courses"

    # Look for course directory matching code
    course_dirs = list(courses_dir.glob(f"{course_code}*"))

    if not course_dirs:
        print(f"✗ Course not found: {course_code}")
        print(f"  Searched in: {courses_dir}")
        sys.exit(1)

    if len(course_dirs) > 1:
        print(f"✗ Multiple courses found for {course_code}:")
        for d in course_dirs:
            print(f"  - {d.name}")
        print("  Please specify full course directory name.")
        sys.exit(1)

    course_path = course_dirs[0]

    # Run generation
    generator = CourseGenerator(course_code, course_path)

    try:
        report = generator.run()

        # Summary
        print("\n" + "=" * 65)
        print("GENERATION COMPLETE")
        print("=" * 65)
        print(f"Completed: {len(report.completed_weeks)}/{report.total_weeks} weeks")
        if report.skipped_weeks:
            print(f"Skipped: {len(report.skipped_weeks)} weeks")
        print(f"Total time: {report.total_time_hours:.1f} hours")
        print(f"Files generated: {report.total_files}")
        print()

        sys.exit(0 if not report.skipped_weeks else 1)

    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
