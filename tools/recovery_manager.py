#!/usr/bin/env python3
"""
Recovery management for interrupted course generation.

Handles detection of interrupted generation and recovery process (Decision 1A).
"""

from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime

from .core_structures import GenerationProgress, GenerationConfig


class RecoveryManager:
    """Handle interruption and recovery for course generation."""

    PROGRESS_FILENAME = "generation-progress.json"

    @staticmethod
    def get_progress_file_path(course_path: Path) -> Path:
        """
        Get path to progress file.

        Args:
            course_path: Path to course directory

        Returns:
            Path to progress file
        """
        return course_path / ".working" / RecoveryManager.PROGRESS_FILENAME

    @staticmethod
    def detect_interrupted_generation(course_path: Path) -> Optional[GenerationProgress]:
        """
        Check for interrupted generation.

        Args:
            course_path: Path to course directory

        Returns:
            GenerationProgress if interrupted generation found, None otherwise
        """
        progress_file = RecoveryManager.get_progress_file_path(course_path)

        if not progress_file.exists():
            return None

        # Load progress
        progress = GenerationProgress.load(progress_file)

        if progress is None:
            return None

        # Verify it's actually interrupted (not complete)
        total_processed = len(progress.completed_weeks) + len(progress.skipped_weeks)
        if total_processed >= progress.total_weeks:
            # Generation was complete, not interrupted
            RecoveryManager.cleanup_progress(course_path)
            return None

        return progress

    @staticmethod
    def format_recovery_prompt(progress: GenerationProgress) -> str:
        """
        Format recovery prompt for user.

        Args:
            progress: Progress from interrupted generation

        Returns:
            Formatted prompt string
        """
        lines = []

        lines.append("═" * 65)
        lines.append("INTERRUPTED GENERATION DETECTED")
        lines.append("═" * 65)
        lines.append("")

        lines.append("Progress found:")
        lines.append(f"- Total weeks: {progress.total_weeks}")
        lines.append(f"- Completed: Weeks {', '.join(map(str, sorted(progress.completed_weeks)))} ({len(progress.completed_weeks)}/{progress.total_weeks})")
        if progress.skipped_weeks:
            lines.append(f"- Skipped: Weeks {', '.join(map(str, sorted(progress.skipped_weeks)))} ({len(progress.skipped_weeks)} weeks)")
        lines.append(f"- Interrupted at: Week {progress.current_week}")
        lines.append(f"- Last updated: {progress.last_updated}")
        lines.append("")

        # Decision 1A: Resume from interrupted week (will regenerate it)
        lines.append("RECOVERY PLAN (Decision 1A):")
        lines.append(f"- Resume from Week {progress.current_week}")
        lines.append(f"- Week {progress.current_week} will be REGENERATED (fresh start)")
        lines.append(f"- Completed weeks ({', '.join(map(str, sorted(progress.completed_weeks)))}) will be KEPT")

        remaining_weeks = progress.total_weeks - len(progress.completed_weeks) - len(progress.skipped_weeks)
        lines.append(f"- Then continue with {remaining_weeks} remaining weeks")
        lines.append("")

        lines.append(f"Estimated time remaining: {progress.estimated_remaining_hours:.1f} hours")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def should_resume(progress: GenerationProgress) -> Tuple[bool, str]:
        """
        Determine if recovery should proceed.

        This is called after user confirms resume. Validates that recovery is safe.

        Args:
            progress: Progress to validate

        Returns:
            (should_resume, reason)
        """
        # Check that progress is recent (within 30 days)
        try:
            last_update = datetime.fromisoformat(progress.last_updated)
            days_ago = (datetime.now() - last_update).days

            if days_ago > 30:
                return (
                    False,
                    f"Progress is {days_ago} days old. Too old to resume safely. "
                    "Please start fresh generation."
                )
        except:
            pass  # If we can't parse date, allow resume

        # Check that some progress was made
        if not progress.completed_weeks and not progress.skipped_weeks:
            return (
                False,
                "No progress was made before interruption. Starting fresh."
            )

        # Validate week numbers make sense
        if progress.current_week < 1 or progress.current_week > progress.total_weeks:
            return (
                False,
                f"Invalid current week: {progress.current_week}. Starting fresh."
            )

        # All checks passed
        return (True, "Recovery validated successfully")

    @staticmethod
    def create_recovery_config(
        progress: GenerationProgress,
        original_config: GenerationConfig
    ) -> GenerationConfig:
        """
        Create config for recovery run.

        Args:
            progress: Progress from interrupted generation
            original_config: Original configuration

        Returns:
            Updated configuration for recovery
        """
        # Decision 1A: Resume from current week (regenerate it)
        return GenerationConfig(
            course_code=original_config.course_code,
            course_path=original_config.course_path,
            total_weeks=original_config.total_weeks,
            resume_from_week=progress.current_week,  # Start from interrupted week
            export_slides=original_config.export_slides,
            skip_on_validation_failure=original_config.skip_on_validation_failure,
            regenerate_interrupted_week=True  # Decision 1A
        )

    @staticmethod
    def save_progress(
        course_path: Path,
        progress: GenerationProgress
    ) -> None:
        """
        Save progress to file.

        Args:
            course_path: Path to course directory
            progress: Progress to save
        """
        progress_file = RecoveryManager.get_progress_file_path(course_path)
        progress.save(progress_file)

    @staticmethod
    def cleanup_progress(course_path: Path) -> None:
        """
        Remove progress file after successful completion.

        Args:
            course_path: Path to course directory
        """
        progress_file = RecoveryManager.get_progress_file_path(course_path)

        if progress_file.exists():
            try:
                progress_file.unlink()
            except Exception as e:
                print(f"Warning: Could not delete progress file: {e}")

    @staticmethod
    def get_weeks_to_generate(progress: Optional[GenerationProgress], total_weeks: int) -> list[int]:
        """
        Get list of weeks that need to be generated.

        Args:
            progress: Progress from interrupted generation (None if fresh start)
            total_weeks: Total weeks in course

        Returns:
            List of week numbers to generate
        """
        if progress is None:
            # Fresh start - generate all weeks
            return list(range(1, total_weeks + 1))

        # Recovery mode - skip completed weeks
        all_weeks = set(range(1, total_weeks + 1))
        completed = set(progress.completed_weeks)

        # Decision 1A: Include current week (will regenerate it)
        # Exclude only the truly completed weeks
        weeks_to_generate = sorted(all_weeks - completed)

        return weeks_to_generate

    @staticmethod
    def format_recovery_confirmation() -> str:
        """Generate recovery confirmation message."""
        lines = []
        lines.append("")
        lines.append("═" * 65)
        lines.append("RESUMING FROM INTERRUPTED GENERATION")
        lines.append("═" * 65)
        lines.append("")
        return "\n".join(lines)


def format_interrupted_week_message(week_num: int) -> str:
    """
    Format message for regenerating interrupted week.

    Args:
        week_num: Week number being regenerated

    Returns:
        Formatted message
    """
    lines = []
    lines.append("")
    lines.append(f"Note: Week {week_num} was interrupted during previous generation")
    lines.append(f"      Regenerating Week {week_num} from scratch (Decision 1A)")
    lines.append("")
    return "\n".join(lines)
