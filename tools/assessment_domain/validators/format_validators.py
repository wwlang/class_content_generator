"""
Layer 1: Format Validators

These validators check structural/syntactic correctness.
All issues are ERROR severity - they block export.

Version: 2.0
Specification: docs/QUIZ-FORMAT-V2-SPEC.md
"""

import re
from typing import List
from .base import BaseValidator, ValidationResult, IssueSeverity
from ..models.question import Question, QuestionType


class RequiredFieldsValidator(BaseValidator):
    """
    Validate that all required fields are present and non-empty.

    This catches issues like:
    - Missing question text
    - Missing general feedback
    - Empty topic
    - Missing correct answer
    """

    def __init__(self):
        super().__init__("format")

    def validate_question(self, question: Question) -> ValidationResult:
        result = self.create_result()
        result.questions_validated = 1

        # Check question ID
        if not question.id or not question.id.strip():
            result.add_error(
                question_id=question.id or "UNKNOWN",
                message="Missing question ID",
                field_path="id",
                suggestion="Add unique ID in format W[week]-Q[number]-[topic-slug]",
            )

        # Check question text
        if not question.question_text or not question.question_text.strip():
            result.add_error(
                question_id=question.id,
                message="Missing question text",
                field_path="question_text",
                suggestion="Add the actual question content",
            )

        # Check topic
        if not question.topic or not question.topic.strip():
            result.add_error(
                question_id=question.id,
                message="Missing topic",
                field_path="topic",
                suggestion="Add a descriptive topic (5-100 characters)",
            )

        # Check general feedback (v2.0 required field)
        if not question.general_feedback or not question.general_feedback.strip():
            result.add_error(
                question_id=question.id,
                message="Missing general feedback (required in v2.0)",
                field_path="general_feedback",
                suggestion="Add conceptual explanation that helps students answer similar questions",
            )

        return result


class QuestionIDFormatValidator(BaseValidator):
    """
    Validate question ID format: W[week]-Q[number]-[topic-slug]

    Examples:
    - W2-Q1-freeman-definition ✅
    - W10-Q15-stakeholder-analysis ✅
    - W2-Q1 ❌ (missing topic)
    - Week2-Q1-topic ❌ (should be W2, not Week2)
    """

    def __init__(self):
        super().__init__("format")
        self.pattern = re.compile(r"^W\d+-Q\d+-[\w-]+$")

    def validate_question(self, question: Question) -> ValidationResult:
        result = self.create_result()
        result.questions_validated = 1

        if not self.pattern.match(question.id):
            result.add_error(
                question_id=question.id,
                message=f"Invalid ID format: '{question.id}'",
                field_path="id",
                suggestion="Use format W[week]-Q[number]-[topic-slug] (e.g., W2-Q1-freeman-definition)",
            )
        else:
            # Extract week from ID and verify it matches question.week
            match = re.match(r"^W(\d+)-", question.id)
            if match:
                id_week = int(match.group(1))
                if id_week != question.week:
                    result.add_error(
                        question_id=question.id,
                        message=f"Week mismatch: ID says W{id_week} but question.week is {question.week}",
                        field_path="id",
                        suggestion=f"Change ID to W{question.week}-... or update question.week to {id_week}",
                    )

        return result


class FieldLengthValidator(BaseValidator):
    """
    Validate field length constraints per specification.

    Constraints:
    - topic: 5-100 characters
    - question_text: 20-1000 characters
    - general_feedback: 50-1000 characters
    - option text: 10-500 characters (MC)
    - option feedback: 20-500 characters (MC)
    """

    def __init__(self):
        super().__init__("format")

    def validate_question(self, question: Question) -> ValidationResult:
        result = self.create_result()
        result.questions_validated = 1

        # Topic length
        topic_len = len(question.topic.strip())
        if topic_len < 5:
            result.add_error(
                question_id=question.id,
                message=f"Topic too short ({topic_len} chars, min 5)",
                field_path="topic",
                suggestion="Provide a more descriptive topic",
            )
        elif topic_len > 100:
            result.add_error(
                question_id=question.id,
                message=f"Topic too long ({topic_len} chars, max 100)",
                field_path="topic",
                suggestion="Shorten topic to 100 characters or less",
            )

        # Question text length
        question_len = len(question.question_text.strip())
        if question_len < 20:
            result.add_error(
                question_id=question.id,
                message=f"Question text too short ({question_len} chars, min 20)",
                field_path="question_text",
                suggestion="Expand question to at least 20 characters",
            )
        elif question_len > 1000:
            result.add_error(
                question_id=question.id,
                message=f"Question text too long ({question_len} chars, max 1000)",
                field_path="question_text",
                suggestion="Simplify question to 1000 characters or less",
            )

        # General feedback length
        feedback_len = len(question.general_feedback.strip())
        if feedback_len > 0:  # Only check if present
            if feedback_len < 50:
                result.add_error(
                    question_id=question.id,
                    message=f"General feedback too short ({feedback_len} chars, min 50)",
                    field_path="general_feedback",
                    suggestion="Expand to 50-200 words with conceptual explanation",
                )
            elif feedback_len > 1000:
                result.add_error(
                    question_id=question.id,
                    message=f"General feedback too long ({feedback_len} chars, max 1000)",
                    field_path="general_feedback",
                    suggestion="Condense to 1000 characters or less",
                )

        # Type-specific validation
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            self._validate_mc_lengths(question, result)
        elif question.question_type == QuestionType.TRUE_FALSE:
            self._validate_tf_lengths(question, result)
        elif question.question_type == QuestionType.MATCHING:
            self._validate_matching_lengths(question, result)

        return result

    def _validate_mc_lengths(self, question: Question, result: ValidationResult):
        """Validate Multiple Choice field lengths."""
        for key, text in question.options.items():
            text_len = len(text.strip())
            if text_len < 10:
                result.add_error(
                    question_id=question.id,
                    message=f"Option {key} text too short ({text_len} chars, min 10)",
                    field_path=f"options.{key}",
                )
            elif text_len > 500:
                result.add_error(
                    question_id=question.id,
                    message=f"Option {key} text too long ({text_len} chars, max 500)",
                    field_path=f"options.{key}",
                )

        # Check option feedback (if using option_feedback field)
        feedback_dict = question.option_feedback or question.feedback
        for key, feedback in feedback_dict.items():
            feedback_len = len(feedback.strip())
            if feedback_len < 20:
                result.add_error(
                    question_id=question.id,
                    message=f"Option {key} feedback too short ({feedback_len} chars, min 20)",
                    field_path=f"feedback.{key}",
                )
            elif feedback_len > 500:
                result.add_error(
                    question_id=question.id,
                    message=f"Option {key} feedback too long ({feedback_len} chars, max 500)",
                    field_path=f"feedback.{key}",
                )

    def _validate_tf_lengths(self, question: Question, result: ValidationResult):
        """Validate True/False field lengths."""
        if question.true_feedback:
            true_len = len(question.true_feedback.strip())
            if true_len < 20:
                result.add_error(
                    question_id=question.id,
                    message=f"True feedback too short ({true_len} chars, min 20)",
                    field_path="feedback.if_true",
                )
            elif true_len > 500:
                result.add_error(
                    question_id=question.id,
                    message=f"True feedback too long ({true_len} chars, max 500)",
                    field_path="feedback.if_true",
                )

        if question.false_feedback:
            false_len = len(question.false_feedback.strip())
            if false_len < 20:
                result.add_error(
                    question_id=question.id,
                    message=f"False feedback too short ({false_len} chars, min 20)",
                    field_path="feedback.if_false",
                )
            elif false_len > 500:
                result.add_error(
                    question_id=question.id,
                    message=f"False feedback too long ({false_len} chars, max 500)",
                    field_path="feedback.if_false",
                )

    def _validate_matching_lengths(self, question: Question, result: ValidationResult):
        """Validate Matching field lengths."""
        for key, item in (question.matching_items or {}).items():
            item_len = len(item.strip())
            if item_len < 5:
                result.add_error(
                    question_id=question.id,
                    message=f"Matching item {key} too short ({item_len} chars, min 5)",
                    field_path=f"items.{key}",
                )
            elif item_len > 200:
                result.add_error(
                    question_id=question.id,
                    message=f"Matching item {key} too long ({item_len} chars, max 200)",
                    field_path=f"items.{key}",
                )


class MultipleChoiceFormatValidator(BaseValidator):
    """
    Validate Multiple Choice format requirements.

    Rules:
    - Exactly 4 options (A, B, C, D)
    - Exactly 1 correct answer
    - All options have feedback
    - Correct answer is one of A-D
    """

    def __init__(self):
        super().__init__("format")

    def validate_question(self, question: Question) -> ValidationResult:
        result = self.create_result()
        result.questions_validated = 1

        if question.question_type != QuestionType.MULTIPLE_CHOICE:
            return result  # Skip non-MC questions

        # Check exactly 4 options
        if len(question.options) != 4:
            result.add_error(
                question_id=question.id,
                message=f"Must have exactly 4 options, found {len(question.options)}",
                field_path="options",
                suggestion="Add or remove options to have exactly A, B, C, D",
            )

        # Check options are labeled A, B, C, D
        expected_keys = {"A", "B", "C", "D"}
        actual_keys = set(question.options.keys())
        if actual_keys != expected_keys:
            missing = expected_keys - actual_keys
            extra = actual_keys - expected_keys
            msg_parts = []
            if missing:
                msg_parts.append(f"missing {sorted(missing)}")
            if extra:
                msg_parts.append(f"unexpected {sorted(extra)}")
            result.add_error(
                question_id=question.id,
                message=f"Options must be A, B, C, D ({', '.join(msg_parts)})",
                field_path="options",
            )

        # Check correct answer is valid
        if question.correct_answer not in question.options:
            result.add_error(
                question_id=question.id,
                message=f"Correct answer '{question.correct_answer}' not in options {list(question.options.keys())}",
                field_path="correct_answer",
                suggestion="Set correct_answer to A, B, C, or D",
            )

        # Check all options have feedback
        feedback_dict = question.option_feedback or question.feedback
        for key in question.options.keys():
            if key not in feedback_dict or not feedback_dict[key].strip():
                result.add_error(
                    question_id=question.id,
                    message=f"Option {key} missing feedback",
                    field_path=f"feedback.{key}",
                    suggestion="Add explanation for why this option is correct/incorrect",
                )

        return result


class TrueFalseFormatValidator(BaseValidator):
    """
    Validate True/False format requirements.

    Rules:
    - correct_answer is boolean or "TRUE"/"FALSE"
    - Has true_feedback
    - Has false_feedback
    """

    def __init__(self):
        super().__init__("format")

    def validate_question(self, question: Question) -> ValidationResult:
        result = self.create_result()
        result.questions_validated = 1

        if question.question_type != QuestionType.TRUE_FALSE:
            return result

        # Check correct answer format
        valid_answers = ["TRUE", "FALSE", "True", "False", "true", "false"]
        if question.correct_answer not in valid_answers:
            result.add_error(
                question_id=question.id,
                message=f"True/False correct_answer must be TRUE or FALSE, found '{question.correct_answer}'",
                field_path="correct_answer",
                suggestion="Set correct_answer to true or false",
            )

        # Check true feedback
        if not question.true_feedback or not question.true_feedback.strip():
            result.add_error(
                question_id=question.id,
                message="Missing true_feedback (if_true)",
                field_path="feedback.if_true",
                suggestion="Add feedback explaining why True is correct/incorrect",
            )

        # Check false feedback
        if not question.false_feedback or not question.false_feedback.strip():
            result.add_error(
                question_id=question.id,
                message="Missing false_feedback (if_false)",
                field_path="feedback.if_false",
                suggestion="Add feedback explaining why False is correct/incorrect",
            )

        return result


class MatchingFormatValidator(BaseValidator):
    """
    Validate Matching format requirements.

    Rules:
    - 3-6 pairs
    - Item keys are sequential integers ("1", "2", "3")
    - Match keys are sequential letters ("A", "B", "C")
    - All pairs have feedback
    """

    def __init__(self):
        super().__init__("format")

    def validate_question(self, question: Question) -> ValidationResult:
        result = self.create_result()
        result.questions_validated = 1

        if question.question_type != QuestionType.MATCHING:
            return result

        items = question.matching_items or {}
        matches = question.matching_matches or {}
        pairs = question.correct_pairs or {}

        # Check pair count
        pair_count = len(pairs)
        if pair_count < 3:
            result.add_error(
                question_id=question.id,
                message=f"Must have at least 3 matching pairs, found {pair_count}",
                field_path="pairs",
                suggestion="Add more matching pairs (3-6 recommended)",
            )
        elif pair_count > 6:
            result.add_error(
                question_id=question.id,
                message=f"Too many matching pairs ({pair_count}, max 6)",
                field_path="pairs",
                suggestion="Reduce to 6 pairs or fewer for clarity",
            )

        # Check item keys are sequential integers
        if items:
            expected_item_keys = [str(i) for i in range(1, len(items) + 1)]
            actual_item_keys = sorted(items.keys(), key=lambda x: int(x) if x.isdigit() else 0)
            if actual_item_keys != expected_item_keys:
                result.add_error(
                    question_id=question.id,
                    message=f"Item keys must be sequential integers ('1', '2', '3'), found {actual_item_keys}",
                    field_path="pairs.item_key",
                )

        # Check match keys are sequential letters
        if matches:
            expected_match_keys = [chr(65 + i) for i in range(len(matches))]
            actual_match_keys = sorted(matches.keys())
            if actual_match_keys != expected_match_keys:
                result.add_error(
                    question_id=question.id,
                    message=f"Match keys must be sequential letters ('A', 'B', 'C'), found {actual_match_keys}",
                    field_path="pairs.match_key",
                )

        # Check all pairs have feedback
        pair_feedback = question.pair_feedback or {}
        for item_key, match_key in pairs.items():
            feedback_key = f"{item_key}-{match_key}"
            if feedback_key not in pair_feedback or not pair_feedback[feedback_key].strip():
                result.add_error(
                    question_id=question.id,
                    message=f"Missing feedback for pair {item_key}-{match_key}",
                    field_path=f"pair_feedback.{feedback_key}",
                    suggestion="Add explanation for why this pairing is correct",
                )

        return result


class BloomLevelValidator(BaseValidator):
    """
    Validate Bloom's taxonomy level.

    Rules:
    - Must be "remembering" or "understanding" (lowercase)
    - No higher-order levels for quizzes
    """

    def __init__(self):
        super().__init__("format")

    def validate_question(self, question: Question) -> ValidationResult:
        result = self.create_result()
        result.questions_validated = 1

        valid_levels = ["remembering", "understanding"]
        actual_level = question.bloom_level.value.lower()

        if actual_level not in valid_levels:
            result.add_error(
                question_id=question.id,
                message=f"Invalid Bloom level '{actual_level}' (must be 'remembering' or 'understanding')",
                field_path="bloom_level",
                suggestion="Change to 'remembering' or 'understanding'",
            )

        return result


# ============================================================================
# Format Validator Registry
# ============================================================================


class FormatValidatorRegistry:
    """
    Registry of all Layer 1 format validators.

    Usage:
        registry = FormatValidatorRegistry()
        result = registry.validate_all(questions)
    """

    def __init__(self):
        self.validators: List[BaseValidator] = [
            RequiredFieldsValidator(),
            QuestionIDFormatValidator(),
            FieldLengthValidator(),
            MultipleChoiceFormatValidator(),
            TrueFalseFormatValidator(),
            MatchingFormatValidator(),
            BloomLevelValidator(),
        ]

    def validate_all(self, questions: List[Question]) -> ValidationResult:
        """
        Run all format validators on questions.

        Args:
            questions: List of questions to validate

        Returns:
            Combined ValidationResult
        """
        result = ValidationResult(validation_layer="format", questions_validated=len(questions))

        for validator in self.validators:
            validator_result = validator.validate_questions(questions)
            result.merge(validator_result)

        return result
