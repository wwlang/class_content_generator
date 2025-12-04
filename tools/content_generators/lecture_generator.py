#!/usr/bin/env python3
"""
Lecture content generator.

Generates lecture slides with speaker notes following the reference design system.
"""

import re
from pathlib import Path
from typing import Tuple
from .base_generator import BaseGenerator


class LectureGenerator(BaseGenerator):
    """Generate lecture content for a week."""

    def __init__(self, course_path: Path, week_number: int):
        """
        Initialize lecture generator.

        Args:
            course_path: Path to course directory
            week_number: Week number to generate
        """
        super().__init__(course_path, week_number)

    def generate(self) -> Tuple[bool, str]:
        """
        Generate lecture content.

        This creates the prompt/context for Claude to generate the lecture.
        In production, this would call Claude API or be used manually.

        Returns:
            (success, error_message)
        """
        try:
            # Check if already exists
            output_file = self.week_dir / "lecture-content.md"
            if output_file.exists():
                return (True, "Lecture already exists")

            # Gather context
            topic = self.get_week_topic()
            objectives = self.get_learning_objectives()
            research = self.read_research()
            assessment_info = self.get_assessment_info()
            instructions = self.read_lecture_instructions()

            # Create generation context
            context = self._create_generation_context(
                topic, objectives, research, assessment_info, instructions
            )

            # In production, this would call Claude API
            # For now, save the context and return instructions
            context_file = self.week_dir / ".lecture-generation-context.md"
            context_file.write_text(context, encoding='utf-8')

            error_msg = (
                f"Lecture generation context created at: {context_file}\n\n"
                f"To generate lecture content:\n"
                f"1. Use Claude Code with /generate-week {self.week_number}\n"
                f"   OR\n"
                f"2. Manually provide the context to Claude and save output to:\n"
                f"   {output_file}\n\n"
                f"The context includes topic, objectives, research, and formatting instructions."
            )

            return (False, error_msg)

        except Exception as e:
            return (False, f"Error generating lecture: {str(e)}")

    def _create_generation_context(
        self,
        topic: str,
        objectives: list,
        research: str,
        assessment_info: dict,
        instructions: str
    ) -> str:
        """
        Create the context/prompt for lecture generation.

        This follows the lecture_content_instructions.md format.
        """
        context = f"""# Lecture Generation Context - Week {self.week_number}

## Course Information
- Week: {self.week_number}
- Topic: {topic}

## Learning Objectives
"""
        if objectives:
            for i, obj in enumerate(objectives, 1):
                context += f"{i}. {obj}\n"
        else:
            context += "- Extract from syllabus or research articles\n"

        context += f"""
## Assessment Connection
"""
        if assessment_info.get('due_this_week'):
            context += "Assessments due this week:\n"
            for assessment in assessment_info['due_this_week']:
                context += f"- {assessment}\n"
        else:
            context += "- Check syllabus for relevant assessments\n"

        context += f"""
## Research Articles

{research}

## Generation Instructions

{instructions if instructions else "Follow lecture_content_instructions.md"}

## Output Requirements

Generate lecture content with:

1. **Structure:**
   - Opening (4-6 slides): Hook, objectives, assessment connection
   - Core content (14-20 slides): 3-4 logical segments
   - Wrap-up (4-6 slides): Synthesis, preview, reflection

2. **Format:**
   - Each slide starts with: **SLIDE N: Title**
   - Slide content (with layout hints where appropriate)
   - Speaker notes after ## Speaker Notes

3. **Citations:**
   - Inline: (Author, Year) for all statistics/research
   - Full APA 7th references with DOI/URL after each slide

4. **Examples:**
   - Current (2023-2025)
   - Vietnam-specific where relevant
   - Culturally diverse

5. **Engagement:**
   - Activities every 15-20 minutes
   - Think-pair-share, polls, case discussions

Total: 22-30 slides
"""

        return context

    def validate_generated_lecture(self, content: str) -> Tuple[bool, list]:
        """
        Validate generated lecture content.

        Args:
            content: Generated lecture markdown

        Returns:
            (is_valid, list_of_issues)
        """
        issues = []

        # Count slides
        slide_count = content.count("**SLIDE")
        if slide_count < 24:
            issues.append(f"Too few slides: {slide_count} (minimum 24)")

        # Check for speaker notes
        notes_count = content.count("## Speaker Notes")
        if notes_count < slide_count * 0.8:  # At least 80% of slides should have notes
            issues.append(f"Insufficient speaker notes: {notes_count}/{slide_count}")

        # Check for citations
        inline_citations = len(re.findall(r'\([A-Z][a-z]+,\s*\d{4}\)', content))
        if inline_citations < 5:
            issues.append(f"Too few inline citations: {inline_citations} (minimum 5)")

        # Check for full references
        full_refs = len(re.findall(r'\*[A-Z][^*]+\(\d{4}\)[^*]+\*', content))
        if full_refs < 3:
            issues.append(f"Too few full references: {full_refs} (minimum 3)")

        return (len(issues) == 0, issues)


# For testing/development: Manual generation helper
def create_lecture_manually(course_path: Path, week_number: int, content: str) -> Tuple[bool, str]:
    """
    Helper function to manually save lecture content.

    Use this during development/testing to provide pre-written content.

    Args:
        course_path: Path to course directory
        week_number: Week number
        content: Lecture markdown content

    Returns:
        (success, message)
    """
    generator = LectureGenerator(course_path, week_number)

    # Validate content
    is_valid, issues = generator.validate_generated_lecture(content)

    if not is_valid:
        return (False, f"Validation failed: {', '.join(issues)}")

    # Save content
    output_file = generator.week_dir / "lecture-content.md"
    generator.save_content("lecture-content.md", content)

    return (True, f"Lecture saved to: {output_file}")
