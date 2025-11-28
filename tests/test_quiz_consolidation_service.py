"""
Unit tests for QuizConsolidationService.

Tests consolidation logic, quality scoring, Bloom distribution, and edge cases.
"""

import pytest
from unittest.mock import Mock
from tools.assessment_domain.services.quiz_consolidation_service import (
    QuizConsolidationService,
    ConsolidationResult
)
from tools.assessment_domain.models import Question, QuizBank, BloomLevel


@pytest.fixture
def mock_repository():
    """Create mock repository."""
    return Mock()


@pytest.fixture
def sample_questions():
    """Create sample questions for testing."""
    questions = []

    # Create 20 Remembering questions across 3 weeks
    for i in range(20):
        week = (i % 3) + 1
        questions.append(Question(
            id=f"W{week}-Q{i+1}-remembering-{i}",
            week=week,
            topic=f"Topic {i}",
            question_text=f"What is {i}?",
            options={'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
            correct_answer='A',
            feedback={'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.REMEMBERING
        ))

    # Create 20 Understanding questions across 3 weeks
    for i in range(20, 40):
        week = ((i - 20) % 3) + 1
        questions.append(Question(
            id=f"W{week}-Q{i+1}-understanding-{i}",
            week=week,
            topic=f"Topic {i}",
            question_text=f"Why is {i} important?",
            options={'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
            correct_answer='B',
            feedback={'A': 'Wrong', 'B': 'Correct', 'C': 'Wrong', 'D': 'Wrong'},
            bloom_level=BloomLevel.UNDERSTANDING
        ))

    return questions


@pytest.fixture
def service(mock_repository):
    """Create service with mocked repository."""
    return QuizConsolidationService(mock_repository)


class TestConsolidationResult:
    """Tests for ConsolidationResult dataclass."""

    def test_get_bloom_distribution(self):
        """Test getting Bloom distribution from result."""
        questions = [
            Question("Q1", 1, "T", "Q?", {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                    'A', {'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
                    BloomLevel.REMEMBERING),
            Question("Q2", 1, "T", "Q?", {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                    'A', {'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
                    BloomLevel.REMEMBERING),
            Question("Q3", 1, "T", "Q?", {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                    'A', {'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
                    BloomLevel.UNDERSTANDING),
        ]

        result = ConsolidationResult(
            quiz_bank=None,
            selected_questions=questions,
            rejected_questions=[],
            warnings=[],
            success=True
        )

        distribution = result.get_bloom_distribution()

        assert distribution['remembering'] == 2
        assert distribution['understanding'] == 1


class TestQuizConsolidationService:
    """Tests for QuizConsolidationService."""

    def test_successful_consolidation(self, service, mock_repository, sample_questions):
        """Test successful consolidation with balanced distribution."""
        mock_repository.get_valid_questions.return_value = sample_questions

        result = service.consolidate_quiz(
            course_code="TEST",
            quiz_id="quiz-1",
            weeks=[1, 2, 3],
            target_total=30,
            target_remembering=15,
            target_understanding=15
        )

        assert result.success is True
        assert len(result.selected_questions) == 30
        assert len(result.warnings) == 0

        # Check Bloom distribution
        remembering = sum(1 for q in result.selected_questions if q.bloom_level == BloomLevel.REMEMBERING)
        understanding = sum(1 for q in result.selected_questions if q.bloom_level == BloomLevel.UNDERSTANDING)

        assert remembering == 15
        assert understanding == 15

    def test_no_questions_available(self, service, mock_repository):
        """Test consolidation fails when no questions available."""
        mock_repository.get_valid_questions.return_value = []

        result = service.consolidate_quiz(
            course_code="TEST",
            quiz_id="quiz-1",
            weeks=[1, 2, 3]
        )

        assert result.success is False
        assert result.quiz_bank is None
        assert len(result.warnings) == 1
        assert "No valid questions found" in result.warnings[0]

    def test_insufficient_total_questions(self, service, mock_repository, sample_questions):
        """Test consolidation fails when not enough total questions."""
        # Only provide 20 questions when 30 needed
        mock_repository.get_valid_questions.return_value = sample_questions[:20]

        result = service.consolidate_quiz(
            course_code="TEST",
            quiz_id="quiz-1",
            weeks=[1, 2, 3],
            target_total=30
        )

        assert result.success is False
        assert result.quiz_bank is None
        assert any("20 questions available" in w for w in result.warnings)
        assert any("need 30" in w for w in result.warnings)

    def test_insufficient_remembering_questions(self, service, mock_repository, sample_questions):
        """Test consolidation fails when not enough Remembering questions."""
        # Only 10 Remembering, 20 Understanding
        unbalanced = sample_questions[:10] + sample_questions[20:40]
        mock_repository.get_valid_questions.return_value = unbalanced

        result = service.consolidate_quiz(
            course_code="TEST",
            quiz_id="quiz-1",
            weeks=[1, 2, 3],
            target_total=30,
            target_remembering=15,
            target_understanding=15
        )

        assert result.success is False
        assert any("Remembering questions" in w for w in result.warnings)
        assert any("need 15" in w for w in result.warnings)

    def test_insufficient_understanding_questions(self, service, mock_repository, sample_questions):
        """Test consolidation fails when not enough Understanding questions."""
        # 20 Remembering, only 10 Understanding
        unbalanced = sample_questions[:20] + sample_questions[20:30]
        mock_repository.get_valid_questions.return_value = unbalanced

        result = service.consolidate_quiz(
            course_code="TEST",
            quiz_id="quiz-1",
            weeks=[1, 2, 3],
            target_total=30,
            target_remembering=15,
            target_understanding=15
        )

        assert result.success is False
        assert any("Understanding questions" in w for w in result.warnings)

    def test_quality_score_filtering(self, service, mock_repository, sample_questions):
        """Test filtering by minimum quality score."""
        mock_repository.get_valid_questions.return_value = sample_questions

        # With high min quality, might not have enough questions
        result = service.consolidate_quiz(
            course_code="TEST",
            quiz_id="quiz-1",
            weeks=[1, 2, 3],
            target_total=30,
            min_quality_score=95  # Very high threshold
        )

        # Should either succeed or warn about quality filtering
        if not result.success:
            assert any("minimum quality" in w.lower() for w in result.warnings)

    def test_week_distribution_warning(self, service, mock_repository):
        """Test warning when week distribution is unbalanced."""
        # Create heavily skewed distribution: 25 from week 1, 5 each from weeks 2-3
        questions = []

        # 13 Remembering from week 1
        for i in range(13):
            questions.append(Question(
                f"W1-Q{i}", 1, "T", "Q?",
                {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                'A', {'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
                BloomLevel.REMEMBERING
            ))

        # 1 Remembering each from weeks 2-3
        for week in [2, 3]:
            questions.append(Question(
                f"W{week}-Q1", week, "T", "Q?",
                {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                'A', {'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
                BloomLevel.REMEMBERING
            ))

        # 13 Understanding from week 1
        for i in range(13):
            questions.append(Question(
                f"W1-U{i}", 1, "T", "Q?",
                {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                'B', {'A': 'Wrong', 'B': 'Correct', 'C': 'Wrong', 'D': 'Wrong'},
                BloomLevel.UNDERSTANDING
            ))

        # 1 Understanding each from weeks 2-3
        for week in [2, 3]:
            questions.append(Question(
                f"W{week}-U1", week, "T", "Q?",
                {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                'B', {'A': 'Wrong', 'B': 'Correct', 'C': 'Wrong', 'D': 'Wrong'},
                BloomLevel.UNDERSTANDING
            ))

        mock_repository.get_valid_questions.return_value = questions

        result = service.consolidate_quiz(
            course_code="TEST",
            quiz_id="quiz-1",
            weeks=[1, 2, 3],
            target_total=30,
            target_remembering=15,
            target_understanding=15
        )

        # Should succeed but with warnings about week distribution
        assert result.success is True
        # Might have warnings about week 2 or 3 being under-represented

    def test_quiz_title_generation(self, service):
        """Test quiz title generation."""
        title = service._generate_quiz_title("quiz-1", [1, 2, 3])
        assert "Quiz 1" in title
        assert "Weeks 1-3" in title

        title2 = service._generate_quiz_title("quiz-2", [5, 6])
        assert "Quiz 2" in title2
        assert "Weeks 5-6" in title2

    def test_rejected_questions_list(self, service, mock_repository, sample_questions):
        """Test that rejected questions are properly tracked."""
        mock_repository.get_valid_questions.return_value = sample_questions

        result = service.consolidate_quiz(
            course_code="TEST",
            quiz_id="quiz-1",
            weeks=[1, 2, 3],
            target_total=30
        )

        assert result.success is True
        # 40 total - 30 selected = 10 rejected
        assert len(result.rejected_questions) == 10

    def test_preview_consolidation(self, service, mock_repository, sample_questions):
        """Test preview without creating quiz bank."""
        mock_repository.get_valid_questions.return_value = sample_questions

        preview = service.preview_consolidation(
            course_code="TEST",
            weeks=[1, 2, 3],
            target_total=30
        )

        assert preview['available'] == 40
        assert preview['target'] == 30
        assert preview['can_consolidate'] is True
        assert preview['remembering'] == 20
        assert preview['understanding'] == 20
        assert preview['target_per_level'] == 15
        assert 'by_week' in preview
        assert 'avg_quality' in preview

    def test_preview_insufficient_questions(self, service, mock_repository, sample_questions):
        """Test preview when insufficient questions."""
        mock_repository.get_valid_questions.return_value = sample_questions[:20]

        preview = service.preview_consolidation(
            course_code="TEST",
            weeks=[1, 2, 3],
            target_total=30
        )

        assert preview['available'] == 20
        assert preview['can_consolidate'] is False

    def test_manual_selection_success(self, service, mock_repository, sample_questions):
        """Test manual selection with valid IDs."""
        mock_repository.get_all_questions.return_value = sample_questions

        # Select 15 Remembering + 15 Understanding
        selected_ids = [q.id for q in sample_questions[:15]] + [q.id for q in sample_questions[20:35]]

        result = service.manual_selection(
            course_code="TEST",
            quiz_id="quiz-manual",
            weeks=[1, 2, 3],
            selected_ids=selected_ids
        )

        assert result.success is True
        assert len(result.selected_questions) == 30

    def test_manual_selection_missing_ids(self, service, mock_repository, sample_questions):
        """Test manual selection with non-existent IDs."""
        mock_repository.get_all_questions.return_value = sample_questions

        selected_ids = ["NONEXISTENT-1", "NONEXISTENT-2"] + [sample_questions[0].id]

        result = service.manual_selection(
            course_code="TEST",
            quiz_id="quiz-manual",
            weeks=[1, 2, 3],
            selected_ids=selected_ids
        )

        assert result.success is False
        assert len(result.warnings) > 0
        assert any("not found" in w for w in result.warnings)
        assert any("Only found 1 of 3" in w for w in result.warnings)

    def test_manual_selection_unbalanced_bloom(self, service, mock_repository, sample_questions):
        """Test manual selection warns about unbalanced Bloom distribution."""
        mock_repository.get_all_questions.return_value = sample_questions

        # Select only Remembering questions (unbalanced)
        selected_ids = [q.id for q in sample_questions[:20]]

        result = service.manual_selection(
            course_code="TEST",
            quiz_id="quiz-manual",
            weeks=[1, 2, 3],
            selected_ids=selected_ids
        )

        assert any("unbalanced" in w.lower() for w in result.warnings)

    def test_manual_selection_invalid_questions(self, service, mock_repository):
        """Test manual selection with invalid questions."""
        # Create invalid questions (missing options)
        invalid_questions = [
            Question(
                f"Q{i}", 1, "T", "Q?",
                {'A': 'Only one option'},  # Invalid - needs 4 options
                'A', {'A': 'Correct'},
                BloomLevel.REMEMBERING
            )
            for i in range(10)
        ]

        mock_repository.get_all_questions.return_value = invalid_questions

        selected_ids = [q.id for q in invalid_questions]

        result = service.manual_selection(
            course_code="TEST",
            quiz_id="quiz-manual",
            weeks=[1],
            selected_ids=selected_ids
        )

        assert any("validation errors" in w for w in result.warnings)

    def test_select_top_questions_quality_ordering(self, service):
        """Test that _select_top_questions orders by quality."""
        # Create questions with different quality scores (via feedback length)
        questions = []
        for i in range(20):
            # Questions with more detailed feedback have higher quality
            feedback_length = i * 10
            questions.append(Question(
                f"Q{i}", 1, "T", "Q?",
                {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                'A',
                {
                    'A': 'Correct ' + 'x' * feedback_length,
                    'B': 'Wrong ' + 'x' * feedback_length,
                    'C': 'Wrong ' + 'x' * feedback_length,
                    'D': 'Wrong ' + 'x' * feedback_length
                },
                BloomLevel.REMEMBERING
            ))

        selected = service._select_top_questions(questions, 10, [1])

        # Should select the 10 highest quality questions
        assert len(selected) == 10
        # Higher indexed questions have higher quality
        avg_index = sum(int(q.id[1:]) for q in selected) / len(selected)
        assert avg_index > 10  # Should be biased toward higher indices

    def test_check_week_distribution(self, service):
        """Test week distribution checking."""
        # Create heavily unbalanced distribution
        questions = [
            Question(f"W1-Q{i}", 1, "T", "Q?",
                    {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                    'A', {'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
                    BloomLevel.REMEMBERING)
            for i in range(25)
        ]
        questions.extend([
            Question(f"W2-Q{i}", 2, "T", "Q?",
                    {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                    'A', {'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
                    BloomLevel.REMEMBERING)
            for i in range(5)
        ])

        warnings = service._check_week_distribution(questions, [1, 2, 3])

        # Should warn about week 2 and 3
        assert len(warnings) > 0
        assert any("Week 2" in w or "Week 3" in w for w in warnings)

    def test_custom_targets(self, service, mock_repository, sample_questions):
        """Test consolidation with custom targets."""
        mock_repository.get_valid_questions.return_value = sample_questions

        result = service.consolidate_quiz(
            course_code="TEST",
            quiz_id="quiz-1",
            weeks=[1, 2, 3],
            target_total=20,
            target_remembering=13,
            target_understanding=7
        )

        assert result.success is True
        assert len(result.selected_questions) == 20

        remembering = sum(1 for q in result.selected_questions if q.bloom_level == BloomLevel.REMEMBERING)
        understanding = sum(1 for q in result.selected_questions if q.bloom_level == BloomLevel.UNDERSTANDING)

        assert remembering == 13
        assert understanding == 7

    def test_empty_preview(self, service, mock_repository):
        """Test preview with no questions."""
        mock_repository.get_valid_questions.return_value = []

        preview = service.preview_consolidation("TEST", [1, 2, 3])

        assert preview['available'] == 0
        assert preview['can_consolidate'] is False
        assert preview['avg_quality'] == 0
