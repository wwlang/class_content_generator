"""
Tutorial-Assessment Alignment Validator

Validates that tutorial activities meaningfully prepare students for assessments.
Checks that tutorials practice specific assessment scenarios, use rubric criteria,
and produce portfolio-ready deliverables.
"""

import re
import time
from pathlib import Path
from typing import List, Dict, Optional

from .base import (
    BaseValidator,
    ValidationResult,
    ValidationIssue,
    IssueSeverity
)


class TutorialAssessmentValidator(BaseValidator):
    """Validates tutorial content aligns with assessment requirements."""

    @property
    def name(self) -> str:
        return "Tutorial-Assessment Alignment"

    @property
    def description(self) -> str:
        return "Checks that tutorials practice specific assessment skills with rubric-based success criteria"

    def validate(self, course_path: Path, **kwargs) -> ValidationResult:
        """
        Validate tutorial-assessment alignment across the course.

        Args:
            course_path: Path to course directory

        Returns:
            ValidationResult with alignment issues
        """
        start_time = time.time()
        issues = []
        items_checked = 0

        # Load assessment handbook for reference
        handbook_path = course_path / "assessment-handbook.md"
        handbook_content = self._read_file(handbook_path) if handbook_path.exists() else None

        if not handbook_content:
            issues.append(ValidationIssue(
                validator=self.name,
                severity=IssueSeverity.CRITICAL,
                message="Assessment Handbook not found - cannot validate tutorial alignment",
                location=str(handbook_path),
                suggestion="Generate Assessment Handbook before tutorials using /generate-handbook"
            ))
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                issues=issues,
                summary="Assessment Handbook missing",
                duration_seconds=time.time() - start_time,
                items_checked=0
            )

        # Extract assessment info from handbook
        assessments = self._extract_assessments(handbook_content)

        # Validate each week's tutorial
        weeks = self._find_weeks(course_path)

        for week_num in weeks:
            week_path = self._get_week_path(course_path, week_num)
            tutorial_path = week_path / "tutorial-content.md"

            if not tutorial_path.exists():
                continue

            tutorial_content = self._read_file(tutorial_path)
            if not tutorial_content:
                continue

            items_checked += 1
            week_issues = self._validate_tutorial(
                tutorial_content,
                week_num,
                assessments,
                handbook_content
            )
            issues.extend(week_issues)

        duration = time.time() - start_time
        passed = not any(i.severity == IssueSeverity.CRITICAL for i in issues)

        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            issues=issues,
            summary=f"Checked {items_checked} tutorials against {len(assessments)} assessments",
            duration_seconds=duration,
            items_checked=items_checked
        )

    def _extract_assessments(self, handbook_content: str) -> List[Dict]:
        """Extract assessment info from handbook."""
        assessments = []

        # Pattern to find assessment sections
        # Looking for: ### N. Assessment Name (weight%)
        pattern = r'###\s+\d+\.\s+(.+?)\s+\((\d+)%\)\s*\n\*\*Due:\*\*\s*(?:End of\s+)?Week\s+(\d+)'

        for match in re.finditer(pattern, handbook_content):
            name = match.group(1).strip()
            weight = int(match.group(2))
            due_week = int(match.group(3))

            assessments.append({
                'name': name,
                'weight': weight,
                'due_week': due_week
            })

        return assessments

    def _validate_tutorial(
        self,
        tutorial_content: str,
        week_num: int,
        assessments: List[Dict],
        handbook_content: str
    ) -> List[ValidationIssue]:
        """Validate a single tutorial against assessment requirements."""
        issues = []

        # Determine which assessment this week should prepare for
        target_assessment = self._find_target_assessment(week_num, assessments)

        if not target_assessment:
            # Week 11-12 might not have content weeks
            if week_num <= 10:
                issues.append(ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.WARNING,
                    message=f"Week {week_num} has no clear target assessment",
                    location=f"Week {week_num} tutorial",
                    suggestion="Ensure tutorial connects to an upcoming assessment"
                ))
            return issues

        # Use Claude to validate alignment
        prompt = self._build_alignment_prompt(
            tutorial_content,
            week_num,
            target_assessment,
            handbook_content
        )

        try:
            response = self._call_claude(prompt)
            issues.extend(self._parse_alignment_response(response, week_num, target_assessment))
        except Exception as e:
            issues.append(ValidationIssue(
                validator=self.name,
                severity=IssueSeverity.WARNING,
                message=f"Could not validate week {week_num}: {str(e)}",
                location=f"Week {week_num}"
            ))

        return issues

    def _find_target_assessment(self, week_num: int, assessments: List[Dict]) -> Optional[Dict]:
        """Find the assessment this week should prepare for."""
        # Find the next upcoming assessment
        upcoming = [a for a in assessments if a['due_week'] > week_num]

        if not upcoming:
            # After last assessment, focus on final presentation
            final = [a for a in assessments if 'presentation' in a['name'].lower()]
            return final[0] if final else None

        # Return the soonest upcoming assessment
        return min(upcoming, key=lambda a: a['due_week'])

    def _build_alignment_prompt(
        self,
        tutorial_content: str,
        week_num: int,
        target_assessment: Dict,
        handbook_content: str
    ) -> str:
        """Build prompt for alignment validation."""
        # Extract relevant handbook section
        assessment_name = target_assessment['name']

        return f"""You are an expert in curriculum alignment and assessment design.

Analyze whether this tutorial effectively prepares students for the target assessment.

**Target Assessment:**
- Name: {assessment_name}
- Due: Week {target_assessment['due_week']}
- Weight: {target_assessment['weight']}%

**Tutorial Content (Week {week_num}):**
```
{tutorial_content[:3000]}
```

**Validation Criteria:**

1. **Assessment Connection (CRITICAL):**
   - Is there an explicit "Assessment Connection" statement?
   - Does it reference the correct assessment?

2. **Activity Alignment (CRITICAL):**
   - Does the activity practice a skill/format from the assessment?
   - Is this a SCALED version (smaller than assessment, but same type)?
   - Is it generic or specifically tied to assessment scenarios?

3. **Success Criteria (WARNING):**
   - Are success criteria pulled from the assessment rubric?
   - Or are they generic/invented criteria?

4. **Deliverable Quality (WARNING):**
   - Is the deliverable concrete and portfolio-ready?
   - Can students use this work toward their assessment?

5. **Framework Application (SUGGESTION):**
   - Does the activity require applying lecture frameworks?
   - Are the frameworks appropriate for this assessment?

**Respond in this exact format:**

ASSESSMENT_CONNECTION: [PASS/FAIL]
Reason: [explanation]

ACTIVITY_ALIGNMENT: [PASS/FAIL]
Reason: [explanation]

SUCCESS_CRITERIA: [PASS/WARN]
Reason: [explanation]

DELIVERABLE_QUALITY: [PASS/WARN]
Reason: [explanation]

FRAMEWORK_APPLICATION: [PASS/SUGGEST]
Reason: [explanation]

OVERALL_SCORE: [1-10]

SUGGESTIONS:
- [suggestion 1]
- [suggestion 2]
- [suggestion 3 if needed]"""

    def _parse_alignment_response(
        self,
        response: str,
        week_num: int,
        target_assessment: Dict
    ) -> List[ValidationIssue]:
        """Parse Claude's alignment analysis into issues."""
        issues = []

        # Parse each criterion
        criteria_patterns = {
            'ASSESSMENT_CONNECTION': (IssueSeverity.CRITICAL, 'FAIL'),
            'ACTIVITY_ALIGNMENT': (IssueSeverity.CRITICAL, 'FAIL'),
            'SUCCESS_CRITERIA': (IssueSeverity.WARNING, 'WARN'),
            'DELIVERABLE_QUALITY': (IssueSeverity.WARNING, 'WARN'),
            'FRAMEWORK_APPLICATION': (IssueSeverity.SUGGESTION, 'SUGGEST')
        }

        for criterion, (severity, fail_marker) in criteria_patterns.items():
            pattern = rf'{criterion}:\s*(PASS|FAIL|WARN|SUGGEST)\s*\nReason:\s*(.+?)(?=\n\n|\n[A-Z])'
            match = re.search(pattern, response, re.DOTALL)

            if match:
                result = match.group(1).strip()
                reason = match.group(2).strip()

                if result in [fail_marker, 'FAIL']:
                    issues.append(ValidationIssue(
                        validator=self.name,
                        severity=severity,
                        message=f"{criterion.replace('_', ' ').title()}: {reason[:100]}",
                        location=f"Week {week_num} tutorial",
                        suggestion=reason if len(reason) < 200 else None,
                        metadata={
                            'criterion': criterion,
                            'target_assessment': target_assessment['name'],
                            'full_reason': reason
                        }
                    ))

        # Extract suggestions
        suggestions_match = re.search(r'SUGGESTIONS:\s*\n((?:- .+\n?)+)', response)
        if suggestions_match and issues:
            suggestions = suggestions_match.group(1).strip()
            # Add to first issue's suggestion if not set
            for issue in issues:
                if not issue.suggestion and suggestions:
                    issue.suggestion = suggestions[:300]
                    break

        return issues
