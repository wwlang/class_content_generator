#!/usr/bin/env python3
"""Cross-reference analyzer - Links concepts across weeks."""

from typing import List
from ..core_structures import CoherenceIssue, WeekContent


class CrossReferenceAnalyzer:
    """Analyze cross-references between weeks."""

    def __init__(self, week_contents: List[WeekContent]):
        self.week_contents = week_contents

    def analyze(self) -> List[CoherenceIssue]:
        """Analyze cross-reference opportunities."""
        issues = []
        issues.extend(self._find_callback_opportunities())
        issues.extend(self._find_forward_link_opportunities())
        return issues

    def _find_callback_opportunities(self) -> List[CoherenceIssue]:
        """Find opportunities to reference earlier concepts."""
        issues = []

        for week in self.week_contents[1:]:  # Skip first week
            # Check if week concepts relate to earlier weeks
            for concept in week.concepts:
                # Simple heuristic: check if concept name contains words from earlier concepts
                for earlier_week in self.week_contents[:week.week_number-1]:
                    for earlier_concept in earlier_week.concepts:
                        if self._concepts_related(concept.name, earlier_concept.name):
                            issue = CoherenceIssue(
                                issue_id=f"callback-{week.week_number}-to-{earlier_week.week_number}",
                                issue_type="missing_callback",
                                quality_score=6,
                                affected_weeks=[week.week_number, earlier_week.week_number],
                                suggested_fix=f"Add callback in Week {week.week_number} referencing "
                                            f"'{earlier_concept.name}' from Week {earlier_week.week_number}",
                                auto_apply_safe=False,
                                category="cross_reference"
                            )
                            issue.details = {
                                "current_concept": concept.name,
                                "earlier_concept": earlier_concept.name,
                                "current_week": week.week_number,
                                "earlier_week": earlier_week.week_number
                            }
                            issues.append(issue)
                            break  # One callback per concept is enough

        return issues[:10]  # Limit to top 10

    def _find_forward_link_opportunities(self) -> List[CoherenceIssue]:
        """Find opportunities to preview upcoming concepts."""
        issues = []

        for i, week in enumerate(self.week_contents[:-1]):  # Skip last week
            next_week = self.week_contents[i + 1]

            # Simple heuristic: suggest forward link if weeks are related
            if self._weeks_related(week, next_week):
                issue = CoherenceIssue(
                    issue_id=f"forward-link-{week.week_number}-to-{next_week.week_number}",
                    issue_type="missing_forward_link",
                    quality_score=5,
                    affected_weeks=[week.week_number, next_week.week_number],
                    suggested_fix=f"Add preview in Week {week.week_number} about upcoming "
                                f"'{next_week.topic}' in Week {next_week.week_number}",
                    auto_apply_safe=False,
                    category="cross_reference"
                )
                issue.details = {
                    "current_week": week.week_number,
                    "next_week": next_week.week_number,
                    "next_topic": next_week.topic
                }
                issues.append(issue)

        return issues

    def _concepts_related(self, concept1: str, concept2: str) -> bool:
        """Check if two concepts are related."""
        words1 = set(concept1.lower().split())
        words2 = set(concept2.lower().split())
        # Remove common words
        common_words = {'the', 'and', 'of', 'to', 'in', 'for', 'a', 'an'}
        words1 -= common_words
        words2 -= common_words
        # Check for overlap
        return len(words1 & words2) > 0

    def _weeks_related(self, week1: WeekContent, week2: WeekContent) -> bool:
        """Check if two weeks are thematically related."""
        # Simple heuristic: check if topics share words
        topic1_words = set(week1.topic.lower().split())
        topic2_words = set(week2.topic.lower().split())
        common_words = {'the', 'and', 'of', 'to', 'in', 'for', 'a', 'an', 'week'}
        topic1_words -= common_words
        topic2_words -= common_words
        return len(topic1_words & topic2_words) > 0
