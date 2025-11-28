#!/usr/bin/env python3
"""
Tutorial content generator.

Generates 90-minute tutorial activities that align with assessments.
"""

import re
from pathlib import Path
from typing import Tuple, Dict, List
from .base_generator import BaseGenerator


class TutorialGenerator(BaseGenerator):
    """Generate tutorial content for a week."""

    def __init__(self, course_path: Path, week_number: int):
        """
        Initialize tutorial generator.

        Args:
            course_path: Path to course directory
            week_number: Week number to generate
        """
        super().__init__(course_path, week_number)

    def generate(self) -> Tuple[bool, str]:
        """
        Generate tutorial content.

        Creates context for Claude to generate 90-min tutorial with assessment alignment.

        Returns:
            (success, error_message)
        """
        try:
            # Check if already exists
            output_file = self.week_dir / "tutorial-content.md"
            if output_file.exists():
                return (True, "Tutorial already exists")

            # Gather context
            topic = self.get_week_topic()
            objectives = self.get_learning_objectives()
            assessment_info = self.get_assessment_info()
            rubric_info = self._extract_rubric_info()

            # Create generation context
            context = self._create_generation_context(
                topic, objectives, assessment_info, rubric_info
            )

            # Save context
            context_file = self.week_dir / ".tutorial-generation-context.md"
            context_file.write_text(context, encoding='utf-8')

            error_msg = (
                f"Tutorial generation context created at: {context_file}\n\n"
                f"To generate tutorial content:\n"
                f"1. Use Claude Code with /generate-week {self.week_number}\n"
                f"   OR\n"
                f"2. Manually provide the context to Claude and save output to:\n"
                f"   {output_file}\n\n"
                f"The context includes topic, objectives, assessment alignment, and rubric."
            )

            return (False, error_msg)

        except Exception as e:
            return (False, f"Error generating tutorial: {str(e)}")

    def _extract_rubric_info(self) -> Dict[str, any]:
        """Extract relevant rubric information for this week's assessment."""
        rubric_info = {
            'assessment_type': None,
            'criteria': [],
            'simplified_criteria': []
        }

        # Read syllabus and handbook
        syllabus = self.read_syllabus()
        handbook = self.read_assessment_handbook()

        # Look for rubric sections in handbook or syllabus
        content = handbook if handbook else syllabus

        # Find rubric sections
        # Pattern: ## Assessment Name followed by rubric criteria
        rubric_patterns = [
            r'###?\s*(Portfolio|Presentation|Project|Essay|Report)\s*Rubric',
            r'###?\s*Rubric\s*[-:]?\s*(Portfolio|Presentation|Project|Essay|Report)'
        ]

        for pattern in rubric_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                rubric_info['assessment_type'] = match.group(1)

                # Extract criteria (look for table or bullet list after rubric heading)
                section_start = match.end()
                section_text = content[section_start:section_start + 2000]  # Next 2000 chars

                # Extract criteria from table or list
                criteria = self._extract_criteria_from_text(section_text)
                if criteria:
                    rubric_info['criteria'] = criteria
                    rubric_info['simplified_criteria'] = self._simplify_criteria(criteria)
                    break

        return rubric_info

    def _extract_criteria_from_text(self, text: str) -> List[str]:
        """Extract rubric criteria from text."""
        criteria = []

        # Try table format first (| Criteria | Description |)
        if '|' in text:
            table_rows = [line for line in text.split('\n') if line.strip().startswith('|')]
            for row in table_rows[2:]:  # Skip header and separator
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                if cells and cells[0] and not cells[0].startswith('-'):
                    criteria.append(cells[0])

        # Try bullet list format
        else:
            bullet_pattern = r'^\s*[-•*]\s*\*\*([^*]+)\*\*'
            for line in text.split('\n'):
                match = re.match(bullet_pattern, line)
                if match:
                    criteria.append(match.group(1).strip())

        return criteria[:6]  # Max 6 criteria

    def _simplify_criteria(self, criteria: List[str]) -> List[str]:
        """
        Simplify rubric criteria for tutorial use.

        Takes full assessment rubric criteria and creates simplified 3-4 criteria.
        """
        if not criteria:
            return []

        # If already 3-4 criteria, return as-is
        if len(criteria) <= 4:
            return criteria

        # Otherwise, group similar criteria
        # For now, take first 4 most important
        # In production, this would use smarter grouping
        return criteria[:4]

    def _create_generation_context(
        self,
        topic: str,
        objectives: list,
        assessment_info: dict,
        rubric_info: dict
    ) -> str:
        """Create the context/prompt for tutorial generation."""
        context = f"""# Tutorial Generation Context - Week {self.week_number}

## Course Information
- Week: {self.week_number}
- Topic: {topic}

## Learning Objectives
"""
        if objectives:
            for i, obj in enumerate(objectives, 1):
                context += f"{i}. {obj}\n"
        else:
            context += "- Extract from syllabus\n"

        context += f"""
## Assessment Alignment

"""
        if assessment_info.get('due_this_week'):
            context += "**Assessments due this week:**\n"
            for assessment in assessment_info['due_this_week']:
                context += f"- {assessment}\n"
            context += "\n"

        if rubric_info.get('assessment_type'):
            context += f"**Assessment Type:** {rubric_info['assessment_type']}\n\n"

            if rubric_info.get('simplified_criteria'):
                context += "**Simplified Rubric (for tutorial use):**\n"
                for i, criterion in enumerate(rubric_info['simplified_criteria'], 1):
                    context += f"{i}. {criterion}\n"
                context += "\n"

        context += """
## Tutorial Structure (90 minutes)

Generate tutorial content with:

### 1. Opening (10 min)
- Quick review of lecture concepts
- Assessment preview (what they'll practice today)
- Introduce simplified rubric

### 2. Main Activity (55-60 min)
- **ONE activity that directly mirrors the actual assessment**
- Uses simplified rubric (3-4 key criteria from full rubric)
- Structure:
  - Setup and instructions (5 min)
  - Individual/group work (20-25 min)
  - Peer review using rubric language (15 min)
  - Revision based on feedback (10 min)
  - Debrief and Q&A (5-10 min)

### 3. Quiz Prep (15-20 min)
- 5-8 multiple choice/short answer questions
- Cover key concepts from lecture and readings
- Similar format to actual quiz
- Review answers together

### 4. Wrap-up (5-10 min)
- Self-assessment against simplified rubric
- Preview next week
- Final questions

## Cultural Considerations
- Vietnamese students: Structured peer interaction, gradual confidence building
- Provide sentence starters for peer feedback
- Clear, numbered instructions
- Examples from Vietnamese context where relevant

## Output Format

Use clear markdown structure:
- H1 for main sections
- H2 for subsections
- Numbered lists for instructions
- Clear time allocations
- Student-facing language (no instructor notes in tutorial content)

NOTE: Tutor notes (answer keys, facilitation guidance) will be generated separately.
"""

        return context

    def validate_generated_tutorial(self, content: str) -> Tuple[bool, List[str]]:
        """
        Validate generated tutorial content.

        Args:
            content: Generated tutorial markdown

        Returns:
            (is_valid, list_of_issues)
        """
        issues = []

        # Check for required sections
        required_sections = [
            r'#.*Opening',
            r'#.*Main Activity',
            r'#.*Quiz',
            r'#.*Wrap'
        ]

        for section_pattern in required_sections:
            if not re.search(section_pattern, content, re.IGNORECASE):
                issues.append(f"Missing required section matching: {section_pattern}")

        # Check for rubric mention
        if 'rubric' not in content.lower():
            issues.append("No rubric mentioned in tutorial")

        # Check for quiz questions
        if content.count('?') < 5:
            issues.append("Insufficient quiz questions (minimum 5)")

        # Check for time allocations
        time_mentions = len(re.findall(r'\d+\s*(?:min|minute)', content, re.IGNORECASE))
        if time_mentions < 4:
            issues.append(f"Insufficient time allocations: {time_mentions} (minimum 4)")

        # Check for peer review/feedback
        if 'peer' not in content.lower() and 'feedback' not in content.lower():
            issues.append("No peer review or feedback activity mentioned")

        return (len(issues) == 0, issues)


# For testing/development
def create_tutorial_manually(course_path: Path, week_number: int, content: str) -> Tuple[bool, str]:
    """
    Helper function to manually save tutorial content.

    Args:
        course_path: Path to course directory
        week_number: Week number
        content: Tutorial markdown content

    Returns:
        (success, message)
    """
    generator = TutorialGenerator(course_path, week_number)

    # Validate content
    is_valid, issues = generator.validate_generated_tutorial(content)

    if not is_valid:
        return (False, f"Validation failed: {', '.join(issues)}")

    # Save content
    generator.save_content("tutorial-content.md", content)

    return (True, f"Tutorial saved to: {generator.week_dir / 'tutorial-content.md'}")
