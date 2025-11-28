#!/usr/bin/env python3
"""
Concept scaffolding analyzer.

Identifies scaffolding issues across weeks:
- Concepts used before being introduced
- Missing prerequisite concepts
- Weak forward references to upcoming concepts
- Concepts introduced too late
"""

from typing import List, Dict, Set, Tuple
from collections import defaultdict

from ..core_structures import CoherenceIssue, WeekContent, Concept, Term


class ScaffoldingAnalyzer:
    """Analyze concept scaffolding and dependencies."""

    def __init__(self, week_contents: List[WeekContent]):
        """
        Initialize analyzer.

        Args:
            week_contents: List of WeekContent objects from all weeks
        """
        self.week_contents = week_contents
        self.concept_introductions: Dict[str, int] = {}  # concept -> week introduced
        self._map_concept_introductions()

    def _map_concept_introductions(self):
        """Map when each concept is first introduced."""
        for week in self.week_contents:
            for concept in week.concepts:
                normalized_name = concept.name.lower().strip()

                if normalized_name not in self.concept_introductions:
                    self.concept_introductions[normalized_name] = concept.introduced_week

    def analyze(self) -> List[CoherenceIssue]:
        """
        Analyze concept scaffolding.

        Returns:
            List of CoherenceIssue objects for scaffolding problems
        """
        issues = []

        # 1. Find concepts used before introduction
        issues.extend(self._find_premature_usage())

        # 2. Find missing prerequisite concepts
        issues.extend(self._find_missing_prerequisites())

        # 3. Find weak forward references
        issues.extend(self._find_weak_forward_references())

        # 4. Find orphaned concepts (introduced but never used again)
        issues.extend(self._find_orphaned_concepts())

        return issues

    def _find_premature_usage(self) -> List[CoherenceIssue]:
        """Find concepts/terms used before they're properly introduced."""
        issues = []

        # Check each week's terms against concept introductions
        for week in self.week_contents:
            for term in week.terms:
                # Check if this term references a concept
                concept_name = self._term_to_concept(term.text)

                if concept_name and concept_name in self.concept_introductions:
                    introduced_week = self.concept_introductions[concept_name]

                    # Check if used before introduction
                    earliest_use = min(u.week for u in term.uses)

                    if earliest_use < introduced_week:
                        issue = CoherenceIssue(
                            issue_id=f"premature-use-{concept_name}-week-{earliest_use}",
                            issue_type="premature_concept_use",
                            quality_score=8,  # Important - confuses students
                            affected_weeks=[earliest_use, introduced_week],
                            suggested_fix=f"Add brief introduction to '{term.text}' in Week {earliest_use}, "
                                        f"or move full introduction from Week {introduced_week} to Week {earliest_use}",
                            auto_apply_safe=False,  # Needs manual review
                            category="scaffolding"
                        )

                        issue.details = {
                            "concept": term.text,
                            "first_use_week": earliest_use,
                            "introduction_week": introduced_week,
                            "gap_weeks": introduced_week - earliest_use
                        }

                        issues.append(issue)

        return issues

    def _term_to_concept(self, term_text: str) -> str:
        """Convert term text to concept name for matching."""
        # Normalize to lowercase
        normalized = term_text.lower().strip()

        # Check against known concepts
        for concept_name in self.concept_introductions.keys():
            if concept_name in normalized or normalized in concept_name:
                return concept_name

        return None

    def _find_missing_prerequisites(self) -> List[CoherenceIssue]:
        """Find concepts that have missing prerequisite knowledge."""
        issues = []

        # Common prerequisite relationships in business/education
        prerequisite_map = {
            'financial analysis': ['accounting basics', 'financial statements'],
            'strategic planning': ['swot analysis', 'competitive analysis'],
            'leadership styles': ['management fundamentals', 'organizational behavior'],
            'change management': ['organizational culture', 'leadership'],
            'performance evaluation': ['goal setting', 'feedback'],
            'project management': ['planning', 'time management'],
        }

        # Check each concept for prerequisites
        for week in self.week_contents:
            for concept in week.concepts:
                concept_key = concept.name.lower()

                # Check if this concept has known prerequisites
                for advanced_concept, prerequisites in prerequisite_map.items():
                    if advanced_concept in concept_key:
                        # Check if prerequisites were introduced earlier
                        missing_prereqs = []

                        for prereq in prerequisites:
                            # Check if prerequisite was introduced
                            prereq_introduced = False

                            for prereq_concept in self.concept_introductions.keys():
                                if prereq in prereq_concept:
                                    prereq_week = self.concept_introductions[prereq_concept]

                                    if prereq_week >= concept.introduced_week:
                                        # Prerequisite introduced too late or same week
                                        missing_prereqs.append((prereq, prereq_week))

                                    prereq_introduced = True
                                    break

                            if not prereq_introduced:
                                # Prerequisite never introduced
                                missing_prereqs.append((prereq, None))

                        # Create issue if prerequisites missing
                        if missing_prereqs:
                            prereq_list = ', '.join([p[0] for p in missing_prereqs])

                            issue = CoherenceIssue(
                                issue_id=f"missing-prereq-{concept_key}-week-{concept.introduced_week}",
                                issue_type="missing_prerequisite",
                                quality_score=7,  # Important for learning progression
                                affected_weeks=[concept.introduced_week],
                                suggested_fix=f"Introduce prerequisites ({prereq_list}) before Week {concept.introduced_week}, "
                                            f"or add brief review in Week {concept.introduced_week}",
                                auto_apply_safe=False,  # Needs curriculum review
                                category="scaffolding"
                            )

                            issue.details = {
                                "concept": concept.name,
                                "week": concept.introduced_week,
                                "missing_prerequisites": [p[0] for p in missing_prereqs],
                                "prerequisite_weeks": {p[0]: p[1] for p in missing_prereqs if p[1]}
                            }

                            issues.append(issue)

        return issues

    def _find_weak_forward_references(self) -> List[CoherenceIssue]:
        """Find concepts that could benefit from forward references."""
        issues = []

        # For each concept, check if there are related concepts in future weeks
        for week in self.week_contents:
            for concept in week.concepts:
                # Find related concepts in later weeks
                related_future = self._find_related_concepts(
                    concept.name,
                    min_week=concept.introduced_week + 1
                )

                if related_future:
                    # Check if forward reference exists in content
                    has_forward_ref = self._has_forward_reference(
                        week,
                        related_future
                    )

                    if not has_forward_ref:
                        future_weeks = [c[1] for c in related_future]
                        future_concepts = [c[0] for c in related_future]

                        issue = CoherenceIssue(
                            issue_id=f"weak-forward-ref-{concept.name.lower()}-week-{concept.introduced_week}",
                            issue_type="weak_forward_reference",
                            quality_score=5,  # Medium-low - nice to have
                            affected_weeks=[concept.introduced_week] + future_weeks[:2],  # Current + next 2
                            suggested_fix=f"Add forward reference in Week {concept.introduced_week} "
                                        f"mentioning upcoming topics: {', '.join(future_concepts[:2])}",
                            auto_apply_safe=False,  # Needs content review
                            category="scaffolding"
                        )

                        issue.details = {
                            "concept": concept.name,
                            "current_week": concept.introduced_week,
                            "related_future_concepts": future_concepts[:3],
                            "future_weeks": future_weeks[:3]
                        }

                        issues.append(issue)

        return issues

    def _find_related_concepts(
        self,
        concept_name: str,
        min_week: int
    ) -> List[Tuple[str, int]]:
        """
        Find concepts related to given concept in future weeks.

        Returns:
            List of (concept_name, week_number) tuples
        """
        related = []
        concept_key = concept_name.lower()

        # Extract key terms from concept name
        key_terms = [
            word for word in concept_key.split()
            if len(word) > 3 and word not in ['the', 'and', 'for', 'with']
        ]

        # Search for related concepts in future weeks
        for week in self.week_contents:
            if week.week_number < min_week:
                continue

            for concept in week.concepts:
                concept_lower = concept.name.lower()

                # Check for shared key terms
                if any(term in concept_lower for term in key_terms):
                    related.append((concept.name, week.week_number))

        return related

    def _has_forward_reference(
        self,
        week: WeekContent,
        future_concepts: List[Tuple[str, int]]
    ) -> bool:
        """Check if week content references future concepts."""
        # Would need to check actual lecture/tutorial content
        # For now, return False to identify potential additions
        return False

    def _find_orphaned_concepts(self) -> List[CoherenceIssue]:
        """Find concepts introduced but never referenced again."""
        issues = []

        # Track concept mentions across weeks
        concept_mentions = defaultdict(list)

        for week in self.week_contents:
            for concept in week.concepts:
                concept_mentions[concept.name.lower()].append(week.week_number)

        # Check for orphaned concepts (only mentioned once)
        for concept_name, weeks in concept_mentions.items():
            if len(weeks) == 1:
                # Concept only appears in one week

                intro_week = weeks[0]

                # Check if this is a final week (OK to not reference again)
                total_weeks = max(w.week_number for w in self.week_contents)

                if intro_week < total_weeks - 1:  # Not in last 2 weeks
                    issue = CoherenceIssue(
                        issue_id=f"orphaned-concept-{concept_name}-week-{intro_week}",
                        issue_type="orphaned_concept",
                        quality_score=6,  # Medium importance
                        affected_weeks=[intro_week],
                        suggested_fix=f"Consider referencing '{concept_name}' in later weeks "
                                    f"or integrating with related concepts",
                        auto_apply_safe=False,  # Needs curriculum review
                        category="scaffolding"
                    )

                    issue.details = {
                        "concept": concept_name,
                        "introduced_week": intro_week,
                        "total_weeks": total_weeks,
                        "weeks_until_end": total_weeks - intro_week
                    }

                    issues.append(issue)

        return issues
