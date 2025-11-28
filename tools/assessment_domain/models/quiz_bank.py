"""
Domain model for consolidated quiz banks.

A quiz bank consolidates questions from multiple weeks into a single
graded assessment with balanced Bloom's taxonomy distribution.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from collections import Counter

from .question import Question, BloomLevel


@dataclass
class QuizBank:
    """
    A consolidated quiz bank for graded assessment.

    Quiz banks combine questions from multiple weeks (typically 3 weeks)
    into a single assessment with:
    - 30 total questions
    - 15 Remembering level (50%)
    - 15 Understanding level (50%)
    - Even distribution across source weeks

    Attributes:
        quiz_id: Identifier (e.g., "quiz-1", "quiz-2", "quiz-3")
        title: Display title (e.g., "Quiz 1 - Weeks 1-3")
        weeks_covered: List of source week numbers
        questions: Selected questions for this quiz bank
        target_total: Target number of questions (default: 30)
        target_remembering: Target Remembering questions (default: 15)
        target_understanding: Target Understanding questions (default: 15)
        course_code: Course identifier (e.g., "BCI2AU")
    """
    quiz_id: str
    title: str
    weeks_covered: List[int]
    questions: List[Question] = field(default_factory=list)
    target_total: int = 30
    target_remembering: int = 15
    target_understanding: int = 15
    course_code: Optional[str] = None

    def validate_distribution(self) -> Dict[str, any]:
        """
        Validate Bloom's taxonomy distribution.

        Returns:
            Dictionary with distribution metrics and validation status:
            - total: Actual total question count
            - target_total: Target total
            - remembering_count: Actual Remembering questions
            - target_remembering: Target Remembering questions
            - understanding_count: Actual Understanding questions
            - target_understanding: Target Understanding questions
            - balanced: Boolean indicating if targets are met
            - errors: List of validation error messages
        """
        remembering = [q for q in self.questions if q.bloom_level == BloomLevel.REMEMBERING]
        understanding = [q for q in self.questions if q.bloom_level == BloomLevel.UNDERSTANDING]

        errors = []

        # Check total count
        if len(self.questions) != self.target_total:
            errors.append(
                f"Total questions ({len(self.questions)}) "
                f"doesn't match target ({self.target_total})"
            )

        # Check Remembering count
        if len(remembering) != self.target_remembering:
            errors.append(
                f"Remembering questions ({len(remembering)}) "
                f"doesn't match target ({self.target_remembering})"
            )

        # Check Understanding count
        if len(understanding) != self.target_understanding:
            errors.append(
                f"Understanding questions ({len(understanding)}) "
                f"doesn't match target ({self.target_understanding})"
            )

        # Check for duplicate question IDs
        question_ids = [q.id for q in self.questions]
        duplicates = [qid for qid, count in Counter(question_ids).items() if count > 1]
        if duplicates:
            errors.append(f"Duplicate question IDs found: {', '.join(duplicates)}")

        # Check all questions are from covered weeks
        invalid_weeks = [
            q.id for q in self.questions
            if q.week not in self.weeks_covered
        ]
        if invalid_weeks:
            errors.append(
                f"Questions from wrong weeks: {', '.join(invalid_weeks)} "
                f"(expected weeks {self.weeks_covered})"
            )

        return {
            'total': len(self.questions),
            'target_total': self.target_total,
            'remembering_count': len(remembering),
            'target_remembering': self.target_remembering,
            'understanding_count': len(understanding),
            'target_understanding': self.target_understanding,
            'balanced': len(errors) == 0,
            'errors': errors
        }

    def get_questions_by_week(self) -> Dict[int, List[Question]]:
        """
        Group questions by source week.

        Returns:
            Dictionary mapping week numbers to questions from that week
        """
        by_week = {}
        for q in self.questions:
            by_week.setdefault(q.week, []).append(q)
        return by_week

    def get_questions_by_bloom(self) -> Dict[BloomLevel, List[Question]]:
        """
        Group questions by Bloom's taxonomy level.

        Returns:
            Dictionary mapping BloomLevel to questions at that level
        """
        by_bloom = {
            BloomLevel.REMEMBERING: [],
            BloomLevel.UNDERSTANDING: []
        }
        for q in self.questions:
            by_bloom[q.bloom_level].append(q)
        return by_bloom

    def get_week_distribution(self) -> Dict[int, Dict[str, int]]:
        """
        Analyze question distribution across weeks.

        Returns:
            Dictionary mapping week number to:
            - total: Total questions from that week
            - remembering: Remembering questions from that week
            - understanding: Understanding questions from that week
        """
        distribution = {}
        by_week = self.get_questions_by_week()

        for week in self.weeks_covered:
            week_questions = by_week.get(week, [])
            distribution[week] = {
                'total': len(week_questions),
                'remembering': len([q for q in week_questions if q.bloom_level == BloomLevel.REMEMBERING]),
                'understanding': len([q for q in week_questions if q.bloom_level == BloomLevel.UNDERSTANDING])
            }

        return distribution

    def is_balanced(self) -> bool:
        """
        Quick check if quiz bank meets all distribution targets.

        Returns:
            True if quiz bank is perfectly balanced
        """
        validation = self.validate_distribution()
        return validation['balanced']

    def get_average_quality_score(self) -> float:
        """
        Calculate average quality score across all questions.

        Returns:
            Average quality score (0 if no questions)
        """
        if not self.questions:
            return 0.0

        total_score = sum(q.get_quality_score() for q in self.questions)
        return total_score / len(self.questions)

    def get_validation_report(self) -> str:
        """
        Generate human-readable validation report.

        Returns:
            Multi-line string report with distribution analysis
        """
        validation = self.validate_distribution()
        week_dist = self.get_week_distribution()

        lines = [
            f"Quiz Bank: {self.title}",
            f"Quiz ID: {self.quiz_id}",
            f"",
            f"=== Overall Distribution ===",
            f"Total Questions: {validation['total']} / {validation['target_total']}",
            f"Remembering: {validation['remembering_count']} / {validation['target_remembering']}",
            f"Understanding: {validation['understanding_count']} / {validation['target_understanding']}",
            f"Balanced: {'✓ Yes' if validation['balanced'] else '✗ No'}",
            f"",
            f"=== Week Distribution ===",
        ]

        for week in sorted(self.weeks_covered):
            dist = week_dist.get(week, {'total': 0, 'remembering': 0, 'understanding': 0})
            lines.append(
                f"Week {week}: {dist['total']} total "
                f"({dist['remembering']} R, {dist['understanding']} U)"
            )

        lines.append("")
        lines.append(f"=== Quality Metrics ===")
        lines.append(f"Average Quality Score: {self.get_average_quality_score():.1f}")

        scenario_count = len([q for q in self.questions if q.is_scenario_based()])
        lines.append(f"Scenario-Based Questions: {scenario_count} / {len(self.questions)}")

        valid_count = len([q for q in self.questions if q.is_valid()])
        lines.append(f"Valid Questions: {valid_count} / {len(self.questions)}")

        if validation['errors']:
            lines.append("")
            lines.append("=== Validation Errors ===")
            for error in validation['errors']:
                lines.append(f"  • {error}")

        return "\n".join(lines)

    def add_question(self, question: Question) -> None:
        """
        Add a question to the quiz bank.

        Args:
            question: Question to add

        Raises:
            ValueError: If question is from wrong week or is duplicate
        """
        # Check week is valid
        if question.week not in self.weeks_covered:
            raise ValueError(
                f"Question {question.id} is from week {question.week}, "
                f"but this quiz bank covers weeks {self.weeks_covered}"
            )

        # Check for duplicate ID
        existing_ids = [q.id for q in self.questions]
        if question.id in existing_ids:
            raise ValueError(f"Question {question.id} already exists in quiz bank")

        self.questions.append(question)

    def remove_question(self, question_id: str) -> Question:
        """
        Remove a question from the quiz bank.

        Args:
            question_id: ID of question to remove

        Returns:
            Removed question

        Raises:
            ValueError: If question ID not found
        """
        for i, q in enumerate(self.questions):
            if q.id == question_id:
                return self.questions.pop(i)

        raise ValueError(f"Question {question_id} not found in quiz bank")

    def replace_question(self, old_id: str, new_question: Question) -> None:
        """
        Replace one question with another.

        Useful for manual review workflow where instructor swaps questions.

        Args:
            old_id: ID of question to replace
            new_question: Replacement question

        Raises:
            ValueError: If old question not found or new question invalid
        """
        # Find and remove old question
        old_question = self.remove_question(old_id)

        # Validate new question is appropriate replacement
        if new_question.bloom_level != old_question.bloom_level:
            # Put old question back and raise error
            self.questions.append(old_question)
            raise ValueError(
                f"Replacement question must be same Bloom level "
                f"(old: {old_question.bloom_level.value}, new: {new_question.bloom_level.value})"
            )

        # Add new question
        self.add_question(new_question)

    def to_dict(self) -> Dict:
        """Convert quiz bank to dictionary representation."""
        return {
            'quiz_id': self.quiz_id,
            'title': self.title,
            'course_code': self.course_code,
            'weeks_covered': self.weeks_covered,
            'target_total': self.target_total,
            'target_remembering': self.target_remembering,
            'target_understanding': self.target_understanding,
            'questions': [q.to_dict() for q in self.questions],
            'distribution': self.validate_distribution(),
            'week_distribution': self.get_week_distribution(),
            'average_quality_score': self.get_average_quality_score()
        }

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"QuizBank({self.quiz_id}: {len(self.questions)}/{self.target_total} questions)"

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"QuizBank(quiz_id='{self.quiz_id}', weeks={self.weeks_covered}, "
            f"questions={len(self.questions)})"
        )
