#!/usr/bin/env python3
"""
Tutor notes generator.

Generates tutor-facing notes with answer keys and facilitation guidance.
"""

import re
from pathlib import Path
from typing import Tuple, List
from .base_generator import BaseGenerator


class TutorNotesGenerator(BaseGenerator):
    """Generate tutor notes for a week."""

    def __init__(self, course_path: Path, week_number: int):
        """
        Initialize tutor notes generator.

        Args:
            course_path: Path to course directory
            week_number: Week number to generate
        """
        super().__init__(course_path, week_number)

    def generate(self) -> Tuple[bool, str]:
        """
        Generate tutor notes.

        Creates context for Claude to generate tutor-facing facilitation guidance.

        Returns:
            (success, error_message)
        """
        try:
            # Check if already exists
            output_file = self.week_dir / "tutorial-tutor-notes.md"
            if output_file.exists():
                return (True, "Tutor notes already exist")

            # Check that tutorial exists first
            tutorial_file = self.week_dir / "tutorial-content.md"
            if not tutorial_file.exists():
                return (False, "Tutorial must be generated before tutor notes")

            # Read tutorial content
            tutorial_content = tutorial_file.read_text(encoding='utf-8')

            # Gather context
            topic = self.get_week_topic()
            quiz_questions = self._extract_quiz_questions(tutorial_content)

            # Create generation context
            context = self._create_generation_context(
                topic, tutorial_content, quiz_questions
            )

            # Save context
            context_file = self.week_dir / ".tutor-notes-generation-context.md"
            context_file.write_text(context, encoding='utf-8')

            error_msg = (
                f"Tutor notes generation context created at: {context_file}\n\n"
                f"To generate tutor notes:\n"
                f"1. Use Claude Code with /generate-week {self.week_number}\n"
                f"   OR\n"
                f"2. Manually provide the context to Claude and save output to:\n"
                f"   {output_file}\n\n"
                f"The context includes tutorial content and requires answer keys + guidance."
            )

            return (False, error_msg)

        except Exception as e:
            return (False, f"Error generating tutor notes: {str(e)}")

    def _extract_quiz_questions(self, tutorial_content: str) -> List[str]:
        """Extract quiz questions from tutorial content."""
        questions = []

        # Look for quiz section
        quiz_section_match = re.search(
            r'##?\s*Quiz.*?(?=##|\Z)',
            tutorial_content,
            re.DOTALL | re.IGNORECASE
        )

        if quiz_section_match:
            quiz_section = quiz_section_match.group(0)

            # Extract numbered questions
            question_pattern = r'^\d+\.\s*(.+?)(?=\n\d+\.|\n##|\Z)'
            questions = re.findall(question_pattern, quiz_section, re.MULTILINE | re.DOTALL)

            # Clean up questions
            questions = [q.strip() for q in questions if q.strip()]

        return questions

    def _create_generation_context(
        self,
        topic: str,
        tutorial_content: str,
        quiz_questions: List[str]
    ) -> str:
        """Create the context/prompt for tutor notes generation."""
        context = f"""# Tutor Notes Generation Context - Week {self.week_number}

## Course Information
- Week: {self.week_number}
- Topic: {topic}

## Tutorial Content (Student-Facing)

{tutorial_content}

## Required Tutor Notes Content

Generate tutor-facing notes with:

### 1. Quiz Answer Key

For each quiz question, provide:
- **Correct answer**
- **Explanation** (why this is correct, common misconceptions)
- **Learning objective tested**

Quiz questions to answer:
"""
        if quiz_questions:
            for i, question in enumerate(quiz_questions, 1):
                # Truncate very long questions for display
                q_display = question[:200] + "..." if len(question) > 200 else question
                context += f"\n{i}. {q_display}\n"
        else:
            context += "\n(Extract quiz questions from tutorial content above)\n"

        context += """
### 2. Expected Student Approaches

For the main tutorial activity, document:
- **3-5 valid approaches** students might take
- **Quality indicators** for each approach (what makes it good?)
- **Common mistakes** to watch for
- **How to guide** students who are stuck

### 3. Facilitation Guidance

For each tutorial section (Opening, Main Activity, Quiz, Wrap-up):
- **Time management tips** (what to do if running over/under)
- **Key discussion points** to emphasize
- **Differentiation strategies** (for struggling/advanced students)
- **Cultural considerations** (Vietnamese student context)

### 4. Rubric Application Guide

For peer review activity:
- **How to model** using the rubric
- **Example feedback** using rubric language
- **Common peer review pitfalls** to avoid
- **When to intervene** during peer review

### 5. Assessment Preparation

- **How this tutorial connects** to the actual graded assessment
- **Key skills practiced** that will be graded
- **Follow-up activities** students can do to improve

## Output Format

Use clear markdown structure:
- H2 for main sections (Quiz Answer Key, Expected Approaches, etc.)
- H3 for subsections
- Clear, actionable guidance for tutors
- Specific examples where helpful

NOTE: These are tutor-facing notes, not student materials.
Keep them separate from tutorial-content.md.
"""

        return context

    def validate_generated_notes(self, content: str) -> Tuple[bool, List[str]]:
        """
        Validate generated tutor notes.

        Args:
            content: Generated tutor notes markdown

        Returns:
            (is_valid, list_of_issues)
        """
        issues = []

        # Check for required sections
        required_sections = [
            r'##\s*Quiz.*Answer.*Key',
            r'##\s*Expected.*Approach',
            r'##\s*Facilitation.*Guidance'
        ]

        for section_pattern in required_sections:
            if not re.search(section_pattern, content, re.IGNORECASE):
                issues.append(f"Missing required section matching: {section_pattern}")

        # Check for answer key content
        if 'correct answer' not in content.lower() and 'answer:' not in content.lower():
            issues.append("Answer key appears incomplete (no 'Correct Answer' labels)")

        # Check for explanations
        if 'explanation' not in content.lower() and 'why' not in content.lower():
            issues.append("Missing explanations for quiz answers")

        # Check for multiple approaches
        approaches_count = content.lower().count('approach')
        if approaches_count < 3:
            issues.append(f"Insufficient student approaches documented: {approaches_count} (minimum 3)")

        # Check for cultural considerations
        if 'vietnamese' not in content.lower() and 'cultural' not in content.lower():
            issues.append("Missing cultural considerations for Vietnamese students")

        return (len(issues) == 0, issues)


# For testing/development
def create_tutor_notes_manually(course_path: Path, week_number: int, content: str) -> Tuple[bool, str]:
    """
    Helper function to manually save tutor notes.

    Args:
        course_path: Path to course directory
        week_number: Week number
        content: Tutor notes markdown content

    Returns:
        (success, message)
    """
    generator = TutorNotesGenerator(course_path, week_number)

    # Validate content
    is_valid, issues = generator.validate_generated_notes(content)

    if not is_valid:
        return (False, f"Validation failed: {', '.join(issues)}")

    # Save content
    generator.save_content("tutorial-tutor-notes.md", content)

    return (True, f"Tutor notes saved to: {generator.week_dir / 'tutorial-tutor-notes.md'}")
