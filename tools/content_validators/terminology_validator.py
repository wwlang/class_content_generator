"""
Terminology Consistency Validator

Validates that the same terms are used consistently across all course content.
Detects variations, inconsistencies, and potential confusion.
"""

import re
import time
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import defaultdict

from .base import (
    BaseValidator,
    ValidationResult,
    ValidationIssue,
    IssueSeverity
)


class TerminologyValidator(BaseValidator):
    """Validates terminology consistency across course content."""

    @property
    def name(self) -> str:
        return "Terminology Consistency"

    @property
    def description(self) -> str:
        return "Checks that terms and concepts are used consistently across all weeks"

    def validate(self, course_path: Path, **kwargs) -> ValidationResult:
        """
        Validate terminology consistency across the course.

        Args:
            course_path: Path to course directory

        Returns:
            ValidationResult with inconsistency issues
        """
        start_time = time.time()
        issues = []

        # Collect all terms and their variations
        term_usage = self._collect_term_usage(course_path)

        # Identify inconsistencies
        inconsistencies = self._find_inconsistencies(term_usage)

        for term_group, variations in inconsistencies.items():
            if len(variations) > 1:
                # Use Claude to determine if these are truly inconsistent
                is_issue, suggestion = self._analyze_variations(term_group, variations)

                if is_issue:
                    var_summary = "; ".join([
                        f"'{v['term']}' (Week {v['week']}, {v['count']}x)"
                        for v in sorted(variations, key=lambda x: -x['count'])[:5]
                    ])

                    issues.append(ValidationIssue(
                        validator=self.name,
                        severity=IssueSeverity.WARNING,
                        message=f"Inconsistent terminology: {var_summary}",
                        location="Course-wide",
                        suggestion=suggestion,
                        metadata={
                            'term_group': term_group,
                            'variations': [v['term'] for v in variations]
                        }
                    ))

        duration = time.time() - start_time
        passed = not any(i.severity == IssueSeverity.CRITICAL for i in issues)

        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            issues=issues,
            summary=f"Analyzed {len(term_usage)} term groups for consistency",
            duration_seconds=duration,
            items_checked=len(term_usage)
        )

    def _collect_term_usage(self, course_path: Path) -> Dict[str, List[Dict]]:
        """
        Collect all bolded terms and their usage across weeks.

        Returns:
            Dict mapping normalized term to list of {term, week, file, count}
        """
        term_usage = defaultdict(list)
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

                # Extract bolded terms
                bolded = re.findall(r'\*\*([^*]+)\*\*', content)

                # Count occurrences
                term_counts = defaultdict(int)
                for term in bolded:
                    term = term.strip()
                    if len(term) > 2 and len(term) < 100:  # Filter very short/long
                        term_counts[term] += 1

                # Add to usage tracking
                for term, count in term_counts.items():
                    normalized = self._normalize_term(term)
                    term_usage[normalized].append({
                        'term': term,
                        'week': week_num,
                        'file': file_name,
                        'count': count
                    })

        return dict(term_usage)

    def _normalize_term(self, term: str) -> str:
        """Normalize term for grouping similar terms."""
        # Lowercase, remove extra spaces
        normalized = term.lower().strip()
        normalized = re.sub(r'\s+', ' ', normalized)

        # Remove common suffixes for grouping
        normalized = re.sub(r'(s|ing|ed|er|tion)$', '', normalized)

        # Remove punctuation
        normalized = re.sub(r'[.,;:!?\'"-]', '', normalized)

        return normalized

    def _find_inconsistencies(self, term_usage: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """
        Find terms with multiple variations.

        Returns:
            Dict of term groups with >1 distinct surface form
        """
        inconsistencies = {}

        for normalized, usages in term_usage.items():
            # Get unique surface forms
            surface_forms = {}
            for usage in usages:
                term = usage['term']
                if term not in surface_forms:
                    surface_forms[term] = {
                        'term': term,
                        'week': usage['week'],
                        'count': usage['count']
                    }
                else:
                    surface_forms[term]['count'] += usage['count']

            # Only flag if multiple distinct forms exist
            if len(surface_forms) > 1:
                # Check if these are actually different (not just capitalization)
                lower_forms = set(t.lower() for t in surface_forms.keys())
                if len(lower_forms) > 1:  # Actually different
                    inconsistencies[normalized] = list(surface_forms.values())

        return inconsistencies

    def _analyze_variations(
        self,
        term_group: str,
        variations: List[Dict]
    ) -> Tuple[bool, str]:
        """
        Use Claude to determine if variations are problematic.

        Returns:
            (is_issue, suggestion)
        """
        var_text = "\n".join([
            f"- '{v['term']}' (used {v['count']} times, first in Week {v['week']})"
            for v in variations
        ])

        prompt = f"""You are an expert in educational content consistency.

Analyze these term variations and determine if they represent a consistency issue.

**Term variations found:**
{var_text}

**Consider:**
1. Are these genuinely different terms that should be standardized?
2. Or are they acceptable variations (e.g., abbreviations, synonyms used intentionally)?
3. Could they cause student confusion?

**Respond in this format:**

IS_ISSUE: [YES/NO]
REASON: [1-2 sentence explanation]
RECOMMENDED_TERM: [the preferred term to use, or "N/A" if no issue]
SUGGESTION: [how to fix, or "None needed"]"""

        try:
            response = self._call_claude(prompt, max_tokens=500)

            is_issue = "IS_ISSUE: YES" in response
            suggestion_match = re.search(r'SUGGESTION:\s*(.+?)(?=\n|$)', response)
            suggestion = suggestion_match.group(1).strip() if suggestion_match else ""

            recommended_match = re.search(r'RECOMMENDED_TERM:\s*(.+?)(?=\n|$)', response)
            if recommended_match and recommended_match.group(1).strip() != "N/A":
                suggestion = f"Standardize to '{recommended_match.group(1).strip()}'. {suggestion}"

            return is_issue, suggestion

        except Exception:
            # Default to flagging if we can't analyze
            return True, "Review these term variations for consistency"
