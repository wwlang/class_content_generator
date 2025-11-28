"""
Cultural Sensitivity and ESL Appropriateness Validator

Validates that content is culturally appropriate for Vietnamese students
and uses language accessible to ESL learners.
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


class CulturalSensitivityValidator(BaseValidator):
    """Validates cultural sensitivity and ESL appropriateness."""

    @property
    def name(self) -> str:
        return "Cultural Sensitivity & ESL"

    @property
    def description(self) -> str:
        return "Checks content for cultural appropriateness and ESL-friendly language"

    # Potentially problematic patterns for ESL students
    COMPLEX_IDIOMS = [
        "hit the ground running", "move the needle", "boil the ocean",
        "low-hanging fruit", "deep dive", "circle back", "touch base",
        "ballpark figure", "back to square one", "bite the bullet",
        "break the ice", "cut corners", "get the ball rolling",
        "in the loop", "on the same page", "think outside the box",
        "up in the air", "wrap your head around", "at the end of the day"
    ]

    # Culture-specific references that may need context
    WESTERN_REFERENCES = [
        "Thanksgiving", "Super Bowl", "March Madness", "Fourth of July",
        "Christmas bonus", "Black Friday", "Labor Day weekend"
    ]

    def validate(self, course_path: Path, **kwargs) -> ValidationResult:
        """
        Validate cultural sensitivity and ESL appropriateness.

        Args:
            course_path: Path to course directory

        Returns:
            ValidationResult with cultural/ESL issues
        """
        start_time = time.time()
        issues = []
        items_checked = 0

        weeks = self._find_weeks(course_path)

        for week_num in weeks:
            week_path = self._get_week_path(course_path, week_num)

            for file_name in ['lecture-content.md', 'tutorial-content.md', 'quiz-questions.md']:
                file_path = week_path / file_name
                if not file_path.exists():
                    continue

                content = self._read_file(file_path)
                if not content:
                    continue

                items_checked += 1

                # Quick pattern-based checks
                pattern_issues = self._quick_pattern_check(content, week_num, file_name)
                issues.extend(pattern_issues)

                # AI-powered cultural analysis (sample content to save API calls)
                if file_name == 'lecture-content.md':
                    ai_issues = self._ai_cultural_check(content, week_num)
                    issues.extend(ai_issues)

        duration = time.time() - start_time
        passed = not any(i.severity == IssueSeverity.CRITICAL for i in issues)

        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            issues=issues,
            summary=f"Checked {items_checked} files for cultural sensitivity and ESL appropriateness",
            duration_seconds=duration,
            items_checked=items_checked
        )

    def _quick_pattern_check(
        self,
        content: str,
        week_num: int,
        file_name: str
    ) -> List[ValidationIssue]:
        """Quick pattern-based checks for common issues."""
        issues = []
        content_lower = content.lower()

        # Check for complex idioms
        for idiom in self.COMPLEX_IDIOMS:
            if idiom.lower() in content_lower:
                issues.append(ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.SUGGESTION,
                    message=f"Business idiom '{idiom}' may be unfamiliar to ESL students",
                    location=f"Week {week_num} > {file_name}",
                    suggestion=f"Consider adding a brief explanation or using clearer phrasing"
                ))

        # Check for culture-specific references
        for ref in self.WESTERN_REFERENCES:
            if ref.lower() in content_lower:
                issues.append(ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.WARNING,
                    message=f"Culture-specific reference '{ref}' may need context for Vietnamese students",
                    location=f"Week {week_num} > {file_name}",
                    suggestion=f"Add brief explanation or use a more universal example"
                ))

        # Check for very long sentences (ESL readability)
        sentences = re.split(r'[.!?]+', content)
        long_sentences = [s for s in sentences if len(s.split()) > 40]
        if len(long_sentences) > 3:
            issues.append(ValidationIssue(
                validator=self.name,
                severity=IssueSeverity.SUGGESTION,
                message=f"Multiple very long sentences (40+ words) may challenge ESL readers",
                location=f"Week {week_num} > {file_name}",
                suggestion="Consider breaking complex sentences into shorter, clearer statements"
            ))

        # Check for passive voice density (harder for ESL)
        passive_patterns = re.findall(r'\b(was|were|is|are|been|being)\s+\w+ed\b', content)
        if len(passive_patterns) > 20:
            issues.append(ValidationIssue(
                validator=self.name,
                severity=IssueSeverity.SUGGESTION,
                message=f"High passive voice usage ({len(passive_patterns)} instances)",
                location=f"Week {week_num} > {file_name}",
                suggestion="Consider using more active voice for clarity"
            ))

        return issues

    def _ai_cultural_check(
        self,
        content: str,
        week_num: int
    ) -> List[ValidationIssue]:
        """Use Claude for deeper cultural sensitivity analysis."""
        issues = []

        # Sample content to reduce API costs
        sample = content[:4000] if len(content) > 4000 else content

        prompt = f"""You are an expert in cross-cultural education and ESL pedagogy.

Analyze this university lecture content for cultural sensitivity and ESL appropriateness.
The students are Vietnamese, studying business communication in English.

**Content (Week {week_num}):**
{sample}

**Check for these issues:**

1. **CULTURAL ASSUMPTIONS**: Western business norms presented as universal
   - Direct communication styles vs. indirect (face-saving) cultures
   - Assumptions about hierarchy, age respect, collectivism
   - US/UK-centric examples without Vietnamese context

2. **ESL ACCESSIBILITY**: Language complexity barriers
   - Unnecessarily complex vocabulary when simpler words exist
   - Unexplained jargon or technical terms
   - Idioms or slang without context

3. **EXAMPLE DIVERSITY**: Representation in scenarios
   - All Western names/companies in examples
   - No Asian business context
   - Stereotypical portrayals

4. **IMPLICIT BIAS**: Unintentional biases
   - Gendered language or role assumptions
   - Age-related stereotypes
   - Socioeconomic assumptions

**Respond ONLY if you find significant issues. Format:**

ISSUE_TYPE: [CULTURAL_ASSUMPTION/ESL_BARRIER/DIVERSITY_GAP/IMPLICIT_BIAS]
SEVERITY: [HIGH/MEDIUM/LOW]
LOCATION: [quote the problematic text, max 50 words]
PROBLEM: [1 sentence explanation]
SUGGESTION: [specific fix]

If content is generally appropriate, respond with: NO_SIGNIFICANT_ISSUES

List all issues found (or NO_SIGNIFICANT_ISSUES):"""

        try:
            response = self._call_claude(prompt, max_tokens=1000)

            if "NO_SIGNIFICANT_ISSUES" in response:
                return issues

            # Parse issues from response
            pattern = r'ISSUE_TYPE:\s*(CULTURAL_ASSUMPTION|ESL_BARRIER|DIVERSITY_GAP|IMPLICIT_BIAS)\s*\nSEVERITY:\s*(HIGH|MEDIUM|LOW)\s*\nLOCATION:\s*(.+?)\s*\nPROBLEM:\s*(.+?)\s*\nSUGGESTION:\s*(.+?)(?=\n\nISSUE_TYPE:|$)'

            for match in re.finditer(pattern, response, re.DOTALL):
                issue_type = match.group(1)
                severity_str = match.group(2)
                location = match.group(3).strip()
                problem = match.group(4).strip()
                suggestion = match.group(5).strip()

                # Map severity
                severity_map = {
                    "HIGH": IssueSeverity.WARNING,
                    "MEDIUM": IssueSeverity.SUGGESTION,
                    "LOW": IssueSeverity.INFO
                }
                severity = severity_map.get(severity_str, IssueSeverity.SUGGESTION)

                issues.append(ValidationIssue(
                    validator=self.name,
                    severity=severity,
                    message=f"{issue_type.replace('_', ' ').title()}: {problem}",
                    location=f"Week {week_num} > lecture-content.md",
                    context=location[:150],
                    suggestion=suggestion,
                    metadata={
                        'issue_type': issue_type,
                        'original_severity': severity_str
                    }
                ))

        except Exception as e:
            issues.append(ValidationIssue(
                validator=self.name,
                severity=IssueSeverity.INFO,
                message=f"Could not complete cultural analysis for Week {week_num}: {str(e)}",
                location=f"Week {week_num}"
            ))

        return issues
