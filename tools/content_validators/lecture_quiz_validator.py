"""
Lecture-Quiz Alignment Validator

Validates that quiz questions test content actually taught in lectures.
Ensures questions reference frameworks, concepts, and examples from the lecture.
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


class LectureQuizValidator(BaseValidator):
    """Validates quiz questions align with lecture content."""

    @property
    def name(self) -> str:
        return "Lecture-Quiz Alignment"

    @property
    def description(self) -> str:
        return "Checks that quiz questions test concepts actually taught in the lecture"

    def validate(self, course_path: Path, **kwargs) -> ValidationResult:
        """
        Validate lecture-quiz alignment across the course.

        Args:
            course_path: Path to course directory

        Returns:
            ValidationResult with alignment issues
        """
        start_time = time.time()
        issues = []
        items_checked = 0

        weeks = self._find_weeks(course_path)

        for week_num in weeks:
            week_path = self._get_week_path(course_path, week_num)

            lecture_path = week_path / "lecture-content.md"
            quiz_path = week_path / "quiz-questions.md"

            if not lecture_path.exists() or not quiz_path.exists():
                continue

            lecture_content = self._read_file(lecture_path)
            quiz_content = self._read_file(quiz_path)

            if not lecture_content or not quiz_content:
                continue

            # Extract questions
            questions = self._extract_questions(quiz_content, week_num)
            items_checked += len(questions)

            # Validate alignment
            week_issues = self._validate_alignment(
                lecture_content,
                questions,
                week_num
            )
            issues.extend(week_issues)

        duration = time.time() - start_time
        passed = not any(i.severity == IssueSeverity.CRITICAL for i in issues)

        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            issues=issues,
            summary=f"Checked {items_checked} questions against lecture content",
            duration_seconds=duration,
            items_checked=items_checked
        )

    def _extract_questions(self, quiz_content: str, week_num: int) -> List[Dict]:
        """Extract questions from quiz file."""
        questions = []

        # Pattern to match question blocks
        pattern = r'###\s+Q(\d+):\s+(.+?)\n.*?\n\n(.+?)(?=\n###|\n---|\Z)'

        for match in re.finditer(pattern, quiz_content, re.DOTALL):
            q_num = match.group(1)
            title = match.group(2).strip()
            body = match.group(3).strip()

            # Get question text (first paragraph)
            question_text = body.split('\n\n')[0] if '\n\n' in body else body.split('\nA)')[0]

            questions.append({
                'id': f"W{week_num}-Q{q_num}",
                'title': title,
                'question_text': question_text[:500],
                'full_body': body[:1500]
            })

        return questions

    def _validate_alignment(
        self,
        lecture_content: str,
        questions: List[Dict],
        week_num: int
    ) -> List[ValidationIssue]:
        """Validate questions against lecture content using Claude."""
        if not questions:
            return []

        # Extract key concepts from lecture
        lecture_summary = self._summarize_lecture(lecture_content)

        # Build validation prompt
        prompt = self._build_alignment_prompt(lecture_summary, questions, week_num)

        try:
            response = self._call_claude(prompt)
            return self._parse_response(response, questions, week_num)
        except Exception as e:
            return [ValidationIssue(
                validator=self.name,
                severity=IssueSeverity.WARNING,
                message=f"Could not validate week {week_num}: {str(e)}",
                location=f"Week {week_num}"
            )]

    def _summarize_lecture(self, lecture_content: str) -> str:
        """Extract key frameworks and concepts from lecture."""
        # Extract section headings
        headings = re.findall(r'^##\s+(.+)$', lecture_content, re.MULTILINE)

        # Extract bolded terms (frameworks, key concepts)
        bolded = re.findall(r'\*\*([^*]+)\*\*', lecture_content)
        unique_bolded = list(dict.fromkeys(bolded))[:30]  # First 30 unique

        # Extract framework mentions
        frameworks = re.findall(
            r'([A-Z][A-Za-z\s]+?)\s+(Model|Framework|Theory|Principle)',
            lecture_content
        )

        summary = f"""
LECTURE SECTIONS:
{chr(10).join(f'- {h}' for h in headings[:15])}

KEY CONCEPTS (bolded terms):
{chr(10).join(f'- {t}' for t in unique_bolded)}

FRAMEWORKS/MODELS:
{chr(10).join(f'- {f[0]} {f[1]}' for f in frameworks[:10])}

LECTURE EXCERPT (first 1500 chars):
{lecture_content[:1500]}
"""
        return summary

    def _build_alignment_prompt(
        self,
        lecture_summary: str,
        questions: List[Dict],
        week_num: int
    ) -> str:
        """Build prompt for alignment validation."""
        questions_text = ""
        for q in questions:
            questions_text += f"""
---
ID: {q['id']}
Title: {q['title']}
Question: {q['question_text']}
---
"""

        return f"""You are an expert in curriculum alignment for university courses.

Analyze whether each quiz question tests content that was actually taught in the lecture.

**Week {week_num} Lecture Summary:**
{lecture_summary}

**Quiz Questions:**
{questions_text}

**For each question, determine:**

1. **COVERED**: The concept/framework is explicitly taught in the lecture
2. **PARTIALLY_COVERED**: Related concept mentioned but not the specific detail tested
3. **NOT_COVERED**: The question tests something not taught in this week's lecture

**Respond in this exact format for each question:**

[ID]: [COVERED/PARTIALLY_COVERED/NOT_COVERED]
Concept tested: [what the question is testing]
Lecture evidence: [where this appears in lecture, or "Not found"]
Issue: [if not covered, explain what's missing]

Analyze all questions:"""

    def _parse_response(
        self,
        response: str,
        questions: List[Dict],
        week_num: int
    ) -> List[ValidationIssue]:
        """Parse Claude's response into validation issues."""
        issues = []

        q_lookup = {q['id']: q for q in questions}

        # Pattern to parse each question's analysis
        pattern = r'\[([^\]]+)\]:\s*(COVERED|PARTIALLY_COVERED|NOT_COVERED)\s*\nConcept tested:\s*(.+?)\s*\nLecture evidence:\s*(.+?)\s*\nIssue:\s*(.+?)(?=\n\[|$)'

        for match in re.finditer(pattern, response, re.DOTALL):
            q_id = match.group(1).strip()
            status = match.group(2).strip()
            concept = match.group(3).strip()
            evidence = match.group(4).strip()
            issue_text = match.group(5).strip()

            if q_id not in q_lookup:
                continue

            q = q_lookup[q_id]

            if status == "NOT_COVERED":
                issues.append(ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.CRITICAL,
                    message=f"Question '{q['title']}' tests content not covered in Week {week_num} lecture",
                    location=f"Week {week_num} > {q_id}",
                    context=q['question_text'][:150],
                    suggestion=f"Add {concept} to lecture content, or move question to appropriate week",
                    metadata={
                        'concept_tested': concept,
                        'issue': issue_text
                    }
                ))
            elif status == "PARTIALLY_COVERED":
                issues.append(ValidationIssue(
                    validator=self.name,
                    severity=IssueSeverity.WARNING,
                    message=f"Question '{q['title']}' tests details not fully covered in lecture",
                    location=f"Week {week_num} > {q_id}",
                    context=q['question_text'][:150],
                    suggestion=f"Consider expanding lecture coverage of: {concept}",
                    metadata={
                        'concept_tested': concept,
                        'evidence': evidence,
                        'issue': issue_text
                    }
                ))

        return issues
