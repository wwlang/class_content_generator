"""
Unit tests for Rubric and RubricCriterion models.

Tests rubric validation, weight normalization, and export formats.
"""

import pytest
from tools.assessment_domain.models import Rubric, RubricCriterion


@pytest.fixture
def sample_criterion():
    """Create a sample rubric criterion."""
    return RubricCriterion(
        name="Content & Strategy",
        weight=0.25,
        excellent="Demonstrates exceptional understanding with clear strategic approach",
        good="Shows solid understanding with good strategic thinking",
        satisfactory="Adequate understanding with basic strategy",
        poor="Limited understanding with weak strategy",
        failing="No understanding or strategy evident"
    )


@pytest.fixture
def sample_rubric():
    """Create a sample rubric with multiple criteria."""
    criteria = [
        RubricCriterion(
            name="Content & Strategy",
            weight=0.25,
            excellent="Exceptional content",
            good="Good content",
            satisfactory="Adequate content",
            poor="Poor content",
            failing="No content"
        ),
        RubricCriterion(
            name="Structure & Organization",
            weight=0.25,
            excellent="Exceptional structure",
            good="Good structure",
            satisfactory="Adequate structure",
            poor="Poor structure",
            failing="No structure"
        ),
        RubricCriterion(
            name="Language & Style",
            weight=0.25,
            excellent="Exceptional language",
            good="Good language",
            satisfactory="Adequate language",
            poor="Poor language",
            failing="No language"
        ),
        RubricCriterion(
            name="Professional Presentation",
            weight=0.25,
            excellent="Exceptional presentation",
            good="Good presentation",
            satisfactory="Adequate presentation",
            poor="Poor presentation",
            failing="No presentation"
        )
    ]

    return Rubric(
        name="Written Communication Rubric",
        criteria=criteria,
        description="Used for: Email, Memo, Reports"
    )


def test_criterion_creation(sample_criterion):
    """Test creating a rubric criterion."""
    assert sample_criterion.name == "Content & Strategy"
    assert sample_criterion.weight == 0.25
    assert "exceptional" in sample_criterion.excellent.lower()
    assert "solid" in sample_criterion.good.lower()


def test_rubric_creation(sample_rubric):
    """Test creating a rubric."""
    assert sample_rubric.name == "Written Communication Rubric"
    assert len(sample_rubric.criteria) == 4
    assert sample_rubric.description == "Used for: Email, Memo, Reports"


def test_validate_weights_success(sample_rubric):
    """Test weight validation passes when sum equals 1.0."""
    errors = sample_rubric.validate()
    assert len(errors) == 0


def test_validate_weights_not_sum_to_one():
    """Test weight validation fails when sum doesn't equal 1.0."""
    criteria = [
        RubricCriterion("A", 0.3, "e", "g", "s", "p", "f"),
        RubricCriterion("B", 0.3, "e", "g", "s", "p", "f"),
        RubricCriterion("C", 0.3, "e", "g", "s", "p", "f"),  # Sum = 0.9
    ]

    rubric = Rubric("Test", criteria)
    errors = rubric.validate()

    assert len(errors) > 0
    assert any("0.90" in error for error in errors)


def test_validate_weights_negative_weight():
    """Test validation detects negative weights."""
    criteria = [
        RubricCriterion("A", -0.1, "e", "g", "s", "p", "f"),
        RubricCriterion("B", 1.1, "e", "g", "s", "p", "f"),
    ]

    rubric = Rubric("Test", criteria)
    errors = rubric.validate()

    assert len(errors) > 0
    # Should have error about weight must be 0.0-1.0
    assert any("0.0-1.0" in error for error in errors)


def test_validate_weights_over_one():
    """Test validation detects weights over 1.0."""
    criteria = [
        RubricCriterion("A", 1.5, "e", "g", "s", "p", "f"),
    ]

    rubric = Rubric("Test", criteria)
    errors = rubric.validate()

    assert len(errors) > 0
    assert any("0.0-1.0" in error for error in errors)


def test_normalize_weights():
    """Test that equal weights sum to 1.0."""
    criteria = [
        RubricCriterion("A", 0.25, "e", "g", "s", "p", "f"),
        RubricCriterion("B", 0.25, "e", "g", "s", "p", "f"),
        RubricCriterion("C", 0.25, "e", "g", "s", "p", "f"),
        RubricCriterion("D", 0.25, "e", "g", "s", "p", "f"),
    ]

    rubric = Rubric("Test", criteria)

    # Weights should already be normalized
    for criterion in rubric.criteria:
        assert abs(criterion.weight - 0.25) < 0.001

    # Sum should be 1.0
    total = sum(c.weight for c in rubric.criteria)
    assert abs(total - 1.0) < 0.001


def test_to_markdown_table(sample_rubric):
    """Test markdown table generation."""
    markdown = sample_rubric.to_markdown_table()

    assert "## Written Communication Rubric" in markdown
    assert "| Criteria |" in markdown
    assert "Excellent" in markdown
    assert "Content & Strategy" in markdown
    assert "Language & Style" in markdown
    assert "25%" in markdown  # Weight percentage


def test_to_html_table(sample_rubric):
    """Test HTML table generation."""
    html = sample_rubric.to_html_table()

    assert "<table" in html
    assert "<th>Criteria</th>" in html
    assert "<th>Excellent" in html
    assert "Content & Strategy" in html
    assert "25%" in html
    assert "</table>" in html


def test_to_simplified_3_levels(sample_rubric):
    """Test simplifying rubric to 3 levels."""
    simplified = sample_rubric.to_simplified(num_levels=3)

    assert len(simplified.criteria) == len(sample_rubric.criteria)
    assert "Simplified" in simplified.name

    # Check mapping for 3-level rubric
    for orig, simp in zip(sample_rubric.criteria, simplified.criteria):
        assert simp.excellent == orig.excellent
        assert simp.good == orig.satisfactory  # Good maps to Satisfactory
        assert simp.satisfactory == orig.poor   # Satisfactory maps to Poor
        assert simp.poor == orig.failing        # Poor maps to Failing
        assert simp.failing == ""               # Failing is empty


def test_to_simplified_invalid_levels(sample_rubric):
    """Test that invalid num_levels raises ValueError."""
    with pytest.raises(ValueError, match="Simplified rubric must have 2 or 3 levels"):
        sample_rubric.to_simplified(num_levels=5)


def test_get_criterion_by_name(sample_rubric):
    """Test finding criterion by name."""
    criterion = sample_rubric.get_criterion("Language & Style")

    assert criterion is not None
    assert criterion.name == "Language & Style"
    assert "language" in criterion.excellent.lower()


def test_get_criterion_not_found(sample_rubric):
    """Test finding non-existent criterion."""
    criterion = sample_rubric.get_criterion("Nonexistent")
    assert criterion is None


def test_to_dict(sample_rubric):
    """Test dictionary conversion."""
    rubric_dict = sample_rubric.to_dict()

    assert rubric_dict['name'] == "Written Communication Rubric"
    assert len(rubric_dict['criteria']) == 4
    assert rubric_dict['total_weight'] == 1.0
    assert rubric_dict['is_valid'] is True


def test_string_representation(sample_rubric):
    """Test string representations."""
    str_repr = str(sample_rubric)
    assert "Written Communication Rubric" in str_repr
    assert "4 criteria" in str_repr

    repr_repr = repr(sample_rubric)
    assert "Rubric" in repr_repr
    assert "Written Communication Rubric" in repr_repr


def test_empty_rubric():
    """Test creating rubric with no criteria."""
    rubric = Rubric("Empty", [])

    assert len(rubric.criteria) == 0
    errors = rubric.validate()
    assert len(errors) > 0  # Empty rubric should have error


def test_single_criterion_rubric():
    """Test rubric with single criterion."""
    criterion = RubricCriterion(
        "Single",
        1.0,
        "Excellent",
        "Good",
        "Satisfactory",
        "Poor",
        "Failing"
    )

    rubric = Rubric("Single Criterion", [criterion])

    assert len(rubric.criteria) == 1
    assert rubric.criteria[0].weight == 1.0
    errors = rubric.validate()
    assert len(errors) == 0


def test_criterion_weight_precision():
    """Test handling of floating point precision in weights."""
    criteria = [
        RubricCriterion("A", 0.333333, "e", "g", "s", "p", "f"),
        RubricCriterion("B", 0.333333, "e", "g", "s", "p", "f"),
        RubricCriterion("C", 0.333334, "e", "g", "s", "p", "f"),
    ]

    rubric = Rubric("Test", criteria)

    # Should be close enough to 1.0 (within tolerance)
    total = sum(c.weight for c in criteria)
    assert abs(total - 1.0) < 0.001

    # Validation should pass with small tolerance (0.01)
    errors = rubric.validate()
    assert len(errors) == 0
