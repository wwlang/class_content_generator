"""
Structured quiz parser using YAML frontmatter.

This parser uses python-frontmatter to parse YAML metadata and Pydantic
schemas for validation. It eliminates complex regex parsing entirely.

Version: 2.0
Specification: docs/QUIZ-FORMAT-V2-SPEC.md
"""

from pathlib import Path
from typing import List, Union
import frontmatter
from pydantic import ValidationError

from ..schemas.quiz_schema import (
    BloomLevel,
    QuestionType,
    QuizDocumentSchema,
    MultipleChoiceQuestionSchema,
    TrueFalseQuestionSchema,
    MatchingQuestionSchema,
)
from ..models.question import Question, QuestionType as ModelQuestionType, BloomLevel as ModelBloomLevel


class ParseError(Exception):
    """Raised when quiz file parsing fails."""

    pass


class StructuredQuizParser:
    """
    Parse quiz questions from YAML frontmatter format.

    Uses python-frontmatter for YAML parsing and Pydantic for validation.
    No regex required - structure is explicit and machine-parseable.

    Example usage:
        parser = StructuredQuizParser()
        questions = parser.parse_file(Path("quiz-questions.md"))
    """

    def parse_file(self, file_path: Path) -> List[Question]:
        """
        Parse quiz questions from YAML frontmatter file.

        Args:
            file_path: Path to quiz questions file

        Returns:
            List of Question objects

        Raises:
            ParseError: If file cannot be parsed or validation fails
        """
        if not file_path.exists():
            raise ParseError(f"File not found: {file_path}")

        try:
            # Parse YAML frontmatter
            with open(file_path, "r", encoding="utf-8") as f:
                post = frontmatter.load(f)

            # Validate against Pydantic schema
            try:
                quiz_doc = QuizDocumentSchema(**post.metadata)
            except ValidationError as e:
                raise ParseError(
                    f"Validation failed for {file_path}:\n{self._format_validation_error(e)}"
                )

            # Convert schemas to domain Question objects
            questions = []
            for question_schema in quiz_doc.questions:
                question = self._schema_to_question(question_schema, quiz_doc.metadata)
                questions.append(question)

            return questions

        except Exception as e:
            if "frontmatter" in str(type(e)).lower():
                raise ParseError(f"Failed to parse YAML frontmatter in {file_path}: {e}")
            raise ParseError(f"Unexpected error parsing {file_path}: {e}")

    def _schema_to_question(
        self,
        schema: Union[
            MultipleChoiceQuestionSchema,
            TrueFalseQuestionSchema,
            MatchingQuestionSchema,
        ],
        metadata,
    ) -> Question:
        """
        Convert Pydantic schema to domain Question object.

        Args:
            schema: Validated question schema
            metadata: Document metadata

        Returns:
            Question domain object
        """
        # Common fields
        question = Question(
            id=schema.id,
            question_type=self._convert_question_type(schema.type),
            bloom_level=ModelBloomLevel.from_string(schema.bloom_level.value),
            topic=schema.topic,
            question_text=schema.question,
            week=metadata.week,
            general_feedback=schema.general_feedback,
            prepares_for=metadata.prepares_for,
            options={},  # Initialize empty, populated per type
            correct_answer="",  # Initialize empty, populated per type
            feedback={},  # Initialize empty, populated per type
        )

        # Type-specific fields
        if isinstance(schema, MultipleChoiceQuestionSchema):
            question.options = {opt.key: opt.text for opt in schema.options}
            question.option_feedback = {opt.key: opt.feedback for opt in schema.options}
            question.correct_answer = next(
                opt.key for opt in schema.options if opt.correct
            )

        elif isinstance(schema, TrueFalseQuestionSchema):
            question.correct_answer = str(schema.correct_answer).upper()  # "TRUE" or "FALSE"
            question.true_feedback = schema.feedback.if_true
            question.false_feedback = schema.feedback.if_false

        elif isinstance(schema, MatchingQuestionSchema):
            # Build items and matches dicts
            question.matching_items = {
                pair.item_key: pair.item for pair in schema.pairs
            }
            question.matching_matches = {
                pair.match_key: pair.match for pair in schema.pairs
            }
            question.correct_pairs = {
                pair.item_key: pair.match_key for pair in schema.pairs
            }
            question.pair_feedback = {
                f"{pair.item_key}-{pair.match_key}": pair.feedback
                for pair in schema.pairs
            }

        return question

    def _convert_question_type(self, schema_type: QuestionType) -> ModelQuestionType:
        """Convert schema QuestionType enum to domain model enum."""
        mapping = {
            QuestionType.MULTIPLE_CHOICE: ModelQuestionType.MULTIPLE_CHOICE,
            QuestionType.TRUE_FALSE: ModelQuestionType.TRUE_FALSE,
            QuestionType.MATCHING: ModelQuestionType.MATCHING,
        }
        return mapping[schema_type]

    def _format_validation_error(self, error: ValidationError) -> str:
        """
        Format Pydantic validation error for human readability.

        Args:
            error: Pydantic ValidationError

        Returns:
            Formatted error message
        """
        lines = []
        for err in error.errors():
            location = " -> ".join(str(loc) for loc in err["loc"])
            message = err["msg"]
            lines.append(f"  • {location}: {message}")

        return "\n".join(lines)


class StructuredQuizParserV2(StructuredQuizParser):
    """
    Alias for StructuredQuizParser with explicit v2.0 naming.

    Use this when you want to be explicit about using v2.0 format.
    """

    pass


def parse_quiz_file(file_path: Path) -> List[Question]:
    """
    Convenience function to parse quiz file.

    Args:
        file_path: Path to quiz questions file

    Returns:
        List of Question objects

    Raises:
        ParseError: If parsing fails
    """
    parser = StructuredQuizParser()
    return parser.parse_file(file_path)
