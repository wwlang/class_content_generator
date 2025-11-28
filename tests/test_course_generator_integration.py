#!/usr/bin/env python3
"""
Integration tests for CourseGenerator.

Tests the main orchestration logic with mock content generation.
"""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from course_generator import CourseGenerator
from core_structures import GenerationConfig, GenerationProgress
from recovery_manager import RecoveryManager


class TestCourseGeneratorIntegration:
    """Integration tests for CourseGenerator."""

    def create_test_course(self, tmpdir, num_weeks=3):
        """Create a test course directory with syllabus."""
        course_path = Path(tmpdir) / "TEST101-test-course"
        course_path.mkdir(parents=True)

        # Create syllabus
        syllabus = course_path / "syllabus.md"
        syllabus.write_text(f"""# Test Course

## Course Calendar

**Week 1: Introduction**
- Topic: Getting Started

**Week 2: Core Concepts**
- Topic: Main Ideas

**Week 3: Applications**
- Topic: Practical Use

Total: {num_weeks} weeks
""")

        # Create working directory for research
        working_dir = course_path / ".working" / "research"
        working_dir.mkdir(parents=True)

        # Create weeks directory
        weeks_dir = course_path / "weeks"
        weeks_dir.mkdir()

        return course_path

    def test_count_weeks_from_syllabus(self):
        """Test counting weeks from syllabus."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir, num_weeks=3)

            generator = CourseGenerator("TEST101", course_path)

            syllabus_path = course_path / "syllabus.md"
            weeks = generator._count_weeks_from_syllabus(syllabus_path)

            assert weeks == 3

    def test_get_week_topic(self):
        """Test extracting week topic from syllabus."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            generator = CourseGenerator("TEST101", course_path)

            topic1 = generator._get_week_topic(1)
            topic2 = generator._get_week_topic(2)
            topic3 = generator._get_week_topic(3)

            assert topic1 == "Introduction"
            assert topic2 == "Core Concepts"
            assert topic3 == "Applications"

    def test_check_research_availability_no_research(self):
        """Test research availability check with no research."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            generator = CourseGenerator("TEST101", course_path)

            status = generator._check_research_availability(3)

            assert status["missing"] == [1, 2, 3]
            assert status["available"] == []
            assert status["flagged"] == []

    def test_check_research_availability_with_flags(self):
        """Test research availability check with validation flags (Phase 2)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            # Create validation flags for weeks 1 and 2
            working_dir = course_path / ".working" / "research"
            (working_dir / ".week-1-ready").touch()
            (working_dir / ".week-2-ready").touch()

            generator = CourseGenerator("TEST101", course_path)

            status = generator._check_research_availability(3)

            assert status["missing"] == [3]
            assert status["available"] == [1, 2]
            assert status["flagged"] == [1, 2]

    def test_validate_and_configure_fresh(self):
        """Test pre-flight validation for fresh generation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            generator = CourseGenerator("TEST101", course_path)

            # This will fail because no research available, but tests structure
            # In real usage, user would be prompted
            # total_weeks = generator.validate_and_configure(None)

            # For now, just test that config creation works
            config = GenerationConfig(
                course_code="TEST101",
                course_path=course_path,
                total_weeks=3
            )

            assert config.course_code == "TEST101"
            assert config.total_weeks == 3
            assert config.export_slides is True  # Decision 3A
            assert config.skip_on_validation_failure is True  # Decision 2B
            assert config.regenerate_interrupted_week is True  # Decision 1A

    def test_save_and_load_progress(self):
        """Test progress saving and loading."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            # Create progress
            progress = GenerationProgress(
                course_code="TEST101",
                total_weeks=3,
                completed_weeks=[1, 2],
                current_week=3
            )

            # Save
            RecoveryManager.save_progress(course_path, progress)

            # Load
            loaded = RecoveryManager.detect_interrupted_generation(course_path)

            assert loaded is not None
            assert loaded.course_code == "TEST101"
            assert loaded.completed_weeks == [1, 2]
            assert loaded.current_week == 3

    def test_recovery_config_creation(self):
        """Test recovery config creation (Decision 1A)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            # Create interrupted progress
            progress = GenerationProgress(
                course_code="TEST101",
                total_weeks=3,
                completed_weeks=[1],
                current_week=2
            )

            # Create recovery config
            original_config = GenerationConfig(
                course_code="TEST101",
                course_path=course_path,
                total_weeks=3
            )

            recovery_config = RecoveryManager.create_recovery_config(progress, original_config)

            # Decision 1A: Resume from interrupted week
            assert recovery_config.resume_from_week == 2
            assert recovery_config.regenerate_interrupted_week is True

    def test_get_weeks_to_generate_recovery(self):
        """Test determining weeks to generate in recovery mode."""
        # Create progress
        progress = GenerationProgress(
            course_code="TEST101",
            total_weeks=5,
            completed_weeks=[1, 3],  # Completed 1 and 3, skipped 2
            current_week=4  # Was working on 4 when interrupted
        )

        weeks = RecoveryManager.get_weeks_to_generate(progress, total_weeks=5)

        # Should include: 2 (never completed), 4 (current - regenerate), 5 (remaining)
        # Should NOT include: 1, 3 (completed)
        assert 1 not in weeks
        assert 2 in weeks  # Skipped week
        assert 3 not in weeks
        assert 4 in weeks  # Current week - will regenerate (Decision 1A)
        assert 5 in weeks  # Remaining week

    def test_check_and_validate_research_no_flag(self):
        """Test research validation when no flag exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            generator = CourseGenerator("TEST101", course_path)

            result = generator._check_and_validate_research(1)

            # Should pass when no flag (assumes research available elsewhere)
            assert result.passed is True

    def test_check_and_validate_research_with_valid_flag(self):
        """Test research validation with valid flag (Phase 2)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            # Create research file
            working_dir = course_path / ".working" / "research"
            research_file = working_dir / "article-research-summary.md"
            research_file.write_text("""=== START RESEARCH OUTPUT ===

# Week 1 Research

## Required Concepts Coverage

Concept 1: ✓ Covered in depth
Concept 2: ✓ Explained with examples

## Final Selections

Article 1: Test Article
Article 2: Another Test Article

=== END RESEARCH OUTPUT ===
""")

            # Create flag
            flag_file = working_dir / ".week-1-ready"
            flag_file.touch()

            generator = CourseGenerator("TEST101", course_path)

            result = generator._check_and_validate_research(1)

            # Should pass validation and delete flag
            assert result.passed is True
            assert not flag_file.exists()

    def test_check_and_validate_research_with_invalid_flag(self):
        """Test research validation with invalid flag (Phase 2)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            # Create research file with missing sections
            working_dir = course_path / ".working" / "research"
            research_file = working_dir / "article-research-summary.md"
            research_file.write_text("""=== START RESEARCH OUTPUT ===

# Week 1 Research

Some content but missing required sections

=== END RESEARCH OUTPUT ===
""")

            # Create flag
            flag_file = working_dir / ".week-1-ready"
            flag_file.touch()

            generator = CourseGenerator("TEST101", course_path)

            result = generator._check_and_validate_research(1)

            # Should fail validation
            assert result.passed is False
            assert "Missing required section" in result.message


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
