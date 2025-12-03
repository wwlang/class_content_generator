"""
Layer 2: Content Quality Validators

These validators check content quality and clarity.
Most issues are WARNING severity - should fix but not blocking.

Version: 2.0
Specification: docs/QUIZ-FORMAT-V2-SPEC.md
"""

import re
from typing import List
from .base import BaseValidator, ValidationResult, IssueSeverity
from ..models.question import Question, QuestionType


class FeedbackQualityValidator(BaseValidator):
    """
    Validate feedback explains WHY, not just right/wrong.

    Good feedback:
    - Explains reasoning
    - References concepts
    - Points to resources

    Bad feedback:
    - "Correct"
    - "Incorrect"
    - "Wrong answer"
    """

    def __init__(self):
        super().__init__("content")

    def validate_question(self, question: Question) -> ValidationResult:
        result = self.create_result()
        result.questions_validated = 1

        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            self._validate_mc_feedback(question, result)
        elif question.question_type == QuestionType.TRUE_FALSE:
            self._validate_tf_feedback(question, result)
        elif question.question_type == QuestionType.MATCHING:
            self._validate_matching_feedback(question, result)

        return result

    def _validate_mc_feedback(self, question: Question, result: ValidationResult):
        """Validate Multiple Choice feedback quality."""
        feedback_dict = question.option_feedback or question.feedback

        for key, feedback in feedback_dict.items():
            score = self._score_feedback(feedback, key == question.correct_answer)

            if score < 30:
                result.add_warning(
                    question_id=question.id,
                    message=f"Option {key} feedback is low quality (score: {score}/100)",
                    field_path=f"feedback.{key}",
                    suggestion="Explain WHY this is correct/incorrect, reference concepts",
                )

    def _validate_tf_feedback(self, question: Question, result: ValidationResult):
        """Validate True/False feedback quality."""
        if question.true_feedback:
            score = self._score_feedback(question.true_feedback, question.correct_answer.upper() == "TRUE")
            if score < 30:
                result.add_warning(
                    question_id=question.id,
                    message=f"True feedback is low quality (score: {score}/100)",
                    field_path="feedback.if_true",
                    suggestion="Explain WHY, reference concepts or lecture resources",
                )

        if question.false_feedback:
            score = self._score_feedback(question.false_feedback, question.correct_answer.upper() == "FALSE")
            if score < 30:
                result.add_warning(
                    question_id=question.id,
                    message=f"False feedback is low quality (score: {score}/100)",
                    field_path="feedback.if_false",
                    suggestion="Explain WHY, reference concepts or lecture resources",
                )

    def _validate_matching_feedback(self, question: Question, result: ValidationResult):
        """Validate Matching pair feedback quality."""
        pair_feedback = question.pair_feedback or {}

        for pair_key, feedback in pair_feedback.items():
            score = self._score_feedback(feedback, is_correct=True)
            if score < 30:
                result.add_warning(
                    question_id=question.id,
                    message=f"Pair {pair_key} feedback is low quality (score: {score}/100)",
                    field_path=f"pair_feedback.{pair_key}",
                    suggestion="Explain WHY this pairing is correct, what relationship connects them",
                )

    def _score_feedback(self, feedback: str, is_correct: bool) -> int:
        """
        Score feedback quality (0-100).

        Scoring:
        - Length >= 50 chars: +25 points
        - Explains WHY (has explanatory words): +25 points
        - References concepts/resources: +25 points
        - Avoids lazy phrases: +25 points
        """
        score = 0
        feedback_lower = feedback.lower()

        # Length check (25 points)
        if len(feedback) >= 50:
            score += 25

        # Explains WHY (25 points)
        explanatory_words = ["because", "since", "reason", "due to", "as a result", "therefore", "thus"]
        if any(word in feedback_lower for word in explanatory_words):
            score += 25

        # References concepts/resources (25 points)
        resource_words = ["lecture", "slide", "week", "reading", "concept", "theory", "model", "framework"]
        if any(word in feedback_lower for word in resource_words):
            score += 25

        # Avoids lazy phrases (25 points)
        lazy_phrases = [
            r"^correct\.?$",
            r"^incorrect\.?$",
            r"^wrong\.?$",
            r"^right\.?$",
            r"^this is (the )?correct",
            r"^this is (the )?incorrect",
        ]
        is_lazy = any(re.match(pattern, feedback_lower.strip()) for pattern in lazy_phrases)
        if not is_lazy:
            score += 25

        return score


class GeneralFeedbackQualityValidator(BaseValidator):
    """
    Validate general feedback is conceptual and helpful.

    Good general feedback:
    - Explains underlying concept
    - Helps with similar questions
    - References lecture resources
    - Provides memory aids

    Bad general feedback:
    - Answer-specific ("Option B is correct because...")
    - Too vague ("This is important to know")
    - Too short (< 50 words)
    """

    def __init__(self):
        super().__init__("content")

    def validate_question(self, question: Question) -> ValidationResult:
        result = self.create_result()
        result.questions_validated = 1

        if not question.general_feedback:
            return result  # Already caught by format validator

        feedback = question.general_feedback
        feedback_lower = feedback.lower()

        # Check for answer-specific phrases (WARNING)
        answer_specific = [
            "the correct answer is",
            "option a is",
            "option b is",
            "option c is",
            "option d is",
            "you should have selected",
            "the right answer",
        ]
        for phrase in answer_specific:
            if phrase in feedback_lower:
                result.add_warning(
                    question_id=question.id,
                    message=f"General feedback is answer-specific (contains '{phrase}')",
                    field_path="general_feedback",
                    suggestion="Focus on explaining the concept, not the answer choice",
                )
                break  # Only report once

        # Check for vague feedback (WARNING)
        if len(feedback.split()) < 20:  # Less than ~20 words
            result.add_warning(
                question_id=question.id,
                message=f"General feedback is too brief ({len(feedback.split())} words, aim for 50-150)",
                field_path="general_feedback",
                suggestion="Expand to explain concept, study tips, and resource references",
            )

        # Check for resource references (INFO if missing)
        resource_words = ["week", "slide", "lecture", "reading", "assessment", "presentation", "memo", "proposal"]
        has_resource = any(word in feedback_lower for word in resource_words)
        if not has_resource:
            result.add_info(
                question_id=question.id,
                message="General feedback doesn't reference lecture resources",
                field_path="general_feedback",
                suggestion="Add reference like 'See Week 2 slides 15-22' or 'Applied in Assessment 3'",
            )

        return result


class ProhibitedPhrasesValidator(BaseValidator):
    """
    Detect prohibited phrases in questions and options.

    Prohibited in options:
    - "All of the above"
    - "None of the above"
    - "Both A and B"
    - "Either A or B"

    Prohibited in questions:
    - Double negatives
    - Ambiguous wording
    """

    def __init__(self):
        super().__init__("content")

    def validate_question(self, question: Question) -> ValidationResult:
        result = self.create_result()
        result.questions_validated = 1

        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            self._check_mc_prohibited_phrases(question, result)

        # Check for double negatives in question text
        self._check_double_negatives(question, result)

        return result

    def _check_mc_prohibited_phrases(self, question: Question, result: ValidationResult):
        """Check for prohibited phrases in MC options."""
        prohibited = [
            "all of the above",
            "none of the above",
            "both a and b",
            "either a or b",
            "a and b",
            "all options",
            "no options",
        ]

        for key, text in question.options.items():
            text_lower = text.lower()
            for phrase in prohibited:
                if phrase in text_lower:
                    result.add_warning(
                        question_id=question.id,
                        message=f"Option {key} contains prohibited phrase '{phrase}'",
                        field_path=f"options.{key}",
                        suggestion=f"Rewrite option {key} to stand alone without referencing other options",
                    )
                    break  # Only report first match per option

    def _check_double_negatives(self, question: Question, result: ValidationResult):
        """Check for double negatives in question text."""
        negative_patterns = [r"\bnot\b", r"n't\b", r"\bno\b", r"\bnever\b", r"\bneither\b"]
        negative_count = sum(
            len(re.findall(pattern, question.question_text, re.IGNORECASE))
            for pattern in negative_patterns
        )

        if negative_count >= 2:
            result.add_warning(
                question_id=question.id,
                message=f"Question may contain double negatives ({negative_count} negative words)",
                field_path="question_text",
                suggestion="Rephrase question to use positive wording for clarity",
            )


class QuestionClarityValidator(BaseValidator):
    """
    Validate question clarity and readability.

    Checks:
    - Ends with question mark (MC)
    - Is a statement (T/F)
    - Clear instruction (Matching)
    - No ambiguous wording
    """

    def __init__(self):
        super().__init__("content")

    def validate_question(self, question: Question) -> ValidationResult:
        result = self.create_result()
        result.questions_validated = 1

        question_text = question.question_text.strip()

        # Multiple Choice: should end with ?
        if question.question_type == QuestionType.MULTIPLE_CHOICE:
            if not question_text.endswith("?"):
                result.add_warning(
                    question_id=question.id,
                    message="Multiple choice question should end with '?'",
                    field_path="question_text",
                    suggestion="Add question mark for clarity",
                )

        # True/False: should NOT end with ?
        elif question.question_type == QuestionType.TRUE_FALSE:
            if question_text.endswith("?"):
                result.add_warning(
                    question_id=question.id,
                    message="True/False should be a statement, not a question",
                    field_path="question_text",
                    suggestion="Rephrase as a statement (e.g., 'Stakeholder theory argues that...')",
                )

        # Matching: should have instruction
        elif question.question_type == QuestionType.MATCHING:
            instruction_words = ["match", "pair", "connect", "associate"]
            has_instruction = any(word in question_text.lower() for word in instruction_words)
            if not has_instruction:
                result.add_info(
                    question_id=question.id,
                    message="Matching question should include clear instruction",
                    field_path="question_text",
                    suggestion="Add instruction like 'Match each model to its key feature'",
                )

        # Check for ambiguous words (all types)
        ambiguous_words = ["might", "could", "may", "possibly", "usually", "often"]
        question_lower = question_text.lower()
        found_ambiguous = [word for word in ambiguous_words if word in question_lower]
        if found_ambiguous:
            result.add_info(
                question_id=question.id,
                message=f"Question contains ambiguous words: {', '.join(found_ambiguous)}",
                field_path="question_text",
                suggestion="Use definitive wording for clarity (is/does, not might/could)",
            )

        return result


class OptionDistinctivenessValidator(BaseValidator):
    """
    Validate MC options are distinct (no near-duplicates).

    Checks:
    - Options are meaningfully different
    - No options are subsets of others
    """

    def __init__(self):
        super().__init__("content")

    def validate_question(self, question: Question) -> ValidationResult:
        result = self.create_result()
        result.questions_validated = 1

        if question.question_type != QuestionType.MULTIPLE_CHOICE:
            return result

        options = list(question.options.items())

        # Compare each pair of options
        for i, (key1, text1) in enumerate(options):
            for key2, text2 in options[i + 1 :]:
                similarity = self._calculate_similarity(text1, text2)
                if similarity > 0.7:  # > 70% similar
                    result.add_warning(
                        question_id=question.id,
                        message=f"Options {key1} and {key2} are very similar ({similarity:.0%})",
                        field_path=f"options.{key1}",
                        suggestion=f"Make options {key1} and {key2} more distinct",
                    )

        return result

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts (0-1).

        Simple word overlap metric:
        similarity = (shared words) / (total unique words)
        """
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        if not words1 or not words2:
            return 0.0

        shared = words1 & words2
        total = words1 | words2

        return len(shared) / len(total)


# ============================================================================
# Content Validator Registry
# ============================================================================


class ContentValidatorRegistry:
    """
    Registry of all Layer 2 content validators.

    Usage:
        registry = ContentValidatorRegistry()
        result = registry.validate_all(questions)
    """

    def __init__(self):
        self.validators: List[BaseValidator] = [
            FeedbackQualityValidator(),
            GeneralFeedbackQualityValidator(),
            ProhibitedPhrasesValidator(),
            QuestionClarityValidator(),
            OptionDistinctivenessValidator(),
        ]

    def validate_all(self, questions: List[Question]) -> ValidationResult:
        """
        Run all content validators on questions.

        Args:
            questions: List of questions to validate

        Returns:
            Combined ValidationResult
        """
        result = ValidationResult(validation_layer="content", questions_validated=len(questions))

        for validator in self.validators:
            validator_result = validator.validate_questions(questions)
            result.merge(validator_result)

        return result
