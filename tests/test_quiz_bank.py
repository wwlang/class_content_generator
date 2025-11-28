"""
Unit tests for QuizBank model.

Tests quiz bank validation, distribution checks, and question management.
"""

import pytest
from tools.assessment_domain.models import Question, QuizBank, BloomLevel, QuestionType


@pytest.fixture
def sample_questions():
    """Create sample questions for testing."""
    questions = []

    # Create 15 Remembering questions
    for i in range(15):
        questions.append(Question(
            id=f"W{(i % 3) + 1}-Q{i+1}-test-{i}",
            week=(i % 3) + 1,
            topic=f"Test Topic {i}",
            question_text=f"What is test question {i}?",
            options={'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING,
            question_type=QuestionType.MULTIPLE_CHOICE
        ))

    # Create 15 Understanding questions
    for i in range(15, 30):
        questions.append(Question(
            id=f"W{(i % 3) + 1}-Q{i+1}-test-{i}",
            week=(i % 3) + 1,
            topic=f"Test Topic {i}",
            question_text=f"Why does test question {i} matter?",
            options={'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
            correct_answer='B',
            feedback={'A': 'Wrong', 'B': 'Correct', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.UNDERSTANDING,
            question_type=QuestionType.MULTIPLE_CHOICE
        ))

    return questions


def test_quiz_bank_creation(sample_questions):
    """Test creating a valid quiz bank."""
    quiz_bank = QuizBank(
        quiz_id="quiz-1",
        title="Quiz 1 - Weeks 1-3",
        weeks_covered=[1, 2, 3],
        questions=sample_questions,
        target_total=30,
        target_remembering=15,
        target_understanding=15
    )

    assert quiz_bank.quiz_id == "quiz-1"
    assert quiz_bank.title == "Quiz 1 - Weeks 1-3"
    assert quiz_bank.weeks_covered == [1, 2, 3]
    assert len(quiz_bank.questions) == 30


def test_validate_distribution_success(sample_questions):
    """Test validation passes with correct distribution."""
    quiz_bank = QuizBank(
        quiz_id="quiz-1",
        title="Test Quiz",
        weeks_covered=[1, 2, 3],
        questions=sample_questions,
        target_total=30,
        target_remembering=15,
        target_understanding=15
    )

    validation = quiz_bank.validate_distribution()

    assert validation['balanced'] is True
    assert validation['total'] == 30
    assert validation['remembering_count'] == 15
    assert validation['understanding_count'] == 15
    assert len(validation['errors']) == 0


def test_validate_distribution_wrong_total(sample_questions):
    """Test validation fails with wrong total count."""
    quiz_bank = QuizBank(
        quiz_id="quiz-1",
        title="Test Quiz",
        weeks_covered=[1, 2, 3],
        questions=sample_questions[:25],  # Only 25 questions
        target_total=30,
        target_remembering=15,
        target_understanding=15
    )

    validation = quiz_bank.validate_distribution()

    assert validation['balanced'] is False
    assert validation['total'] == 25
    assert len(validation['errors']) > 0
    assert any('Total questions' in error for error in validation['errors'])


def test_validate_distribution_unbalanced_bloom(sample_questions):
    """Test validation fails with unbalanced Bloom distribution."""
    # Create unbalanced set: first 15 are Remembering (0-14), next 15 are Understanding (15-29)
    # Take all 15 Remembering + extra 5 Remembering duplicates + only 10 Understanding
    unbalanced = (
        sample_questions[:15] +  # 15 Remembering
        [sample_questions[i] for i in range(5)] +  # 5 more Remembering (duplicates with different IDs)
        sample_questions[15:25]  # 10 Understanding
    )

    # Fix duplicate IDs
    for i, q in enumerate(unbalanced[15:20]):
        q.id = f"W{q.week}-Q{100+i}-duplicate"

    quiz_bank = QuizBank(
        quiz_id="quiz-1",
        title="Test Quiz",
        weeks_covered=[1, 2, 3],
        questions=unbalanced,
        target_total=30,
        target_remembering=15,
        target_understanding=15
    )

    validation = quiz_bank.validate_distribution()

    assert validation['balanced'] is False
    assert validation['remembering_count'] == 20
    assert validation['understanding_count'] == 10
    assert any('Remembering questions' in error for error in validation['errors'])
    assert any('Understanding questions' in error for error in validation['errors'])


def test_validate_distribution_duplicate_ids(sample_questions):
    """Test validation detects duplicate question IDs."""
    # Add a duplicate
    duplicate_questions = sample_questions[:29] + [sample_questions[0]]

    quiz_bank = QuizBank(
        quiz_id="quiz-1",
        title="Test Quiz",
        weeks_covered=[1, 2, 3],
        questions=duplicate_questions,
        target_total=30,
        target_remembering=15,
        target_understanding=15
    )

    validation = quiz_bank.validate_distribution()

    assert validation['balanced'] is False
    assert any('Duplicate question IDs' in error for error in validation['errors'])


def test_validate_distribution_wrong_weeks(sample_questions):
    """Test validation detects questions from wrong weeks."""
    # Add question from week 5
    wrong_week_q = Question(
        id="W5-Q1-wrong-week",
        week=5,
        topic="Wrong Week",
        question_text="From week 5?",
        options={'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
        correct_answer='A',
        feedback={'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
        bloom_level=BloomLevel.REMEMBERING
    )

    questions_with_wrong_week = sample_questions[:29] + [wrong_week_q]

    quiz_bank = QuizBank(
        quiz_id="quiz-1",
        title="Test Quiz",
        weeks_covered=[1, 2, 3],
        questions=questions_with_wrong_week,
        target_total=30,
        target_remembering=15,
        target_understanding=15
    )

    validation = quiz_bank.validate_distribution()

    assert validation['balanced'] is False
    assert any('wrong weeks' in error.lower() for error in validation['errors'])


def test_get_questions_by_week(sample_questions):
    """Test grouping questions by week."""
    quiz_bank = QuizBank(
        quiz_id="quiz-1",
        title="Test Quiz",
        weeks_covered=[1, 2, 3],
        questions=sample_questions,
        target_total=30,
        target_remembering=15,
        target_understanding=15
    )

    by_week = quiz_bank.get_questions_by_week()

    assert 1 in by_week
    assert 2 in by_week
    assert 3 in by_week
    assert len(by_week[1]) == 10
    assert len(by_week[2]) == 10
    assert len(by_week[3]) == 10


def test_get_questions_by_bloom(sample_questions):
    """Test grouping questions by Bloom level."""
    quiz_bank = QuizBank(
        quiz_id="quiz-1",
        title="Test Quiz",
        weeks_covered=[1, 2, 3],
        questions=sample_questions,
        target_total=30,
        target_remembering=15,
        target_understanding=15
    )

    by_bloom = quiz_bank.get_questions_by_bloom()

    assert BloomLevel.REMEMBERING in by_bloom
    assert BloomLevel.UNDERSTANDING in by_bloom
    assert len(by_bloom[BloomLevel.REMEMBERING]) == 15
    assert len(by_bloom[BloomLevel.UNDERSTANDING]) == 15


def test_to_dict(sample_questions):
    """Test dictionary conversion."""
    quiz_bank = QuizBank(
        quiz_id="quiz-1",
        title="Quiz 1 - Weeks 1-3",
        weeks_covered=[1, 2, 3],
        questions=sample_questions,
        target_total=30,
        target_remembering=15,
        target_understanding=15
    )

    quiz_dict = quiz_bank.to_dict()

    assert quiz_dict['quiz_id'] == "quiz-1"
    assert quiz_dict['title'] == "Quiz 1 - Weeks 1-3"
    assert quiz_dict['weeks_covered'] == [1, 2, 3]
    assert len(quiz_dict['questions']) == 30
    assert quiz_dict['distribution']['balanced'] is True
    assert 'week_distribution' in quiz_dict
    assert 'average_quality_score' in quiz_dict


def test_string_representation(sample_questions):
    """Test string representations."""
    quiz_bank = QuizBank(
        quiz_id="quiz-1",
        title="Quiz 1",
        weeks_covered=[1, 2, 3],
        questions=sample_questions[:10]
    )

    str_repr = str(quiz_bank)
    assert "quiz-1" in str_repr
    assert "10" in str_repr  # Has 10 questions

    repr_repr = repr(quiz_bank)
    assert "QuizBank" in repr_repr
    assert "quiz-1" in repr_repr
    assert "questions=10" in repr_repr


def test_empty_quiz_bank():
    """Test creating empty quiz bank."""
    quiz_bank = QuizBank(
        quiz_id="empty",
        title="Empty Quiz",
        weeks_covered=[1],
        questions=[]
    )

    assert len(quiz_bank.questions) == 0

    validation = quiz_bank.validate_distribution()
    assert validation['balanced'] is False
    assert validation['total'] == 0


def test_custom_targets(sample_questions):
    """Test quiz bank with custom targets."""
    quiz_bank = QuizBank(
        quiz_id="quiz-custom",
        title="Custom Quiz",
        weeks_covered=[1, 2, 3],
        questions=sample_questions[:20],
        target_total=20,
        target_remembering=13,
        target_understanding=7
    )

    validation = quiz_bank.validate_distribution()

    assert validation['target_total'] == 20
    assert validation['target_remembering'] == 13
    assert validation['target_understanding'] == 7

    # Check if distribution is close enough (we have 15/15 from sample)
    assert validation['total'] == 20
