"""
Learning Objective Coverage Validator

Validates that all stated learning objectives are covered by lectures and assessments.
Ensures alignment between objectives, content, and assessment.
"""

import re
import time
from pathlib import Path
from typing import List, Dict, Set

from .base import (
    BaseValidator,
    ValidationResult,
    ValidationIssue,
    IssueSeverity
)


class LearningObjectiveValidator(BaseValidator):
    """Validates learning objective coverage across course content."""

    @property
    def name(self) -> str:
        return "Learning Objective Coverage"

    @property
    def description(self) -> str:
        return "Checks that all learning objectives are covered by lectures and assessed"

    def validate(self, course_path: Path, **kwargs) -> ValidationResult:
        """
        Validate learning objective coverage.

        Args:
            course_path: Path to course directory

        Returns:
            ValidationResult with coverage issues
        """
        start_time = time.time()
        issues = []

        # Extract learning objectives from syllabus
        syllabus_path = course_path / "syllabus.md"
        syllabus_content = self._read_file(syllabus_path)

        if not syllabus_content:
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                issues=[ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.CRITICAL,
                    message="Syllabus not found - cannot validate LO coverage",
                    location=str(syllabus_path)
                )],
                summary="Syllabus missing",
                duration_seconds=time.time() - start_time,
                items_checked=0
            )

        # Extract LOs
        learning_objectives = self._extract_learning_objectives(syllabus_content)

        if not learning_objectives:
            return ValidationResult(
                validator_name=self.name,
                passed=False,
                issues=[ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.CRITICAL,
                    message="No learning objectives found in syllabus",
                    location=str(syllabus_path)
                )],
                summary="No LOs found",
                duration_seconds=time.time() - start_time,
                items_checked=0
            )

        # Check coverage in lectures and assessments
        coverage_issues = self._check_coverage(
            course_path,
            learning_objectives
        )
        issues.extend(coverage_issues)

        duration = time.time() - start_time
        passed = not any(i.severity == IssueSeverity.CRITICAL for i in issues)

        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            issues=issues,
            summary=f"Checked coverage of {len(learning_objectives)} learning objectives",
            duration_seconds=duration,
            items_checked=len(learning_objectives),
            metadata={'learning_objectives': learning_objectives}
        )

    def _extract_learning_objectives(self, syllabus_content: str) -> List[Dict]:
        """Extract learning objectives from syllabus."""
        objectives = []

        # Look for numbered objectives after "Learning Objectives" heading
        lo_section = re.search(
            r'(?:LEARNING OBJECTIVES|Learning Objectives).*?\n((?:\d+\..*?\n)+)',
            syllabus_content,
            re.DOTALL | re.IGNORECASE
        )

        if lo_section:
            lo_text = lo_section.group(1)

            # Pattern: "1. **Verb** description" or "1. Verb description"
            pattern = r'(\d+)\.\s+\*\*([A-Z][a-z]+)\*\*\s+(.+?)(?=\n\d+\.|\n\n|\Z)'
            alt_pattern = r'(\d+)\.\s+([A-Z][a-z]+)\s+(.+?)(?=\n\d+\.|\n\n|\Z)'

            matches = re.finditer(pattern, lo_text, re.DOTALL)
            if not list(matches):
                matches = re.finditer(alt_pattern, lo_text, re.DOTALL)

            for match in re.finditer(pattern, lo_text, re.DOTALL):
                num = int(match.group(1))
                verb = match.group(2).strip()
                description = match.group(3).strip()

                objectives.append({
                    'number': num,
                    'verb': verb,
                    'description': description,
                    'full_text': f"{verb} {description}"
                })

        return objectives

    def _check_coverage(
        self,
        course_path: Path,
        learning_objectives: List[Dict]
    ) -> List[ValidationIssue]:
        """Check if all LOs are covered in content and assessments."""
        issues = []

        # Collect all content for analysis
        all_lecture_content = self._collect_lecture_content(course_path)
        assessment_content = self._get_assessment_content(course_path)

        # Use Claude to analyze coverage
        prompt = self._build_coverage_prompt(
            learning_objectives,
            all_lecture_content,
            assessment_content
        )

        try:
            response = self._call_claude(prompt)
            issues = self._parse_coverage_response(response, learning_objectives)
        except Exception as e:
            issues.append(ValidationIssue(
                validator=self.name,
                severity=IssueSeverity.WARNING,
                message=f"Could not analyze LO coverage: {str(e)}",
                location="Course-wide"
            ))

        return issues

    def _collect_lecture_content(self, course_path: Path) -> str:
        """Collect key content from all lectures."""
        content_parts = []
        weeks = self._find_weeks(course_path)

        for week_num in weeks:
            week_path = self._get_week_path(course_path, week_num)
            lecture_path = week_path / "lecture-content.md"

            if lecture_path.exists():
                content = self._read_file(lecture_path)
                if content:
                    # Extract headings and key concepts
                    headings = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
                    bolded = re.findall(r'\*\*([^*]+)\*\*', content)[:20]

                    content_parts.append(f"""
Week {week_num}:
Sections: {', '.join(headings[:10])}
Key concepts: {', '.join(bolded)}
""")

        return '\n'.join(content_parts)

    def _get_assessment_content(self, course_path: Path) -> str:
        """Get assessment information."""
        # Try assessment handbook first
        handbook_path = course_path / "assessment-handbook.md"
        if handbook_path.exists():
            content = self._read_file(handbook_path)
            if content:
                # Extract assessment overview section
                overview = re.search(
                    r'## Assessment Overview.*?(?=##[^#])',
                    content,
                    re.DOTALL
                )
                return overview.group(0) if overview else content[:2000]

        # Fallback to syllabus assessment section
        syllabus_path = course_path / "syllabus.md"
        if syllabus_path.exists():
            content = self._read_file(syllabus_path)
            if content:
                assessment = re.search(
                    r'(?:ASSESSMENT|Assessment).*?(?=\n#[^#]|\Z)',
                    content,
                    re.DOTALL
                )
                return assessment.group(0) if assessment else ""

        return ""

    def _build_coverage_prompt(
        self,
        objectives: List[Dict],
        lecture_content: str,
        assessment_content: str
    ) -> str:
        """Build prompt for coverage analysis."""
        objectives_text = "\n".join([
            f"LO{obj['number']}: {obj['full_text']}"
            for obj in objectives
        ])

        return f"""You are an expert in curriculum design and learning objective alignment.

Analyze whether each learning objective is adequately covered in the course content and assessed.

**Learning Objectives:**
{objectives_text}

**Lecture Content Summary:**
{lecture_content[:3000]}

**Assessment Overview:**
{assessment_content[:2000]}

**For each learning objective, determine:**

1. **COVERED**: Explicitly taught in lectures with sufficient depth
2. **PARTIALLY_COVERED**: Mentioned but not deeply taught
3. **NOT_COVERED**: Not addressed in any lecture

4. **ASSESSED**: Clearly tested in an assessment
5. **PARTIALLY_ASSESSED**: Indirectly tested
6. **NOT_ASSESSED**: No assessment targets this objective

**Respond in this exact format for each LO:**

[LO#]:
Content: [COVERED/PARTIALLY_COVERED/NOT_COVERED]
Evidence: [which weeks/content covers this]
Assessment: [ASSESSED/PARTIALLY_ASSESSED/NOT_ASSESSED]
Assessment evidence: [which assessment tests this]
Issue: [any gap identified, or "None"]

Analyze all learning objectives:"""

    def _parse_coverage_response(
        self,
        response: str,
        objectives: List[Dict]
    ) -> List[ValidationIssue]:
        """Parse Claude's coverage analysis."""
        issues = []

        for obj in objectives:
            lo_num = obj['number']

            # Find this LO's analysis
            pattern = rf'\[LO{lo_num}\]:\s*\nContent:\s*(COVERED|PARTIALLY_COVERED|NOT_COVERED)\s*\nEvidence:\s*(.+?)\s*\nAssessment:\s*(ASSESSED|PARTIALLY_ASSESSED|NOT_ASSESSED)\s*\nAssessment evidence:\s*(.+?)\s*\nIssue:\s*(.+?)(?=\n\[LO|$)'

            match = re.search(pattern, response, re.DOTALL)
            if not match:
                continue

            content_status = match.group(1)
            content_evidence = match.group(2).strip()
            assess_status = match.group(3)
            assess_evidence = match.group(4).strip()
            issue_text = match.group(5).strip()

            # Check for content coverage issues
            if content_status == "NOT_COVERED":
                issues.append(ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.CRITICAL,
                    message=f"LO{lo_num} '{obj['verb']} {obj['description'][:50]}...' is not covered in any lecture",
                    location=f"Learning Objective {lo_num}",
                    suggestion=f"Add content covering LO{lo_num} to relevant week's lecture",
                    metadata={
                        'objective': obj['full_text'],
                        'issue': issue_text
                    }
                ))
            elif content_status == "PARTIALLY_COVERED":
                issues.append(ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.WARNING,
                    message=f"LO{lo_num} is only partially covered: {content_evidence[:100]}",
                    location=f"Learning Objective {lo_num}",
                    suggestion=f"Expand coverage of LO{lo_num} in lectures",
                    metadata={
                        'objective': obj['full_text'],
                        'evidence': content_evidence
                    }
                ))

            # Check for assessment alignment issues
            if assess_status == "NOT_ASSESSED":
                issues.append(ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.CRITICAL,
                    message=f"LO{lo_num} is not assessed by any assignment or quiz",
                    location=f"Learning Objective {lo_num}",
                    suggestion=f"Add assessment targeting LO{lo_num}",
                    metadata={
                        'objective': obj['full_text']
                    }
                ))
            elif assess_status == "PARTIALLY_ASSESSED":
                issues.append(ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.WARNING,
                    message=f"LO{lo_num} is only indirectly assessed: {assess_evidence[:100]}",
                    location=f"Learning Objective {lo_num}",
                    suggestion=f"Strengthen assessment alignment for LO{lo_num}",
                    metadata={
                        'objective': obj['full_text'],
                        'evidence': assess_evidence
                    }
                ))

        return issues
