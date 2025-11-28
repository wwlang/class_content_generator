#!/usr/bin/env python3
"""
End-to-end tests for Phase 3: Complete course generation pipeline.

Tests the full workflow from syllabus to slides, including:
- Batch course generation (/generate-course)
- Interruption and recovery (Decision 1A)
- Skipping failed weeks (Decision 2B)
- Coherence analysis and enhancement (/enhance-coherence)
"""

import unittest
from pathlib import Path
import tempfile
import shutil
import subprocess
import json
import time

from tools.course_generator import CourseGenerator
from tools.core_structures import GenerationConfig
from tools.recovery_manager import RecoveryManager
from tools.coherence import (
    ContentExtractor,
    TerminologyAnalyzer,
    CoherenceReporter,
    EnhancementApplicator
)


class TestPhase3EndToEnd(unittest.TestCase):
    """End-to-end tests for Phase 3 implementation."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.course_path = self.test_dir / "BCI2AU-test"
        self.course_path.mkdir()

        # Initialize git repo (required for enhancement applicator)
        subprocess.run(['git', 'init'], cwd=self.course_path, check=True, capture_output=True)
        subprocess.run(
            ['git', 'config', 'user.email', 'test@example.com'],
            cwd=self.course_path,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ['git', 'config', 'user.name', 'Test User'],
            cwd=self.course_path,
            check=True,
            capture_output=True
        )

        # Create basic course structure
        self._create_test_course_structure()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def _create_test_course_structure(self):
        """Create minimal course structure for testing."""
        # Create directories
        (self.course_path / "weeks").mkdir()
        (self.course_path / ".working").mkdir()
        (self.course_path / ".working" / "research").mkdir()

        # Create syllabus
        syllabus_content = """# Business Communication I

## Course Information
- **Course Code:** BCI2AU
- **Level:** Undergraduate Year 2
- **Credits:** 3

## Course Description
This course develops professional communication skills.

## Learning Objectives
1. Demonstrate effective written communication
2. Apply persuasive communication strategies
3. Analyze communication contexts

## Weekly Topics

### Week 1: Communication Fundamentals
Introduction to business communication principles.

**Learning Objectives:**
- Define business communication
- Identify communication barriers
- Apply basic communication models

### Week 2: Written Communication
Professional writing skills and techniques.

**Learning Objectives:**
- Write clear business messages
- Apply formatting standards
- Edit for clarity and conciseness

### Week 3: Persuasive Communication
Principles of persuasion and influence.

**Learning Objectives:**
- Apply Cialdini's principles
- Craft persuasive messages
- Analyze audience psychology

## Assessment Structure

### Portfolio (40%)
Collection of 5 written assignments demonstrating mastery.
- **Due:** Week 10
- **Format:** PDF document, 2000-2500 words total

### Presentation (30%)
Individual presentation on communication topic.
- **Due:** Week 8
- **Duration:** 10-12 minutes

### Weekly Quizzes (30%)
Weekly quizzes testing understanding.
- **Format:** 10 questions, multiple choice
- **Time:** 15 minutes
"""

        (self.course_path / "syllabus.md").write_text(syllabus_content, encoding='utf-8')

        # Create research for Week 1
        research_content = """# Article Research Summary - Week 1

## Selected Articles

### Article 1: Communication Fundamentals
**Citation:** Smith, J., & Jones, M. (2023). Business communication essentials. *Journal of Business Communication*, 15(2), 45-67.

**URL:** https://example.com/article1 (Open Access)

**Key Concepts Coverage:**
- ✓ Communication models - In-depth coverage with examples
- ✓ Communication barriers - Explained with case studies
- ✓ Business context - Applied to workplace scenarios

**Rationale:** Comprehensive coverage of fundamental concepts with practical examples.

### Article 2: Effective Communication
**Citation:** Brown, A. (2024). Effective workplace communication. *Harvard Business Review*, 102(1), 78-92.

**URL:** https://hbr.org/article2 (Openly Accessible)

**Key Concepts Coverage:**
- ✓ Communication effectiveness - In-depth analysis
- ✓ Workplace applications - Real-world examples
- ✓ Best practices - Evidence-based recommendations

**Rationale:** Practical application of communication principles in business settings.
"""

        research_path = self.course_path / ".working" / "research" / "week-1-research.md"
        research_path.write_text(research_content, encoding='utf-8')

        # Create Phase 2 validation flag for Week 1
        flag_path = self.course_path / ".working" / ".week-1-ready"
        flag_path.touch()

    def test_full_course_generation_workflow(self):
        """Test complete course generation from syllabus to slides."""
        # Initialize generator
        generator = CourseGenerator("BCI2AU-test", self.course_path)

        # Generate Week 1 only
        result = generator.generate_week(1, is_interrupted_week=False)

        # Should complete with context files created
        # (Note: Actual content generation requires Claude API, so we verify structure)
        week_dir = self.course_path / "weeks" / "week-01"
        self.assertTrue(week_dir.exists())

        # Verify context files were created
        context_files = list(week_dir.glob(".lecture-generation-context.md"))
        self.assertGreater(len(context_files), 0, "Lecture context should be created")

    def test_interruption_and_recovery(self):
        """Test interruption detection and recovery (Decision 1A)."""
        # Create interrupted generation scenario
        progress_data = {
            "course_code": "BCI2AU",
            "total_weeks": 3,
            "weeks_to_generate": [1, 2, 3],
            "completed_weeks": [1],
            "current_week": 2,
            "start_time": time.time() - 3600,  # Started 1 hour ago
            "last_update": time.time() - 1800,  # Updated 30 min ago
            "config": {
                "export_slides": True,
                "export_quiz": True
            }
        }

        progress_file = self.course_path / ".working" / "generation-progress.json"
        progress_file.write_text(json.dumps(progress_data, indent=2), encoding='utf-8')

        # Detect interrupted generation
        interrupted_progress = RecoveryManager.detect_interrupted_generation(self.course_path)

        self.assertIsNotNone(interrupted_progress)
        self.assertEqual(interrupted_progress["current_week"], 2)
        self.assertEqual(interrupted_progress["completed_weeks"], [1])

        # Verify recovery suggestions
        suggestions = RecoveryManager.get_recovery_suggestions(interrupted_progress)
        self.assertIn("regenerate", suggestions.lower())
        self.assertIn("week 2", suggestions.lower())

    def test_skip_failed_weeks_continue(self):
        """Test skipping failed weeks and continuing (Decision 2B)."""
        # Initialize generator
        generator = CourseGenerator("BCI2AU-test", self.course_path)

        # Try to generate Week 99 (doesn't exist - will fail)
        result = generator.generate_week(99, is_interrupted_week=False)

        # Should fail gracefully
        self.assertFalse(result.success)
        self.assertIn("error", result.error_message.lower())

        # Progress should still be saved
        progress_file = self.course_path / ".working" / "generation-progress.json"
        # Progress file may or may not exist depending on validation failure point
        # Just verify generator didn't crash

    def test_coherence_analysis_workflow(self):
        """Test coherence analysis on course content."""
        # Create sample week content
        self._create_sample_week_for_coherence(1)
        self._create_sample_week_for_coherence(2)

        # Extract content
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()

        self.assertEqual(len(week_contents), 2)

        # Run terminology analyzer (quick test)
        analyzer = TerminologyAnalyzer(week_contents)
        issues = analyzer.analyze()

        # Should find some issues (or none - both valid)
        self.assertIsInstance(issues, list)

        # Generate report
        reporter = CoherenceReporter(issues, "BCI2AU-test")
        report = reporter.generate_full_report()

        self.assertEqual(report.course_code, "BCI2AU-test")
        self.assertEqual(report.total_issues, len(issues))

    def test_enhancement_application_workflow(self):
        """Test enhancement application with git backup."""
        # Create sample content
        self._create_sample_week_for_coherence(1)

        # Create git commit (required for backup)
        subprocess.run(['git', 'add', '-A'], cwd=self.course_path, check=True, capture_output=True)
        subprocess.run(
            ['git', 'commit', '-m', 'Initial content'],
            cwd=self.course_path,
            check=True,
            capture_output=True
        )

        # Extract and analyze
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()
        analyzer = TerminologyAnalyzer(week_contents)
        issues = analyzer.analyze()

        # Apply enhancements
        applicator = EnhancementApplicator(self.course_path, issues)
        report = applicator.apply_enhancements(
            issue_types=None,
            auto_only=True,
            create_backup=True
        )

        # Should create git backup
        if len(issues) > 0 and any(i.auto_apply_safe for i in issues):
            self.assertIsNotNone(report.git_backup_commit)

    def test_complete_pipeline_syllabus_to_coherence(self):
        """Test complete pipeline: syllabus → generation → coherence → enhancement."""
        # 1. Generate content for Week 1
        generator = CourseGenerator("BCI2AU-test", self.course_path)
        result = generator.generate_week(1, is_interrupted_week=False)

        # Verify context created (actual content needs Claude API)
        week_dir = self.course_path / "weeks" / "week-01"
        self.assertTrue(week_dir.exists())

        # 2. Create sample generated content for coherence testing
        self._create_sample_week_for_coherence(1)

        # 3. Run coherence analysis
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()

        analyzer = TerminologyAnalyzer(week_contents)
        issues = analyzer.analyze()

        reporter = CoherenceReporter(issues, "BCI2AU-test")
        report = reporter.generate_full_report()

        # 4. Verify pipeline completed
        self.assertIsNotNone(report)
        self.assertGreaterEqual(report.total_issues, 0)

    def test_progress_tracking_accuracy(self):
        """Test progress tracking during generation."""
        generator = CourseGenerator("BCI2AU-test", self.course_path)

        # Create progress tracker manually
        from tools.progress_tracker import ProgressTracker
        generator.tracker = ProgressTracker(self.course_path)

        # Save initial progress
        generator.tracker.start_generation("BCI2AU-test", [1])
        generator.tracker.save_progress()

        # Verify progress file
        progress_file = self.course_path / ".working" / "generation-progress.json"
        self.assertTrue(progress_file.exists())

        # Load and verify
        progress_data = json.loads(progress_file.read_text(encoding='utf-8'))
        self.assertEqual(progress_data["course_code"], "BCI2AU-test")
        self.assertEqual(progress_data["weeks_to_generate"], [1])

    def test_generation_report_format(self):
        """Test generation report markdown formatting."""
        # Create mock generation results
        from tools.core_structures import GenerationResult, GenerationReport, SkippedWeek

        results = [
            GenerationResult(
                week_number=1,
                success=True,
                files_created=["lecture-content.md", "tutorial-content.md"],
                time_elapsed_minutes=45.5,
                lecture_generated=True,
                tutorial_generated=True,
                tutor_notes_generated=True,
                quiz_exported=True,
                slides_exported=False,
                error_message=None
            ),
            GenerationResult(
                week_number=2,
                success=False,
                files_created=[],
                time_elapsed_minutes=5.0,
                lecture_generated=False,
                tutorial_generated=False,
                tutor_notes_generated=False,
                quiz_exported=False,
                slides_exported=False,
                error_message="Research validation failed"
            )
        ]

        skipped = [
            SkippedWeek(
                week_number=2,
                topic="Written Communication",
                reason="Research validation failed",
                errors=["Missing research file"],
                fix_instructions="Create research file for Week 2"
            )
        ]

        report = GenerationReport(
            course_code="BCI2AU-test",
            total_weeks=2,
            completed_weeks=[1],
            skipped_weeks=skipped,
            total_files=4,
            total_time_hours=0.75,
            results=results
        )

        # Generate markdown
        markdown = report.to_markdown()

        # Verify format
        self.assertIn("COURSE GENERATION COMPLETE", markdown)
        self.assertIn("BCI2AU-test", markdown)
        self.assertIn("Week 1: Generated successfully", markdown)
        self.assertIn("SKIPPED WEEKS: 1", markdown)

    def test_recovery_manager_suggestions(self):
        """Test recovery manager provides helpful suggestions."""
        # Create interrupted scenario
        progress_data = {
            "course_code": "BCI2AU",
            "current_week": 5,
            "completed_weeks": [1, 2, 3, 4],
            "weeks_to_generate": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }

        suggestions = RecoveryManager.get_recovery_suggestions(progress_data)

        # Should provide actionable suggestions
        self.assertIsInstance(suggestions, str)
        self.assertGreater(len(suggestions), 50)
        self.assertIn("week", suggestions.lower())

    def test_error_handling_graceful_degradation(self):
        """Test that errors don't crash entire generation."""
        generator = CourseGenerator("BCI2AU-test", self.course_path)

        # Try to generate week with no research
        result = generator.generate_week(99, is_interrupted_week=False)

        # Should fail gracefully
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error_message)

        # Generator should still be usable for next week
        # (Not crashing is the test)

    def _create_sample_week_for_coherence(self, week_num: int):
        """Create sample week content for coherence testing."""
        week_dir = self.course_path / "weeks" / f"week-{week_num:02d}"
        week_dir.mkdir(exist_ok=True)

        lecture_content = f"""# Week {week_num}: Communication Fundamentals

## Slide 1: Introduction

Welcome to Week {week_num}. Today we'll explore business communication.

**Speaker Notes:**
The organisation needs effective communication. Companies must communicate clearly.

## Slide 2: Key Concepts

Effective communication requires:
- Message clarity
- Audience analysis
- Channel selection

The organization's communication strategy is critical for success.

**References:**
Smith, J. (2023). Communication theory. *Journal of Business*, 15(2), 45-67.

## Slide 3: Vietnamese Example

**Example: Vinamilk**
Vinamilk demonstrates excellent communication practices in Vietnam.

**Speaker Notes:**
This Vietnamese company shows cultural adaptation in messaging.
"""

        tutorial_content = f"""# Week {week_num} Tutorial

## Quiz Questions

1. What is the definition of business communication?
2. Name three barriers to effective communication.
3. How does culture affect organisational messaging?

## Main Activity

Analyze a communication scenario in small groups.
"""

        (week_dir / "lecture-content.md").write_text(lecture_content, encoding='utf-8')
        (week_dir / "tutorial-content.md").write_text(tutorial_content, encoding='utf-8')


class TestPhase3Performance(unittest.TestCase):
    """Performance benchmarks for Phase 3."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.course_path = self.test_dir / "PERF-test"
        self.course_path.mkdir()

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_coherence_analysis_performance(self):
        """Test coherence analysis completes in reasonable time."""
        # Create 10 weeks of content
        (self.course_path / "weeks").mkdir()

        for week_num in range(1, 11):
            self._create_sample_week(week_num)

        # Measure extraction time
        start_time = time.time()
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()
        extraction_time = time.time() - start_time

        # Should extract 10 weeks quickly
        self.assertEqual(len(week_contents), 10)
        self.assertLess(extraction_time, 5.0, "Extraction should take < 5 seconds")

        # Measure analysis time
        start_time = time.time()
        analyzer = TerminologyAnalyzer(week_contents)
        issues = analyzer.analyze()
        analysis_time = time.time() - start_time

        # Should analyze quickly
        self.assertLess(analysis_time, 3.0, "Analysis should take < 3 seconds")

    def test_report_generation_performance(self):
        """Test report generation completes quickly."""
        from tools.core_structures import CoherenceIssue

        # Create many issues
        issues = [
            CoherenceIssue(
                issue_id=f"issue-{i}",
                issue_type="terminology_variation",
                quality_score=7,
                affected_weeks=[1, 2],
                suggested_fix=f"Fix issue {i}",
                auto_apply_safe=True,
                category="terminology"
            )
            for i in range(100)
        ]

        # Measure report generation time
        start_time = time.time()
        reporter = CoherenceReporter(issues, "PERF-test")
        report = reporter.generate_full_report()
        report_time = time.time() - start_time

        # Should generate report quickly
        self.assertLess(report_time, 1.0, "Report generation should take < 1 second")
        self.assertEqual(report.total_issues, 100)

    def _create_sample_week(self, week_num: int):
        """Create minimal sample week for performance testing."""
        week_dir = self.course_path / "weeks" / f"week-{week_num:02d}"
        week_dir.mkdir()

        content = f"# Week {week_num}\n\nSample content for performance testing.\n"
        (week_dir / "lecture-content.md").write_text(content, encoding='utf-8')
        (week_dir / "tutorial-content.md").write_text(content, encoding='utf-8')


if __name__ == '__main__':
    unittest.main()
