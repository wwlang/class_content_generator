#!/usr/bin/env python3
"""
Lecture content parser framework.

Provides parser for lecture-content.md files in XML format.
"""

from dataclasses import dataclass
from typing import List, Optional
import re


@dataclass
class SlideData:
    """Structured representation of a lecture slide."""

    number: int
    title: str
    content: str
    speaker_notes: str
    layout: str = "content"  # Default layout

    def __repr__(self) -> str:
        return f"Slide {self.number}: {self.title} ({self.layout})"


@dataclass
class LectureData:
    """Structured representation of a complete lecture."""

    topic: str
    week_number: int
    slides: List[SlideData]
    course_code: str = ""
    instructor: str = ""

    @property
    def slide_count(self) -> int:
        """Total number of slides."""
        return len(self.slides)

    def get_slide(self, number: int) -> Optional[SlideData]:
        """Get slide by number."""
        for slide in self.slides:
            if slide.number == number:
                return slide
        return None


class XMLParser:
    """Parser for XML-format lecture content."""

    def can_parse(self, content: str) -> bool:
        """Check if content is XML format."""
        return bool(re.search(r'<slide\s+[^>]*number=', content))

    def count_slides(self, content: str) -> int:
        """Count slides in XML format."""
        return len(re.findall(r'<slide\s+[^>]+>', content))

    def parse(self, content: str) -> LectureData:
        """Parse XML lecture content."""
        if not self.can_parse(content):
            raise ValueError("Content is not valid XML lecture format. Expected <slide> tags.")

        # Extract topic from XML metadata (multiple formats)
        topic = None

        # Try child elements first: <topic>...</topic> or <title>...</title>
        topic_xml = re.search(r'<topic>([^<]+)</topic>', content)
        if not topic_xml:
            topic_xml = re.search(r'<title>([^<]+)</title>', content)
        if topic_xml:
            topic = topic_xml.group(1).strip()

        # Try lecture tag attributes: topic="..." or title="..."
        if not topic:
            lecture_topic = re.search(r'<lecture[^>]+topic="([^"]+)"', content)
            if not lecture_topic:
                lecture_topic = re.search(r'<lecture[^>]+title="([^"]+)"', content)
            if lecture_topic:
                topic = lecture_topic.group(1).strip()

        # Fallback to first H1 or slide title
        if not topic:
            topic_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if topic_match:
                topic = topic_match.group(1).strip()
            else:
                # Try first slide title
                title_match = re.search(r'<slide[^>]+title="([^"]+)"', content)
                topic = title_match.group(1) if title_match else "Unknown Topic"

        # Remove "Week N:" prefix if present
        topic = re.sub(r'^Week\s+\d+:\s*', '', topic, count=1, flags=re.IGNORECASE)

        # Extract week number
        week_match = re.search(r'Week\s+(\d+)', content, re.IGNORECASE)
        week_number = int(week_match.group(1)) if week_match else 0

        # Parse slides
        slides = self._parse_slides(content)

        return LectureData(
            topic=topic,
            week_number=week_number,
            slides=slides
        )

    def _parse_slides(self, content: str) -> List[SlideData]:
        """Extract all slides from XML content."""
        slides = []

        # Find all <slide> tags with content
        slide_pattern = r'<slide\s+([^>]+)>(.*?)</slide>'
        matches = re.finditer(slide_pattern, content, re.DOTALL)

        for match in matches:
            attrs_str = match.group(1)
            slide_content_full = match.group(2).strip()

            # Parse attributes
            number = self._extract_attr(attrs_str, 'number')
            title = self._extract_attr(attrs_str, 'title', '')
            layout = self._extract_attr(attrs_str, 'layout', 'content')

            # Extract speaker notes
            notes_match = re.search(
                r'<speaker-notes>(.*?)</speaker-notes>',
                slide_content_full,
                re.DOTALL
            )

            if notes_match:
                speaker_notes = notes_match.group(1).strip()
                # Remove notes from content
                slide_content = slide_content_full[:notes_match.start()].strip()
            else:
                speaker_notes = ""
                slide_content = slide_content_full

            slides.append(SlideData(
                number=int(number),
                title=title,
                content=slide_content,
                speaker_notes=speaker_notes,
                layout=layout
            ))

        return slides

    def _extract_attr(self, attrs_str: str, attr_name: str, default: str = None) -> str:
        """Extract attribute value from attribute string."""
        pattern = rf'{attr_name}="([^"]*)"'
        match = re.search(pattern, attrs_str)

        if match:
            return match.group(1)
        elif default is not None:
            return default
        else:
            raise ValueError(f"Required attribute '{attr_name}' not found")


def create_parser(content: str) -> XMLParser:
    """
    Factory function to create parser.

    Args:
        content: Raw lecture content string

    Returns:
        XMLParser instance

    Raises:
        ValueError: If content is not valid XML format
    """
    parser = XMLParser()
    if not parser.can_parse(content):
        raise ValueError("Content is not valid XML lecture format. Expected <slide> tags.")
    return parser
