#!/usr/bin/env python3
"""
Coherence reporter - Generates reports from analysis results.

Creates comprehensive reports with scored issues (Decision 3C).
"""

from typing import List, Dict
from pathlib import Path
from collections import defaultdict

from ..core_structures import CoherenceIssue, CoherenceReport


class CoherenceReporter:
    """Generate coherence analysis reports."""

    def __init__(self, issues: List[CoherenceIssue], course_code: str):
        """
        Initialize reporter.

        Args:
            issues: List of all coherence issues found
            course_code: Course code for identification
        """
        self.issues = issues
        self.course_code = course_code

    def generate_full_report(self) -> CoherenceReport:
        """
        Generate comprehensive report.

        Returns:
            CoherenceReport object
        """
        # Group issues by category
        issues_by_category = self._group_by_category()

        # Sort issues by priority (score descending)
        sorted_issues = sorted(self.issues, key=lambda x: x.quality_score, reverse=True)

        # Calculate statistics
        stats = self._calculate_statistics(issues_by_category)

        # Create report
        report = CoherenceReport(
            course_code=self.course_code,
            total_issues=len(self.issues),
            issues_by_category=issues_by_category,
            critical_issues=[i for i in sorted_issues if i.quality_score >= 9],
            important_issues=[i for i in sorted_issues if 7 <= i.quality_score < 9],
            medium_issues=[i for i in sorted_issues if 4 <= i.quality_score < 7],
            minor_issues=[i for i in sorted_issues if i.quality_score < 4],
            auto_fixable_count=sum(1 for i in self.issues if i.auto_apply_safe),
            manual_review_count=sum(1 for i in self.issues if not i.auto_apply_safe)
        )

        return report

    def save_full_report(self, output_path: Path) -> None:
        """
        Save comprehensive markdown report.

        Args:
            output_path: Path to save report
        """
        report = self.generate_full_report()
        markdown = self._format_full_markdown(report)

        output_path.write_text(markdown, encoding='utf-8')

    def save_summary_report(self, output_path: Path) -> None:
        """
        Save executive summary report.

        Args:
            output_path: Path to save summary
        """
        report = self.generate_full_report()
        markdown = self._format_summary_markdown(report)

        output_path.write_text(markdown, encoding='utf-8')

    def save_manual_todo(self, output_path: Path) -> None:
        """
        Save manual enhancement todo list.

        Args:
            output_path: Path to save todo list
        """
        manual_issues = [i for i in self.issues if not i.auto_apply_safe]
        manual_issues.sort(key=lambda x: x.quality_score, reverse=True)

        markdown = self._format_manual_todo(manual_issues)

        output_path.write_text(markdown, encoding='utf-8')

    def _group_by_category(self) -> Dict[str, List[CoherenceIssue]]:
        """Group issues by category."""
        grouped = defaultdict(list)

        for issue in self.issues:
            grouped[issue.category].append(issue)

        return dict(grouped)

    def _calculate_statistics(self, issues_by_category: Dict) -> Dict:
        """Calculate report statistics."""
        return {
            "total_issues": len(self.issues),
            "categories": list(issues_by_category.keys()),
            "avg_score": sum(i.quality_score for i in self.issues) / len(self.issues) if self.issues else 0,
            "critical_count": sum(1 for i in self.issues if i.quality_score >= 9),
            "auto_fixable": sum(1 for i in self.issues if i.auto_apply_safe)
        }

    def _format_full_markdown(self, report: CoherenceReport) -> str:
        """Format comprehensive markdown report."""
        md = f"""# Coherence Analysis Report: {self.course_code}

## Executive Summary

- **Total Issues Found:** {report.total_issues}
- **Critical (9-10):** {len(report.critical_issues)}
- **Important (7-8):** {len(report.important_issues)}
- **Medium (4-6):** {len(report.medium_issues)}
- **Minor (1-3):** {len(report.minor_issues)}

- **Auto-Fixable:** {report.auto_fixable_count} ({(report.auto_fixable_count/report.total_issues*100):.0f}%)
- **Manual Review:** {report.manual_review_count} ({(report.manual_review_count/report.total_issues*100):.0f}%)

## Issues by Category

"""
        for category, issues in report.issues_by_category.items():
            md += f"### {category.title()} ({len(issues)} issues)\n\n"

            # Sort by score
            issues.sort(key=lambda x: x.quality_score, reverse=True)

            for issue in issues:
                priority = issue.get_priority()
                auto = "✓ Auto" if issue.auto_apply_safe else "⚠ Manual"

                md += f"#### [{priority}] {issue.issue_type.replace('_', ' ').title()}\n\n"
                md += f"- **Score:** {issue.quality_score}/10\n"
                md += f"- **Weeks:** {', '.join(map(str, issue.affected_weeks))}\n"
                md += f"- **Fix Type:** {auto}\n"
                md += f"- **Suggested Fix:** {issue.suggested_fix}\n\n"

                if hasattr(issue, 'details') and issue.details:
                    md += f"**Details:**\n```\n{issue.details}\n```\n\n"

        md += "\n## Recommendations\n\n"
        md += "1. Address CRITICAL issues first (score 9-10)\n"
        md += "2. Apply auto-fixable changes with git backup\n"
        md += "3. Review IMPORTANT issues (score 7-8)\n"
        md += "4. Prioritize manual enhancements based on effort vs. impact\n\n"

        return md

    def _format_summary_markdown(self, report: CoherenceReport) -> str:
        """Format executive summary."""
        md = f"""# Coherence Analysis Summary: {self.course_code}

## Quick Stats

| Metric | Count |
|--------|-------|
| Total Issues | {report.total_issues} |
| Critical (9-10) | {len(report.critical_issues)} |
| Important (7-8) | {len(report.important_issues)} |
| Medium (4-6) | {len(report.medium_issues)} |
| Minor (1-3) | {len(report.minor_issues)} |
| Auto-Fixable | {report.auto_fixable_count} |
| Manual Review | {report.manual_review_count} |

## Top 10 Issues (by priority)

"""
        top_issues = sorted(self.issues, key=lambda x: x.quality_score, reverse=True)[:10]

        for i, issue in enumerate(top_issues, 1):
            md += f"{i}. **[{issue.quality_score}/10]** {issue.suggested_fix[:80]}...\n"

        md += f"\n## Next Steps\n\n"
        md += f"1. Review full report: `coherence-report.md`\n"
        md += f"2. Check manual todo list: `manual-enhancements-todo.md`\n"
        md += f"3. Apply auto-fixes with: `/enhance-coherence {self.course_code} --auto-apply`\n\n"

        return md

    def _format_manual_todo(self, manual_issues: List[CoherenceIssue]) -> str:
        """Format manual enhancement todo list."""
        md = f"""# Manual Enhancements TODO: {self.course_code}

These issues require manual review and cannot be auto-applied.
Issues are sorted by priority (quality score).

## Critical + Important (Score 7-10)

"""
        high_priority = [i for i in manual_issues if i.quality_score >= 7]

        if high_priority:
            for issue in high_priority:
                md += f"- [ ] **[{issue.quality_score}/10]** Week {', '.join(map(str, issue.affected_weeks))}: "
                md += f"{issue.suggested_fix}\n"
        else:
            md += "*No high-priority manual issues*\n"

        md += f"\n## Medium Priority (Score 4-6)\n\n"

        medium_priority = [i for i in manual_issues if 4 <= i.quality_score < 7]

        if medium_priority:
            for issue in medium_priority:
                md += f"- [ ] **[{issue.quality_score}/10]** Week {', '.join(map(str, issue.affected_weeks))}: "
                md += f"{issue.suggested_fix}\n"
        else:
            md += "*No medium-priority manual issues*\n"

        md += f"\n## Low Priority (Score 1-3)\n\n"

        low_priority = [i for i in manual_issues if i.quality_score < 4]

        if low_priority:
            for issue in low_priority:
                md += f"- [ ] **[{issue.quality_score}/10]** Week {', '.join(map(str, issue.affected_weeks))}: "
                md += f"{issue.suggested_fix}\n"
        else:
            md += "*No low-priority manual issues*\n"

        md += f"\n---\n\n"
        md += f"**Total manual issues:** {len(manual_issues)}\n"
        md += f"**High priority:** {len(high_priority)}\n"
        md += f"**Medium priority:** {len(medium_priority)}\n"
        md += f"**Low priority:** {len(low_priority)}\n"

        return md
