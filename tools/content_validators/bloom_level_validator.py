"""
Bloom's Level Validator

Validates that quiz questions are actually at their stated cognitive level.
Remembering = recall facts, definitions, sequences
Understanding = explain why, distinguish concepts, interpret
"""

import re
import time
from pathlib import Path
from typing import List, Dict, Tuple

from .base import (
    BaseValidator,
    ValidationResult,
    ValidationIssue,
    IssueSeverity
)


class BloomLevelValidator(BaseValidator):
    """Validates quiz questions match their stated Bloom's taxonomy level."""

    @property
    def name(self) -> str:
        return "Bloom's Level Accuracy"

    @property
    def description(self) -> str:
        return "Checks that quiz questions are at their stated cognitive level (Remembering vs Understanding)"

    def validate(self, course_path: Path, **kwargs) -> ValidationResult:
        """
        Validate all quiz questions in the course.

        Args:
            course_path: Path to course directory

        Returns:
            ValidationResult with misclassified questions
        """
        start_time = time.time()
        issues = []
        items_checked = 0

        weeks = self._find_weeks(course_path)

        for week_num in weeks:
            week_path = self._get_week_path(course_path, week_num)
            quiz_path = week_path / "quiz-questions.md"

            if not quiz_path.exists():
                continue

            content = self._read_file(quiz_path)
            if not content:
                continue

            # Extract questions with their stated categories
            questions = self._extract_questions(content, week_num)
            items_checked += len(questions)

            # Validate each question's Bloom's level
            week_issues = self._validate_questions(questions, week_num)
            issues.extend(week_issues)

        duration = time.time() - start_time
        passed = not any(i.severity == IssueSeverity.CRITICAL for i in issues)

        return ValidationResult(
            validator_name=self.name,
            passed=passed,
            issues=issues,
            summary=f"Checked {items_checked} questions across {len(weeks)} weeks",
            duration_seconds=duration,
            items_checked=items_checked
        )

    def _extract_questions(self, content: str, week_num: int) -> List[Dict]:
        """Extract questions with metadata from quiz-questions.md."""
        questions = []

        # Pattern to match question blocks
        question_pattern = r'###\s+Q(\d+):\s+(.+?)\n\*\*Type:\*\*\s+(.+?)\n\*\*Category:\*\*\s+(.+?)\n\n(.+?)(?=\n###|\n---|\Z)'

        for match in re.finditer(question_pattern, content, re.DOTALL):
            q_num = match.group(1)
            title = match.group(2).strip()
            q_type = match.group(3).strip()
            category = match.group(4).strip()
            body = match.group(5).strip()

            # Extract just the question text (before options)
            question_text = body.split('\n\n')[0] if '\n\n' in body else body.split('\nA)')[0]

            questions.append({
                'id': f"W{week_num}-Q{q_num}",
                'week': week_num,
                'title': title,
                'type': q_type,
                'stated_category': category,
                'question_text': question_text[:500],  # First 500 chars
                'full_body': body[:1000]  # First 1000 chars for context
            })

        return questions

    def _validate_questions(self, questions: List[Dict], week_num: int) -> List[ValidationIssue]:
        """Validate questions using Claude."""
        if not questions:
            return []

        # Build prompt for batch analysis
        prompt = self._build_validation_prompt(questions)

        try:
            response = self._call_claude(prompt)
            return self._parse_validation_response(response, questions, week_num)
        except Exception as e:
            return [ValidationIssue(
                validator=self.name,
                severity=IssueSeverity.WARNING,
                message=f"Could not validate week {week_num}: {str(e)}",
                location=f"Week {week_num}"
            )]

    def _build_validation_prompt(self, questions: List[Dict]) -> str:
        """Build prompt for Bloom's level validation."""
        questions_text = ""
        for q in questions:
            questions_text += f"""
---
ID: {q['id']}
Stated Category: {q['stated_category']}
Question: {q['question_text']}
---
"""

        return f"""You are an expert in Bloom's taxonomy for educational assessment.

Analyze each question and determine if it matches its stated cognitive level.

**Bloom's Level Definitions for Quizzes:**

REMEMBERING (Lower-order):
- Recall facts, definitions, sequences, lists
- Identify components of a framework
- Match terms to definitions
- Recognize correct sequences
- "What is...", "Name the...", "Which of the following is..."
- NO scenarios or application required

UNDERSTANDING (Higher-order for quizzes):
- Explain WHY something works
- Distinguish between similar concepts
- Interpret the meaning or purpose
- Identify misconceptions (True/False)
- "What is the PURPOSE of...", "Why does...", "What is the DIFFERENCE between..."
- Brief context is OK, but focus is on comprehension, not application

NOT APPROPRIATE for Remember/Understand quizzes:
- Scenario-based problem solving (this is APPLICATION level)
- "What should the manager do?" type questions
- Multi-step analysis or diagnosis

**Questions to Analyze:**
{questions_text}

**For each question, respond in this exact format:**

[ID]: [MATCH/MISMATCH]
Stated: [stated level]
Actual: [your assessment of actual level]
Reason: [1-2 sentence explanation]
Suggestion: [if mismatch, how to fix; if match, write "None"]

Analyze all questions:"""

    def _parse_validation_response(
        self,
        response: str,
        questions: List[Dict],
        week_num: int
    ) -> List[ValidationIssue]:
        """Parse Claude's response into validation issues."""
        issues = []

        # Create lookup for questions
        q_lookup = {q['id']: q for q in questions}

        # Parse each question's analysis
        pattern = r'\[([^\]]+)\]:\s*(MATCH|MISMATCH)\s*\nStated:\s*(.+?)\s*\nActual:\s*(.+?)\s*\nReason:\s*(.+?)\s*\nSuggestion:\s*(.+?)(?=\n\[|$)'

        for match in re.finditer(pattern, response, re.DOTALL):
            q_id = match.group(1).strip()
            result = match.group(2).strip()
            stated = match.group(3).strip()
            actual = match.group(4).strip()
            reason = match.group(5).strip()
            suggestion = match.group(6).strip()

            if result == "MISMATCH" and q_id in q_lookup:
                q = q_lookup[q_id]

                # Determine severity
                # If stated as Remembering but actually Application = Critical
                # If stated as Understanding but actually Remembering = Warning
                if "application" in actual.lower() or "applying" in actual.lower():
                    severity = IssueSeverity.CRITICAL
                else:
                    severity = IssueSeverity.WARNING

                issues.append(ValidationIssue(
                    validator=self.name,
                    severity=severity,
                    message=f"Question '{q['title']}' is labeled as {stated} but appears to be {actual}",
                    location=f"Week {week_num} > {q_id}",
                    context=q['question_text'][:200],
                    suggestion=suggestion if suggestion != "None" else None,
                    metadata={
                        'stated_level': stated,
                        'actual_level': actual,
                        'reason': reason
                    }
                ))

        return issues
