"""
Pydantic schemas for quiz question validation.

This module defines the single source of truth for quiz question format.
All quiz questions must validate against these schemas before export to GIFT.

Version: 2.0
Specification: docs/QUIZ-FORMAT-V2-SPEC.md
"""

from enum import Enum
from typing import List, Literal, Union
from pydantic import BaseModel, Field, field_validator, model_validator
import re


# ============================================================================
# Enumerations
# ============================================================================


class BloomLevel(str, Enum):
    """Bloom's Taxonomy cognitive levels (lower-order only for quizzes)."""

    REMEMBERING = "remembering"
    UNDERSTANDING = "understanding"


class QuestionType(str, Enum):
    """Supported question types."""

    MULTIPLE_CHOICE = "multiple_choice"
    TRUE_FALSE = "true_false"
    MATCHING = "matching"


# ============================================================================
# Metadata Schema
# ============================================================================


class MetadataSchema(BaseModel):
    """Document-level metadata for quiz questions file."""

    week: int = Field(..., ge=1, le=12, description="Week number (1-12)")
    topic: str = Field(
        ..., min_length=5, max_length=200, description="Week topic from syllabus"
    )
    prepares_for: str = Field(
        ..., min_length=5, max_length=100, description="Assessment name from syllabus"
    )
    source: str = Field(
        default="lecture-content.md", description="Source file for quiz content"
    )

    @field_validator("topic")
    @classmethod
    def topic_must_be_descriptive(cls, v: str) -> str:
        """Ensure topic is descriptive, not generic."""
        generic_topics = ["quiz", "questions", "test", "assessment"]
        if any(word in v.lower() for word in generic_topics):
            raise ValueError(
                f"Topic must be descriptive (not generic like 'quiz'): {v}"
            )
        return v


# ============================================================================
# Multiple Choice Schemas
# ============================================================================


class OptionSchema(BaseModel):
    """Single option in a multiple choice question."""

    key: str = Field(..., pattern=r"^[A-D]$", description="Option key (A, B, C, or D)")
    text: str = Field(
        ..., min_length=10, max_length=500, description="Option text (10-500 chars)"
    )
    feedback: str = Field(
        ...,
        min_length=20,
        max_length=500,
        description="Explanation for this option (20-500 chars)",
    )
    correct: bool = Field(default=False, description="Whether this is the correct answer")

    @field_validator("text")
    @classmethod
    def no_prohibited_phrases(cls, v: str) -> str:
        """Prohibit ambiguous or lazy phrases."""
        prohibited = [
            "all of the above",
            "none of the above",
            "both a and b",
            "either a or b",
        ]
        v_lower = v.lower()
        for phrase in prohibited:
            if phrase in v_lower:
                raise ValueError(
                    f"Prohibited phrase '{phrase}' found in option text. "
                    "Each option should stand alone."
                )
        return v

    @field_validator("feedback")
    @classmethod
    def feedback_must_explain_why(cls, v: str) -> str:
        """Ensure feedback explains reasoning, not just states right/wrong."""
        # Check for lazy feedback
        lazy_patterns = [
            r"^correct\.?$",
            r"^incorrect\.?$",
            r"^wrong\.?$",
            r"^right\.?$",
        ]
        v_lower = v.lower().strip()
        for pattern in lazy_patterns:
            if re.match(pattern, v_lower):
                raise ValueError(
                    f"Feedback must explain WHY, not just state 'correct' or 'incorrect': {v}"
                )
        return v


class MultipleChoiceQuestionSchema(BaseModel):
    """Multiple choice question with 4 options."""

    id: str = Field(
        ...,
        pattern=r"^W\d+-Q\d+-[\w-]+$",
        description="Question ID (format: W2-Q1-topic-slug)",
    )
    type: Literal[QuestionType.MULTIPLE_CHOICE] = Field(
        ..., description="Must be 'multiple_choice'"
    )
    bloom_level: BloomLevel = Field(..., description="Bloom's taxonomy level")
    topic: str = Field(
        ..., min_length=5, max_length=100, description="Question topic (5-100 chars)"
    )
    question: str = Field(
        ...,
        min_length=20,
        max_length=1000,
        description="Question text (20-1000 chars)",
    )
    options: List[OptionSchema] = Field(
        ..., min_length=4, max_length=4, description="Exactly 4 options (A, B, C, D)"
    )
    general_feedback: str = Field(
        ...,
        min_length=50,
        max_length=1000,
        description="General feedback shown to all students (50-1000 chars)",
    )

    @field_validator("question")
    @classmethod
    def question_must_be_clear(cls, v: str) -> str:
        """Ensure question is clear and ends with question mark."""
        if not v.strip().endswith("?"):
            raise ValueError(
                f"Question should end with a question mark for clarity: {v}"
            )
        return v

    @model_validator(mode="after")
    def validate_options(self) -> "MultipleChoiceQuestionSchema":
        """Validate option constraints."""
        # Check exactly 4 options
        if len(self.options) != 4:
            raise ValueError(f"Must have exactly 4 options, got {len(self.options)}")

        # Check keys are A, B, C, D
        keys = [opt.key for opt in self.options]
        if keys != ["A", "B", "C", "D"]:
            raise ValueError(f"Option keys must be A, B, C, D in order, got: {keys}")

        # Check exactly one correct answer
        correct_count = sum(1 for opt in self.options if opt.correct)
        if correct_count == 0:
            raise ValueError("Must have at least one correct answer")
        if correct_count > 1:
            raise ValueError(
                f"Must have exactly one correct answer, got {correct_count}"
            )

        return self

    @field_validator("general_feedback")
    @classmethod
    def general_feedback_must_be_conceptual(cls, v: str) -> str:
        """Ensure general feedback is conceptual, not answer-specific."""
        # Check for answer-specific phrases
        answer_specific = [
            "the correct answer is",
            "option a is",
            "option b is",
            "option c is",
            "option d is",
            "you should have selected",
        ]
        v_lower = v.lower()
        for phrase in answer_specific:
            if phrase in v_lower:
                raise ValueError(
                    f"General feedback should be conceptual, not answer-specific. "
                    f"Avoid phrases like '{phrase}'"
                )
        return v


# ============================================================================
# True/False Schemas
# ============================================================================


class TrueFalseFeedbackSchema(BaseModel):
    """Feedback for true/false questions (one for each possible answer)."""

    if_true: str = Field(
        ...,
        min_length=20,
        max_length=500,
        description="Feedback if student answers True (20-500 chars)",
    )
    if_false: str = Field(
        ...,
        min_length=20,
        max_length=500,
        description="Feedback if student answers False (20-500 chars)",
    )

    @field_validator("if_true", "if_false")
    @classmethod
    def feedback_must_explain_why(cls, v: str) -> str:
        """Ensure feedback explains reasoning, not just states right/wrong."""
        lazy_patterns = [
            r"^correct\.?$",
            r"^incorrect\.?$",
            r"^wrong\.?$",
            r"^right\.?$",
        ]
        v_lower = v.lower().strip()
        for pattern in lazy_patterns:
            if re.match(pattern, v_lower):
                raise ValueError(
                    f"Feedback must explain WHY, not just state 'correct' or 'incorrect': {v}"
                )
        return v


class TrueFalseQuestionSchema(BaseModel):
    """True/False question."""

    id: str = Field(
        ...,
        pattern=r"^W\d+-Q\d+-[\w-]+$",
        description="Question ID (format: W2-Q1-topic-slug)",
    )
    type: Literal[QuestionType.TRUE_FALSE] = Field(
        ..., description="Must be 'true_false'"
    )
    bloom_level: BloomLevel = Field(..., description="Bloom's taxonomy level")
    topic: str = Field(
        ..., min_length=5, max_length=100, description="Question topic (5-100 chars)"
    )
    question: str = Field(
        ...,
        min_length=20,
        max_length=1000,
        description="Question text (20-1000 chars)",
    )
    correct_answer: bool = Field(..., description="Correct answer (true or false)")
    feedback: TrueFalseFeedbackSchema = Field(
        ..., description="Feedback for both true and false answers"
    )
    general_feedback: str = Field(
        ...,
        min_length=50,
        max_length=1000,
        description="General feedback shown to all students (50-1000 chars)",
    )

    @field_validator("question")
    @classmethod
    def question_must_be_statement(cls, v: str) -> str:
        """True/False questions should be statements, not questions."""
        if v.strip().endswith("?"):
            raise ValueError(
                f"True/False questions should be statements (not questions): {v}"
            )
        return v


# ============================================================================
# Matching Schemas
# ============================================================================


class MatchingPairSchema(BaseModel):
    """Single matching pair (item-to-match relationship)."""

    item: str = Field(
        ..., min_length=5, max_length=200, description="Item to match (5-200 chars)"
    )
    match: str = Field(
        ..., min_length=5, max_length=200, description="Correct match (5-200 chars)"
    )
    item_key: str = Field(
        ..., pattern=r"^[1-9]\d*$", description="Item key (numeric string: '1', '2', '3')"
    )
    match_key: str = Field(
        ..., pattern=r"^[A-Z]$", description="Match key (letter: 'A', 'B', 'C')"
    )
    feedback: str = Field(
        ...,
        min_length=20,
        max_length=500,
        description="Explanation for this pairing (20-500 chars)",
    )

    @field_validator("feedback")
    @classmethod
    def feedback_must_explain_why(cls, v: str) -> str:
        """Ensure feedback explains the relationship."""
        lazy_patterns = [
            r"^correct\.?$",
            r"^incorrect\.?$",
            r"^wrong\.?$",
            r"^right\.?$",
        ]
        v_lower = v.lower().strip()
        for pattern in lazy_patterns:
            if re.match(pattern, v_lower):
                raise ValueError(
                    f"Feedback must explain WHY this pairing is correct: {v}"
                )
        return v


class MatchingQuestionSchema(BaseModel):
    """Matching question with 3-6 pairs."""

    id: str = Field(
        ...,
        pattern=r"^W\d+-Q\d+-[\w-]+$",
        description="Question ID (format: W2-Q1-topic-slug)",
    )
    type: Literal[QuestionType.MATCHING] = Field(..., description="Must be 'matching'")
    bloom_level: BloomLevel = Field(..., description="Bloom's taxonomy level")
    topic: str = Field(
        ..., min_length=5, max_length=100, description="Question topic (5-100 chars)"
    )
    question: str = Field(
        ...,
        min_length=20,
        max_length=1000,
        description="Question instruction (20-1000 chars)",
    )
    pairs: List[MatchingPairSchema] = Field(
        ..., min_length=3, max_length=6, description="3-6 matching pairs"
    )
    general_feedback: str = Field(
        ...,
        min_length=50,
        max_length=1000,
        description="General feedback shown to all students (50-1000 chars)",
    )

    @model_validator(mode="after")
    def validate_pairs(self) -> "MatchingQuestionSchema":
        """Validate pair constraints."""
        # Check pair count
        if len(self.pairs) < 3 or len(self.pairs) > 6:
            raise ValueError(f"Must have 3-6 pairs, got {len(self.pairs)}")

        # Check item_key sequence
        item_keys = [pair.item_key for pair in self.pairs]
        expected_item_keys = [str(i) for i in range(1, len(self.pairs) + 1)]
        if item_keys != expected_item_keys:
            raise ValueError(
                f"item_key must be sequential integers as strings ('1', '2', '3', ...), "
                f"got: {item_keys}"
            )

        # Check match_key sequence
        match_keys = [pair.match_key for pair in self.pairs]
        expected_match_keys = [chr(65 + i) for i in range(len(self.pairs))]  # A, B, C, ...
        if match_keys != expected_match_keys:
            raise ValueError(
                f"match_key must be sequential letters ('A', 'B', 'C', ...), "
                f"got: {match_keys}"
            )

        return self


# ============================================================================
# Quiz Document Schema
# ============================================================================


class QuizDocumentSchema(BaseModel):
    """Complete quiz questions file with metadata and questions."""

    metadata: MetadataSchema = Field(..., description="Document metadata")
    questions: List[
        Union[
            MultipleChoiceQuestionSchema,
            TrueFalseQuestionSchema,
            MatchingQuestionSchema,
        ]
    ] = Field(..., min_length=1, description="List of questions (min 1)")

    @model_validator(mode="after")
    def validate_questions(self) -> "QuizDocumentSchema":
        """Cross-validate questions."""
        # Check for duplicate IDs
        ids = [q.id for q in self.questions]
        if len(ids) != len(set(ids)):
            duplicates = [id for id in ids if ids.count(id) > 1]
            raise ValueError(f"Duplicate question IDs found: {duplicates}")

        # Check week consistency
        for question in self.questions:
            # Extract week from question ID (format: W2-Q1-topic-slug)
            match = re.match(r"^W(\d+)-", question.id)
            if not match:
                raise ValueError(f"Invalid question ID format: {question.id}")

            question_week = int(match.group(1))
            if question_week != self.metadata.week:
                raise ValueError(
                    f"Question {question.id} week ({question_week}) does not match "
                    f"metadata week ({self.metadata.week})"
                )

        return self

    @field_validator("questions")
    @classmethod
    def validate_bloom_distribution(
        cls,
        questions: List[
            Union[
                MultipleChoiceQuestionSchema,
                TrueFalseQuestionSchema,
                MatchingQuestionSchema,
            ]
        ],
    ) -> List[
        Union[
            MultipleChoiceQuestionSchema,
            TrueFalseQuestionSchema,
            MatchingQuestionSchema,
        ]
    ]:
        """Warn if Bloom distribution is skewed (not blocking)."""
        if len(questions) < 5:
            # Skip for small question sets
            return questions

        remembering_count = sum(
            1 for q in questions if q.bloom_level == BloomLevel.REMEMBERING
        )
        understanding_count = sum(
            1 for q in questions if q.bloom_level == BloomLevel.UNDERSTANDING
        )

        total = len(questions)
        remembering_pct = (remembering_count / total) * 100
        understanding_pct = (understanding_count / total) * 100

        # Warn if heavily skewed (>80% one type)
        if remembering_pct > 80 or understanding_pct > 80:
            print(
                f"⚠️  WARNING: Bloom distribution is skewed - "
                f"{remembering_pct:.0f}% Remembering, {understanding_pct:.0f}% Understanding. "
                f"Aim for balanced mix."
            )

        return questions
