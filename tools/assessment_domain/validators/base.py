"""
Base validator framework for quiz questions.

Provides severity-based validation with ERROR, WARNING, and INFO levels.
Validators are organized into 4 layers matching the validation pyramid.

Version: 2.0
Specification: docs/QUIZ-FORMAT-V2-SPEC.md
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
from ..models.question import Question


# ============================================================================
# Issue Severity Levels
# ============================================================================


class IssueSeverity(Enum):
    """Severity levels for validation issues."""

    ERROR = "error"  # Blocks export - must fix
    WARNING = "warning"  # Should fix but not blocking
    INFO = "info"  # Suggestion for improvement


# ============================================================================
# Validation Issue
# ============================================================================


@dataclass
class ValidationIssue:
    """
    Single validation issue found in a question.

    Attributes:
        question_id: ID of question with issue
        severity: ERROR, WARNING, or INFO
        category: Validation layer (format, content, pedagogical, export)
        message: Human-readable description of issue
        suggestion: Optional suggestion for fixing (default: None)
        field_path: Optional path to field with issue (default: None)
    """

    question_id: str
    severity: IssueSeverity
    category: str
    message: str
    suggestion: Optional[str] = None
    field_path: Optional[str] = None

    def __str__(self) -> str:
        """Human-readable string representation."""
        parts = [
            f"[{self.severity.value.upper()}]",
            f"[{self.category}]",
            f"{self.question_id}:",
            self.message,
        ]

        if self.field_path:
            parts.insert(3, f"({self.field_path})")

        result = " ".join(parts)

        if self.suggestion:
            result += f"\n  💡 Suggestion: {self.suggestion}"

        return result

    def is_blocking(self) -> bool:
        """Check if this issue blocks export."""
        return self.severity == IssueSeverity.ERROR


# ============================================================================
# Validation Result
# ============================================================================


@dataclass
class ValidationResult:
    """
    Result of validating one or more questions.

    Attributes:
        issues: List of validation issues found
        questions_validated: Number of questions validated
        validation_layer: Which validation layer ran (e.g., "format", "content")
    """

    issues: List[ValidationIssue] = field(default_factory=list)
    questions_validated: int = 0
    validation_layer: str = "unknown"

    def add_issue(self, issue: ValidationIssue) -> None:
        """Add a validation issue."""
        self.issues.append(issue)

    def add_error(
        self,
        question_id: str,
        message: str,
        field_path: Optional[str] = None,
        suggestion: Optional[str] = None,
    ) -> None:
        """Add an ERROR-level issue."""
        self.issues.append(
            ValidationIssue(
                question_id=question_id,
                severity=IssueSeverity.ERROR,
                category=self.validation_layer,
                message=message,
                suggestion=suggestion,
                field_path=field_path,
            )
        )

    def add_warning(
        self,
        question_id: str,
        message: str,
        field_path: Optional[str] = None,
        suggestion: Optional[str] = None,
    ) -> None:
        """Add a WARNING-level issue."""
        self.issues.append(
            ValidationIssue(
                question_id=question_id,
                severity=IssueSeverity.WARNING,
                category=self.validation_layer,
                message=message,
                suggestion=suggestion,
                field_path=field_path,
            )
        )

    def add_info(
        self,
        question_id: str,
        message: str,
        field_path: Optional[str] = None,
        suggestion: Optional[str] = None,
    ) -> None:
        """Add an INFO-level issue."""
        self.issues.append(
            ValidationIssue(
                question_id=question_id,
                severity=IssueSeverity.INFO,
                category=self.validation_layer,
                message=message,
                suggestion=suggestion,
                field_path=field_path,
            )
        )

    def has_errors(self) -> bool:
        """Check if there are any blocking errors."""
        return any(issue.is_blocking() for issue in self.issues)

    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return any(issue.severity == IssueSeverity.WARNING for issue in self.issues)

    def has_info(self) -> bool:
        """Check if there are any info messages."""
        return any(issue.severity == IssueSeverity.INFO for issue in self.issues)

    def get_errors(self) -> List[ValidationIssue]:
        """Get all ERROR-level issues."""
        return [i for i in self.issues if i.severity == IssueSeverity.ERROR]

    def get_warnings(self) -> List[ValidationIssue]:
        """Get all WARNING-level issues."""
        return [i for i in self.issues if i.severity == IssueSeverity.WARNING]

    def get_info(self) -> List[ValidationIssue]:
        """Get all INFO-level issues."""
        return [i for i in self.issues if i.severity == IssueSeverity.INFO]

    def merge(self, other: "ValidationResult") -> "ValidationResult":
        """
        Merge another validation result into this one.

        Args:
            other: Another ValidationResult to merge

        Returns:
            This ValidationResult (for chaining)
        """
        self.issues.extend(other.issues)
        self.questions_validated += other.questions_validated
        return self

    def is_valid(self) -> bool:
        """Check if validation passed (no blocking errors)."""
        return not self.has_errors()

    def summary(self) -> str:
        """Generate summary string."""
        error_count = len(self.get_errors())
        warning_count = len(self.get_warnings())
        info_count = len(self.get_info())

        parts = [f"Validated {self.questions_validated} questions"]

        if error_count > 0:
            parts.append(f"❌ {error_count} errors")
        if warning_count > 0:
            parts.append(f"⚠️  {warning_count} warnings")
        if info_count > 0:
            parts.append(f"ℹ️  {info_count} suggestions")

        if error_count == 0 and warning_count == 0:
            parts.append("✅ All checks passed")

        return " | ".join(parts)

    def __str__(self) -> str:
        """Human-readable string representation."""
        lines = [self.summary(), ""]

        # Group issues by severity
        for severity in [IssueSeverity.ERROR, IssueSeverity.WARNING, IssueSeverity.INFO]:
            severity_issues = [i for i in self.issues if i.severity == severity]
            if severity_issues:
                lines.append(f"\n{severity.value.upper()}S:")
                for issue in severity_issues:
                    lines.append(f"  {issue}")

        return "\n".join(lines)


# ============================================================================
# Base Validator
# ============================================================================


class BaseValidator(ABC):
    """
    Abstract base class for all validators.

    Validators are organized into 4 layers:
    - Layer 1: Format validators (schema compliance)
    - Layer 2: Content validators (quality, clarity)
    - Layer 3: Pedagogical validators (Bloom alignment, distractors)
    - Layer 4: Export validators (GIFT syntax, round-trip)

    Each validator operates on a single question and returns a ValidationResult.
    """

    def __init__(self, layer_name: str):
        """
        Initialize validator.

        Args:
            layer_name: Name of validation layer (e.g., "format", "content")
        """
        self.layer_name = layer_name

    @abstractmethod
    def validate_question(self, question: Question) -> ValidationResult:
        """
        Validate a single question.

        Args:
            question: Question to validate

        Returns:
            ValidationResult with any issues found
        """
        pass

    def validate_questions(self, questions: List[Question]) -> ValidationResult:
        """
        Validate multiple questions.

        Args:
            questions: List of questions to validate

        Returns:
            Combined ValidationResult for all questions
        """
        result = ValidationResult(
            questions_validated=len(questions), validation_layer=self.layer_name
        )

        for question in questions:
            question_result = self.validate_question(question)
            result.merge(question_result)

        return result

    def create_result(self) -> ValidationResult:
        """
        Create a new ValidationResult for this validator's layer.

        Returns:
            Empty ValidationResult
        """
        return ValidationResult(validation_layer=self.layer_name, questions_validated=0)
