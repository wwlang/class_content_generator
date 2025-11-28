"""
Unit tests for QuizMarkdownParser and HandbookParser.

Tests markdown parsing logic and error handling.
"""

import pytest
from pathlib import Path
from tools.assessment_domain.parsers import QuizMarkdownParser, HandbookParser
from tools.assessment_domain.models import BloomLevel, AssessmentType


class TestQuizMarkdownParser:
    """Tests for QuizMarkdownParser."""

    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return QuizMarkdownParser(infer_bloom=True)

    @pytest.fixture
    def sample_quiz_content(self):
        """Sample quiz markdown content."""
        return """**Topic:** Communication Models
**Prepares for:** Quiz 1
**Source:** lecture-content.md

### Q1: Shannon-Weaver Model
**Type:** Multiple Choice

According to the Shannon-Weaver model, what is noise?

A) Only technical issues
B) Any interference that distorts the message
C) The receiver's interpretation
D) The feedback loop

**Answer:** B
**Feedback:** B is correct because noise refers to any interference. A is incorrect as noise includes more than technical issues. C and D are other model components.

---

### Q2: Communication Process
**Type:** Multiple Choice
**Bloom's Level:** Understanding

Why is feedback important in communication?

A) It makes messages longer
B) It confirms the message was understood
C) It replaces the original message
D) It eliminates noise

**Answer:** B
**Feedback:** B is correct because feedback confirms understanding. A, C, and D are incorrect interpretations of feedback's role.
"""

    def test_extract_week_from_path(self, parser):
        """Test extracting week number from file path."""
        path = Path("courses/BCI2AU/weeks/week-03/quiz-questions.md")
        week = parser._extract_week_from_path(path)
        assert week == 3

    def test_extract_week_from_path_different_format(self, parser):
        """Test extracting week from different path format."""
        path = Path("/some/path/week-10/quiz.md")
        week = parser._extract_week_from_path(path)
        assert week == 10

    def test_extract_week_no_match_raises_error(self, parser):
        """Test error when no week number found."""
        path = Path("courses/BCI2AU/quiz.md")
        with pytest.raises(ValueError, match="Cannot extract week number"):
            parser._extract_week_from_path(path)

    def test_parse_metadata(self, parser, sample_quiz_content):
        """Test parsing metadata from quiz content."""
        metadata = parser._parse_metadata(sample_quiz_content)

        assert metadata.topic == "Communication Models"
        assert metadata.prepares_for == "Quiz 1"
        assert metadata.source == "lecture-content.md"

    def test_split_questions(self, parser, sample_quiz_content):
        """Test splitting content into question sections."""
        sections = parser._split_questions(sample_quiz_content)

        assert len(sections) == 2
        assert "Q1" in sections[0]
        assert "Q2" in sections[1]

    def test_infer_bloom_understanding(self, parser):
        """Test inferring Understanding level."""
        section = "Why is this important? How does it work?"
        level = parser._infer_bloom_level(section)
        assert level == BloomLevel.UNDERSTANDING

    def test_infer_bloom_remembering(self, parser):
        """Test inferring Remembering level."""
        section = "What is the definition? List the components."
        level = parser._infer_bloom_level(section)
        assert level == BloomLevel.REMEMBERING

    def test_extract_question_text(self, parser):
        """Test extracting question text."""
        section = """### Q1: Topic
**Type:** Multiple Choice

This is the question text?

A) Option A
"""
        question_text = parser._extract_question_text(section)
        assert question_text == "This is the question text?"

    def test_extract_options(self, parser):
        """Test extracting answer options."""
        section = """
A) First option
B) Second option
C) Third option
D) Fourth option

**Answer:** C
"""
        options = parser._extract_options(section)

        assert len(options) == 4
        assert options['A'] == "First option"
        assert options['D'] == "Fourth option"

    def test_extract_answer(self, parser):
        """Test extracting correct answer."""
        section = "**Answer:** C"
        answer = parser._extract_answer(section)
        assert answer == "C"

    def test_extract_feedback(self, parser):
        """Test extracting feedback."""
        section = "**Feedback:** C is correct because of reasons."
        options = {'A': 'Opt A', 'B': 'Opt B', 'C': 'Opt C', 'D': 'Opt D'}
        feedback = parser._extract_feedback(section, options, 'C')

        assert 'A' in feedback
        assert 'C' in feedback
        assert "Correct" in feedback['C']

    def test_slugify(self, parser):
        """Test text slugification."""
        text = "Communication Models & Theory!"
        slug = parser._slugify(text)

        assert slug == "communication-models-theory"
        assert len(slug) <= 30


class TestHandbookParser:
    """Tests for HandbookParser."""

    @pytest.fixture
    def parser(self):
        """Create parser instance."""
        return HandbookParser()

    @pytest.fixture
    def sample_handbook_content(self):
        """Sample handbook markdown content."""
        return """# Assessment Handbook

## Assessment Overview

| Assessment | Type | Weight | Due Week | Learning Objectives |
|-----------|------|--------|----------|-------------------|
| Email + Memo | Portfolio | 10% | Week 3 | 1, 2, 9 |
| Mini-Pitch | Presentation | 10% | Week 5 | 3-5 |

### 1. Email + Memo (10%)

#### Overview
Students will demonstrate professional communication skills.

#### Requirements
- [ ] Professional email (200 words)
- [ ] Business memo (300 words)
- [ ] APA citations

#### Submission Format
Submit as single PDF via LMS.

**File naming:** STUDENTID_EmailMemo.pdf

## Rubrics

### Written Communication Rubric

Used for: Email, Memo, Reports

| Criteria | Excellent (94-100%) | Good (84-93%) | Satisfactory (74-83%) | Poor (60-73%) | Failing (<60%) |
|----------|-------------------|--------------|---------------------|--------------|---------------|
| **Content** | Exceptional depth | Good depth | Adequate depth | Limited depth | No depth |
| **Style** | Exceptional style | Good style | Adequate style | Poor style | No style |
"""

    def test_parse_overview_table(self, parser, sample_handbook_content):
        """Test parsing assessment overview table."""
        parser.content = sample_handbook_content
        overview = parser._parse_overview_table()

        assert len(overview) == 2
        assert overview[0].name == "Email + Memo"
        assert overview[0].weight_str == "10%"
        assert overview[0].due_week == 3
        assert "1" in overview[0].learning_objectives

    def test_parse_weight(self, parser):
        """Test parsing weight string."""
        assert parser._parse_weight("10%") == 0.10
        assert parser._parse_weight("15%") == 0.15
        assert parser._parse_weight("5") == 0.05

    def test_parse_type(self, parser):
        """Test parsing assessment type."""
        assert parser._parse_type("Portfolio") == AssessmentType.PORTFOLIO
        assert parser._parse_type("Presentation") == AssessmentType.PRESENTATION
        assert parser._parse_type("Quiz") == AssessmentType.QUIZ

    def test_parse_description(self, parser):
        """Test extracting task overview."""
        section = """### 1. Assessment Name

#### Overview
This is the task description.
It spans multiple lines.

#### Requirements
"""
        description = parser._parse_description(section)
        assert "task description" in description

    def test_parse_requirements(self, parser):
        """Test parsing requirements checklist."""
        section = """#### Requirements
- [ ] First requirement
- [ ] Second requirement
- [ ] Third requirement
"""
        requirements = parser._parse_requirements(section)

        assert len(requirements) == 3
        assert "First requirement" in requirements

    def test_parse_submission_format(self, parser):
        """Test parsing submission format."""
        section = """#### Submission Format
Submit as PDF via LMS.

**File naming:** STUDENTID_Assessment.pdf
"""
        submission = parser._parse_submission_format(section)

        assert "PDF via LMS" in submission
        assert "File naming" in submission

    def test_parse_rubric_table(self, parser):
        """Test parsing rubric table."""
        table_content = """| **Content** | Excellent depth | Good depth | OK depth | Poor depth | No depth |
| **Style** | Excellent style | Good style | OK style | Poor style | No style |"""

        criteria = parser._parse_rubric_table(table_content)

        assert len(criteria) == 2
        assert criteria[0].name == "Content"
        assert criteria[1].name == "Style"
        assert "Excellent depth" in criteria[0].excellent

        # Check weights sum to 1.0
        total_weight = sum(c.weight for c in criteria)
        assert abs(total_weight - 1.0) < 0.001

    def test_find_rubric_for_assessment(self, parser):
        """Test finding appropriate rubric."""
        parser.rubrics_cache = {
            'written communication': "RubricObject1",
            'presentation': "RubricObject2"
        }

        # Email should match written communication
        rubric = parser._find_rubric_for_assessment("Email + Memo")
        assert rubric == "RubricObject1"

        # Pitch should match presentation
        rubric = parser._find_rubric_for_assessment("Mini-Pitch")
        assert rubric == "RubricObject2"

    def test_slugify(self, parser):
        """Test slugification."""
        slug = parser._slugify("Email + Memo Assessment")
        assert slug == "email-memo-assessment"
        assert "-" in slug
        assert "+" not in slug


def test_quiz_parser_integration(tmp_path):
    """Integration test: Parse complete quiz file."""
    quiz_content = """**Topic:** Test Topic
**Prepares for:** Quiz 1

### Q1: Test Question
**Type:** Multiple Choice

What is 2+2?

A) 3
B) 4
C) 5
D) 6

**Answer:** B
**Feedback:** B is correct. 2+2 equals 4.
"""
    # Create temp file
    quiz_file = tmp_path / "quiz-questions.md"
    quiz_file.write_text(quiz_content)

    # Mock the path to include week-1
    test_file = tmp_path / "week-1" / "quiz-questions.md"
    test_file.parent.mkdir()
    test_file.write_text(quiz_content)

    # Parse
    parser = QuizMarkdownParser()
    questions = parser.parse_file(test_file)

    assert len(questions) == 1
    assert questions[0].topic == "Test Question"
    assert questions[0].correct_answer == "B"
    assert questions[0].week == 1


def test_handbook_parser_integration(tmp_path):
    """Integration test: Parse complete handbook file."""
    handbook_content = """## Assessment Overview

| Assessment | Type | Weight | Due Week | Learning Objectives |
|-----------|------|--------|----------|-------------------|
| Test Assignment | Portfolio | 10% | Week 3 | 1, 2 |

### 1. Test Assignment (10%)

#### Overview
Test description.

#### Requirements
- [ ] Requirement 1

## Rubrics

### Test Rubric

| Criteria | Excellent (94-100%) | Good (84-93%) | Satisfactory (74-83%) | Poor (60-73%) | Failing (<60%) |
|----------|-------------------|--------------|---------------------|--------------|---------------|
| **Content** | Excellent | Good | OK | Poor | Fail |
"""
    # Create temp file
    handbook_file = tmp_path / "assessment-handbook.md"
    handbook_file.write_text(handbook_content)

    # Parse
    parser = HandbookParser()
    assessments = parser.parse_file(handbook_file)

    assert len(assessments) > 0
    assert "test-assignment" in assessments
    assessment = assessments["test-assignment"]
    assert assessment.name == "Test Assignment"
    assert assessment.weight == 0.10
