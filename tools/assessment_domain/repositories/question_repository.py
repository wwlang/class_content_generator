"""
Repository for accessing quiz questions from the file system.

Handles file path abstraction, caching, and batch loading of questions.
"""

from pathlib import Path
from typing import List, Dict, Optional
from ..models import Question, BloomLevel
from ..parsers import QuizMarkdownParser


class QuestionRepository:
    """
    Repository for loading and caching quiz questions.

    Responsibilities:
    - Abstract file system paths
    - Load questions by week, course, or Bloom level
    - Cache loaded questions for performance
    - Batch load multiple weeks efficiently

    Usage:
        repo = QuestionRepository(base_path="courses")
        questions = repo.get_questions_by_week("BCI2AU", 1)
        all_q = repo.get_all_questions("BCI2AU", weeks=[1, 2, 3])
    """

    def __init__(self, base_path: str = "courses"):
        """
        Initialize repository.

        Args:
            base_path: Root directory containing course folders
        """
        self.base_path = Path(base_path)
        self.parser = QuizMarkdownParser(infer_bloom=True)
        self._cache: Dict[str, List[Question]] = {}

    def get_questions_by_week(
        self,
        course_code: str,
        week: int,
        use_cache: bool = True
    ) -> List[Question]:
        """
        Load questions for a specific week.

        Args:
            course_code: Course identifier (e.g., "BCI2AU")
            week: Week number (1-10)
            use_cache: If True, return cached questions if available

        Returns:
            List of Question objects from that week

        Raises:
            FileNotFoundError: If quiz file doesn't exist
            ValueError: If week number is invalid

        Example:
            questions = repo.get_questions_by_week("BCI2AU", 3)
            # Returns all questions from week 3
        """
        if not (1 <= week <= 10):
            raise ValueError(f"Week must be 1-10, got {week}")

        cache_key = f"{course_code}_week_{week}"

        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]

        quiz_file = self._get_quiz_file_path(course_code, week)

        if not quiz_file.exists():
            raise FileNotFoundError(
                f"Quiz questions file not found: {quiz_file}\n"
                f"Expected location: courses/{course_code}/weeks/week-{week:02d}/quiz-questions.md"
            )

        questions = self.parser.parse_file(quiz_file)

        if use_cache:
            self._cache[cache_key] = questions

        return questions

    def get_all_questions(
        self,
        course_code: str,
        weeks: Optional[List[int]] = None,
        use_cache: bool = True
    ) -> List[Question]:
        """
        Load questions from multiple weeks.

        Args:
            course_code: Course identifier
            weeks: List of week numbers to load (defaults to [1-10])
            use_cache: If True, use cached questions where available

        Returns:
            Combined list of questions from all specified weeks

        Example:
            # Get questions from weeks 1-3 for Quiz 1
            questions = repo.get_all_questions("BCI2AU", weeks=[1, 2, 3])
        """
        if weeks is None:
            weeks = list(range(1, 11))

        all_questions = []
        for week in weeks:
            try:
                questions = self.get_questions_by_week(course_code, week, use_cache)
                all_questions.extend(questions)
            except FileNotFoundError:
                # Skip weeks without quiz files (might not be created yet)
                continue

        return all_questions

    def get_questions_by_bloom(
        self,
        course_code: str,
        bloom_level: BloomLevel,
        weeks: Optional[List[int]] = None,
        use_cache: bool = True
    ) -> List[Question]:
        """
        Filter questions by Bloom's taxonomy level.

        Args:
            course_code: Course identifier
            bloom_level: BloomLevel enum value
            weeks: List of weeks to search (defaults to all)
            use_cache: If True, use cached questions

        Returns:
            Questions matching the specified Bloom level

        Example:
            # Get all Understanding questions from weeks 1-3
            understanding_q = repo.get_questions_by_bloom(
                "BCI2AU",
                BloomLevel.UNDERSTANDING,
                weeks=[1, 2, 3]
            )
        """
        all_questions = self.get_all_questions(course_code, weeks, use_cache)
        return [q for q in all_questions if q.bloom_level == bloom_level]

    def get_questions_by_topic(
        self,
        course_code: str,
        topic_keyword: str,
        weeks: Optional[List[int]] = None,
        use_cache: bool = True
    ) -> List[Question]:
        """
        Search questions by topic keyword.

        Args:
            course_code: Course identifier
            topic_keyword: Keyword to search in question topics (case-insensitive)
            weeks: List of weeks to search
            use_cache: If True, use cached questions

        Returns:
            Questions with matching topic

        Example:
            # Find all questions about "communication models"
            model_questions = repo.get_questions_by_topic(
                "BCI2AU",
                "model"
            )
        """
        all_questions = self.get_all_questions(course_code, weeks, use_cache)
        keyword_lower = topic_keyword.lower()
        return [
            q for q in all_questions
            if keyword_lower in q.topic.lower()
        ]

    def get_valid_questions(
        self,
        course_code: str,
        weeks: Optional[List[int]] = None,
        use_cache: bool = True
    ) -> List[Question]:
        """
        Get only questions that pass validation.

        Args:
            course_code: Course identifier
            weeks: List of weeks to search
            use_cache: If True, use cached questions

        Returns:
            Questions with no validation errors

        Example:
            # Get all valid questions for consolidation
            valid_q = repo.get_valid_questions("BCI2AU", weeks=[1, 2, 3])
        """
        all_questions = self.get_all_questions(course_code, weeks, use_cache)
        return [q for q in all_questions if q.is_valid()]

    def clear_cache(self, course_code: Optional[str] = None):
        """
        Clear cached questions.

        Args:
            course_code: If provided, clear only this course's cache.
                        If None, clear entire cache.

        Example:
            # Clear cache after updating quiz files
            repo.clear_cache("BCI2AU")
        """
        if course_code:
            keys_to_remove = [k for k in self._cache.keys() if k.startswith(course_code)]
            for key in keys_to_remove:
                del self._cache[key]
        else:
            self._cache.clear()

    def _get_quiz_file_path(self, course_code: str, week: int) -> Path:
        """
        Get path to quiz-questions.md file.

        Args:
            course_code: Course identifier
            week: Week number

        Returns:
            Path to quiz file
        """
        return (
            self.base_path /
            f"{course_code}-business-communication" /
            "weeks" /
            f"week-{week:02d}" /
            "quiz-questions.md"
        )

    def get_statistics(
        self,
        course_code: str,
        weeks: Optional[List[int]] = None
    ) -> Dict[str, any]:
        """
        Get statistics about questions in the repository.

        Args:
            course_code: Course identifier
            weeks: List of weeks to analyze

        Returns:
            Dictionary with statistics:
            - total: Total question count
            - by_week: Count per week
            - by_bloom: Count per Bloom level
            - valid: Count of valid questions
            - avg_quality: Average quality score

        Example:
            stats = repo.get_statistics("BCI2AU", weeks=[1, 2, 3])
            print(f"Total questions: {stats['total']}")
            print(f"Remembering: {stats['by_bloom']['remembering']}")
        """
        all_questions = self.get_all_questions(course_code, weeks, use_cache=True)

        by_week: Dict[int, int] = {}
        by_bloom: Dict[str, int] = {'remembering': 0, 'understanding': 0}
        valid_count = 0
        total_quality = 0

        for q in all_questions:
            by_week[q.week] = by_week.get(q.week, 0) + 1
            by_bloom[q.bloom_level.value] += 1
            if q.is_valid():
                valid_count += 1
            total_quality += q.get_quality_score()

        return {
            'total': len(all_questions),
            'by_week': by_week,
            'by_bloom': by_bloom,
            'valid': valid_count,
            'avg_quality': total_quality / len(all_questions) if all_questions else 0,
            'scenario_based': sum(1 for q in all_questions if q.is_scenario_based()),
        }
