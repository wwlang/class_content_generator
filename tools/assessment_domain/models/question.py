"""
Domain model for quiz questions.

This module defines the Question model with comprehensive validation
rules based on the quality guidelines from assessment-design skills.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
import re


class BloomLevel(Enum):
    """Bloom's taxonomy cognitive levels (restricted to lower two levels)."""
    REMEMBERING = "remembering"
    UNDERSTANDING = "understanding"

    @classmethod
    def from_string(cls, value: str) -> 'BloomLevel':
        """Parse Bloom level from string (case-insensitive)."""
        value_lower = value.lower().strip()
        for level in cls:
            if level.value == value_lower:
                return level
        raise ValueError(f"Invalid Bloom level: {value}. Must be 'remembering' or 'understanding'")


class QuestionType(Enum):
    """Question format types."""
    MULTIPLE_CHOICE = "multiple_choice"


@dataclass
class Question:
    """
    A quiz question with answer options and feedback.

    Attributes:
        id: Unique identifier (format: W1-Q1-ComponentName)
        week: Source week number (1-10)
        topic: Brief topic description
        question_text: The actual question text
        options: Dictionary mapping option letters (A-D) to option text
        correct_answer: Letter of correct option (A, B, C, or D)
        feedback: Dictionary mapping option letters to feedback text
        bloom_level: Cognitive level (Remembering or Understanding)
        question_type: Format type (currently only Multiple Choice)
    """
    id: str
    week: int
    topic: str
    question_text: str
    options: Dict[str, str]
    correct_answer: str
    feedback: Dict[str, str]
    bloom_level: BloomLevel
    question_type: QuestionType = QuestionType.MULTIPLE_CHOICE

    def validate(self) -> List[str]:
        """
        Validate question against quality rules.

        Returns:
            List of validation error messages (empty if valid)

        Quality rules enforced:
        1. Multiple choice only (4 options A-D)
        2. One clearly correct answer
        3. All options have feedback
        4. No "All of the above" / "None of the above"
        5. No double negatives
        6. No trick questions (basic checks)
        7. Remembering/Understanding levels only
        """
        errors = []

        # Rule 1: Must have exactly 4 options
        if len(self.options) != 4:
            errors.append(f"Question {self.id} must have exactly 4 options (found {len(self.options)})")

        # Check options are labeled A, B, C, D
        expected_options = {'A', 'B', 'C', 'D'}
        if set(self.options.keys()) != expected_options:
            errors.append(
                f"Question {self.id} options must be labeled A, B, C, D "
                f"(found {', '.join(sorted(self.options.keys()))})"
            )

        # Rule 2: Correct answer must be in options
        if self.correct_answer not in self.options:
            errors.append(
                f"Question {self.id} correct answer '{self.correct_answer}' "
                f"not in options {list(self.options.keys())}"
            )

        # Rule 3: All options need feedback
        for opt in self.options.keys():
            if opt not in self.feedback:
                errors.append(f"Question {self.id} missing feedback for option {opt}")
            elif not self.feedback[opt].strip():
                errors.append(f"Question {self.id} has empty feedback for option {opt}")

        # Rule 4a: No "All of the above"
        if self._contains_phrase(self.question_text, ["all of the above"]):
            errors.append(f"Question {self.id} uses 'all of the above' in question text (prohibited)")

        for opt_letter, opt_text in self.options.items():
            if self._contains_phrase(opt_text, ["all of the above"]):
                errors.append(
                    f"Question {self.id} option {opt_letter} uses 'all of the above' (prohibited)"
                )

        # Rule 4b: No "None of the above"
        if self._contains_phrase(self.question_text, ["none of the above"]):
            errors.append(f"Question {self.id} uses 'none of the above' in question text (prohibited)")

        for opt_letter, opt_text in self.options.items():
            if self._contains_phrase(opt_text, ["none of the above"]):
                errors.append(
                    f"Question {self.id} option {opt_letter} uses 'none of the above' (prohibited)"
                )

        # Rule 5: Check for double negatives
        negative_patterns = [r'\bnot\b', r"n't\b", r'\bno\b', r'\bnever\b']
        negative_count = sum(
            len(re.findall(pattern, self.question_text, re.IGNORECASE))
            for pattern in negative_patterns
        )
        if negative_count >= 2:
            errors.append(
                f"Question {self.id} may contain double negatives "
                f"(found {negative_count} negative words/phrases)"
            )

        # Rule 6: Check question text is substantive
        if len(self.question_text.strip()) < 10:
            errors.append(f"Question {self.id} text is too short (minimum 10 characters)")

        # Check option text is substantive
        for opt_letter, opt_text in self.options.items():
            if len(opt_text.strip()) < 3:
                errors.append(f"Question {self.id} option {opt_letter} is too short")

        # Rule 7: Week number validation
        if not (1 <= self.week <= 10):
            errors.append(f"Question {self.id} week must be 1-10 (found {self.week})")

        # ID format validation (allow hyphens in topic slug)
        if not re.match(r'^W\d+-Q\d+-[\w-]+$', self.id):
            errors.append(
                f"Question ID '{self.id}' doesn't match expected format: W[week]-Q[number]-[topic]"
            )

        return errors

    def _contains_phrase(self, text: str, phrases: List[str]) -> bool:
        """Check if text contains any of the given phrases (case-insensitive)."""
        text_lower = text.lower()
        return any(phrase.lower() in text_lower for phrase in phrases)

    def is_valid(self) -> bool:
        """Quick check if question passes all validation rules."""
        return len(self.validate()) == 0

    def is_scenario_based(self) -> bool:
        """
        Heuristic check for scenario-based questions.

        Scenario-based questions are preferred as they test application
        of concepts rather than pure recall.

        Returns:
            True if question appears to be scenario-based
        """
        # Check for reasonable length (scenarios are typically longer)
        if len(self.question_text) < 100:
            return False

        # Check for scenario keywords
        scenario_keywords = [
            'manager', 'team', 'client', 'employee', 'stakeholder',
            'company', 'organization', 'department', 'colleague',
            'supervisor', 'executive', 'customer', 'vendor',
            'project', 'meeting', 'presentation', 'email', 'memo'
        ]

        text_lower = self.question_text.lower()
        keyword_matches = sum(1 for keyword in scenario_keywords if keyword in text_lower)

        return keyword_matches >= 2

    def has_detailed_feedback(self, min_length: int = 30) -> bool:
        """
        Check if all feedback options are detailed.

        Args:
            min_length: Minimum character length for "detailed" feedback

        Returns:
            True if all feedback meets minimum length requirement
        """
        return all(len(fb.strip()) >= min_length for fb in self.feedback.values())

    def get_quality_score(self, weights: Optional[Dict[str, int]] = None) -> int:
        """
        Calculate quality score for question selection.

        Args:
            weights: Optional custom weights for scoring factors
                    Default: scenario_based=2, detailed_feedback=2, valid=2

        Returns:
            Integer quality score (higher is better)
        """
        if weights is None:
            weights = {
                'scenario_based': 2,
                'detailed_feedback': 2,
                'valid': 2,
                'base': 10
            }

        score = weights.get('base', 10)

        if self.is_scenario_based():
            score += weights.get('scenario_based', 2)

        if self.has_detailed_feedback():
            score += weights.get('detailed_feedback', 2)

        if self.is_valid():
            score += weights.get('valid', 2)

        # Bonus: Correct answer not always 'A' (checked elsewhere across question set)
        # This helps avoid pattern gaming by students

        return score

    def to_dict(self) -> Dict:
        """Convert question to dictionary representation."""
        return {
            'id': self.id,
            'week': self.week,
            'topic': self.topic,
            'question_text': self.question_text,
            'options': self.options.copy(),
            'correct_answer': self.correct_answer,
            'feedback': self.feedback.copy(),
            'bloom_level': self.bloom_level.value,
            'question_type': self.question_type.value,
            'quality_score': self.get_quality_score(),
            'is_scenario_based': self.is_scenario_based(),
            'is_valid': self.is_valid()
        }

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"Question({self.id}, Week {self.week}, {self.bloom_level.value})"

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"Question(id='{self.id}', week={self.week}, topic='{self.topic}', "
            f"bloom_level={self.bloom_level})"
        )
