"""
Domain model for course assessments.

Assessments include portfolios, presentations, and projects with requirements,
rubrics, and scenarios.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

from .rubric import Rubric


class AssessmentType(Enum):
    """Types of assessments."""
    PORTFOLIO = "portfolio"
    PRESENTATION = "presentation"
    QUIZ = "quiz"
    PROJECT = "project"


@dataclass
class Scenario:
    """
    A scenario option for an assessment.

    Many assessments offer multiple scenario options for students to choose from.

    Attributes:
        title: Scenario title (e.g., "Option A: New Initiative Proposal")
        description: Detailed scenario description
        specific_requirements: Additional requirements specific to this scenario
    """
    title: str
    description: str
    specific_requirements: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Generate markdown representation of scenario."""
        lines = [f"**{self.title}**", "", self.description, ""]

        if self.specific_requirements:
            lines.append("**Specific Requirements:**")
            for req in self.specific_requirements:
                lines.append(f"- {req}")
            lines.append("")

        return "\n".join(lines)

    def to_html(self) -> str:
        """Generate HTML representation of scenario."""
        html = f"""
<div class="scenario">
    <h4>{self.title}</h4>
    <p>{self.description}</p>
"""

        if self.specific_requirements:
            html += """
    <p><strong>Specific Requirements:</strong></p>
    <ul>
"""
            for req in self.specific_requirements:
                html += f"        <li>{req}</li>\n"
            html += "    </ul>\n"

        html += "</div>\n"
        return html


@dataclass
class Assessment:
    """
    A course assessment with requirements and rubric.

    Attributes:
        id: Unique identifier (slug format, e.g., "email-memo")
        name: Display name (e.g., "Email + Memo")
        type: Assessment type (portfolio, presentation, quiz, project)
        weight: Percentage of final grade (0.0-1.0, e.g., 0.10 for 10%)
        due_week: Week when assessment is due
        description: Overview of the assessment task
        requirements: List of requirement statements
        rubric: Grading rubric (optional for quizzes)
        scenarios: List of scenario options (optional)
        submission_format: File format and submission instructions
        learning_objectives: Learning objectives addressed
    """
    id: str
    name: str
    type: AssessmentType
    weight: float
    due_week: int
    description: str
    requirements: List[str] = field(default_factory=list)
    rubric: Optional[Rubric] = None
    scenarios: List[Scenario] = field(default_factory=list)
    submission_format: Optional[str] = None
    learning_objectives: List[str] = field(default_factory=list)

    def validate(self) -> List[str]:
        """
        Validate assessment.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Weight must be between 0 and 1
        if not (0.0 <= self.weight <= 1.0):
            errors.append(
                f"Assessment '{self.name}' weight must be 0.0-1.0 "
                f"(found {self.weight})"
            )

        # Due week must be valid (1-12 typically)
        if not (1 <= self.due_week <= 12):
            errors.append(
                f"Assessment '{self.name}' due week must be 1-12 "
                f"(found {self.due_week})"
            )

        # ID should be slug format
        if ' ' in self.id or self.id != self.id.lower():
            errors.append(
                f"Assessment ID '{self.id}' should be lowercase slug format "
                f"(e.g., 'email-memo')"
            )

        # Validate rubric if present
        if self.rubric:
            rubric_errors = self.rubric.validate()
            errors.extend(rubric_errors)

        # Non-quiz assessments should have requirements
        if self.type != AssessmentType.QUIZ and not self.requirements:
            errors.append(
                f"Assessment '{self.name}' should have requirements listed"
            )

        # Non-quiz assessments should have rubric
        if self.type != AssessmentType.QUIZ and not self.rubric:
            errors.append(
                f"Assessment '{self.name}' should have a rubric"
            )

        return errors

    def is_valid(self) -> bool:
        """Quick check if assessment passes all validation rules."""
        return len(self.validate()) == 0

    def get_weight_percentage(self) -> str:
        """Get weight as percentage string (e.g., '10%')."""
        return f"{self.weight * 100:.0f}%"

    def add_requirement(self, requirement: str) -> None:
        """Add a requirement to the assessment."""
        if requirement.strip():
            self.requirements.append(requirement.strip())

    def add_scenario(self, scenario: Scenario) -> None:
        """Add a scenario option to the assessment."""
        self.scenarios.append(scenario)

    def get_scenario(self, title: str) -> Optional[Scenario]:
        """
        Get scenario by title (case-insensitive).

        Args:
            title: Scenario title to search for

        Returns:
            Matching scenario or None if not found
        """
        title_lower = title.lower()
        for scenario in self.scenarios:
            if title_lower in scenario.title.lower():
                return scenario
        return None

    def to_markdown_brief(self) -> str:
        """
        Generate markdown brief for this assessment.

        Returns:
            Complete markdown document suitable for student handout
        """
        lines = [
            f"# {self.name}",
            "",
            f"**Type:** {self.type.value.title()}  ",
            f"**Weight:** {self.get_weight_percentage()}  ",
            f"**Due:** Week {self.due_week}  ",
            "",
            "---",
            "",
            "## Overview",
            "",
            self.description,
            ""
        ]

        # Learning objectives
        if self.learning_objectives:
            lines.extend([
                "## Learning Objectives",
                "",
                "This assessment addresses the following learning objectives:",
                ""
            ])
            for obj in self.learning_objectives:
                lines.append(f"- {obj}")
            lines.append("")

        # Scenarios
        if self.scenarios:
            lines.extend([
                "## Scenario Options",
                "",
                "Choose ONE of the following scenarios:",
                ""
            ])
            for scenario in self.scenarios:
                lines.append(scenario.to_markdown())

        # Requirements
        if self.requirements:
            lines.extend([
                "## Requirements",
                ""
            ])
            for req in self.requirements:
                # Convert checkbox format if present
                if req.strip().startswith("[ ]"):
                    lines.append(f"- {req[4:]}")
                elif req.strip().startswith("-"):
                    lines.append(req)
                else:
                    lines.append(f"- {req}")
            lines.append("")

        # Submission format
        if self.submission_format:
            lines.extend([
                "## Submission",
                "",
                self.submission_format,
                ""
            ])

        # Rubric
        if self.rubric:
            lines.extend([
                "",
                self.rubric.to_markdown_table(),
                ""
            ])

        return "\n".join(lines)

    def to_html_brief(self, course_code: Optional[str] = None) -> str:
        """
        Generate HTML brief for this assessment.

        Args:
            course_code: Optional course code for header

        Returns:
            Complete HTML document suitable for PDF export
        """
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        @page { size: A4; margin: 2cm; }
        body {
            font-family: 'Calibri', 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
        }
        .header {
            border-bottom: 3px solid #003E7E;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        h1 {
            color: #003E7E;
            margin-bottom: 5px;
        }
        .metadata {
            color: #666;
            font-size: 14px;
        }
        h2 {
            color: #003E7E;
            border-bottom: 2px solid #E6E6E6;
            padding-bottom: 5px;
            margin-top: 25px;
        }
        h3, h4 {
            color: #333;
        }
        ul, ol {
            padding-left: 25px;
        }
        li {
            margin-bottom: 8px;
        }
        .scenario {
            background: #F5F5F5;
            padding: 15px;
            margin: 15px 0;
            border-left: 4px solid #003E7E;
        }
        .rubric-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        .rubric-table th {
            background: #003E7E;
            color: white;
            padding: 10px;
            text-align: left;
            font-size: 12px;
        }
        .rubric-table td {
            border: 1px solid #DDD;
            padding: 10px;
            font-size: 11px;
            vertical-align: top;
        }
        .rubric-table tr:nth-child(even) {
            background: #F9F9F9;
        }
    </style>
</head>
<body>
"""

        # Header
        html += f"""
    <div class="header">
        <h1>{self.name}</h1>
        <p class="metadata">
"""
        if course_code:
            html += f"            {course_code} | "
        html += f"""Weight: {self.get_weight_percentage()} | Due: Week {self.due_week} | Type: {self.type.value.title()}
        </p>
    </div>
"""

        # Overview
        html += f"""
    <h2>Overview</h2>
    <p>{self.description}</p>
"""

        # Learning objectives
        if self.learning_objectives:
            html += """
    <h2>Learning Objectives</h2>
    <p>This assessment addresses the following learning objectives:</p>
    <ul>
"""
            for obj in self.learning_objectives:
                html += f"        <li>{obj}</li>\n"
            html += "    </ul>\n"

        # Scenarios
        if self.scenarios:
            html += """
    <h2>Scenario Options</h2>
    <p>Choose ONE of the following scenarios:</p>
"""
            for scenario in self.scenarios:
                html += scenario.to_html()

        # Requirements
        if self.requirements:
            html += """
    <h2>Requirements</h2>
    <ul>
"""
            for req in self.requirements:
                # Strip checkbox format if present
                clean_req = req.replace("[ ]", "").replace("- ", "").strip()
                html += f"        <li>{clean_req}</li>\n"
            html += "    </ul>\n"

        # Submission format
        if self.submission_format:
            html += f"""
    <h2>Submission</h2>
    <p>{self.submission_format}</p>
"""

        # Rubric
        if self.rubric:
            html += self.rubric.to_html_table()

        html += """
</body>
</html>
"""
        return html

    def to_dict(self) -> dict:
        """Convert assessment to dictionary representation."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type.value,
            'weight': self.weight,
            'weight_percentage': self.get_weight_percentage(),
            'due_week': self.due_week,
            'description': self.description,
            'requirements': self.requirements.copy(),
            'scenarios': [
                {
                    'title': s.title,
                    'description': s.description,
                    'specific_requirements': s.specific_requirements.copy()
                }
                for s in self.scenarios
            ],
            'submission_format': self.submission_format,
            'learning_objectives': self.learning_objectives.copy(),
            'rubric': self.rubric.to_dict() if self.rubric else None,
            'is_valid': self.is_valid()
        }

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"Assessment({self.name}, {self.get_weight_percentage()}, Week {self.due_week})"

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return (
            f"Assessment(id='{self.id}', name='{self.name}', "
            f"type={self.type}, weight={self.weight})"
        )
