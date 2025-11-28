"""
Domain model for assessment rubrics.

Rubrics define grading criteria and performance levels for assessments.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RubricCriterion:
    """
    A single criterion in a rubric with performance level descriptors.

    Attributes:
        name: Criterion name (e.g., "Content & Strategy")
        weight: Percentage weight (0.0-1.0, e.g., 0.25 for 25%)
        excellent: Descriptor for excellent performance (94-100%)
        good: Descriptor for good performance (84-93%)
        satisfactory: Descriptor for satisfactory performance (74-83%)
        poor: Descriptor for poor performance (60-73%)
        failing: Descriptor for failing performance (<60%)
    """
    name: str
    weight: float
    excellent: str
    good: str
    satisfactory: str
    poor: str
    failing: str

    def validate(self) -> List[str]:
        """
        Validate criterion.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Weight must be between 0 and 1
        if not (0.0 <= self.weight <= 1.0):
            errors.append(
                f"Criterion '{self.name}' weight must be 0.0-1.0 "
                f"(found {self.weight})"
            )

        # All descriptors must be non-empty
        descriptors = {
            'excellent': self.excellent,
            'good': self.good,
            'satisfactory': self.satisfactory,
            'poor': self.poor,
            'failing': self.failing
        }

        for level, descriptor in descriptors.items():
            if not descriptor.strip():
                errors.append(
                    f"Criterion '{self.name}' has empty {level} descriptor"
                )

        return errors

    def to_markdown_row(self) -> str:
        """
        Convert criterion to markdown table row.

        Returns:
            Markdown formatted table row
        """
        weight_pct = f"{self.weight * 100:.0f}%"
        return (
            f"| {self.name} ({weight_pct}) | {self.excellent} | {self.good} | "
            f"{self.satisfactory} | {self.poor} | {self.failing} |"
        )

    def to_html_row(self) -> str:
        """
        Convert criterion to HTML table row.

        Returns:
            HTML formatted table row
        """
        weight_pct = f"{self.weight * 100:.0f}%"
        return f"""
<tr>
    <td><strong>{self.name}</strong><br><em>{weight_pct}</em></td>
    <td>{self.excellent}</td>
    <td>{self.good}</td>
    <td>{self.satisfactory}</td>
    <td>{self.poor}</td>
    <td>{self.failing}</td>
</tr>
"""

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"RubricCriterion({self.name}, {self.weight * 100:.0f}%)"


@dataclass
class Rubric:
    """
    A complete rubric with multiple criteria.

    Attributes:
        name: Rubric name (e.g., "Written Communication Rubric")
        criteria: List of rubric criteria
        description: Optional description of rubric purpose
    """
    name: str
    criteria: List[RubricCriterion] = field(default_factory=list)
    description: Optional[str] = None

    def validate(self) -> List[str]:
        """
        Validate rubric.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Must have at least one criterion
        if not self.criteria:
            errors.append(f"Rubric '{self.name}' has no criteria")

        # Validate each criterion
        for criterion in self.criteria:
            criterion_errors = criterion.validate()
            errors.extend(criterion_errors)

        # Weights should sum to approximately 1.0 (allow small float error)
        total_weight = sum(c.weight for c in self.criteria)
        if abs(total_weight - 1.0) > 0.01:
            errors.append(
                f"Rubric '{self.name}' weights sum to {total_weight:.2f}, "
                f"should sum to 1.0"
            )

        return errors

    def is_valid(self) -> bool:
        """Quick check if rubric passes all validation rules."""
        return len(self.validate()) == 0

    def get_criterion(self, name: str) -> Optional[RubricCriterion]:
        """
        Get criterion by name.

        Args:
            name: Criterion name (case-insensitive)

        Returns:
            Matching criterion or None if not found
        """
        name_lower = name.lower()
        for criterion in self.criteria:
            if criterion.name.lower() == name_lower:
                return criterion
        return None

    def add_criterion(self, criterion: RubricCriterion) -> None:
        """
        Add a criterion to the rubric.

        Args:
            criterion: Criterion to add

        Raises:
            ValueError: If criterion with same name already exists
        """
        existing = self.get_criterion(criterion.name)
        if existing:
            raise ValueError(
                f"Criterion '{criterion.name}' already exists in rubric '{self.name}'"
            )

        self.criteria.append(criterion)

    def to_markdown_table(self) -> str:
        """
        Generate markdown table representation.

        Returns:
            Complete markdown table with header and all criteria
        """
        lines = [
            f"## {self.name}",
            ""
        ]

        if self.description:
            lines.extend([self.description, ""])

        # Table header
        lines.extend([
            "| Criteria | Excellent (94-100%) | Good (84-93%) | Satisfactory (74-83%) | Poor (60-73%) | Failing (<60%) |",
            "|----------|---------------------|---------------|----------------------|---------------|----------------|"
        ])

        # Table rows
        for criterion in self.criteria:
            lines.append(criterion.to_markdown_row())

        return "\n".join(lines)

    def to_html_table(self) -> str:
        """
        Generate HTML table representation.

        Returns:
            Complete HTML table with styling
        """
        html = f"""
<div class="rubric">
    <h2>{self.name}</h2>
"""

        if self.description:
            html += f"    <p>{self.description}</p>\n"

        html += """
    <table class="rubric-table">
        <thead>
            <tr>
                <th>Criteria</th>
                <th>Excellent<br>(94-100%)</th>
                <th>Good<br>(84-93%)</th>
                <th>Satisfactory<br>(74-83%)</th>
                <th>Poor<br>(60-73%)</th>
                <th>Failing<br>(&lt;60%)</th>
            </tr>
        </thead>
        <tbody>
"""

        for criterion in self.criteria:
            html += criterion.to_html_row()

        html += """
        </tbody>
    </table>
</div>
"""

        return html

    def to_simplified(self, num_levels: int = 3) -> 'Rubric':
        """
        Create simplified rubric with fewer performance levels.

        Used for tutorial activities where full 5-level rubric is too detailed.

        Args:
            num_levels: Number of performance levels (2 or 3)

        Returns:
            Simplified rubric with reduced levels

        Raises:
            ValueError: If num_levels not 2 or 3
        """
        if num_levels not in (2, 3):
            raise ValueError("Simplified rubric must have 2 or 3 levels")

        simplified_criteria = []

        for criterion in self.criteria:
            if num_levels == 3:
                # Keep Excellent, Satisfactory, and Poor
                simplified = RubricCriterion(
                    name=criterion.name,
                    weight=criterion.weight,
                    excellent=criterion.excellent,
                    good=criterion.satisfactory,  # Map Good to Satisfactory
                    satisfactory=criterion.poor,   # Map Satisfactory to Poor
                    poor=criterion.failing,        # Map Poor to Failing
                    failing=""                     # Empty (unused)
                )
            else:  # num_levels == 2
                # Keep Excellent and Satisfactory
                simplified = RubricCriterion(
                    name=criterion.name,
                    weight=criterion.weight,
                    excellent=criterion.excellent,
                    good=criterion.satisfactory,
                    satisfactory="",
                    poor="",
                    failing=""
                )

            simplified_criteria.append(simplified)

        return Rubric(
            name=f"{self.name} (Simplified)",
            criteria=simplified_criteria,
            description="Simplified version for tutorial practice"
        )

    def to_dict(self) -> dict:
        """Convert rubric to dictionary representation."""
        return {
            'name': self.name,
            'description': self.description,
            'criteria': [
                {
                    'name': c.name,
                    'weight': c.weight,
                    'excellent': c.excellent,
                    'good': c.good,
                    'satisfactory': c.satisfactory,
                    'poor': c.poor,
                    'failing': c.failing
                }
                for c in self.criteria
            ],
            'total_weight': sum(c.weight for c in self.criteria),
            'is_valid': self.is_valid()
        }

    def __str__(self) -> str:
        """Human-readable string representation."""
        return f"Rubric({self.name}, {len(self.criteria)} criteria)"

    def __repr__(self) -> str:
        """Developer-friendly representation."""
        return f"Rubric(name='{self.name}', criteria={len(self.criteria)})"
