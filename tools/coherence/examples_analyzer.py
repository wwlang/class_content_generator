#!/usr/bin/env python3
"""
Examples diversity analyzer.

Identifies example issues:
- Duplicate examples across weeks
- Insufficient Vietnamese context
- Domain concentration (too many examples from one industry)
- Missing cultural relevance
"""

from typing import List, Dict
from collections import defaultdict, Counter

from ..core_structures import CoherenceIssue, WeekContent, Example


class ExamplesAnalyzer:
    """Analyze example diversity and cultural relevance."""

    def __init__(self, week_contents: List[WeekContent]):
        self.week_contents = week_contents
        self.all_examples: List[Example] = []
        self._collect_examples()

    def _collect_examples(self):
        """Collect all examples from all weeks."""
        for week in self.week_contents:
            self.all_examples.extend(week.examples)

    def analyze(self) -> List[CoherenceIssue]:
        """Analyze example diversity."""
        issues = []
        issues.extend(self._find_duplicate_examples())
        issues.extend(self._find_vietnamese_gaps())
        issues.extend(self._find_domain_concentration())
        return issues

    def _find_duplicate_examples(self) -> List[CoherenceIssue]:
        """Find duplicate or very similar examples."""
        issues = []
        seen_companies = defaultdict(list)

        for example in self.all_examples:
            if example.company_name:
                seen_companies[example.company_name].append(example.week)

        # Find companies used multiple times
        for company, weeks in seen_companies.items():
            if len(weeks) > 1:
                issue = CoherenceIssue(
                    issue_id=f"duplicate-example-{company.lower().replace(' ', '-')}",
                    issue_type="duplicate_example",
                    quality_score=4,  # Low-medium - variety is nice but not critical
                    affected_weeks=sorted(set(weeks)),
                    suggested_fix=f"Replace duplicate '{company}' examples in some weeks with diverse examples",
                    auto_apply_safe=False,  # Needs content review
                    category="examples"
                )
                issue.details = {"company": company, "weeks": weeks, "count": len(weeks)}
                issues.append(issue)

        return issues

    def _find_vietnamese_gaps(self) -> List[CoherenceIssue]:
        """Find weeks lacking Vietnamese context."""
        issues = []

        for week in self.week_contents:
            vietnamese_examples = [e for e in week.examples if e.context == "vietnamese"]

            if not vietnamese_examples and week.examples:
                issue = CoherenceIssue(
                    issue_id=f"no-vietnamese-examples-week-{week.week_number}",
                    issue_type="missing_vietnamese_context",
                    quality_score=7,  # Important for Vietnamese students
                    affected_weeks=[week.week_number],
                    suggested_fix=f"Add Vietnamese company/context example to Week {week.week_number}",
                    auto_apply_safe=False,  # Needs content creation
                    category="examples"
                )
                issue.details = {
                    "week": week.week_number,
                    "total_examples": len(week.examples),
                    "vietnamese_examples": 0
                }
                issues.append(issue)

        return issues

    def _find_domain_concentration(self) -> List[CoherenceIssue]:
        """Find over-concentration in specific industries."""
        issues = []

        # Count examples by domain
        domain_counts = Counter(e.domain for e in self.all_examples if e.domain)

        total_examples = len(self.all_examples)
        if total_examples == 0:
            return issues

        # Check for over-concentration (>40% from one domain)
        for domain, count in domain_counts.most_common(3):
            percentage = (count / total_examples) * 100

            if percentage > 40:
                # Find affected weeks
                affected_weeks = list(set(
                    e.week for e in self.all_examples if e.domain == domain
                ))

                issue = CoherenceIssue(
                    issue_id=f"domain-concentration-{domain}",
                    issue_type="domain_concentration",
                    quality_score=5,  # Medium - diversity is good
                    affected_weeks=sorted(affected_weeks),
                    suggested_fix=f"Reduce {domain} examples ({percentage:.0f}%) and add diverse industry examples",
                    auto_apply_safe=False,  # Needs content review
                    category="examples"
                )
                issue.details = {
                    "domain": domain,
                    "count": count,
                    "percentage": round(percentage, 1),
                    "total_examples": total_examples
                }
                issues.append(issue)

        return issues
