"""
Rubric Specificity Validator

Validates that rubric criteria are specific, measurable, and actionable.
Checks for vague language and ensures students can understand expectations.
"""

import re
import time
from pathlib import Path
from typing import List, Dict

from .base import (
    BaseValidator,
    ValidationResult,
    ValidationIssue,
    IssueSeverity
)


class RubricValidator(BaseValidator):
    """Validates rubric criteria quality and specificity."""

    @property
    def name(self) -> str:
        return "Rubric Specificity"

    @property
    def description(self) -> str:
        return "Checks that rubric criteria are specific, measurable, and actionable"

    # Common vague phrases to flag
    VAGUE_PHRASES = [
        "appropriate", "adequate", "sufficient", "good", "excellent",
        "acceptable", "satisfactory", "reasonable", "proper", "correct",
        "well-written", "well-organized", "clear", "effective",
        "demonstrates understanding", "shows knowledge", "uses correctly"
    ]

    def validate(self, course_path: Path, **kwargs) -> ValidationResult:
        """
        Validate rubric quality in assessment handbook.

        Args:
            course_path: Path to course directory

        Returns:
            ValidationResult with rubric issues
        """
        start_time = time.time()
        issues = []

        # Load assessment handbook
        handbook_path = course_path / "assessment-handbook.md"
        handbook_content = self._read_file(handbook_path)

        if not handbook_content:
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                issues=[ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.CRITICAL,
                    message="Assessment Handbook not found",
                    location=str(handbook_path),
                    suggestion="Generate Assessment Handbook using /generate-handbook"
                )],
                summary="Handbook missing",
                duration_seconds=time.time() - start_time,
                items_checked=0
            )

        # Extract rubrics
        rubrics = self._extract_rubrics(handbook_content)

        if not rubrics:
            issues.append(ValidationIssue(
                validator=self.name,
                severity=IssueSeverity.WARNING,
                message="No rubric tables found in Assessment Handbook",
                location=str(handbook_path),
                suggestion="Add rubric tables to Assessment Handbook"
            ))
        else:
            # Validate each rubric
            for rubric in rubrics:
                rubric_issues = self._validate_rubric(rubric)
                issues.extend(rubric_issues)

        duration = time.time() - start_time
        passed = not any(i.severity == IssueSeverity.CRITICAL for i in issues)

        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            issues=issues,
            summary=f"Checked {len(rubrics)} rubrics for specificity",
            duration_seconds=duration,
            items_checked=len(rubrics)
        )

    def _extract_rubrics(self, handbook_content: str) -> List[Dict]:
        """Extract rubric information from handbook."""
        rubrics = []

        # Find rubric sections (### [Name] Rubric)
        rubric_sections = re.finditer(
            r'###\s+(.+?Rubric)\s*\n(.*?)(?=\n###|\n##[^#]|\Z)',
            handbook_content,
            re.DOTALL
        )

        for match in rubric_sections:
            name = match.group(1).strip()
            content = match.group(2).strip()

            # Extract criteria from table
            criteria = self._extract_criteria(content)

            rubrics.append({
                'name': name,
                'content': content,
                'criteria': criteria
            })

        return rubrics

    def _extract_criteria(self, rubric_content: str) -> List[Dict]:
        """Extract criteria from rubric table."""
        criteria = []

        # Find table rows (looking for | pattern)
        table_match = re.search(r'\|.*\|(?:\n\|.*\|)+', rubric_content)
        if not table_match:
            return criteria

        table_text = table_match.group(0)
        rows = table_text.strip().split('\n')

        # Skip header and separator rows
        data_rows = [r for r in rows[2:] if r.strip() and not r.strip().startswith('|-')]

        for row in data_rows:
            cells = [c.strip() for c in row.split('|')[1:-1]]
            if len(cells) >= 2:
                criterion_name = cells[0].replace('**', '')
                descriptors = cells[1:]

                criteria.append({
                    'name': criterion_name,
                    'descriptors': descriptors
                })

        return criteria

    def _validate_rubric(self, rubric: Dict) -> List[ValidationIssue]:
        """Validate a single rubric using Claude."""
        issues = []

        # First, do quick pattern matching for obvious issues
        issues.extend(self._quick_pattern_check(rubric))

        # Then use Claude for deeper analysis
        if rubric['criteria']:
            prompt = self._build_validation_prompt(rubric)

            try:
                response = self._call_claude(prompt)
                issues.extend(self._parse_response(response, rubric))
            except Exception as e:
                issues.append(ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.WARNING,
                    message=f"Could not analyze rubric '{rubric['name']}': {str(e)}",
                    location=rubric['name']
                ))

        return issues

    def _quick_pattern_check(self, rubric: Dict) -> List[ValidationIssue]:
        """Quick pattern-based checks for common issues."""
        issues = []

        for criterion in rubric['criteria']:
            # Check for vague phrases in descriptors
            for i, descriptor in enumerate(criterion['descriptors']):
                descriptor_lower = descriptor.lower()

                for vague in self.VAGUE_PHRASES:
                    if vague in descriptor_lower:
                        # Check if it's qualified (e.g., "clear structure" vs just "clear")
                        if not re.search(rf'{vague}\s+\w+', descriptor_lower):
                            issues.append(ValidationIssue(
                                validator=self.name,
                                severity=IssueSeverity.WARNING,
                                message=f"Vague term '{vague}' in criterion '{criterion['name']}'",
                                location=f"{rubric['name']} > {criterion['name']}",
                                context=descriptor[:100],
                                suggestion=f"Replace '{vague}' with specific, measurable descriptor"
                            ))
                            break  # Only flag once per descriptor

        return issues

    def _build_validation_prompt(self, rubric: Dict) -> str:
        """Build prompt for rubric analysis."""
        criteria_text = ""
        for c in rubric['criteria']:
            criteria_text += f"\nCriterion: {c['name']}\n"
            for i, d in enumerate(c['descriptors']):
                level = ['Excellent', 'Good', 'Satisfactory', 'Needs Work', 'Failing'][i] if i < 5 else f"Level {i+1}"
                criteria_text += f"  {level}: {d[:200]}\n"

        return f"""You are an expert in assessment design and rubric development.

Analyze this rubric for specificity, measurability, and actionability.

**Rubric: {rubric['name']}**
{criteria_text}

**For each criterion, check:**

1. **SPECIFICITY**: Are descriptors specific or vague?
   - BAD: "Good organization" / "Clear writing"
   - GOOD: "Pyramid structure with main point in first paragraph"

2. **MEASURABILITY**: Can students objectively verify achievement?
   - BAD: "Demonstrates understanding"
   - GOOD: "Correctly identifies 3+ stakeholders using Freeman's categories"

3. **DIFFERENTIATION**: Are performance levels clearly distinguished?
   - BAD: Excellent="Very good", Good="Good", Satisfactory="Acceptable"
   - GOOD: Quantified differences (e.g., "0 errors" vs "1-2 errors" vs "3+ errors")

4. **ACTIONABILITY**: Do descriptors tell students HOW to succeed?
   - BAD: "Professional quality"
   - GOOD: "Uses formal register, avoids contractions, proper salutation"

**Respond with issues found (skip criteria that are fine):**

For each issue:
CRITERION: [name]
ISSUE: [VAGUE/NOT_MEASURABLE/POOR_DIFFERENTIATION/NOT_ACTIONABLE]
CURRENT: [problematic text]
SUGGESTED: [improved text]

List all issues found:"""

    def _parse_response(self, response: str, rubric: Dict) -> List[ValidationIssue]:
        """Parse Claude's rubric analysis."""
        issues = []

        # Pattern to extract issues
        pattern = r'CRITERION:\s*(.+?)\s*\nISSUE:\s*(VAGUE|NOT_MEASURABLE|POOR_DIFFERENTIATION|NOT_ACTIONABLE)\s*\nCURRENT:\s*(.+?)\s*\nSUGGESTED:\s*(.+?)(?=\n\nCRITERION:|\Z)'

        for match in re.finditer(pattern, response, re.DOTALL):
            criterion = match.group(1).strip()
            issue_type = match.group(2).strip()
            current = match.group(3).strip()
            suggested = match.group(4).strip()

            # Determine severity based on issue type
            severity = IssueSeverity.WARNING
            if issue_type in ['NOT_MEASURABLE', 'POOR_DIFFERENTIATION']:
                severity = IssueSeverity.WARNING
            elif issue_type == 'VAGUE':
                severity = IssueSeverity.SUGGESTION

            issues.append(ValidationIssue(
                validator=self.name,
                severity=severity,
                message=f"{issue_type.replace('_', ' ').title()}: {criterion}",
                location=f"{rubric['name']} > {criterion}",
                context=current[:150],
                suggestion=suggested[:300],
                metadata={
                    'issue_type': issue_type,
                    'current_text': current,
                    'suggested_text': suggested
                }
            ))

        return issues
