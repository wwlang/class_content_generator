"""
Parser for assessment-handbook.md files.

Converts assessment handbook markdown into Assessment and Rubric domain objects.
"""

import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass

from ..models import Assessment, AssessmentType, Scenario, Rubric, RubricCriterion


@dataclass
class AssessmentMetadata:
    """Basic metadata from overview table."""
    name: str
    type_str: str
    weight_str: str
    due_week: int
    learning_objectives: List[str]


class HandbookParser:
    """
    Parse assessment-handbook.md files into Assessment and Rubric objects.

    Handles:
    - Assessment overview table
    - Individual assessment sections
    - Scenario options
    - Requirements checklists
    - Rubric tables
    """

    def __init__(self):
        """Initialize parser."""
        self.content = ""
        self.assessments_cache: Dict[str, Assessment] = {}
        self.rubrics_cache: Dict[str, Rubric] = {}

    def parse_file(self, file_path: Path) -> Dict[str, Assessment]:
        """
        Parse assessment handbook file.

        Args:
            file_path: Path to assessment-handbook.md

        Returns:
            Dictionary mapping assessment IDs to Assessment objects

        Raises:
            ValueError: If file cannot be parsed
        """
        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")

        self.content = file_path.read_text(encoding='utf-8')

        # Parse overview table first for metadata
        overview = self._parse_overview_table()

        # Parse rubrics (they're at the end)
        self.rubrics_cache = self._parse_all_rubrics()

        # Parse individual assessment sections
        assessments = {}
        for meta in overview:
            try:
                assessment = self._parse_assessment_section(meta)
                if assessment:
                    assessments[assessment.id] = assessment
            except Exception as e:
                # Log but don't fail entire parse
                print(f"Warning: Could not parse assessment '{meta.name}': {e}")

        return assessments

    def _parse_overview_table(self) -> List[AssessmentMetadata]:
        """Parse the Assessment Overview table."""
        # Find table section
        overview_match = re.search(
            r'## Assessment Overview\s+\|.+?\|.+?\n\|[-|]+\|.+?\n((?:\|.+?\n)+)',
            self.content,
            re.DOTALL
        )

        if not overview_match:
            raise ValueError("Cannot find Assessment Overview table")

        table_rows = overview_match.group(1).strip().split('\n')

        metadata_list = []
        for row in table_rows:
            # Parse: | Email + Memo | Portfolio | 10% | Week 3 | 1, 2, 9, 12 |
            cells = [cell.strip() for cell in row.split('|')[1:-1]]  # Remove empty first/last

            if len(cells) >= 4:
                name = cells[0]
                type_str = cells[1]
                weight_str = cells[2]
                due_str = cells[3]
                objectives_str = cells[4] if len(cells) > 4 else ""

                # Extract week number
                week_match = re.search(r'\d+', due_str)
                due_week = int(week_match.group()) if week_match else 0

                # Parse objectives
                objectives = []
                if objectives_str:
                    # Handle ranges like "1-8" or lists like "1, 2, 9, 12"
                    obj_parts = re.findall(r'\d+(?:-\d+)?', objectives_str)
                    for part in obj_parts:
                        if '-' in part:
                            start, end = map(int, part.split('-'))
                            objectives.extend(str(i) for i in range(start, end + 1))
                        else:
                            objectives.append(part)

                metadata_list.append(AssessmentMetadata(
                    name=name,
                    type_str=type_str,
                    weight_str=weight_str,
                    due_week=due_week,
                    learning_objectives=objectives
                ))

        return metadata_list

    def _parse_assessment_section(self, meta: AssessmentMetadata) -> Optional[Assessment]:
        """Parse individual assessment section."""
        # Skip quizzes for now (they don't have full sections)
        if 'quiz' in meta.name.lower():
            return None

        # Find section header
        # Look for patterns like "### 1. Email + Memo (10%)"
        section_pattern = rf'###\s+\d+\.\s+{re.escape(meta.name)}\s*\(?\d+%?\)?'
        section_match = re.search(section_pattern, self.content, re.IGNORECASE)

        if not section_match:
            # Try without number prefix
            section_pattern = rf'###\s+{re.escape(meta.name)}\s*\(?\d+%?\)?'
            section_match = re.search(section_pattern, self.content, re.IGNORECASE)

        if not section_match:
            return None

        # Extract section content (up to next ### or ##)
        start = section_match.start()
        next_section = re.search(r'\n##[#]?\s+', self.content[start + 10:])
        end = start + 10 + next_section.start() if next_section else len(self.content)

        section_content = self.content[start:end]

        # Parse components
        assessment_type = self._parse_type(meta.type_str)
        weight = self._parse_weight(meta.weight_str)
        description = self._parse_description(section_content)
        scenarios = self._parse_scenarios(section_content)
        requirements = self._parse_requirements(section_content)
        submission_format = self._parse_submission_format(section_content)

        # Find appropriate rubric
        rubric = self._find_rubric_for_assessment(meta.name)

        # Generate assessment ID
        assessment_id = self._slugify(meta.name)

        return Assessment(
            id=assessment_id,
            name=meta.name,
            type=assessment_type,
            weight=weight,
            due_week=meta.due_week,
            description=description,
            requirements=requirements,
            rubric=rubric,
            scenarios=scenarios,
            submission_format=submission_format,
            learning_objectives=meta.learning_objectives
        )

    def _parse_type(self, type_str: str) -> AssessmentType:
        """Convert type string to AssessmentType enum."""
        type_lower = type_str.lower().strip()

        if 'portfolio' in type_lower:
            return AssessmentType.PORTFOLIO
        elif 'presentation' in type_lower:
            return AssessmentType.PRESENTATION
        elif 'quiz' in type_lower:
            return AssessmentType.QUIZ
        elif 'project' in type_lower:
            return AssessmentType.PROJECT
        else:
            return AssessmentType.PORTFOLIO  # Default

    def _parse_weight(self, weight_str: str) -> float:
        """Convert weight string to float (e.g., '10%' -> 0.10)."""
        weight_match = re.search(r'(\d+)', weight_str)
        if weight_match:
            return int(weight_match.group(1)) / 100.0
        return 0.1  # Default 10%

    def _parse_description(self, section: str) -> str:
        """Extract Task Overview description."""
        # Look for "Task Overview" or "Overview" section
        overview_match = re.search(
            r'####\s+(?:Task\s+)?Overview\s*\n+((?:.+?\n)+?)(?:\n####|\Z)',
            section,
            re.DOTALL
        )

        if overview_match:
            description = overview_match.group(1).strip()
            # Clean up markdown list formatting
            description = re.sub(r'^\d+\.\s+\*\*', '• ', description, flags=re.MULTILINE)
            return description

        # Fallback: Get first few paragraphs after header
        lines = section.split('\n')[2:10]  # Skip header
        paragraphs = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('**'):
                paragraphs.append(line)
            if len(paragraphs) >= 3:
                break

        return '\n\n'.join(paragraphs) if paragraphs else "Assessment description"

    def _parse_scenarios(self, section: str) -> List[Scenario]:
        """Parse scenario options."""
        scenarios = []

        # Look for "Scenario (Choose ONE)" or "Scenario Options" section
        scenario_section_match = re.search(
            r'####\s+Scenario.*?\n+((?:.+?\n)+?)(?:\n####|\n\*\*\w)',
            section,
            re.DOTALL | re.IGNORECASE
        )

        if not scenario_section_match:
            return scenarios

        scenario_content = scenario_section_match.group(1)

        # Find Option A, Option B, etc.
        option_pattern = r'\*\*Option\s+([A-Z]):\s+(.+?)\*\*\s*\n((?:.*?\n)+?)(?=\*\*Option|$)'

        for match in re.finditer(option_pattern, scenario_content, re.DOTALL):
            option_letter = match.group(1)
            title = match.group(2).strip()
            description_block = match.group(3).strip()

            # Extract description (text before any sub-bullets)
            description_lines = []
            specific_reqs = []

            for line in description_block.split('\n'):
                line = line.strip()
                if not line:
                    continue
                if line.startswith('- **'):
                    # Specific requirement like "- **Email:** ..."
                    specific_reqs.append(line[2:].strip())
                elif not line.startswith('-'):
                    description_lines.append(line)
                else:
                    # General bullet point
                    description_lines.append(line[2:].strip())

            title_full = f"Option {option_letter}: {title}"
            description = '\n'.join(description_lines)

            scenarios.append(Scenario(
                title=title_full,
                description=description,
                specific_requirements=specific_reqs
            ))

        return scenarios

    def _parse_requirements(self, section: str) -> List[str]:
        """Parse requirements checklist."""
        requirements = []

        # Look for "Requirements" section
        req_section_match = re.search(
            r'####\s+Requirements?\s*\n+((?:.+?\n)+?)(?:\n####|\Z)',
            section,
            re.DOTALL
        )

        if not req_section_match:
            return requirements

        req_content = req_section_match.group(1)

        # Extract checklist items: - [ ] Item text
        checklist_pattern = r'-\s+\[\s*\]\s+(.+)'

        for match in re.finditer(checklist_pattern, req_content):
            requirement = match.group(1).strip()
            requirements.append(requirement)

        # Also capture regular bullet points if no checkboxes found
        if not requirements:
            bullet_pattern = r'^-\s+(.+?)$'
            for match in re.finditer(bullet_pattern, req_content, re.MULTILINE):
                requirement = match.group(1).strip()
                if not requirement.startswith('['):  # Skip checkbox notation
                    requirements.append(requirement)

        return requirements

    def _parse_submission_format(self, section: str) -> Optional[str]:
        """Parse submission format instructions."""
        # Look for "Submission Format" or "Submission" section
        sub_match = re.search(
            r'####\s+Submission(?:\s+Format)?\s*\n+((?:.+?\n)+?)(?:\n####|\n\*\*File|\Z)',
            section,
            re.DOTALL
        )

        if sub_match:
            submission = sub_match.group(1).strip()

            # Also grab file naming if present
            filename_match = re.search(
                r'\*\*File naming:\*\*\s*(.+)',
                section
            )
            if filename_match:
                submission += f"\n\nFile naming: {filename_match.group(1).strip()}"

            return submission

        return None

    def _parse_all_rubrics(self) -> Dict[str, Rubric]:
        """Parse all rubrics from the Rubrics section."""
        rubrics = {}

        # Find Rubrics section
        rubrics_match = re.search(
            r'##\s+Rubrics\s*\n+((?:.+?\n)+?)(?:\n##\s+[^#]|$)',
            self.content,
            re.DOTALL
        )

        if not rubrics_match:
            return rubrics

        rubrics_section = rubrics_match.group(1)

        # Find individual rubric tables
        # Pattern: ### Rubric Name \n (Used for: ...) \n table
        rubric_pattern = r'###\s+(.+?)\s+Rubric\s*\n+((?:Used for:.+?\n)?)(?:\|.+?\n)+\|[-|\s]+\|\s*\n((?:\|.+?\n)+)'

        for match in re.finditer(rubric_pattern, rubrics_section, re.DOTALL):
            rubric_name_base = match.group(1).strip()
            used_for_line = match.group(2).strip()
            table_content = match.group(3).strip()

            rubric_name = f"{rubric_name_base} Rubric"

            # Parse table into criteria
            criteria = self._parse_rubric_table(table_content)

            if criteria:
                rubric = Rubric(
                    name=rubric_name,
                    criteria=criteria,
                    description=used_for_line if used_for_line else None
                )
                rubrics[rubric_name_base.lower()] = rubric

        return rubrics

    def _parse_rubric_table(self, table_content: str) -> List[RubricCriterion]:
        """Parse rubric table rows into RubricCriterion objects."""
        criteria = []

        rows = [row.strip() for row in table_content.split('\n') if row.strip()]

        for row in rows:
            # Parse: | **Content & Strategy** | Excellent desc | Good desc | ... |
            cells = [cell.strip() for cell in row.split('|')[1:-1]]

            if len(cells) >= 6:  # Name + 5 performance levels
                # Extract criterion name (remove ** markdown)
                name_cell = cells[0]
                name = re.sub(r'\*\*(.+?)\*\*', r'\1', name_cell).strip()

                # Skip if this looks like a header row
                if 'criteria' in name.lower() or 'excellent' in cells[1].lower():
                    continue

                # Parse performance levels
                excellent = cells[1].strip()
                good = cells[2].strip()
                satisfactory = cells[3].strip()
                poor = cells[4].strip()
                failing = cells[5].strip()

                # Assume equal weight for now (will be normalized)
                weight = 0.2  # 20% each for 5 criteria

                criterion = RubricCriterion(
                    name=name,
                    weight=weight,
                    excellent=excellent,
                    good=good,
                    satisfactory=satisfactory,
                    poor=poor,
                    failing=failing
                )
                criteria.append(criterion)

        # Normalize weights to sum to 1.0
        if criteria:
            total = sum(c.weight for c in criteria)
            for criterion in criteria:
                criterion.weight = criterion.weight / total

        return criteria

    def _find_rubric_for_assessment(self, assessment_name: str) -> Optional[Rubric]:
        """Find appropriate rubric for an assessment."""
        name_lower = assessment_name.lower()

        # Try direct matches first
        rubric_keywords = {
            'email': 'written communication',
            'memo': 'written communication',
            'data visualization': 'data visualization',
            'proposal': 'persuasive proposal',
            'persuasive': 'persuasive proposal',
            'reflection': 'reflection',
            'pitch': 'presentation',
            'presentation': 'presentation',
        }

        for keyword, rubric_key in rubric_keywords.items():
            if keyword in name_lower:
                rubric = self.rubrics_cache.get(rubric_key)
                if rubric:
                    return rubric

        # Fallback: Return first rubric if available
        if self.rubrics_cache:
            return next(iter(self.rubrics_cache.values()))

        return None

    def _slugify(self, text: str) -> str:
        """Convert text to slug format for IDs."""
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
