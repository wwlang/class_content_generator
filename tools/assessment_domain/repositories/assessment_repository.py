"""
Repository for accessing assessments from the file system.

Handles loading assessment handbooks and individual assessments.
"""

from pathlib import Path
from typing import Dict, List, Optional
from ..models import Assessment, AssessmentType
from ..parsers import HandbookParser


class AssessmentRepository:
    """
    Repository for loading and caching assessments.

    Responsibilities:
    - Abstract file system paths
    - Load assessments from handbook files
    - Cache parsed assessments
    - Filter assessments by type or due week

    Usage:
        repo = AssessmentRepository(base_path="courses")
        assessment = repo.get_assessment("BCI2AU", "persuasive-proposal")
        portfolio = repo.get_assessments_by_type("BCI2AU", AssessmentType.PORTFOLIO)
    """

    def __init__(self, base_path: str = "courses"):
        """
        Initialize repository.

        Args:
            base_path: Root directory containing course folders
        """
        self.base_path = Path(base_path)
        self.parser = HandbookParser()
        self._cache: Dict[str, Dict[str, Assessment]] = {}

    def get_assessment(
        self,
        course_code: str,
        assessment_id: str,
        use_cache: bool = True
    ) -> Optional[Assessment]:
        """
        Load a specific assessment by ID.

        Args:
            course_code: Course identifier (e.g., "BCI2AU")
            assessment_id: Assessment slug (e.g., "persuasive-proposal")
            use_cache: If True, use cached assessments

        Returns:
            Assessment object, or None if not found

        Example:
            proposal = repo.get_assessment("BCI2AU", "persuasive-proposal")
            print(f"Due: Week {proposal.due_week}")
        """
        assessments = self.get_all_assessments(course_code, use_cache)
        return assessments.get(assessment_id)

    def get_all_assessments(
        self,
        course_code: str,
        use_cache: bool = True
    ) -> Dict[str, Assessment]:
        """
        Load all assessments for a course.

        Args:
            course_code: Course identifier
            use_cache: If True, return cached assessments if available

        Returns:
            Dictionary mapping assessment IDs to Assessment objects

        Raises:
            FileNotFoundError: If assessment handbook doesn't exist

        Example:
            assessments = repo.get_all_assessments("BCI2AU")
            for aid, assessment in assessments.items():
                print(f"{aid}: {assessment.name}")
        """
        if use_cache and course_code in self._cache:
            return self._cache[course_code]

        handbook_path = self._get_handbook_path(course_code)

        if not handbook_path.exists():
            raise FileNotFoundError(
                f"Assessment handbook not found: {handbook_path}\n"
                f"Expected location: courses/{course_code}/assessment-handbook.md"
            )

        assessments = self.parser.parse_file(handbook_path)

        if use_cache:
            self._cache[course_code] = assessments

        return assessments

    def get_assessments_by_type(
        self,
        course_code: str,
        assessment_type: AssessmentType,
        use_cache: bool = True
    ) -> List[Assessment]:
        """
        Filter assessments by type.

        Args:
            course_code: Course identifier
            assessment_type: AssessmentType enum value
            use_cache: If True, use cached assessments

        Returns:
            List of assessments matching the type

        Example:
            # Get all portfolio assessments
            portfolios = repo.get_assessments_by_type(
                "BCI2AU",
                AssessmentType.PORTFOLIO
            )
        """
        all_assessments = self.get_all_assessments(course_code, use_cache)
        return [
            a for a in all_assessments.values()
            if a.type == assessment_type
        ]

    def get_assessments_by_week(
        self,
        course_code: str,
        week: int,
        use_cache: bool = True
    ) -> List[Assessment]:
        """
        Get assessments due in a specific week.

        Args:
            course_code: Course identifier
            week: Week number
            use_cache: If True, use cached assessments

        Returns:
            List of assessments due in that week

        Example:
            # Check what's due in week 6
            due_week6 = repo.get_assessments_by_week("BCI2AU", 6)
        """
        all_assessments = self.get_all_assessments(course_code, use_cache)
        return [
            a for a in all_assessments.values()
            if a.due_week == week
        ]

    def get_assessments_with_rubrics(
        self,
        course_code: str,
        use_cache: bool = True
    ) -> List[Assessment]:
        """
        Get assessments that have rubrics attached.

        Args:
            course_code: Course identifier
            use_cache: If True, use cached assessments

        Returns:
            List of assessments with rubrics

        Example:
            # Find assessments ready for PDF export
            with_rubrics = repo.get_assessments_with_rubrics("BCI2AU")
        """
        all_assessments = self.get_all_assessments(course_code, use_cache)
        return [
            a for a in all_assessments.values()
            if a.rubric is not None
        ]

    def get_assessments_with_scenarios(
        self,
        course_code: str,
        use_cache: bool = True
    ) -> List[Assessment]:
        """
        Get assessments that have scenario options.

        Args:
            course_code: Course identifier
            use_cache: If True, use cached assessments

        Returns:
            List of assessments with scenarios

        Example:
            # Find assessments with choice options
            with_scenarios = repo.get_assessments_with_scenarios("BCI2AU")
        """
        all_assessments = self.get_all_assessments(course_code, use_cache)
        return [
            a for a in all_assessments.values()
            if len(a.scenarios) > 0
        ]

    def clear_cache(self, course_code: Optional[str] = None):
        """
        Clear cached assessments.

        Args:
            course_code: If provided, clear only this course's cache.
                        If None, clear entire cache.

        Example:
            # Clear cache after updating handbook
            repo.clear_cache("BCI2AU")
        """
        if course_code:
            if course_code in self._cache:
                del self._cache[course_code]
        else:
            self._cache.clear()

    def _get_handbook_path(self, course_code: str) -> Path:
        """
        Get path to assessment handbook file.

        Args:
            course_code: Course identifier

        Returns:
            Path to assessment-handbook.md
        """
        return (
            self.base_path /
            f"{course_code}-business-communication" /
            "assessment-handbook.md"
        )

    def get_statistics(
        self,
        course_code: str
    ) -> Dict[str, any]:
        """
        Get statistics about assessments in the repository.

        Args:
            course_code: Course identifier

        Returns:
            Dictionary with statistics:
            - total: Total assessment count
            - by_type: Count per assessment type
            - with_rubrics: Count with rubrics
            - with_scenarios: Count with scenarios
            - total_weight: Sum of all weights

        Example:
            stats = repo.get_statistics("BCI2AU")
            print(f"Total assessments: {stats['total']}")
            print(f"Portfolio: {stats['by_type']['portfolio']}")
        """
        all_assessments = self.get_all_assessments(course_code, use_cache=True)

        by_type: Dict[str, int] = {
            'portfolio': 0,
            'presentation': 0,
            'quiz': 0,
            'project': 0
        }
        with_rubrics = 0
        with_scenarios = 0
        total_weight = 0.0

        for assessment in all_assessments.values():
            by_type[assessment.type.value] += 1
            if assessment.rubric:
                with_rubrics += 1
            if assessment.scenarios:
                with_scenarios += 1
            total_weight += assessment.weight

        return {
            'total': len(all_assessments),
            'by_type': by_type,
            'with_rubrics': with_rubrics,
            'with_scenarios': with_scenarios,
            'total_weight': total_weight,
            'avg_weight': total_weight / len(all_assessments) if all_assessments else 0,
        }
