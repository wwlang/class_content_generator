"""
Base Validator Framework

Provides common structures and interfaces for all content validators.
"""

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

import anthropic


class IssueSeverity(Enum):
    """Severity levels for validation issues."""
    CRITICAL = "critical"      # Must fix before use
    WARNING = "warning"        # Should fix, but usable
    SUGGESTION = "suggestion"  # Nice to have improvement
    INFO = "info"              # Informational note


@dataclass
class ValidationIssue:
    """A single validation issue found in content."""
    validator: str              # Which validator found this
    severity: IssueSeverity
    message: str                # Human-readable description
    location: str               # File path or "Week X > Section"
    line_number: Optional[int] = None
    suggestion: Optional[str] = None  # How to fix
    context: Optional[str] = None     # Surrounding content
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'validator': self.validator,
            'severity': self.severity.value,
            'message': self.message,
            'location': self.location,
            'line_number': self.line_number,
            'suggestion': self.suggestion,
            'context': self.context,
            'metadata': self.metadata
        }


@dataclass
class ValidationResult:
    """Result from a single validator."""
    validator_name: str
    passed: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    summary: str = ""
    duration_seconds: float = 0.0
    items_checked: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == IssueSeverity.CRITICAL)

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == IssueSeverity.WARNING)

    @property
    def suggestion_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == IssueSeverity.SUGGESTION)


@dataclass
class ValidationReport:
    """Complete validation report for a course."""
    course_code: str
    timestamp: datetime
    results: List[ValidationResult] = field(default_factory=list)
    overall_passed: bool = True

    def add_result(self, result: ValidationResult):
        """Add a validator result to the report."""
        self.results.append(result)
        if result.critical_count > 0:
            self.overall_passed = False

    @property
    def total_issues(self) -> int:
        return sum(len(r.issues) for r in self.results)

    @property
    def total_critical(self) -> int:
        return sum(r.critical_count for r in self.results)

    @property
    def total_warnings(self) -> int:
        return sum(r.warning_count for r in self.results)

    @property
    def total_duration(self) -> float:
        return sum(r.duration_seconds for r in self.results)

    def to_markdown(self) -> str:
        """Generate markdown report."""
        lines = [
            f"# Content Validation Report: {self.course_code}",
            f"",
            f"**Generated:** {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Status:** {'PASSED' if self.overall_passed else 'FAILED'}",
            f"",
            f"## Summary",
            f"",
            f"| Metric | Count |",
            f"|--------|-------|",
            f"| Total Issues | {self.total_issues} |",
            f"| Critical | {self.total_critical} |",
            f"| Warnings | {self.total_warnings} |",
            f"| Validators Run | {len(self.results)} |",
            f"",
        ]

        for result in self.results:
            status = "PASS" if result.passed else "FAIL"
            lines.append(f"## {result.validator_name} [{status}]")
            lines.append(f"")
            lines.append(f"{result.summary}")
            lines.append(f"")
            lines.append(f"- Items checked: {result.items_checked}")
            lines.append(f"- Issues found: {len(result.issues)}")
            lines.append(f"- Duration: {result.duration_seconds:.2f}s")
            lines.append(f"")

            if result.issues:
                lines.append(f"### Issues")
                lines.append(f"")

                for issue in result.issues:
                    icon = {
                        IssueSeverity.CRITICAL: "🔴",
                        IssueSeverity.WARNING: "🟡",
                        IssueSeverity.SUGGESTION: "🔵",
                        IssueSeverity.INFO: "⚪"
                    }[issue.severity]

                    lines.append(f"#### {icon} {issue.severity.value.upper()}: {issue.message}")
                    lines.append(f"")
                    lines.append(f"**Location:** {issue.location}")
                    if issue.line_number:
                        lines.append(f" (line {issue.line_number})")
                    lines.append(f"")

                    if issue.context:
                        lines.append(f"**Context:**")
                        lines.append(f"```")
                        lines.append(issue.context[:300])
                        lines.append(f"```")
                        lines.append(f"")

                    if issue.suggestion:
                        lines.append(f"**Suggestion:** {issue.suggestion}")
                        lines.append(f"")

            lines.append(f"---")
            lines.append(f"")

        return "\n".join(lines)


class BaseValidator(ABC):
    """Base class for all content validators."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize validator with Anthropic API.

        Args:
            api_key: Anthropic API key (uses env var if not provided)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found")

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-5-20250929"

    @property
    @abstractmethod
    def name(self) -> str:
        """Validator display name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """What this validator checks."""
        pass

    @abstractmethod
    def validate(self, course_path: Path, **kwargs) -> ValidationResult:
        """
        Run validation on course content.

        Args:
            course_path: Path to course directory

        Returns:
            ValidationResult with issues found
        """
        pass

    def _call_claude(self, prompt: str, max_tokens: int = 4000) -> str:
        """
        Call Claude API with prompt.

        Args:
            prompt: The prompt to send
            max_tokens: Maximum response tokens

        Returns:
            Response text
        """
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def _read_file(self, path: Path) -> Optional[str]:
        """Safely read a file."""
        try:
            return path.read_text(encoding='utf-8')
        except Exception:
            return None

    def _find_weeks(self, course_path: Path) -> List[int]:
        """Find all week numbers in course."""
        weeks_path = course_path / "weeks"
        if not weeks_path.exists():
            return []

        weeks = []
        for d in weeks_path.iterdir():
            if d.is_dir() and d.name.startswith("week-"):
                try:
                    week_num = int(d.name.split("-")[1])
                    weeks.append(week_num)
                except (IndexError, ValueError):
                    continue

        return sorted(weeks)

    def _get_week_path(self, course_path: Path, week_num: int) -> Path:
        """Get path to a specific week directory."""
        return course_path / "weeks" / f"week-{week_num:02d}"
