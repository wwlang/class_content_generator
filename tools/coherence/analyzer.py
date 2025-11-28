#!/usr/bin/env python3
"""
Content extraction and analysis for coherence enhancement.

Extracts terms, concepts, examples, citations, and frameworks from course content.
"""

import re
from pathlib import Path
from typing import List, Optional, Set
from dataclasses import replace

from ..core_structures import (
    WeekContent,
    Term,
    TermUsage,
    Concept,
    Example,
    Citation,
    Framework
)


class ContentExtractor:
    """Extract content from all weeks for analysis."""

    def __init__(self, course_path: Path):
        """
        Initialize extractor.

        Args:
            course_path: Path to course directory
        """
        self.course_path = course_path
        self.weeks_path = course_path / "weeks"

    def extract_all_weeks(self) -> List[WeekContent]:
        """
        Extract content from all generated weeks.

        Returns:
            List of WeekContent objects
        """
        week_contents = []

        if not self.weeks_path.exists():
            return week_contents

        # Find all week directories
        week_dirs = sorted([d for d in self.weeks_path.iterdir() if d.is_dir() and d.name.startswith("week-")])

        for week_dir in week_dirs:
            # Extract week number from directory name (e.g., "week-05" -> 5)
            try:
                week_num = int(week_dir.name.split("-")[1])
            except (IndexError, ValueError):
                continue

            week_content = self._extract_week(week_num, week_dir)
            if week_content:
                week_contents.append(week_content)

        return week_contents

    def _extract_week(self, week_num: int, week_dir: Path) -> Optional[WeekContent]:
        """
        Extract content from a single week.

        Args:
            week_num: Week number
            week_dir: Path to week directory

        Returns:
            WeekContent object or None if files missing
        """
        lecture_path = week_dir / "lecture-content.md"
        tutorial_path = week_dir / "tutorial-content.md"

        if not lecture_path.exists() or not tutorial_path.exists():
            return None

        # Read content
        lecture_content = lecture_path.read_text(encoding='utf-8')
        tutorial_content = tutorial_path.read_text(encoding='utf-8')

        # Extract topic from lecture (first H1 heading)
        topic = self._extract_topic(lecture_content)

        # Create week content object
        week_content = WeekContent(
            week_number=week_num,
            topic=topic,
            lecture_path=lecture_path,
            tutorial_path=tutorial_path,
            word_count_lecture=len(lecture_content.split()),
            word_count_tutorial=len(tutorial_content.split())
        )

        # Extract various elements
        week_content.terms = self._extract_terms(lecture_content, tutorial_content, week_num)
        week_content.concepts = self._extract_concepts(lecture_content, tutorial_content, week_num)
        week_content.examples = self._extract_examples(lecture_content, tutorial_content, week_num)
        week_content.citations = self._extract_citations(lecture_content, tutorial_content, week_num)
        week_content.frameworks = self._extract_frameworks(lecture_content, tutorial_content, week_num)

        return week_content

    def _extract_topic(self, markdown_content: str) -> str:
        """Extract week topic from markdown."""
        # Look for first H1 heading
        match = re.search(r'^#\s+(.+)$', markdown_content, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return "Unknown Topic"

    def _extract_terms(self, lecture_content: str, tutorial_content: str, week_num: int) -> List[Term]:
        """
        Extract key terms from content.

        Looks for:
        - **bolded terms**
        - Terms followed by definition patterns
        - Terms in definition lists

        Args:
            lecture_content: Lecture markdown
            tutorial_content: Tutorial markdown
            week_num: Week number

        Returns:
            List of Term objects
        """
        terms = {}  # {normalized: Term}

        # Extract from lecture
        lecture_terms = self._find_bolded_terms(lecture_content, week_num, "lecture")
        for term in lecture_terms:
            normalized = term.normalized
            if normalized in terms:
                terms[normalized].uses.extend(term.uses)
            else:
                terms[normalized] = term

        # Extract from tutorial
        tutorial_terms = self._find_bolded_terms(tutorial_content, week_num, "tutorial")
        for term in tutorial_terms:
            normalized = term.normalized
            if normalized in terms:
                terms[normalized].uses.extend(term.uses)
            else:
                terms[normalized] = term

        return list(terms.values())

    def _find_bolded_terms(self, content: str, week_num: int, file_type: str) -> List[Term]:
        """Find bolded terms in markdown."""
        terms = []
        seen = set()

        # Pattern: **term** or __term__
        pattern = r'\*\*([^*]+)\*\*|__([^_]+)__'

        for line_num, line in enumerate(content.split('\n'), 1):
            for match in re.finditer(pattern, line):
                term_text = match.group(1) or match.group(2)
                term_text = term_text.strip()

                if not term_text or len(term_text) < 2:
                    continue

                normalized = self._normalize_term(term_text)

                if normalized not in seen:
                    seen.add(normalized)

                    # Check if this is a definition (line contains "is" or ":" after the term)
                    is_definition = bool(re.search(r':\s|\bis\b|\bmeans\b|\brefers to\b', line))

                    term_usage = TermUsage(
                        week=week_num,
                        file=file_type,
                        line_number=line_num,
                        context=line[:100],  # First 100 chars of line
                        is_definition=is_definition
                    )

                    term = Term(
                        text=term_text,
                        normalized=normalized,
                        first_use_week=week_num,
                        uses=[term_usage]
                    )
                    terms.append(term)

        return terms

    def _normalize_term(self, term: str) -> str:
        """Normalize term for comparison."""
        # Lowercase, strip punctuation
        normalized = term.lower().strip()
        # Remove common punctuation
        normalized = re.sub(r'[,\.;:!?]$', '', normalized)
        return normalized

    def _extract_concepts(self, lecture_content: str, tutorial_content: str, week_num: int) -> List[Concept]:
        """
        Extract concepts and frameworks.

        Looks for:
        - Section headings
        - Definition patterns
        - Framework/model mentions

        Args:
            lecture_content: Lecture markdown
            tutorial_content: Tutorial markdown
            week_num: Week number

        Returns:
            List of Concept objects
        """
        concepts = []

        # Extract from section headings (H2, H3)
        heading_pattern = r'^##\s+(.+)$|^###\s+(.+)$'

        for match in re.finditer(heading_pattern, lecture_content, re.MULTILINE):
            concept_name = match.group(1) or match.group(2)
            concept_name = concept_name.strip()

            # Skip generic headings
            if concept_name.lower() in ['introduction', 'conclusion', 'summary', 'references', 'objectives']:
                continue

            # Look for definition in following lines
            start_pos = match.end()
            next_section = re.search(r'^##', lecture_content[start_pos:], re.MULTILINE)
            section_end = start_pos + next_section.start() if next_section else len(lecture_content)
            section_text = lecture_content[start_pos:section_end]

            definition = self._extract_definition(section_text)

            concept = Concept(
                name=concept_name,
                introduced_week=week_num,
                definition=definition
            )
            concepts.append(concept)

        return concepts

    def _extract_definition(self, text: str, max_length: int = 200) -> str:
        """Extract first definition-like sentence from text."""
        # Look for definition patterns in first few sentences
        sentences = re.split(r'[.!?]\s+', text[:500])

        for sentence in sentences[:3]:  # Check first 3 sentences
            if re.search(r'\bis\b|\bmeans\b|\brefers to\b|\bdefined as\b', sentence, re.IGNORECASE):
                return sentence.strip()[:max_length]

        return ""

    def _extract_examples(self, lecture_content: str, tutorial_content: str, week_num: int) -> List[Example]:
        """
        Extract examples and case studies.

        Looks for:
        - "Example:" or "For example" markers
        - Company names (capitalized words)
        - Case study sections

        Args:
            lecture_content: Lecture markdown
            tutorial_content: Tutorial markdown
            week_num: Week number

        Returns:
            List of Example objects
        """
        examples = []

        # Pattern: "Example:", "For example", "Case study:", etc.
        example_markers = [
            r'Example:\s*(.+)',
            r'For example,\s*(.+)',
            r'Case study:\s*(.+)',
            r'Consider\s+(.+)',
        ]

        combined_pattern = '|'.join(example_markers)

        # Extract from lecture
        for match in re.finditer(combined_pattern, lecture_content, re.IGNORECASE):
            example_text = match.group(1) or match.group(2) or match.group(3) or match.group(4)
            if example_text:
                example_text = example_text.strip()[:200]  # First 200 chars

                # Try to identify domain and context
                domain = self._classify_domain(example_text)
                context = self._classify_context(example_text)
                company = self._extract_company_name(example_text)

                example = Example(
                    text=example_text,
                    week=week_num,
                    file="lecture",
                    domain=domain,
                    context=context,
                    usage_type="illustration",
                    company_name=company
                )
                examples.append(example)

        return examples

    def _classify_domain(self, text: str) -> str:
        """Classify example domain/industry."""
        text_lower = text.lower()

        domains = {
            "technology": ["tech", "software", "app", "digital", "platform", "ai", "data"],
            "finance": ["bank", "finance", "investment", "trading", "stock"],
            "retail": ["retail", "store", "shopping", "customer", "product"],
            "healthcare": ["health", "medical", "hospital", "patient"],
            "education": ["education", "university", "school", "student"],
            "manufacturing": ["manufact", "factory", "production", "supply chain"]
        }

        for domain, keywords in domains.items():
            if any(keyword in text_lower for keyword in keywords):
                return domain

        return "general"

    def _classify_context(self, text: str) -> str:
        """Classify example context (geographic/cultural)."""
        text_lower = text.lower()

        if any(keyword in text_lower for keyword in ["vietnam", "vietnamese", "hanoi", "saigon", "hcmc"]):
            return "vietnamese"
        elif any(keyword in text_lower for keyword in ["asia", "asean", "southeast asia"]):
            return "asian"
        elif any(keyword in text_lower for keyword in ["us", "american", "united states"]):
            return "us"
        else:
            return "global"

    def _extract_company_name(self, text: str) -> Optional[str]:
        """Extract company name from text if present."""
        # Look for capitalized words (2+ words)
        pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return None

    def _extract_citations(self, lecture_content: str, tutorial_content: str, week_num: int) -> List[Citation]:
        """
        Extract citations.

        Looks for:
        - Inline citations (Author, Year)
        - Reference lists
        - Speaker notes references

        Args:
            lecture_content: Lecture markdown
            tutorial_content: Tutorial markdown
            week_num: Week number

        Returns:
            List of Citation objects
        """
        citations = []

        # Pattern: (Author, Year) or (Author et al., Year)
        inline_pattern = r'\(([A-Z][a-z]+(?:\s+et al\.)?),\s*(\d{4})\)'

        for match in re.finditer(inline_pattern, lecture_content):
            author = match.group(1)
            year = match.group(2)

            citation = Citation(
                text=match.group(0),
                week=week_num,
                file="lecture",
                format_type="inline",
                is_apa_7th=True,  # Assuming if it matches pattern
                author=author,
                year=year
            )
            citations.append(citation)

        return citations

    def _extract_frameworks(self, lecture_content: str, tutorial_content: str, week_num: int) -> List[Framework]:
        """
        Extract frameworks and models.

        Looks for:
        - "X Model", "X Framework", "X Theory"
        - Lists of components

        Args:
            lecture_content: Lecture markdown
            tutorial_content: Tutorial markdown
            week_num: Week number

        Returns:
            List of Framework objects
        """
        frameworks = []

        # Pattern: [Name] Model/Framework/Theory/Principle
        framework_pattern = r'([A-Z][A-Za-z\s]+?)\s+(Model|Framework|Theory|Principle|Approach)'

        for match in re.finditer(framework_pattern, lecture_content):
            name = match.group(1).strip()
            framework_type = match.group(2).lower()

            # Skip very short names
            if len(name) < 3:
                continue

            framework = Framework(
                name=name,
                week=week_num,
                type=framework_type
            )
            frameworks.append(framework)

        return frameworks
