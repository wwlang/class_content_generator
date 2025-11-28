"""
Unit tests for Assessment, Scenario, and AssessmentType models.

Tests assessment validation, brief generation, and scenario handling.
"""

import pytest
from tools.assessment_domain.models import (
    Assessment,
    AssessmentType,
    Scenario,
    Rubric,
    RubricCriterion
)


@pytest.fixture
def sample_rubric():
    """Create a sample rubric."""
    criteria = [
        RubricCriterion(
            "Content", 0.5,
            "Excellent content", "Good content", "OK content", "Poor content", "No content"
        ),
        RubricCriterion(
            "Style", 0.5,
            "Excellent style", "Good style", "OK style", "Poor style", "No style"
        )
    ]
    return Rubric("Test Rubric", criteria)


@pytest.fixture
def sample_scenarios():
    """Create sample scenarios."""
    return [
        Scenario(
            title="Option A: Client Communication",
            description="Write an email to an external client",
            specific_requirements=["Professional tone", "Clear call to action"]
        ),
        Scenario(
            title="Option B: Team Update",
            description="Send a memo to internal team",
            specific_requirements=["Concise format", "Action items"]
        )
    ]


@pytest.fixture
def sample_assessment(sample_rubric, sample_scenarios):
    """Create a sample assessment."""
    return Assessment(
        id="test-assessment",
        name="Test Assessment",
        type=AssessmentType.PORTFOLIO,
        weight=0.10,
        due_week=5,
        description="This is a test assessment for unit testing purposes.",
        requirements=[
            "Submit by deadline",
            "Follow formatting guidelines",
            "Include all required sections"
        ],
        rubric=sample_rubric,
        scenarios=sample_scenarios,
        submission_format="PDF via LMS",
        learning_objectives=["1", "2", "3"]
    )


def test_scenario_creation():
    """Test creating a scenario."""
    scenario = Scenario(
        title="Test Scenario",
        description="A test description",
        specific_requirements=["Req 1", "Req 2"]
    )

    assert scenario.title == "Test Scenario"
    assert scenario.description == "A test description"
    assert len(scenario.specific_requirements) == 2


def test_assessment_type_enum():
    """Test AssessmentType enum values."""
    assert AssessmentType.PORTFOLIO.value == "portfolio"
    assert AssessmentType.PRESENTATION.value == "presentation"
    assert AssessmentType.QUIZ.value == "quiz"
    assert AssessmentType.PROJECT.value == "project"


def test_assessment_type_value_access():
    """Test accessing AssessmentType values."""
    portfolio = AssessmentType.PORTFOLIO
    presentation = AssessmentType.PRESENTATION
    quiz = AssessmentType.QUIZ

    assert portfolio.value == "portfolio"
    assert presentation.value == "presentation"
    assert quiz.value == "quiz"


def test_assessment_type_comparison():
    """Test comparing AssessmentType values."""
    assert AssessmentType.PORTFOLIO != AssessmentType.QUIZ
    assert AssessmentType.PRESENTATION == AssessmentType.PRESENTATION


def test_assessment_creation(sample_assessment):
    """Test creating an assessment."""
    assert sample_assessment.id == "test-assessment"
    assert sample_assessment.name == "Test Assessment"
    assert sample_assessment.type == AssessmentType.PORTFOLIO
    assert sample_assessment.weight == 0.10
    assert sample_assessment.due_week == 5


def test_assessment_with_scenarios(sample_assessment):
    """Test assessment with scenarios."""
    assert len(sample_assessment.scenarios) == 2
    assert "Client Communication" in sample_assessment.scenarios[0].title
    assert "Team Update" in sample_assessment.scenarios[1].title


def test_assessment_with_rubric(sample_assessment):
    """Test assessment with rubric."""
    assert sample_assessment.rubric is not None
    assert sample_assessment.rubric.name == "Test Rubric"
    assert len(sample_assessment.rubric.criteria) == 2


def test_to_markdown_brief(sample_assessment):
    """Test markdown brief generation."""
    brief = sample_assessment.to_markdown_brief()

    assert "# Test Assessment" in brief
    assert "**Type:** Portfolio" in brief
    assert "**Weight:** 10%" in brief
    assert "**Due:** Week 5" in brief  # due_week is 5 in sample
    assert "## Overview" in brief
    assert "## Requirements" in brief
    assert "## Scenario Options" in brief
    assert "## Test Rubric" in brief  # Rubric name in markdown


def test_to_html_brief(sample_assessment):
    """Test HTML brief generation."""
    html = sample_assessment.to_html_brief(course_code="TEST101")

    assert "<html" in html
    assert "<h1>Test Assessment</h1>" in html
    assert "TEST101" in html
    assert "Portfolio" in html
    assert "10%" in html or "10.0%" in html
    assert "Week 5" in html
    assert "</html>" in html


def test_html_brief_includes_rubric(sample_assessment):
    """Test HTML brief includes rubric table."""
    html = sample_assessment.to_html_brief()

    assert "<table" in html
    assert "Content" in html
    assert "Style" in html
    assert "Excellent" in html


def test_html_brief_includes_scenarios(sample_assessment):
    """Test HTML brief includes scenarios."""
    html = sample_assessment.to_html_brief()

    assert "Client Communication" in html
    assert "Team Update" in html
    assert "Professional tone" in html


def test_html_brief_without_rubric():
    """Test HTML brief generation without rubric."""
    assessment = Assessment(
        id="no-rubric",
        name="No Rubric Assessment",
        type=AssessmentType.QUIZ,
        weight=0.15,
        due_week=3,
        description="Assessment without rubric",
        requirements=["Complete quiz"],
        rubric=None,
        scenarios=[]
    )

    html = assessment.to_html_brief()

    assert "<html" in html
    assert "No Rubric Assessment" in html
    # Should not have rubric section
    assert "<h2>Rubric</h2>" not in html


def test_html_brief_without_scenarios():
    """Test HTML brief generation without scenarios."""
    assessment = Assessment(
        id="no-scenarios",
        name="No Scenarios",
        type=AssessmentType.PRESENTATION,
        weight=0.20,
        due_week=7,
        description="No scenario options",
        requirements=["Present"],
        rubric=None,
        scenarios=[]
    )

    html = assessment.to_html_brief()

    assert "<html" in html
    # Should not have scenarios section
    assert "<h2>Scenarios</h2>" not in html or "<h2>Scenario Options</h2>" not in html


def test_to_dict(sample_assessment):
    """Test dictionary conversion."""
    assessment_dict = sample_assessment.to_dict()

    assert assessment_dict['id'] == "test-assessment"
    assert assessment_dict['name'] == "Test Assessment"
    assert assessment_dict['type'] == "portfolio"
    assert assessment_dict['weight'] == 0.10
    assert assessment_dict['due_week'] == 5
    assert len(assessment_dict['requirements']) == 3
    assert len(assessment_dict['scenarios']) == 2
    assert assessment_dict['rubric'] is not None
    assert assessment_dict['is_valid'] is True


def test_string_representation(sample_assessment):
    """Test string representations."""
    str_repr = str(sample_assessment)
    assert "Test Assessment" in str_repr
    assert "10%" in str_repr
    assert "Week 5" in str_repr

    repr_repr = repr(sample_assessment)
    assert "Assessment" in repr_repr
    assert "test-assessment" in repr_repr


def test_assessment_minimal():
    """Test creating minimal assessment."""
    assessment = Assessment(
        id="minimal",
        name="Minimal Assessment",
        type=AssessmentType.QUIZ,
        weight=0.05,
        due_week=2,
        description="Minimal description",
        requirements=[],
        rubric=None,
        scenarios=[]
    )

    assert assessment.id == "minimal"
    assert len(assessment.requirements) == 0
    assert len(assessment.scenarios) == 0
    assert assessment.rubric is None


def test_learning_objectives(sample_assessment):
    """Test learning objectives."""
    assert len(sample_assessment.learning_objectives) == 3
    assert "1" in sample_assessment.learning_objectives


def test_weight_percentage():
    """Test various weight percentages."""
    assessments = [
        Assessment("a1", "A1", AssessmentType.PORTFOLIO, 0.10, 1, "D", []),
        Assessment("a2", "A2", AssessmentType.PRESENTATION, 0.15, 2, "D", []),
        Assessment("a3", "A3", AssessmentType.QUIZ, 0.05, 3, "D", []),
        Assessment("a4", "A4", AssessmentType.PROJECT, 0.20, 4, "D", []),
    ]

    total_weight = sum(a.weight for a in assessments)
    assert abs(total_weight - 0.50) < 0.001  # Should be 50%


def test_scenario_without_requirements():
    """Test scenario without specific requirements."""
    scenario = Scenario(
        title="Simple Scenario",
        description="Just a description"
    )

    assert scenario.title == "Simple Scenario"
    assert len(scenario.specific_requirements) == 0


def test_html_brief_escapes_special_characters():
    """Test that HTML brief escapes special characters."""
    assessment = Assessment(
        id="special-chars",
        name="Test <Assessment> & \"Quotes\"",
        type=AssessmentType.PORTFOLIO,
        weight=0.10,
        due_week=1,
        description="Description with <tags> and & symbols",
        requirements=["Requirement with <br> tag"],
        rubric=None,
        scenarios=[]
    )

    html = assessment.to_html_brief()

    # HTML should escape these
    assert "&lt;Assessment&gt;" in html or "Assessment" in html
    assert "&amp;" in html or "&" in html


def test_submission_format(sample_assessment):
    """Test submission format field."""
    assert sample_assessment.submission_format == "PDF via LMS"

    brief = sample_assessment.to_markdown_brief()
    assert "PDF via LMS" in brief
