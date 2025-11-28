#!/usr/bin/env python3
"""Citation formatting analyzer - Ensures APA 7th consistency."""

from typing import List
import re
from collections import defaultdict

from ..core_structures import CoherenceIssue, WeekContent, Citation


class CitationAnalyzer:
    """Analyze citation formatting consistency."""

    def __init__(self, week_contents: List[WeekContent]):
        self.week_contents = week_contents
        self.all_citations: List[Citation] = []
        self._collect_citations()

    def _collect_citations(self):
        """Collect all citations from all weeks."""
        for week in self.week_contents:
            self.all_citations.extend(week.citations)

    def analyze(self) -> List[CoherenceIssue]:
        """Analyze citation formatting."""
        issues = []
        issues.extend(self._find_non_apa_citations())
        issues.extend(self._find_duplicate_citations())
        issues.extend(self._find_inconsistent_formatting())
        return issues

    def _find_non_apa_citations(self) -> List[CoherenceIssue]:
        """Find citations not following APA 7th format."""
        issues = []

        for citation in self.all_citations:
            if not citation.is_apa_7th:
                issue = CoherenceIssue(
                    issue_id=f"non-apa-citation-week-{citation.week}",
                    issue_type="non_apa_citation",
                    quality_score=6,
                    affected_weeks=[citation.week],
                    suggested_fix=f"Convert citation to APA 7th format in Week {citation.week}: {citation.text[:50]}...",
                    auto_apply_safe=False,  # Needs manual formatting
                    category="citations"
                )
                issue.details = {
                    "citation_text": citation.text,
                    "week": citation.week,
                    "file": citation.file
                }
                issues.append(issue)

        return issues[:10]  # Limit to first 10

    def _find_duplicate_citations(self) -> List[CoherenceIssue]:
        """Find duplicate citations (same work cited multiple times)."""
        issues = []
        citations_by_author_year = defaultdict(list)

        for citation in self.all_citations:
            if citation.author and citation.year:
                key = f"{citation.author}_{citation.year}"
                citations_by_author_year[key].append(citation)

        # Find duplicates
        for key, cits in citations_by_author_year.items():
            if len(cits) > 1:
                weeks = [c.week for c in cits]

                issue = CoherenceIssue(
                    issue_id=f"duplicate-citation-{key}",
                    issue_type="duplicate_citation",
                    quality_score=3,  # Low - just informational
                    affected_weeks=sorted(set(weeks)),
                    suggested_fix=f"Citation '{cits[0].author} ({cits[0].year})' appears {len(cits)} times - ensure consistent formatting",
                    auto_apply_safe=True,  # Safe to standardize
                    category="citations"
                )
                issue.details = {
                    "author": cits[0].author,
                    "year": cits[0].year,
                    "count": len(cits),
                    "weeks": weeks
                }
                issues.append(issue)

        return issues

    def _find_inconsistent_formatting(self) -> List[CoherenceIssue]:
        """Find formatting inconsistencies in citations."""
        issues = []

        # Check for inline vs. full reference format consistency
        inline_count = sum(1 for c in self.all_citations if c.format_type == "inline")
        full_count = sum(1 for c in self.all_citations if c.format_type == "full")

        if inline_count > 0 and full_count > 0:
            # Both formats present - check if appropriate
            weeks_with_both = []

            for week in self.week_contents:
                week_cits = [c for c in week.citations]
                has_inline = any(c.format_type == "inline" for c in week_cits)
                has_full = any(c.format_type == "full" for c in week_cits)

                if has_inline and not has_full:
                    weeks_with_both.append(week.week_number)

            if weeks_with_both:
                issue = CoherenceIssue(
                    issue_id="missing-full-references",
                    issue_type="incomplete_citations",
                    quality_score=7,  # Important - incomplete citations
                    affected_weeks=weeks_with_both,
                    suggested_fix=f"Add full APA references for inline citations in weeks: {', '.join(map(str, weeks_with_both))}",
                    auto_apply_safe=False,  # Needs bibliographic info
                    category="citations"
                )
                issue.details = {
                    "weeks_missing_full_refs": weeks_with_both,
                    "inline_count": inline_count,
                    "full_count": full_count
                }
                issues.append(issue)

        return issues
