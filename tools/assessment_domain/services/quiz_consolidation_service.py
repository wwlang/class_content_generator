"""
Service for consolidating quiz questions into balanced quiz banks.

Implements the core business logic for selecting questions based on
quality scores while maintaining Bloom's taxonomy distribution.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from ..models import Question, QuizBank, BloomLevel
from ..repositories import QuestionRepository


@dataclass
class ConsolidationResult:
    """Result of consolidation operation."""
    quiz_bank: QuizBank
    selected_questions: List[Question]
    rejected_questions: List[Question]
    warnings: List[str]
    success: bool

    def get_bloom_distribution(self) -> Dict[str, int]:
        """Get Bloom level counts in selected questions."""
        dist = {'remembering': 0, 'understanding': 0}
        for q in self.selected_questions:
            dist[q.bloom_level.value] += 1
        return dist


class QuizConsolidationService:
    """
    Service for consolidating quiz questions into quiz banks.

    Responsibilities:
    - Select best questions based on quality scores
    - Maintain 50/50 Bloom's taxonomy distribution
    - Ensure even week representation
    - Provide manual review capabilities
    - Generate warnings for edge cases

    Strategy:
    1. Filter to valid questions only
    2. Sort by quality score
    3. Select top questions while balancing Bloom levels
    4. Verify distribution meets targets
    5. Generate warnings for any issues

    Usage:
        service = QuizConsolidationService(repository)
        result = service.consolidate_quiz(
            course_code="BCI2AU",
            quiz_id="quiz-1",
            weeks=[1, 2, 3]
        )
        if result.success:
            print(f"Selected {len(result.selected_questions)} questions")
    """

    def __init__(self, repository: QuestionRepository):
        """
        Initialize service.

        Args:
            repository: QuestionRepository for loading questions
        """
        self.repository = repository

    def consolidate_quiz(
        self,
        course_code: str,
        quiz_id: str,
        weeks: List[int],
        target_total: int = 30,
        target_remembering: int = 15,
        target_understanding: int = 15,
        min_quality_score: Optional[int] = None
    ) -> ConsolidationResult:
        """
        Consolidate questions from multiple weeks into a quiz bank.

        Args:
            course_code: Course identifier
            quiz_id: Quiz identifier (e.g., "quiz-1")
            weeks: List of week numbers to consolidate
            target_total: Target total questions (default 30)
            target_remembering: Target Remembering questions (default 15)
            target_understanding: Target Understanding questions (default 15)
            min_quality_score: Optional minimum quality score filter

        Returns:
            ConsolidationResult with selected questions and status

        Example:
            result = service.consolidate_quiz(
                "BCI2AU",
                "quiz-1",
                weeks=[1, 2, 3],
                target_total=30
            )
        """
        warnings = []

        # Step 1: Load all valid questions
        all_questions = self.repository.get_valid_questions(
            course_code,
            weeks=weeks,
            use_cache=True
        )

        if len(all_questions) == 0:
            return ConsolidationResult(
                quiz_bank=None,
                selected_questions=[],
                rejected_questions=[],
                warnings=["No valid questions found in specified weeks"],
                success=False
            )

        # Step 2: Filter by minimum quality if specified
        if min_quality_score:
            all_questions = [
                q for q in all_questions
                if q.get_quality_score() >= min_quality_score
            ]
            if len(all_questions) < target_total:
                warnings.append(
                    f"Only {len(all_questions)} questions meet minimum quality "
                    f"score of {min_quality_score}"
                )

        # Step 3: Check if we have enough questions
        if len(all_questions) < target_total:
            warnings.append(
                f"Only {len(all_questions)} questions available, "
                f"need {target_total}"
            )
            return ConsolidationResult(
                quiz_bank=None,
                selected_questions=[],
                rejected_questions=all_questions,
                warnings=warnings,
                success=False
            )

        # Step 4: Separate by Bloom level
        remembering_pool = [
            q for q in all_questions
            if q.bloom_level == BloomLevel.REMEMBERING
        ]
        understanding_pool = [
            q for q in all_questions
            if q.bloom_level == BloomLevel.UNDERSTANDING
        ]

        # Check Bloom distribution availability
        if len(remembering_pool) < target_remembering:
            warnings.append(
                f"Only {len(remembering_pool)} Remembering questions available, "
                f"need {target_remembering}"
            )
        if len(understanding_pool) < target_understanding:
            warnings.append(
                f"Only {len(understanding_pool)} Understanding questions available, "
                f"need {target_understanding}"
            )

        if warnings:
            return ConsolidationResult(
                quiz_bank=None,
                selected_questions=[],
                rejected_questions=all_questions,
                warnings=warnings,
                success=False
            )

        # Step 5: Select best questions from each pool
        selected_remembering = self._select_top_questions(
            remembering_pool,
            target_remembering,
            weeks
        )
        selected_understanding = self._select_top_questions(
            understanding_pool,
            target_understanding,
            weeks
        )

        selected_questions = selected_remembering + selected_understanding

        # Step 6: Check week distribution
        week_warnings = self._check_week_distribution(selected_questions, weeks)
        warnings.extend(week_warnings)

        # Step 7: Create quiz bank
        quiz_title = self._generate_quiz_title(quiz_id, weeks)
        quiz_bank = QuizBank(
            quiz_id=quiz_id,
            title=quiz_title,
            weeks_covered=weeks,
            questions=selected_questions,
            target_total=target_total,
            target_remembering=target_remembering,
            target_understanding=target_understanding
        )

        # Step 8: Determine rejected questions
        rejected_questions = [
            q for q in all_questions
            if q not in selected_questions
        ]

        return ConsolidationResult(
            quiz_bank=quiz_bank,
            selected_questions=selected_questions,
            rejected_questions=rejected_questions,
            warnings=warnings,
            success=True
        )

    def _select_top_questions(
        self,
        pool: List[Question],
        target: int,
        weeks: List[int]
    ) -> List[Question]:
        """
        Select top questions from pool, trying to balance across weeks.

        Strategy:
        1. Sort by quality score (descending)
        2. Select questions trying to maintain even week distribution
        3. If even distribution not possible, prioritize quality

        Args:
            pool: List of questions to select from
            target: Number of questions to select
            weeks: Weeks to consider for distribution

        Returns:
            Selected questions
        """
        # Sort by quality score (highest first)
        sorted_pool = sorted(
            pool,
            key=lambda q: q.get_quality_score(),
            reverse=True
        )

        # Try to balance across weeks
        questions_per_week = target // len(weeks)
        remainder = target % len(weeks)

        selected = []
        week_counts = {week: 0 for week in weeks}

        # First pass: Try to get even distribution
        for question in sorted_pool:
            if len(selected) >= target:
                break

            current_week_count = week_counts[question.week]
            target_for_week = questions_per_week + (1 if week_counts[question.week] < remainder else 0)

            # Take question if week needs more or if we're running out of options
            if current_week_count < target_for_week or len(selected) + (target - len(selected)) <= len(sorted_pool) - sorted_pool.index(question):
                selected.append(question)
                week_counts[question.week] += 1

        # Second pass: Fill remaining slots with best available
        if len(selected) < target:
            for question in sorted_pool:
                if question not in selected:
                    selected.append(question)
                    if len(selected) >= target:
                        break

        return selected

    def _check_week_distribution(
        self,
        questions: List[Question],
        weeks: List[int]
    ) -> List[str]:
        """
        Check if questions are reasonably distributed across weeks.

        Warns if any week is severely under-represented.

        Args:
            questions: Selected questions
            weeks: Weeks that should be represented

        Returns:
            List of warning messages
        """
        warnings = []
        week_counts = {}

        for q in questions:
            week_counts[q.week] = week_counts.get(q.week, 0) + 1

        expected_per_week = len(questions) / len(weeks)
        min_acceptable = expected_per_week * 0.5  # 50% of expected

        for week in weeks:
            count = week_counts.get(week, 0)
            if count < min_acceptable:
                warnings.append(
                    f"Week {week} only has {count} questions "
                    f"(expected ~{expected_per_week:.1f})"
                )

        return warnings

    def _generate_quiz_title(self, quiz_id: str, weeks: List[int]) -> str:
        """
        Generate human-readable quiz title.

        Args:
            quiz_id: Quiz identifier
            weeks: Covered weeks

        Returns:
            Title like "Quiz 1 - Weeks 1-3"
        """
        quiz_number = quiz_id.split('-')[-1] if '-' in quiz_id else quiz_id
        week_range = f"{min(weeks)}-{max(weeks)}"
        return f"Quiz {quiz_number} - Weeks {week_range}"

    def preview_consolidation(
        self,
        course_code: str,
        weeks: List[int],
        target_total: int = 30
    ) -> Dict[str, any]:
        """
        Preview consolidation without actually creating quiz bank.

        Useful for analyzing available questions before consolidation.

        Args:
            course_code: Course identifier
            weeks: Weeks to consolidate
            target_total: Target question count

        Returns:
            Dictionary with preview statistics

        Example:
            preview = service.preview_consolidation("BCI2AU", [1, 2, 3])
            print(f"Available: {preview['available']}")
            print(f"Can consolidate: {preview['can_consolidate']}")
        """
        all_questions = self.repository.get_valid_questions(
            course_code,
            weeks=weeks
        )

        remembering = [q for q in all_questions if q.bloom_level == BloomLevel.REMEMBERING]
        understanding = [q for q in all_questions if q.bloom_level == BloomLevel.UNDERSTANDING]

        week_counts = {}
        for q in all_questions:
            week_counts[q.week] = week_counts.get(q.week, 0) + 1

        target_per_level = target_total // 2

        can_consolidate = (
            len(all_questions) >= target_total and
            len(remembering) >= target_per_level and
            len(understanding) >= target_per_level
        )

        return {
            'available': len(all_questions),
            'target': target_total,
            'can_consolidate': can_consolidate,
            'remembering': len(remembering),
            'understanding': len(understanding),
            'target_per_level': target_per_level,
            'by_week': week_counts,
            'avg_quality': sum(q.get_quality_score() for q in all_questions) / len(all_questions) if all_questions else 0,
        }

    def manual_selection(
        self,
        course_code: str,
        quiz_id: str,
        weeks: List[int],
        selected_ids: List[str]
    ) -> ConsolidationResult:
        """
        Create quiz bank from manually selected question IDs.

        Allows manual override of automatic selection.

        Args:
            course_code: Course identifier
            quiz_id: Quiz identifier
            weeks: Weeks covered
            selected_ids: List of question IDs to include

        Returns:
            ConsolidationResult with validation

        Example:
            result = service.manual_selection(
                "BCI2AU",
                "quiz-1",
                [1, 2, 3],
                ["W1-Q1-topic", "W2-Q3-topic", ...]
            )
        """
        warnings = []

        # Load all questions
        all_questions = self.repository.get_all_questions(course_code, weeks)

        # Find selected questions
        id_to_question = {q.id: q for q in all_questions}
        selected_questions = []

        for qid in selected_ids:
            if qid in id_to_question:
                selected_questions.append(id_to_question[qid])
            else:
                warnings.append(f"Question ID not found: {qid}")

        if len(selected_questions) != len(selected_ids):
            warnings.append(
                f"Only found {len(selected_questions)} of {len(selected_ids)} "
                "requested questions"
            )

        # Validate selection
        invalid_questions = [q for q in selected_questions if not q.is_valid()]
        if invalid_questions:
            warnings.append(
                f"{len(invalid_questions)} selected questions have validation errors"
            )

        # Check Bloom distribution
        remembering = sum(1 for q in selected_questions if q.bloom_level == BloomLevel.REMEMBERING)
        understanding = len(selected_questions) - remembering

        if abs(remembering - understanding) > 2:
            warnings.append(
                f"Bloom distribution unbalanced: {remembering} Remembering, "
                f"{understanding} Understanding"
            )

        # Create quiz bank
        quiz_title = self._generate_quiz_title(quiz_id, weeks)
        quiz_bank = QuizBank(
            quiz_id=quiz_id,
            title=quiz_title,
            weeks_covered=weeks,
            questions=selected_questions
        )

        rejected_questions = [
            q for q in all_questions
            if q not in selected_questions
        ]

        return ConsolidationResult(
            quiz_bank=quiz_bank,
            selected_questions=selected_questions,
            rejected_questions=rejected_questions,
            warnings=warnings,
            success=len(warnings) == 0
        )
