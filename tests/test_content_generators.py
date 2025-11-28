#!/usr/bin/env python3
"""
Unit tests for content generators.

Tests LectureGenerator, TutorialGenerator, and TutorNotesGenerator.
"""

import pytest
import tempfile
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from content_generators import (
    LectureGenerator,
    TutorialGenerator,
    TutorNotesGenerator
)


class TestBaseGenerator:
    """Test BaseGenerator functionality."""

    def create_test_course(self, tmpdir):
        """Create a test course with syllabus."""
        course_path = Path(tmpdir) / "TEST101-test-course"
        course_path.mkdir(parents=True)

        # Create syllabus
        syllabus = course_path / "syllabus.md"
        syllabus.write_text("""# Test Course

## Course Calendar

**Week 1: Introduction to Testing**
- Topic: Getting Started with Testing
- Objectives:
  - Understand testing fundamentals
  - Write basic test cases
  - Use testing frameworks

**Week 2: Advanced Testing**
- Topic: Complex Test Scenarios
""")

        # Create research directory
        working_dir = course_path / ".working" / "research"
        working_dir.mkdir(parents=True)

        # Create research file
        research = working_dir / "article-research-summary.md"
        research.write_text("""=== START RESEARCH OUTPUT ===

# Week 1 Research

## Required Concepts Coverage

- Testing fundamentals: ✓ In-depth
- Test cases: ✓ Explained with examples

## Final Selections

Article 1: Testing Best Practices (Author, 2024)
Article 2: Test-Driven Development (Smith, 2023)

=== END RESEARCH OUTPUT ===
""")

        return course_path

    def test_get_week_topic(self):
        """Test extracting week topic from syllabus."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            generator = LectureGenerator(course_path, 1)
            topic = generator.get_week_topic()

            assert topic == "Introduction to Testing"

    def test_get_learning_objectives(self):
        """Test extracting learning objectives from syllabus."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            generator = LectureGenerator(course_path, 1)
            objectives = generator.get_learning_objectives()

            assert len(objectives) == 3
            assert "Understand testing fundamentals" in objectives
            assert "Write basic test cases" in objectives
            assert "Use testing frameworks" in objectives

    def test_read_research(self):
        """Test reading research for a week."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            generator = LectureGenerator(course_path, 1)
            research = generator.read_research()

            assert "Week 1 Research" in research
            assert "Testing fundamentals" in research
            assert "Article 1" in research


class TestLectureGenerator:
    """Test LectureGenerator."""

    def create_test_course(self, tmpdir):
        """Create test course."""
        course_path = Path(tmpdir) / "TEST101-test-course"
        course_path.mkdir(parents=True)

        # Create syllabus
        syllabus = course_path / "syllabus.md"
        syllabus.write_text("""# Test Course

**Week 1: Introduction**
""")

        # Create research
        working_dir = course_path / ".working" / "research"
        working_dir.mkdir(parents=True)
        research = working_dir / "article-research-summary.md"
        research.write_text("=== START RESEARCH OUTPUT ===\n\n# Week 1 Research\n\n=== END ===")

        return course_path

    def test_generate_creates_context(self):
        """Test that generate() creates context file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            generator = LectureGenerator(course_path, 1)
            success, message = generator.generate()

            # Should create context file
            context_file = course_path / "weeks" / "week-01" / ".lecture-generation-context.md"
            assert context_file.exists()

            # Should return false (content not generated yet)
            assert success is False
            assert "context created" in message.lower()

    def test_validate_lecture_slide_count(self):
        """Test lecture validation - slide count."""
        generator = LectureGenerator(Path("/tmp"), 1)

        # Too few slides
        content = "**SLIDE 1: Title**\n" * 10
        is_valid, issues = generator.validate_generated_lecture(content)
        assert not is_valid
        assert any("Too few slides" in issue for issue in issues)

        # Good slide count
        content = "**SLIDE 1: Title**\n## Speaker Notes\nNotes here\n" * 25
        is_valid, issues = generator.validate_generated_lecture(content)
        assert is_valid or not any("slide" in issue.lower() for issue in issues)

    def test_validate_lecture_speaker_notes(self):
        """Test lecture validation - speaker notes."""
        generator = LectureGenerator(Path("/tmp"), 1)

        # Missing speaker notes
        content = "**SLIDE 1: Title**\nContent\n" * 25
        is_valid, issues = generator.validate_generated_lecture(content)
        assert not is_valid
        assert any("speaker notes" in issue.lower() for issue in issues)

    def test_validate_lecture_citations(self):
        """Test lecture validation - citations."""
        generator = LectureGenerator(Path("/tmp"), 1)

        # Missing citations
        content = "**SLIDE 1: Title**\n## Speaker Notes\nNotes\n" * 25
        is_valid, issues = generator.validate_generated_lecture(content)
        assert not is_valid
        assert any("citation" in issue.lower() for issue in issues)


class TestTutorialGenerator:
    """Test TutorialGenerator."""

    def create_test_course(self, tmpdir):
        """Create test course."""
        course_path = Path(tmpdir) / "TEST101-test-course"
        course_path.mkdir(parents=True)

        # Create syllabus
        syllabus = course_path / "syllabus.md"
        syllabus.write_text("""# Test Course

**Week 1: Introduction**

## Portfolio Rubric

| Criteria | Description |
|----------|-------------|
| Content Quality | Well-researched and organized |
| Analysis Depth | Critical thinking demonstrated |
| Writing Clarity | Clear and professional |
""")

        # Create research
        working_dir = course_path / ".working" / "research"
        working_dir.mkdir(parents=True)
        research = working_dir / "article-research-summary.md"
        research.write_text("=== START RESEARCH OUTPUT ===\n\n# Week 1 Research\n\n=== END ===")

        return course_path

    def test_generate_creates_context(self):
        """Test that generate() creates context file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            generator = TutorialGenerator(course_path, 1)
            success, message = generator.generate()

            # Should create context file
            context_file = course_path / "weeks" / "week-01" / ".tutorial-generation-context.md"
            assert context_file.exists()

            assert success is False
            assert "context created" in message.lower()

    def test_extract_rubric_criteria(self):
        """Test rubric criteria extraction from table."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course(tmpdir)

            generator = TutorialGenerator(course_path, 1)
            rubric_info = generator._extract_rubric_info()

            assert rubric_info['assessment_type'] == "Portfolio"
            assert len(rubric_info['criteria']) > 0
            assert "Content Quality" in rubric_info['criteria']

    def test_validate_tutorial_structure(self):
        """Test tutorial validation - required sections."""
        generator = TutorialGenerator(Path("/tmp"), 1)

        # Missing sections
        content = "# Tutorial\n\nSome content"
        is_valid, issues = generator.validate_generated_tutorial(content)
        assert not is_valid
        assert len(issues) > 0

        # All sections present
        content = """# Opening

Content here (10 min)

# Main Activity

Activity content (60 min)

Peer review using rubric

# Quiz Prep

1. Question one?
2. Question two?
3. Question three?
4. Question four?
5. Question five?

# Wrap-up

Summary (5 min)
"""
        is_valid, issues = generator.validate_generated_tutorial(content)
        assert is_valid


class TestTutorNotesGenerator:
    """Test TutorNotesGenerator."""

    def create_test_course_with_tutorial(self, tmpdir):
        """Create test course with tutorial."""
        course_path = Path(tmpdir) / "TEST101-test-course"
        weeks_dir = course_path / "weeks" / "week-01"
        weeks_dir.mkdir(parents=True)

        # Create tutorial
        tutorial = weeks_dir / "tutorial-content.md"
        tutorial.write_text("""# Tutorial

## Quiz Prep

1. What is testing?
2. Why is testing important?
3. Name three types of tests.
""")

        # Create research
        working_dir = course_path / ".working" / "research"
        working_dir.mkdir(parents=True)
        research = working_dir / "article-research-summary.md"
        research.write_text("# Week 1 Research")

        # Create syllabus
        syllabus = course_path / "syllabus.md"
        syllabus.write_text("**Week 1: Introduction**")

        return course_path

    def test_generate_requires_tutorial(self):
        """Test that tutor notes require tutorial to exist first."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = Path(tmpdir) / "TEST101-test-course"
            course_path.mkdir()

            generator = TutorNotesGenerator(course_path, 1)
            success, message = generator.generate()

            assert success is False
            assert "tutorial must be generated" in message.lower()

    def test_generate_creates_context(self):
        """Test that generate() creates context file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course_with_tutorial(tmpdir)

            generator = TutorNotesGenerator(course_path, 1)
            success, message = generator.generate()

            # Should create context file
            context_file = course_path / "weeks" / "week-01" / ".tutor-notes-generation-context.md"
            assert context_file.exists()

            assert success is False
            assert "context created" in message.lower()

    def test_extract_quiz_questions(self):
        """Test extracting quiz questions from tutorial."""
        with tempfile.TemporaryDirectory() as tmpdir:
            course_path = self.create_test_course_with_tutorial(tmpdir)

            generator = TutorNotesGenerator(course_path, 1)
            tutorial_content = (course_path / "weeks" / "week-01" / "tutorial-content.md").read_text()

            questions = generator._extract_quiz_questions(tutorial_content)

            assert len(questions) == 3
            assert "What is testing?" in questions[0]

    def test_validate_tutor_notes_structure(self):
        """Test tutor notes validation."""
        generator = TutorNotesGenerator(Path("/tmp"), 1)

        # Missing sections
        content = "# Notes\n\nSome guidance"
        is_valid, issues = generator.validate_generated_notes(content)
        assert not is_valid

        # Complete notes
        content = """# Quiz Answer Key

Correct answer: Testing is...
Explanation: This is important because...

# Expected Student Approaches

Approach 1: Students might...
Approach 2: Alternative approach...
Approach 3: Third approach...

# Facilitation Guidance

Vietnamese students often...
"""
        is_valid, issues = generator.validate_generated_notes(content)
        assert is_valid


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
