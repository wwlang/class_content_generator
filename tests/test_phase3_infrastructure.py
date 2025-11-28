#!/usr/bin/env python3
"""
Unit tests for Phase 3 core infrastructure.

Tests core data structures, ProgressTracker, and RecoveryManager.
"""

import json
import pytest
import tempfile
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from core_structures import (
    GenerationConfig,
    GenerationProgress,
    GenerationResult,
    GenerationReport,
    SkippedWeek,
    ValidationResult,
    ResearchStatus,
    Term,
    TermUsage,
    WeekContent
)
from progress_tracker import ProgressTracker, format_time_delta, estimate_course_time
from recovery_manager import RecoveryManager


class TestGenerationConfig:
    """Test GenerationConfig data structure."""

    def test_creation_with_defaults(self):
        """Test creating config with default values."""
        config = GenerationConfig(
            course_code="TEST101",
            course_path=Path("/test/path"),
            total_weeks=10
        )

        assert config.course_code == "TEST101"
        assert config.total_weeks == 10
        assert config.export_slides is True  # Decision 3A
        assert config.skip_on_validation_failure is True  # Decision 2B
        assert config.regenerate_interrupted_week is True  # Decision 1A

    def test_creation_with_string_path(self):
        """Test path conversion from string."""
        config = GenerationConfig(
            course_code="TEST101",
            course_path="/test/path",
            total_weeks=10
        )

        assert isinstance(config.course_path, Path)
        assert config.course_path == Path("/test/path")


class TestGenerationProgress:
    """Test GenerationProgress data structure."""

    def test_creation(self):
        """Test creating progress object."""
        progress = GenerationProgress(
            course_code="TEST101",
            total_weeks=10,
            completed_weeks=[1, 2, 3],
            skipped_weeks=[],
            current_week=4
        )

        assert progress.course_code == "TEST101"
        assert progress.total_weeks == 10
        assert progress.completed_weeks == [1, 2, 3]
        assert progress.current_week == 4

    def test_json_serialization(self):
        """Test JSON serialization round-trip."""
        progress = GenerationProgress(
            course_code="TEST101",
            total_weeks=10,
            completed_weeks=[1, 2],
            current_week=3
        )

        json_str = progress.to_json()
        loaded = GenerationProgress.from_json(json_str)

        assert loaded.course_code == progress.course_code
        assert loaded.total_weeks == progress.total_weeks
        assert loaded.completed_weeks == progress.completed_weeks
        assert loaded.current_week == progress.current_week

    def test_save_and_load(self):
        """Test saving and loading from file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "progress.json"

            progress = GenerationProgress(
                course_code="TEST101",
                total_weeks=10,
                completed_weeks=[1, 2, 3]
            )

            progress.save(file_path)
            assert file_path.exists()

            loaded = GenerationProgress.load(file_path)
            assert loaded is not None
            assert loaded.course_code == "TEST101"
            assert loaded.completed_weeks == [1, 2, 3]

    def test_load_nonexistent_file(self):
        """Test loading from nonexistent file."""
        result = GenerationProgress.load(Path("/nonexistent/file.json"))
        assert result is None


class TestGenerationResult:
    """Test GenerationResult data structure."""

    def test_add_error(self):
        """Test adding error sets success to False."""
        result = GenerationResult(week_number=1, success=True)

        result.add_error("Something went wrong")

        assert result.success is False
        assert len(result.errors) == 1
        assert result.errors[0] == "Something went wrong"

    def test_add_warning(self):
        """Test adding warning doesn't affect success."""
        result = GenerationResult(week_number=1, success=True)

        result.add_warning("This is a warning")

        assert result.success is True
        assert len(result.warnings) == 1


class TestGenerationReport:
    """Test GenerationReport and markdown generation."""

    def test_creation(self):
        """Test creating report."""
        report = GenerationReport(
            course_code="TEST101",
            total_weeks=10,
            completed_weeks=[1, 2, 3],
            skipped_weeks=[],
            total_files=15,
            total_time_hours=5.5
        )

        assert report.course_code == "TEST101"
        assert len(report.completed_weeks) == 3

    def test_markdown_generation(self):
        """Test markdown report generation."""
        skipped = SkippedWeek(
            week_number=3,
            topic="Test Topic",
            reason="Validation failed",
            errors=["Error 1", "Error 2"],
            fix_instructions="Fix the research"
        )

        report = GenerationReport(
            course_code="TEST101",
            total_weeks=10,
            completed_weeks=[1, 2],
            skipped_weeks=[skipped],
            total_files=10,
            total_time_hours=4.0
        )

        markdown = report.to_markdown()

        assert "COURSE GENERATION COMPLETE" in markdown
        assert "TEST101" in markdown
        assert "2/10" in markdown
        assert "SKIPPED WEEKS: 1" in markdown
        assert "Week 3" in markdown

    def test_save_report(self):
        """Test saving report to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.md"

            report = GenerationReport(
                course_code="TEST101",
                total_weeks=10,
                completed_weeks=[1, 2, 3],
                skipped_weeks=[],
                total_files=15,
                total_time_hours=5.5
            )

            report.save(output_path)

            assert output_path.exists()
            content = output_path.read_text()
            assert "TEST101" in content


class TestProgressTracker:
    """Test ProgressTracker functionality."""

    def test_initialization(self):
        """Test creating tracker."""
        tracker = ProgressTracker(total_weeks=10, course_code="TEST101")

        assert tracker.total_weeks == 10
        assert tracker.course_code == "TEST101"
        assert tracker.completed == 0

    def test_week_completion(self):
        """Test marking weeks as complete."""
        tracker = ProgressTracker(total_weeks=10, course_code="TEST101")

        tracker.start_week(1)
        elapsed = tracker.complete_week(1, success=True)

        assert tracker.completed == 1
        assert tracker.skipped == 0
        assert elapsed >= 0

    def test_week_skipped(self):
        """Test marking weeks as skipped."""
        tracker = ProgressTracker(total_weeks=10, course_code="TEST101")

        tracker.start_week(1)
        tracker.complete_week(1, success=False)

        assert tracker.completed == 0
        assert tracker.skipped == 1

    def test_progress_percentage(self):
        """Test progress percentage calculation."""
        tracker = ProgressTracker(total_weeks=10, course_code="TEST101")

        assert tracker.get_progress_percentage() == 0

        tracker.start_week(1)
        tracker.complete_week(1, success=True)
        assert tracker.get_progress_percentage() == 10

        tracker.start_week(2)
        tracker.complete_week(2, success=True)
        assert tracker.get_progress_percentage() == 20

    def test_progress_bar(self):
        """Test progress bar visualization."""
        tracker = ProgressTracker(total_weeks=10, course_code="TEST101")

        # 0%
        bar = tracker.get_progress_bar(width=10)
        assert bar == "[░░░░░░░░░░]"

        # 50%
        for i in range(1, 6):
            tracker.start_week(i)
            tracker.complete_week(i, success=True)

        bar = tracker.get_progress_bar(width=10)
        assert bar == "[█████░░░░░]"

    def test_time_estimation(self):
        """Test time remaining estimation."""
        tracker = ProgressTracker(total_weeks=10, course_code="TEST101")

        # No weeks complete - uses default estimate
        estimate = tracker.estimate_time_remaining()
        assert "h" in estimate or "m" in estimate

        # Add some completed weeks with times
        tracker.week_times = [50.0, 55.0, 48.0]  # minutes
        tracker.completed = 3

        estimate = tracker.estimate_time_remaining()
        # Should estimate ~6 hours for remaining 7 weeks
        assert estimate != "0m"

    def test_week_header_display(self):
        """Test week header formatting."""
        tracker = ProgressTracker(total_weeks=10, course_code="TEST101")

        header = tracker.display_week_header(1, "Introduction to Business")

        assert "Week 1/10" in header
        assert "Introduction to Business" in header
        assert "Progress:" in header
        assert "Time elapsed:" in header

    def test_conversion_to_generation_progress(self):
        """Test converting to GenerationProgress."""
        tracker = ProgressTracker(total_weeks=10, course_code="TEST101")

        tracker.start_week(1)
        tracker.complete_week(1, success=True)
        tracker.start_week(2)
        tracker.complete_week(2, success=True)

        progress = tracker.to_generation_progress(
            completed_weeks=[1, 2],
            skipped_weeks=[]
        )

        assert progress.course_code == "TEST101"
        assert progress.total_weeks == 10
        assert progress.completed_weeks == [1, 2]
        assert len(progress.week_times) == 2


class TestRecoveryManager:
    """Test RecoveryManager functionality."""

    def test_no_interrupted_generation(self):
        """Test when no interrupted generation exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = Path(tmpdir)

            result = RecoveryManager.detect_interrupted_generation(course_path)

            assert result is None

    def test_detect_interrupted_generation(self):
        """Test detecting interrupted generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = Path(tmpdir)

            # Create progress file
            progress = GenerationProgress(
                course_code="TEST101",
                total_weeks=10,
                completed_weeks=[1, 2, 3],
                current_week=4
            )

            progress_file = RecoveryManager.get_progress_file_path(course_path)
            progress.save(progress_file)

            # Detect
            detected = RecoveryManager.detect_interrupted_generation(course_path)

            assert detected is not None
            assert detected.course_code == "TEST101"
            assert detected.current_week == 4
            assert detected.completed_weeks == [1, 2, 3]

    def test_format_recovery_prompt(self):
        """Test recovery prompt formatting."""
        progress = GenerationProgress(
            course_code="TEST101",
            total_weeks=10,
            completed_weeks=[1, 2, 3],
            skipped_weeks=[5],
            current_week=4,
            estimated_remaining_hours=5.5
        )

        prompt = RecoveryManager.format_recovery_prompt(progress)

        assert "INTERRUPTED GENERATION DETECTED" in prompt
        assert "Week 4" in prompt
        assert "Weeks 1, 2, 3" in prompt
        assert "5.5 hours" in prompt

    def test_should_resume_valid(self):
        """Test validation of valid progress."""
        progress = GenerationProgress(
            course_code="TEST101",
            total_weeks=10,
            completed_weeks=[1, 2, 3],
            current_week=4
        )

        should_resume, reason = RecoveryManager.should_resume(progress)

        assert should_resume is True
        assert "validated successfully" in reason.lower()

    def test_should_resume_no_progress(self):
        """Test validation when no progress made."""
        progress = GenerationProgress(
            course_code="TEST101",
            total_weeks=10,
            completed_weeks=[],
            skipped_weeks=[],
            current_week=1
        )

        should_resume, reason = RecoveryManager.should_resume(progress)

        assert should_resume is False
        assert "no progress" in reason.lower()

    def test_create_recovery_config(self):
        """Test creating recovery config (Decision 1A)."""
        progress = GenerationProgress(
            course_code="TEST101",
            total_weeks=10,
            completed_weeks=[1, 2],
            current_week=3
        )

        original_config = GenerationConfig(
            course_code="TEST101",
            course_path=Path("/test"),
            total_weeks=10
        )

        recovery_config = RecoveryManager.create_recovery_config(progress, original_config)

        assert recovery_config.resume_from_week == 3  # Decision 1A: resume from current
        assert recovery_config.regenerate_interrupted_week is True

    def test_get_weeks_to_generate_fresh(self):
        """Test getting weeks to generate for fresh start."""
        weeks = RecoveryManager.get_weeks_to_generate(None, total_weeks=10)

        assert weeks == list(range(1, 11))

    def test_get_weeks_to_generate_recovery(self):
        """Test getting weeks to generate for recovery (Decision 1A)."""
        progress = GenerationProgress(
            course_code="TEST101",
            total_weeks=10,
            completed_weeks=[1, 2, 3, 5],  # Skipped 4, completed 5
            current_week=6
        )

        weeks = RecoveryManager.get_weeks_to_generate(progress, total_weeks=10)

        # Should include 4 (never completed), 6 (current - will regenerate), 7-10
        # Should NOT include 1, 2, 3, 5 (completed)
        assert 1 not in weeks
        assert 2 not in weeks
        assert 3 not in weeks
        assert 4 in weeks
        assert 5 not in weeks
        assert 6 in weeks  # Current week - will regenerate
        assert 7 in weeks

    def test_save_and_cleanup_progress(self):
        """Test saving and cleaning up progress."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = Path(tmpdir)

            progress = GenerationProgress(
                course_code="TEST101",
                total_weeks=10,
                completed_weeks=[1, 2]
            )

            # Save
            RecoveryManager.save_progress(course_path, progress)

            progress_file = RecoveryManager.get_progress_file_path(course_path)
            assert progress_file.exists()

            # Cleanup
            RecoveryManager.cleanup_progress(course_path)
            assert not progress_file.exists()


class TestUtilityFunctions:
    """Test utility functions."""

    def test_format_time_delta(self):
        """Test time delta formatting."""
        assert format_time_delta(30) == "30s"
        assert format_time_delta(90) == "1m"
        assert format_time_delta(3600) == "1h"
        assert format_time_delta(3900) == "1h 5m"

    def test_estimate_course_time(self):
        """Test course time estimation."""
        estimate = estimate_course_time(total_weeks=10, avg_minutes_per_week=50)

        assert "hours" in estimate
        # 10 weeks * 50 min = 500 min = 8.3 hours
        assert "8.3" in estimate


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
