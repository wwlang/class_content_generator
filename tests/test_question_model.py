"""
Unit tests for Question domain model.

Tests validation rules, quality scoring, and business logic.
"""

import pytest
from tools.assessment_domain.models import Question, QuestionType, BloomLevel


class TestQuestionValidation:
    """Test Question validation rules."""

    def test_valid_question(self):
        """Test that a properly formatted question passes validation."""
        question = Question(
            id='W1-Q1-Shannon',
            week=1,
            topic='Shannon-Weaver Model',
            question_text='How many components are in the Shannon-Weaver communication model?',
            options={
                'A': 'Five components',
                'B': 'Six components',
                'C': 'Seven components',
                'D': 'Eight components'
            },
            correct_answer='C',
            feedback={
                'A': 'Incorrect. The model has seven components.',
                'B': 'Incorrect. The model includes seven components total.',
                'C': 'Correct. The model includes sender, encoder, channel, noise, decoder, receiver, and feedback.',
                'D': 'Incorrect. There are seven components in the Shannon-Weaver model.'
            },
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert len(errors) == 0, f"Expected no errors, got: {errors}"
        assert question.is_valid()

    def test_invalid_option_count(self):
        """Test that questions without exactly 4 options fail validation."""
        question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text='Test question?',
            options={'A': 'Option A', 'B': 'Option B'},  # Only 2 options
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert any('4 options' in error for error in errors)
        assert not question.is_valid()

    def test_wrong_option_labels(self):
        """Test that options must be labeled A, B, C, D."""
        question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text='Test question?',
            options={'1': 'One', '2': 'Two', '3': 'Three', '4': 'Four'},  # Wrong labels
            correct_answer='1',
            feedback={'1': 'Correct', '2': 'Wrong', '3': 'Wrong', '4': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert any('A, B, C, D' in error for error in errors)

    def test_correct_answer_not_in_options(self):
        """Test that correct answer must be one of the options."""
        question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text='Test question?',
            options={'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
            correct_answer='E',  # Not in options
            feedback={'A': 'Wrong', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert any('not in options' in error for error in errors)

    def test_missing_feedback(self):
        """Test that all options must have feedback."""
        question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text='Test question?',
            options={'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong'},  # Missing C and D
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert any('Missing feedback for option C' in error for error in errors)
        assert any('Missing feedback for option D' in error for error in errors)

    def test_empty_feedback(self):
        """Test that feedback cannot be empty strings."""
        question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text='Test question?',
            options={'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
            correct_answer='A',
            feedback={'A': 'Correct', 'B': '', 'C': 'Wrong', 'D': 'Wrong'},  # Empty feedback for B
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert any('empty feedback for option B' in error for error in errors)

    def test_all_of_the_above_prohibited_in_question(self):
        """Test that 'all of the above' is prohibited in question text."""
        question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text='Which of the following are true? Select all of the above.',
            options={'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert any('all of the above' in error.lower() for error in errors)

    def test_all_of_the_above_prohibited_in_options(self):
        """Test that 'all of the above' is prohibited in option text."""
        question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text='Test question?',
            options={
                'A': 'Option A',
                'B': 'Option B',
                'C': 'Option C',
                'D': 'All of the above'
            },
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert any('all of the above' in error.lower() and 'option D' in error for error in errors)

    def test_none_of_the_above_prohibited(self):
        """Test that 'none of the above' is prohibited."""
        question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text='Test question?',
            options={
                'A': 'Option A',
                'B': 'Option B',
                'C': 'Option C',
                'D': 'None of the above'
            },
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert any('none of the above' in error.lower() for error in errors)

    def test_double_negatives_detected(self):
        """Test that double negatives are flagged."""
        question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text='Which statement is not incorrect?',  # Double negative
            options={'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert any('double negative' in error.lower() for error in errors)

    def test_question_text_too_short(self):
        """Test that question text must be substantive."""
        question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text='What?',  # Too short
            options={'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert any('too short' in error for error in errors)

    def test_invalid_week_number(self):
        """Test that week must be 1-10."""
        question = Question(
            id='W99-Q1-Test',
            week=99,  # Invalid
            topic='Test',
            question_text='Test question?',
            options={'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert any('week must be 1-10' in error for error in errors)

    def test_invalid_id_format(self):
        """Test that ID must match W[week]-Q[number]-[topic] format."""
        question = Question(
            id='invalid-id',  # Wrong format
            week=1,
            topic='Test',
            question_text='Test question?',
            options={'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        )

        errors = question.validate()
        assert any('ID' in error and 'format' in error for error in errors)


class TestQuestionQualityScoring:
    """Test Question quality scoring logic."""

    def test_scenario_based_detection(self):
        """Test that scenario-based questions are detected."""
        # Scenario-based question (long with context)
        scenario_question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text=(
                "A manager needs to communicate a significant organizational change "
                "to their team of 15 employees. The change will affect work schedules "
                "and some job responsibilities. Which communication approach would be "
                "most effective for this situation?"
            ),
            options={'A': 'Email', 'B': 'Meeting', 'C': 'Memo', 'D': 'Text message'},
            correct_answer='B',
            feedback={'A': 'Wrong', 'B': 'Correct', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.UNDERSTANDING
        )

        assert scenario_question.is_scenario_based()

        # Non-scenario question (short, direct)
        direct_question = Question(
            id='W1-Q2-Test',
            week=1,
            topic='Test',
            question_text='What is communication?',
            options={'A': 'Process', 'B': 'Action', 'C': 'Event', 'D': 'System'},
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        )

        assert not direct_question.is_scenario_based()

    def test_detailed_feedback_check(self):
        """Test that detailed feedback is properly detected."""
        # Detailed feedback (>30 chars each)
        detailed_question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text='Test question?',
            options={'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
            correct_answer='A',
            feedback={
                'A': 'Correct. This answer demonstrates understanding of the key concept.',
                'B': 'Incorrect. This misses the main point of the framework.',
                'C': 'Incorrect. This confuses two different concepts.',
                'D': 'Incorrect. This is not supported by the lecture material.'
            },
            bloom_level=BloomLevel.REMEMBERING
        )

        assert detailed_question.has_detailed_feedback()

        # Brief feedback (<30 chars)
        brief_question = Question(
            id='W1-Q2-Test',
            week=1,
            topic='Test',
            question_text='Test question?',
            options={'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
            correct_answer='A',
            feedback={'A': 'Right', 'B': 'Wrong', 'C': 'No', 'D': 'Nope'},
            bloom_level=BloomLevel.REMEMBERING
        )

        assert not brief_question.has_detailed_feedback()

    def test_quality_score_calculation(self):
        """Test that quality scores are calculated correctly."""
        # High quality: scenario-based + detailed feedback + valid
        high_quality = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text=(
                "A project team leader notices that one team member consistently "
                "dominates meetings while others remain silent. Using DISC communication "
                "styles, what approach would best address this situation?"
            ),
            options={
                'A': 'Confront the dominant member publicly',
                'B': 'Adapt facilitation to encourage all styles',
                'C': 'Cancel future meetings',
                'D': 'Ignore the behavior'
            },
            correct_answer='B',
            feedback={
                'A': 'Incorrect. Public confrontation is unlikely to improve dynamics.',
                'B': 'Correct. Adapting to different DISC styles creates inclusive communication.',
                'C': 'Incorrect. Meetings are still needed for team coordination.',
                'D': 'Incorrect. Ignoring the issue prevents team growth.'
            },
            bloom_level=BloomLevel.UNDERSTANDING
        )

        # Base score (10) + scenario (2) + detailed feedback (2) + valid (2) = 16
        assert high_quality.get_quality_score() == 16

        # Low quality: no scenario, brief feedback, but valid
        low_quality = Question(
            id='W1-Q2-Test',
            week=1,
            topic='Test',
            question_text='What is DISC?',
            options={'A': 'Framework', 'B': 'Tool', 'C': 'Model', 'D': 'System'},
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong', 'C': 'No', 'D': 'Nope'},
            bloom_level=BloomLevel.REMEMBERING
        )

        # Base score (10) + valid (2) = 12
        assert low_quality.get_quality_score() == 12


class TestQuestionEnums:
    """Test Question enum types."""

    def test_bloom_level_from_string(self):
        """Test parsing Bloom levels from strings."""
        assert BloomLevel.from_string('remembering') == BloomLevel.REMEMBERING
        assert BloomLevel.from_string('Remembering') == BloomLevel.REMEMBERING
        assert BloomLevel.from_string('REMEMBERING') == BloomLevel.REMEMBERING
        assert BloomLevel.from_string('understanding') == BloomLevel.UNDERSTANDING

    def test_bloom_level_invalid_string(self):
        """Test that invalid Bloom levels raise errors."""
        with pytest.raises(ValueError):
            BloomLevel.from_string('applying')  # Not supported

        with pytest.raises(ValueError):
            BloomLevel.from_string('invalid')


class TestQuestionDataConversion:
    """Test Question data conversion methods."""

    def test_to_dict(self):
        """Test converting question to dictionary."""
        question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test Topic',
            question_text='Test question?',
            options={'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
            correct_answer='C',
            feedback={'A': 'Wrong', 'B': 'Wrong', 'C': 'Correct', 'D': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        )

        data = question.to_dict()

        assert data['id'] == 'W1-Q1-Test'
        assert data['week'] == 1
        assert data['bloom_level'] == 'remembering'
        assert data['question_type'] == 'multiple_choice'
        assert 'quality_score' in data
        assert 'is_scenario_based' in data
        assert 'is_valid' in data

    def test_string_representations(self):
        """Test __str__ and __repr__ methods."""
        question = Question(
            id='W1-Q1-Test',
            week=1,
            topic='Test',
            question_text='Test?',
            options={'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
            correct_answer='A',
            feedback={'A': 'Right', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.UNDERSTANDING
        )

        str_repr = str(question)
        assert 'W1-Q1-Test' in str_repr
        assert 'Week 1' in str_repr
        assert 'understanding' in str_repr

        repr_str = repr(question)
        assert 'Question(' in repr_str
        assert "id='W1-Q1-Test'" in repr_str
