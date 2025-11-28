"""
Framework Scaffolding Validator

Validates that concepts and frameworks are introduced before being referenced.
Ensures proper pedagogical scaffolding across weeks.
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


class FrameworkScaffoldingValidator(BaseValidator):
    """Validates proper scaffolding of frameworks and concepts across weeks."""

    @property
    def name(self) -> str:
        return "Framework Scaffolding"

    @property
    def description(self) -> str:
        return "Checks that frameworks are introduced before being referenced in later content"

    def validate(self, course_path: Path, **kwargs) -> ValidationResult:
        """
        Validate framework scaffolding across the course.

        Args:
            course_path: Path to course directory

        Returns:
            ValidationResult with scaffolding issues
        """
        start_time = time.time()
        issues = []

        # First, extract all framework introductions
        framework_intros = self._extract_framework_introductions(course_path)

        # Then, check for references before introduction
        weeks = self._find_weeks(course_path)
        items_checked = 0

        for week_num in weeks:
            week_path = self._get_week_path(course_path, week_num)

            # Check lecture, tutorial, and quiz content
            for file_name in ['lecture-content.md', 'tutorial-content.md', 'quiz-questions.md']:
                file_path = week_path / file_name
                if not file_path.exists():
                    continue

                content = self._read_file(file_path)
                if not content:
                    continue

                items_checked += 1
                file_issues = self._check_references(
                    content,
                    week_num,
                    file_name,
                    framework_intros
                )
                issues.extend(file_issues)

        duration = time.time() - start_time
        passed = not any(i.severity == IssueSeverity.CRITICAL for i in issues)

        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            issues=issues,
            summary=f"Checked {items_checked} files for {len(framework_intros)} frameworks",
            duration_seconds=duration,
            items_checked=items_checked,
            metadata={'frameworks_tracked': list(framework_intros.keys())}
        )

    def _extract_framework_introductions(self, course_path: Path) -> Dict[str, int]:
        """
        Extract when each framework is first introduced (in lecture).

        Returns:
            Dict mapping framework name (normalized) to week number
        """
        frameworks = {}
        weeks = self._find_weeks(course_path)

        for week_num in weeks:
            week_path = self._get_week_path(course_path, week_num)
            lecture_path = week_path / "lecture-content.md"

            if not lecture_path.exists():
                continue

            content = self._read_file(lecture_path)
            if not content:
                continue

            # Find framework definitions (usually in bold or as section headers)
            week_frameworks = self._find_framework_definitions(content)

            for fw in week_frameworks:
                normalized = self._normalize_name(fw)
                if normalized not in frameworks:
                    frameworks[normalized] = week_num

        return frameworks

    def _find_framework_definitions(self, content: str) -> List[str]:
        """Find framework/model definitions in lecture content."""
        frameworks = []

        # Pattern 1: "**Framework Name**" or "**Framework Name Model**"
        bolded = re.findall(r'\*\*([^*]+(?:Model|Framework|Theory|Principle)[^*]*)\*\*', content, re.IGNORECASE)
        frameworks.extend(bolded)

        # Pattern 2: Section headers with framework names
        headers = re.findall(r'^##\s+(.+(?:Model|Framework|Theory|Principle).*)$', content, re.MULTILINE | re.IGNORECASE)
        frameworks.extend(headers)

        # Pattern 3: "The X Model/Framework"
        the_pattern = re.findall(r'[Tt]he\s+([A-Z][A-Za-z\s\-]+)\s+(Model|Framework|Theory|Principle)', content)
        frameworks.extend([f"{m[0]} {m[1]}" for m in the_pattern])

        # Pattern 4: Named frameworks like "Pyramid Principle", "SCQA", "MKS"
        named = re.findall(r'\b(Pyramid Principle|SCQA|MKS|BLUF|Shannon-Weaver|Munter|Hofstede|Cialdini|Duarte|Kolb)\b', content)
        frameworks.extend(named)

        return list(set(frameworks))

    def _normalize_name(self, name: str) -> str:
        """Normalize framework name for comparison."""
        # Lowercase, remove extra spaces, remove common suffixes
        normalized = name.lower().strip()
        normalized = re.sub(r'\s+', ' ', normalized)
        # Remove trailing punctuation
        normalized = re.sub(r'[.,;:!?]+$', '', normalized)
        return normalized

    def _check_references(
        self,
        content: str,
        week_num: int,
        file_name: str,
        framework_intros: Dict[str, int]
    ) -> List[ValidationIssue]:
        """Check for framework references before introduction."""
        issues = []

        # Find all framework mentions in this content
        mentioned_frameworks = self._find_framework_mentions(content)

        for framework in mentioned_frameworks:
            normalized = self._normalize_name(framework)

            # Check if this framework was introduced
            if normalized in framework_intros:
                intro_week = framework_intros[normalized]

                # Is it referenced before introduction?
                if week_num < intro_week:
                    # This is only a problem in tutorials/quizzes
                    # Lectures can preview upcoming frameworks
                    if file_name != 'lecture-content.md':
                        issues.append(ValidationIssue(
                            validator=self.name,
                            severity=IssueSeverity.CRITICAL,
                            message=f"'{framework}' referenced in Week {week_num} but not introduced until Week {intro_week}",
                            location=f"Week {week_num} > {file_name}",
                            suggestion=f"Add introduction to '{framework}' in Week {week_num} lecture, or move reference to Week {intro_week} or later",
                            metadata={
                                'framework': framework,
                                'reference_week': week_num,
                                'introduction_week': intro_week
                            }
                        ))
                    else:
                        # In lecture, this might be a forward reference (warning, not critical)
                        issues.append(ValidationIssue(
                            validator=self.name,
                            severity=IssueSeverity.SUGGESTION,
                            message=f"'{framework}' mentioned in Week {week_num} lecture but formally introduced in Week {intro_week}",
                            location=f"Week {week_num} > {file_name}",
                            suggestion=f"Consider adding 'We'll explore {framework} in Week {intro_week}' as a forward reference",
                            metadata={
                                'framework': framework,
                                'reference_week': week_num,
                                'introduction_week': intro_week
                            }
                        ))
            else:
                # Framework mentioned but never formally introduced
                # Check if it's in any week's lecture
                if self._is_significant_framework(framework):
                    issues.append(ValidationIssue(
                        validator=self.name,
                        severity=IssueSeverity.WARNING,
                        message=f"'{framework}' used in Week {week_num} but never formally introduced in any lecture",
                        location=f"Week {week_num} > {file_name}",
                        suggestion=f"Add formal introduction of '{framework}' before first use",
                        metadata={
                            'framework': framework,
                            'reference_week': week_num
                        }
                    ))

        return issues

    def _find_framework_mentions(self, content: str) -> List[str]:
        """Find all framework mentions in content."""
        mentions = []

        # Pattern: [Name] Model/Framework/Theory/Principle
        pattern = re.findall(
            r'([A-Z][A-Za-z\s\-\']+)\s+(Model|Framework|Theory|Principle)',
            content
        )
        mentions.extend([f"{m[0].strip()} {m[1]}" for m in pattern])

        # Named frameworks
        named = re.findall(
            r'\b(Pyramid Principle|SCQA|MKS|BLUF|Shannon-Weaver|Munter|Hofstede|Cialdini|Duarte|Kolb|Minto|Aristotle|Hewlett)\b',
            content
        )
        mentions.extend(named)

        return list(set(mentions))

    def _is_significant_framework(self, framework: str) -> bool:
        """Check if this is a significant framework worth tracking."""
        # Skip very short or generic terms
        if len(framework) < 5:
            return False

        # Skip common words that might match pattern
        skip_words = ['the model', 'this framework', 'a theory', 'the principle']
        if framework.lower() in skip_words:
            return False

        return True
