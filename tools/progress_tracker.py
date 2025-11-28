#!/usr/bin/env python3
"""
Progress tracking for batch course generation.

Provides real-time progress updates with time estimation and visual progress bars.
"""

import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any

from .core_structures import GenerationProgress, GenerationResult


class ProgressTracker:
    """Track and display generation progress."""

    def __init__(self, total_weeks: int, course_code: str):
        """
        Initialize progress tracker.

        Args:
            total_weeks: Total number of weeks to generate
            course_code: Course code for identification
        """
        self.total_weeks = total_weeks
        self.course_code = course_code
        self.completed = 0
        self.skipped = 0
        self.start_time = time.time()
        self.week_times: List[float] = []  # Times in minutes
        self.current_week: Optional[int] = None
        self.current_week_start: Optional[float] = None

    def start_week(self, week_num: int) -> None:
        """Mark the start of week generation."""
        self.current_week = week_num
        self.current_week_start = time.time()

    def complete_week(self, week_num: int, success: bool) -> float:
        """
        Mark week as complete.

        Args:
            week_num: Week number that completed
            success: Whether generation succeeded

        Returns:
            Time elapsed for this week in minutes
        """
        if self.current_week_start is None:
            elapsed_minutes = 0.0
        else:
            elapsed_seconds = time.time() - self.current_week_start
            elapsed_minutes = elapsed_seconds / 60.0
            self.week_times.append(elapsed_minutes)

        if success:
            self.completed += 1
        else:
            self.skipped += 1

        self.current_week = None
        self.current_week_start = None

        return elapsed_minutes

    def get_progress_percentage(self) -> int:
        """Get progress percentage (0-100)."""
        total_processed = self.completed + self.skipped
        if self.total_weeks == 0:
            return 100
        return int((total_processed / self.total_weeks) * 100)

    def get_average_week_time(self) -> float:
        """Get average time per week in minutes."""
        if not self.week_times:
            return 50.0  # Default estimate
        return sum(self.week_times) / len(self.week_times)

    def estimate_time_remaining(self) -> str:
        """
        Calculate estimated time remaining.

        Returns:
            Human-readable time estimate (e.g., "4h 15m")
        """
        weeks_remaining = self.total_weeks - (self.completed + self.skipped)
        if weeks_remaining <= 0:
            return "0m"

        avg_minutes = self.get_average_week_time()
        total_minutes_remaining = avg_minutes * weeks_remaining

        hours = int(total_minutes_remaining // 60)
        minutes = int(total_minutes_remaining % 60)

        if hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

    def get_progress_bar(self, width: int = 10) -> str:
        """
        Generate progress bar visualization.

        Args:
            width: Width of progress bar in characters

        Returns:
            Progress bar string (e.g., "[█████░░░░░]")
        """
        percentage = self.get_progress_percentage()
        filled = int((percentage / 100) * width)
        empty = width - filled

        return f"[{'█' * filled}{'░' * empty}]"

    def display_week_header(self, week_num: int, topic: str) -> str:
        """
        Generate week header display.

        Args:
            week_num: Current week number
            topic: Week topic name

        Returns:
            Formatted header string
        """
        lines = []

        lines.append("═" * 65)
        lines.append(f"Week {week_num}/{self.total_weeks}: {topic}")
        lines.append(f"Progress: {self.get_progress_bar()} {self.get_progress_percentage()}%")
        lines.append("═" * 65)
        lines.append("")

        # Additional info
        elapsed_total = (time.time() - self.start_time) / 3600  # hours
        lines.append(f"Time elapsed: {elapsed_total:.1f}h")
        lines.append(f"Time remaining: ~{self.estimate_time_remaining()} (estimated)")
        lines.append("")

        # Status
        lines.append(f"Completed weeks: {', '.join(map(str, range(1, self.completed + 1))) if self.completed > 0 else 'None'} ({self.completed} generated)")
        if self.skipped > 0:
            lines.append(f"Skipped weeks: {self.skipped} skipped")
        weeks_remaining_count = self.total_weeks - (self.completed + self.skipped)
        lines.append(f"Remaining weeks: {weeks_remaining_count} to go")
        lines.append("")

        return "\n".join(lines)

    def display_step_progress(self, step: int, total_steps: int, step_name: str) -> str:
        """
        Display progress within a week (e.g., generating lecture, tutorial, etc.).

        Args:
            step: Current step number (1-indexed)
            total_steps: Total number of steps
            step_name: Name of current step

        Returns:
            Progress string
        """
        percentage = int((step / total_steps) * 100)
        bar_width = 7
        filled = int((step / total_steps) * bar_width)
        empty = bar_width - filled

        return f"Current task: {step_name}... ({step}/{total_steps}) [{'█' * filled}{'░' * empty}] {percentage}%"

    def get_summary(self) -> Dict[str, Any]:
        """
        Get progress summary.

        Returns:
            Dictionary with progress statistics
        """
        total_time = (time.time() - self.start_time) / 3600  # hours

        return {
            "total_weeks": self.total_weeks,
            "completed": self.completed,
            "skipped": self.skipped,
            "percentage": self.get_progress_percentage(),
            "total_time_hours": round(total_time, 2),
            "average_week_time_minutes": round(self.get_average_week_time(), 1),
            "estimated_remaining": self.estimate_time_remaining()
        }

    def to_generation_progress(self, completed_weeks: List[int], skipped_weeks: List[int]) -> GenerationProgress:
        """
        Convert to GenerationProgress object for persistence.

        Args:
            completed_weeks: List of completed week numbers
            skipped_weeks: List of skipped week numbers

        Returns:
            GenerationProgress object
        """
        total_time = (time.time() - self.start_time) / 3600  # hours
        remaining_weeks = self.total_weeks - len(completed_weeks) - len(skipped_weeks)
        avg_time = self.get_average_week_time() / 60.0  # Convert to hours
        estimated_remaining = avg_time * remaining_weeks

        return GenerationProgress(
            course_code=self.course_code,
            total_weeks=self.total_weeks,
            completed_weeks=completed_weeks,
            skipped_weeks=skipped_weeks,
            current_week=self.current_week if self.current_week else 1,
            last_updated=datetime.now().isoformat(),
            estimated_remaining_hours=round(estimated_remaining, 2),
            week_times=self.week_times
        )

    def display_completion_message(self) -> str:
        """Generate completion message."""
        total_time = (time.time() - self.start_time) / 3600

        lines = []
        lines.append("")
        lines.append("═" * 65)
        lines.append("✓ BATCH GENERATION COMPLETE")
        lines.append("═" * 65)
        lines.append(f"Total time: {total_time:.1f} hours")
        lines.append(f"Weeks generated: {self.completed}/{self.total_weeks}")
        if self.skipped > 0:
            lines.append(f"Weeks skipped: {self.skipped}")
        lines.append(f"Average time per week: {self.get_average_week_time():.0f} minutes")
        lines.append("")

        return "\n".join(lines)


def format_time_delta(seconds: float) -> str:
    """
    Format time delta into human-readable string.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted string (e.g., "2h 30m", "45m", "30s")
    """
    if seconds < 60:
        return f"{int(seconds)}s"

    minutes = int(seconds // 60)
    if minutes < 60:
        return f"{minutes}m"

    hours = minutes // 60
    remaining_minutes = minutes % 60

    if remaining_minutes > 0:
        return f"{hours}h {remaining_minutes}m"
    else:
        return f"{hours}h"


def estimate_course_time(total_weeks: int, avg_minutes_per_week: float = 50.0) -> str:
    """
    Estimate total time for course generation.

    Args:
        total_weeks: Number of weeks in course
        avg_minutes_per_week: Average time per week

    Returns:
        Human-readable estimate
    """
    total_minutes = total_weeks * avg_minutes_per_week
    hours = total_minutes / 60.0

    if hours < 1:
        return f"{int(total_minutes)} minutes"
    else:
        return f"{hours:.1f} hours"
