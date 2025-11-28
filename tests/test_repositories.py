"""
Unit tests for QuestionRepository and AssessmentRepository.

Tests repository caching, filtering, and statistics.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from tools.assessment_domain.repositories import QuestionRepository, AssessmentRepository
from tools.assessment_domain.models import Question, Assessment, BloomLevel, AssessmentType


class TestQuestionRepository:
    """Tests for QuestionRepository."""

    @pytest.fixture
    def mock_parser(self):
        """Create mock parser."""
        parser = Mock()
        # Create sample questions
        questions = [
            Question(
                f"W1-Q{i}", 1, f"Topic{i}", "Question?",
                {'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D'},
                'A', {'A': 'Correct', 'B': 'Wrong', 'C': 'Wrong', 'D': 'Wrong'},
                BloomLevel.REMEMBERING if i < 5 else BloomLevel.UNDERSTANDING
            )
            for i in range(10)
        ]
        parser.parse_file.return_value = questions
        return parser

    @pytest.fixture
    def repository(self, mock_parser):
        """Create repository with mocked parser."""
        repo = QuestionRepository(base_path="test_courses")
        repo.parser = mock_parser
        return repo

    def test_get_questions_by_week(self, repository, tmp_path):
        """Test loading questions by week."""
        # Create mock file
        with patch.object(Path, 'exists', return_value=True):
            questions = repository.get_questions_by_week("TEST", 1, use_cache=False)

        assert len(questions) == 10
        assert all(q.week == 1 for q in questions)

    def test_get_questions_by_week_caching(self, repository):
        """Test that caching works."""
        with patch.object(Path, 'exists', return_value=True):
            # First call
            questions1 = repository.get_questions_by_week("TEST", 1, use_cache=True)
            # Second call should use cache
            questions2 = repository.get_questions_by_week("TEST", 1, use_cache=True)

        assert questions1 is questions2  # Same object from cache
        assert repository.parser.parse_file.call_count == 1  # Only called once

    def test_get_questions_by_week_file_not_found(self, repository):
        """Test error when quiz file doesn't exist."""
        with pytest.raises(FileNotFoundError, match="Quiz questions file not found"):
            repository.get_questions_by_week("NOEXIST", 1, use_cache=False)

    def test_get_questions_by_week_invalid_week(self, repository):
        """Test error with invalid week number."""
        with pytest.raises(ValueError, match="Week must be 1-10"):
            repository.get_questions_by_week("TEST", 15)

    def test_get_all_questions(self, repository):
        """Test loading questions from multiple weeks."""
        with patch.object(Path, 'exists', return_value=True):
            questions = repository.get_all_questions("TEST", weeks=[1, 2, 3], use_cache=False)

        # Should have questions from 3 weeks
        assert len(questions) == 30  # 10 per week

    def test_get_questions_by_bloom(self, repository):
        """Test filtering by Bloom level."""
        with patch.object(Path, 'exists', return_value=True):
            remembering = repository.get_questions_by_bloom(
                "TEST", BloomLevel.REMEMBERING, weeks=[1], use_cache=False
            )
            understanding = repository.get_questions_by_bloom(
                "TEST", BloomLevel.UNDERSTANDING, weeks=[1], use_cache=False
            )

        assert len(remembering) == 5
        assert len(understanding) == 5

    def test_get_questions_by_topic(self, repository):
        """Test searching by topic keyword."""
        with patch.object(Path, 'exists', return_value=True):
            topic_questions = repository.get_questions_by_topic(
                "TEST", "Topic1", weeks=[1], use_cache=False
            )

        # Should find Topic1 (case-insensitive)
        assert len(topic_questions) >= 1

    def test_get_valid_questions(self, repository, mock_parser):
        """Test filtering for valid questions only."""
        # Make some questions invalid
        questions = mock_parser.parse_file.return_value
        questions[0].options = {'A': 'Only one'}  # Invalid - not 4 options

        with patch.object(Path, 'exists', return_value=True):
            valid = repository.get_valid_questions("TEST", weeks=[1], use_cache=False)

        assert len(valid) == 9  # One invalid

    def test_clear_cache(self, repository):
        """Test clearing cache."""
        with patch.object(Path, 'exists', return_value=True):
            repository.get_questions_by_week("TEST", 1, use_cache=True)
            assert len(repository._cache) > 0

            repository.clear_cache("TEST")
            assert len(repository._cache) == 0

    def test_get_statistics(self, repository):
        """Test statistics generation."""
        with patch.object(Path, 'exists', return_value=True):
            stats = repository.get_statistics("TEST", weeks=[1])

        assert stats['total'] == 10
        assert stats['by_bloom']['remembering'] == 5
        assert stats['by_bloom']['understanding'] == 5
        assert stats['valid'] == 10
        assert stats['by_week'][1] == 10


class TestAssessmentRepository:
    """Tests for AssessmentRepository."""

    @pytest.fixture
    def mock_parser(self):
        """Create mock parser."""
        parser = Mock()
        assessments = {
            'email-memo': Assessment(
                'email-memo', 'Email + Memo', AssessmentType.PORTFOLIO,
                0.10, 3, "Description", []
            ),
            'presentation': Assessment(
                'presentation', 'Presentation', AssessmentType.PRESENTATION,
                0.20, 5, "Description", []
            )
        }
        parser.parse_file.return_value = assessments
        return parser

    @pytest.fixture
    def repository(self, mock_parser):
        """Create repository with mocked parser."""
        repo = AssessmentRepository(base_path="test_courses")
        repo.parser = mock_parser
        return repo

    def test_get_assessment(self, repository):
        """Test loading specific assessment."""
        with patch.object(Path, 'exists', return_value=True):
            assessment = repository.get_assessment("TEST", "email-memo", use_cache=False)

        assert assessment is not None
        assert assessment.id == "email-memo"
        assert assessment.name == "Email + Memo"

    def test_get_assessment_not_found(self, repository):
        """Test getting non-existent assessment."""
        with patch.object(Path, 'exists', return_value=True):
            assessment = repository.get_assessment("TEST", "nonexistent", use_cache=False)

        assert assessment is None

    def test_get_all_assessments(self, repository):
        """Test loading all assessments."""
        with patch.object(Path, 'exists', return_value=True):
            assessments = repository.get_all_assessments("TEST", use_cache=False)

        assert len(assessments) == 2
        assert "email-memo" in assessments
        assert "presentation" in assessments

    def test_get_all_assessments_file_not_found(self, repository):
        """Test error when handbook doesn't exist."""
        with pytest.raises(FileNotFoundError, match="Assessment handbook not found"):
            repository.get_all_assessments("NOEXIST", use_cache=False)

    def test_get_assessments_by_type(self, repository):
        """Test filtering by assessment type."""
        with patch.object(Path, 'exists', return_value=True):
            portfolios = repository.get_assessments_by_type(
                "TEST", AssessmentType.PORTFOLIO, use_cache=False
            )
            presentations = repository.get_assessments_by_type(
                "TEST", AssessmentType.PRESENTATION, use_cache=False
            )

        assert len(portfolios) == 1
        assert len(presentations) == 1

    def test_get_assessments_by_week(self, repository):
        """Test filtering by due week."""
        with patch.object(Path, 'exists', return_value=True):
            week3 = repository.get_assessments_by_week("TEST", 3, use_cache=False)
            week5 = repository.get_assessments_by_week("TEST", 5, use_cache=False)

        assert len(week3) == 1
        assert len(week5) == 1

    def test_caching(self, repository):
        """Test assessment caching."""
        with patch.object(Path, 'exists', return_value=True):
            assessments1 = repository.get_all_assessments("TEST", use_cache=True)
            assessments2 = repository.get_all_assessments("TEST", use_cache=True)

        assert assessments1 is assessments2
        assert repository.parser.parse_file.call_count == 1

    def test_clear_cache(self, repository):
        """Test clearing cache."""
        with patch.object(Path, 'exists', return_value=True):
            repository.get_all_assessments("TEST", use_cache=True)
            assert len(repository._cache) > 0

            repository.clear_cache("TEST")
            assert len(repository._cache) == 0

    def test_get_statistics(self, repository):
        """Test statistics generation."""
        with patch.object(Path, 'exists', return_value=True):
            stats = repository.get_statistics("TEST")

        assert stats['total'] == 2
        assert stats['by_type']['portfolio'] == 1
        assert stats['by_type']['presentation'] == 1
        assert stats['total_weight'] == 0.30  # 10% + 20%
