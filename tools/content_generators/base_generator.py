#!/usr/bin/env python3
"""
Base generator class for content generation.

Provides common functionality for all content generators.
"""

import re
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    """Abstract base class for content generators."""

    def __init__(self, course_path: Path, week_number: int):
        """
        Initialize generator.

        Args:
            course_path: Path to course directory
            week_number: Week number to generate
        """
        self.course_path = Path(course_path)
        self.week_number = week_number
        self.week_dir = course_path / "weeks" / f"week-{week_number:02d}"
        self.week_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def generate(self) -> Tuple[bool, str]:
        """
        Generate content.

        Returns:
            (success, error_message)
        """
        pass

    def read_syllabus(self) -> str:
        """Read syllabus content."""
        syllabus_path = self.course_path / "syllabus.md"

        if not syllabus_path.exists():
            raise FileNotFoundError(f"Syllabus not found: {syllabus_path}")

        return syllabus_path.read_text(encoding='utf-8')

    def read_assessment_handbook(self) -> Optional[str]:
        """Read assessment handbook if it exists."""
        handbook_path = self.course_path / "assessment-handbook.md"

        if handbook_path.exists():
            return handbook_path.read_text(encoding='utf-8')

        return None

    def read_research(self) -> str:
        """Read research for this week."""
        research_path = self.course_path / ".working" / "research" / "article-research-summary.md"

        if not research_path.exists():
            raise FileNotFoundError(f"Research not found: {research_path}")

        content = research_path.read_text(encoding='utf-8')

        # Extract this week's research
        week_section = self._extract_week_section(content, self.week_number)

        return week_section

    def get_week_topic(self) -> str:
        """Extract week topic from syllabus."""
        syllabus = self.read_syllabus()

        # Pattern: **Week N: Topic**
        pattern = rf'\*\*Week {self.week_number}[:\-]\s*(.+?)\*\*'
        match = re.search(pattern, syllabus)

        if match:
            return match.group(1).strip()

        return f"Week {self.week_number}"

    def get_learning_objectives(self) -> List[str]:
        """Extract learning objectives from syllabus."""
        syllabus = self.read_syllabus()

        # Look for objectives in the week section
        week_section = self._extract_week_section(syllabus, self.week_number)

        objectives = []

        # Pattern: - Objective text or numbered objectives
        obj_patterns = [
            r'^\s*[-•]\s*(.+)$',  # Bulleted
            r'^\s*\d+\.\s*(.+)$'  # Numbered
        ]

        in_objectives = False
        for line in week_section.split('\n'):
            # Check if we're in objectives section
            if 'objective' in line.lower() or 'learning outcome' in line.lower():
                in_objectives = True
                continue

            if in_objectives:
                # Stop at next heading or empty line after objectives
                if line.startswith('#') or (not line.strip() and objectives):
                    break

                # Try to match objective patterns
                for pattern in obj_patterns:
                    match = re.match(pattern, line)
                    if match:
                        objectives.append(match.group(1).strip())
                        break

        return objectives

    def get_assessment_info(self) -> Dict[str, any]:
        """Extract relevant assessment information for this week."""
        syllabus = self.read_syllabus()
        handbook = self.read_assessment_handbook()

        # Look for assessment mentions in the week section
        week_section = self._extract_week_section(syllabus, self.week_number)

        assessment_info = {
            'due_this_week': [],
            'upcoming': [],
            'relevant_rubrics': []
        }

        # Check for assessment keywords
        assessment_keywords = ['assignment', 'portfolio', 'presentation', 'quiz', 'exam', 'project']

        for line in week_section.split('\n'):
            line_lower = line.lower()
            for keyword in assessment_keywords:
                if keyword in line_lower and ('due' in line_lower or 'submit' in line_lower):
                    assessment_info['due_this_week'].append(line.strip())

        return assessment_info

    def _extract_week_section(self, content: str, week_num: int) -> str:
        """
        Extract section for specific week from content.

        Args:
            content: Full content
            week_num: Week number

        Returns:
            Section text for that week
        """
        # Pattern: **Week N: ... until **Week N+1:
        start_pattern = rf'\*\*Week {week_num}[:\-]'
        next_pattern = rf'\*\*Week {week_num + 1}[:\-]'

        start_match = re.search(start_pattern, content)
        if not start_match:
            return ""

        start_pos = start_match.start()

        # Find next week or end of document
        next_match = re.search(next_pattern, content[start_pos:])
        if next_match:
            end_pos = start_pos + next_match.start()
        else:
            end_pos = len(content)

        return content[start_pos:end_pos]

    def read_lecture_instructions(self) -> str:
        """Read lecture content generation instructions."""
        instructions_path = self.course_path.parent.parent / "lecture_content_instructions.md"

        if instructions_path.exists():
            return instructions_path.read_text(encoding='utf-8')

        return ""

    def save_content(self, filename: str, content: str) -> None:
        """
        Save generated content to file.

        Args:
            filename: Output filename
            content: Content to save
        """
        output_path = self.week_dir / filename
        output_path.write_text(content, encoding='utf-8')
