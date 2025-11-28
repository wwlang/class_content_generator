#!/usr/bin/env python3
"""
Terminology consistency analyzer.

Identifies terminology inconsistencies across weeks:
- Terms with multiple variations (e.g., "company culture" vs "organizational culture")
- Undefined jargon
- Missing definitions on first use
- Inconsistent capitalization
"""

from typing import List, Dict, Set
from collections import defaultdict
import re

from ..core_structures import CoherenceIssue, WeekContent, Term, TermUsage


class TerminologyAnalyzer:
    """Analyze terminology consistency across course."""

    def __init__(self, week_contents: List[WeekContent]):
        """
        Initialize analyzer.

        Args:
            week_contents: List of WeekContent objects from all weeks
        """
        self.week_contents = week_contents
        self.all_terms: Dict[str, List[Term]] = defaultdict(list)
        self._collect_terms()

    def _collect_terms(self):
        """Collect all terms from all weeks."""
        for week in self.week_contents:
            for term in week.terms:
                self.all_terms[term.normalized].append(term)

    def analyze(self) -> List[CoherenceIssue]:
        """
        Analyze terminology consistency.

        Returns:
            List of CoherenceIssue objects for terminology problems
        """
        issues = []

        # 1. Find term variations
        issues.extend(self._find_term_variations())

        # 2. Find undefined jargon
        issues.extend(self._find_undefined_jargon())

        # 3. Find missing first-use definitions
        issues.extend(self._find_missing_first_definitions())

        # 4. Find inconsistent capitalization
        issues.extend(self._find_capitalization_issues())

        return issues

    def _find_term_variations(self) -> List[CoherenceIssue]:
        """Find terms with multiple variations across weeks."""
        issues = []

        # Group terms by semantic similarity
        term_groups = self._group_similar_terms()

        for group_key, variants in term_groups.items():
            if len(variants) < 2:
                continue  # No variation issue

            # Get all weeks using any variant
            affected_weeks = set()
            variant_usage = {}

            for variant in variants:
                for term in self.all_terms[variant]:
                    affected_weeks.update([u.week for u in term.uses])
                    variant_usage[variant] = len(term.uses)

            # Determine canonical form (most frequently used)
            canonical = max(variant_usage.items(), key=lambda x: x[1])[0]
            other_variants = [v for v in variants if v != canonical]

            # Create issue
            issue = CoherenceIssue(
                issue_id=f"term-variation-{group_key}",
                issue_type="terminology_variation",
                quality_score=7,  # Important but not critical
                affected_weeks=sorted(affected_weeks),
                suggested_fix=f"Standardize to '{canonical}' (used {variant_usage[canonical]} times)",
                auto_apply_safe=True,  # Safe to auto-standardize
                category="terminology"
            )

            # Add details
            issue.details = {
                "canonical_form": canonical,
                "variants": other_variants,
                "usage_counts": variant_usage
            }

            issues.append(issue)

        return issues

    def _group_similar_terms(self) -> Dict[str, List[str]]:
        """
        Group semantically similar terms.

        Returns:
            Dict mapping group key to list of variant normalized forms
        """
        groups = defaultdict(list)

        # Common synonyms in business/education
        synonym_patterns = [
            # Company/Organization
            (r'\bcompany\b', r'\borganization\b', r'\bfirm\b'),
            (r'\bcompany culture\b', r'\borganizational culture\b', r'\bcorporate culture\b'),

            # Employee/Worker
            (r'\bemployee\b', r'\bworker\b', r'\bstaff\b'),

            # Manager/Leader
            (r'\bmanager\b', r'\bleader\b', r'\bsupervisor\b'),

            # Student/Learner
            (r'\bstudent\b', r'\blearner\b'),

            # Business/Enterprise
            (r'\bbusiness\b', r'\benterprise\b', r'\bcompany\b'),
        ]

        # Check each term against patterns
        for normalized_term in self.all_terms.keys():
            matched = False

            for pattern_group in synonym_patterns:
                # Check if term matches any pattern in group
                if any(re.search(p, normalized_term) for p in pattern_group):
                    # Use first pattern as group key
                    group_key = pattern_group[0].replace(r'\b', '')
                    groups[group_key].append(normalized_term)
                    matched = True
                    break

            # If no pattern match, term is its own group
            if not matched:
                groups[normalized_term].append(normalized_term)

        # Filter to only groups with variations
        return {k: v for k, v in groups.items() if len(v) > 1}

    def _find_undefined_jargon(self) -> List[CoherenceIssue]:
        """Find technical jargon that's never defined."""
        issues = []

        # Identify potential jargon (terms used but never defined)
        for normalized, term_list in self.all_terms.items():
            # Check if any usage includes a definition
            has_definition = any(
                any(u.is_definition for u in term.uses)
                for term in term_list
            )

            if not has_definition:
                # Check if it looks like jargon (capitalized, multi-word, or technical)
                first_term = term_list[0]

                if self._looks_like_jargon(first_term.text):
                    # Get all weeks using this term
                    affected_weeks = set()
                    for term in term_list:
                        affected_weeks.update([u.week for u in term.uses])

                    # Create issue
                    issue = CoherenceIssue(
                        issue_id=f"undefined-jargon-{normalized}",
                        issue_type="undefined_jargon",
                        quality_score=6,  # Medium importance
                        affected_weeks=sorted(affected_weeks),
                        suggested_fix=f"Add definition for '{first_term.text}' on first use (Week {min(affected_weeks)})",
                        auto_apply_safe=False,  # Needs manual definition
                        category="terminology"
                    )

                    issue.details = {
                        "term": first_term.text,
                        "first_use_week": min(affected_weeks),
                        "total_uses": sum(len(t.uses) for t in term_list)
                    }

                    issues.append(issue)

        return issues

    def _looks_like_jargon(self, term_text: str) -> bool:
        """Check if term looks like technical jargon."""
        # Multi-word terms with capitals
        if len(term_text.split()) > 1 and any(c.isupper() for c in term_text):
            return True

        # Common business/academic jargon patterns
        jargon_indicators = [
            'framework', 'model', 'theory', 'principle', 'approach',
            'strategy', 'methodology', 'paradigm', 'concept'
        ]

        return any(indicator in term_text.lower() for indicator in jargon_indicators)

    def _find_missing_first_definitions(self) -> List[CoherenceIssue]:
        """Find terms that should be defined on first use but aren't."""
        issues = []

        for normalized, term_list in self.all_terms.items():
            # Get first use
            first_uses = []
            for term in term_list:
                first_uses.extend(term.uses)

            if not first_uses:
                continue

            # Sort by week and line number
            first_uses.sort(key=lambda u: (u.week, u.line_number))
            first_use = first_uses[0]

            # Check if first use includes definition
            if not first_use.is_definition:
                # Check if this term should be defined
                term_text = term_list[0].text

                if self._should_define_on_first_use(term_text):
                    issue = CoherenceIssue(
                        issue_id=f"missing-first-def-{normalized}",
                        issue_type="missing_first_definition",
                        quality_score=5,  # Medium-low importance
                        affected_weeks=[first_use.week],
                        suggested_fix=f"Add definition for '{term_text}' in Week {first_use.week} when first introduced",
                        auto_apply_safe=False,  # Needs manual definition
                        category="terminology"
                    )

                    issue.details = {
                        "term": term_text,
                        "first_use_week": first_use.week,
                        "first_use_file": first_use.file,
                        "context": first_use.context
                    }

                    issues.append(issue)

        return issues

    def _should_define_on_first_use(self, term_text: str) -> bool:
        """Check if term should be defined on first use."""
        # Multi-word technical terms
        if len(term_text.split()) > 1:
            return True

        # Capitalized terms (proper nouns/frameworks)
        if term_text[0].isupper() and len(term_text) > 3:
            return True

        # Common terms that don't need definition
        common_terms = [
            'student', 'teacher', 'class', 'course', 'week',
            'assignment', 'quiz', 'exam', 'grade', 'skill'
        ]

        if term_text.lower() in common_terms:
            return False

        return False

    def _find_capitalization_issues(self) -> List[CoherenceIssue]:
        """Find inconsistent capitalization of the same term."""
        issues = []

        # Group terms by normalized form (case-insensitive)
        for normalized, term_list in self.all_terms.items():
            # Get all unique capitalizations
            capitalizations = defaultdict(int)

            for term in term_list:
                capitalizations[term.text] += len(term.uses)

            # If multiple capitalizations exist
            if len(capitalizations) > 1:
                # Determine canonical (most frequent)
                canonical = max(capitalizations.items(), key=lambda x: x[1])[0]
                variants = [k for k in capitalizations.keys() if k != canonical]

                # Get affected weeks
                affected_weeks = set()
                for term in term_list:
                    affected_weeks.update([u.week for u in term.uses])

                issue = CoherenceIssue(
                    issue_id=f"capitalization-{normalized}",
                    issue_type="inconsistent_capitalization",
                    quality_score=3,  # Low importance (cosmetic)
                    affected_weeks=sorted(affected_weeks),
                    suggested_fix=f"Standardize capitalization to '{canonical}'",
                    auto_apply_safe=True,  # Safe to auto-fix
                    category="terminology"
                )

                issue.details = {
                    "canonical": canonical,
                    "variants": variants,
                    "usage_counts": dict(capitalizations)
                }

                issues.append(issue)

        return issues
