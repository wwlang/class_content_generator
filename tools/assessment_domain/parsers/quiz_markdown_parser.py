"""
Parser for quiz-questions.md files.

Converts markdown quiz questions into Question domain objects.
"""

import re
from pathlib import Path
from typing import List, Optional, Dict
from dataclasses import dataclass

from ..models import Question, BloomLevel, QuestionType


@dataclass
class QuizMetadata:
    """Metadata from quiz questions file header."""
    topic: str
    prepares_for: str
    source: str
    week: Optional[int] = None


class QuizMarkdownParser:
    """
    Parse quiz-questions.md files into Question objects.

    Format expected:
    ```markdown
    ### Q1: Topic Name
    **Type:** Multiple Choice
    **Bloom's Level:** Remembering  (optional)

    Question text here?

    A) Option A
    B) Option B
    C) Option C
    D) Option D

    **Answer:** C
    **Feedback:** Explanation with details for all options.
    ```
    """

    def __init__(self, infer_bloom: bool = True):
        """
        Initialize parser.

        Args:
            infer_bloom: If True, attempt to infer Bloom's level from question patterns
        """
        self.infer_bloom = infer_bloom

    def parse_file(self, file_path: Path) -> List[Question]:
        """
        Parse a quiz-questions.md file.

        Args:
            file_path: Path to quiz-questions.md

        Returns:
            List of Question objects

        Raises:
            ValueError: If file cannot be parsed
        """
        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")

        content = file_path.read_text(encoding='utf-8')

        # Extract week number from path
        week = self._extract_week_from_path(file_path)

        # Parse metadata
        metadata = self._parse_metadata(content)
        if metadata.week is None:
            metadata.week = week

        # Split into question sections
        question_sections = self._split_questions(content)

        # Parse each question
        questions = []
        for i, section in enumerate(question_sections, 1):
            try:
                question = self._parse_question(section, week, i)
                questions.append(question)
            except Exception as e:
                raise ValueError(
                    f"Error parsing question {i} in {file_path}: {e}"
                ) from e

        return questions

    def _extract_week_from_path(self, file_path: Path) -> int:
        """Extract week number from file path like .../week-03/quiz-questions.md"""
        week_match = re.search(r'week-(\d+)', str(file_path))
        if week_match:
            return int(week_match.group(1))

        # Try to find it in parent directory names
        for part in file_path.parts:
            if part.startswith('week-'):
                week_num = part.replace('week-', '')
                if week_num.isdigit():
                    return int(week_num)

        raise ValueError(f"Cannot extract week number from path: {file_path}")

    def _parse_metadata(self, content: str) -> QuizMetadata:
        """Parse header metadata from quiz file."""
        metadata = QuizMetadata(
            topic="Unknown",
            prepares_for="Unknown",
            source="lecture-content.md"
        )

        # Extract topic
        topic_match = re.search(r'\*\*Topic:\*\*\s*(.+)', content)
        if topic_match:
            metadata.topic = topic_match.group(1).strip()

        # Extract prepares_for
        prepares_match = re.search(r'\*\*Prepares for:\*\*\s*(.+)', content)
        if prepares_match:
            metadata.prepares_for = prepares_match.group(1).strip()

        # Extract source
        source_match = re.search(r'\*\*Source:\*\*\s*(.+)', content)
        if source_match:
            metadata.source = source_match.group(1).strip()

        return metadata

    def _split_questions(self, content: str) -> List[str]:
        """Split content into individual question sections."""
        # Find all question headers: ### Q1: Topic
        question_pattern = r'###\s+Q\d+:'

        # Find all question start positions
        matches = list(re.finditer(question_pattern, content))

        if not matches:
            raise ValueError("No questions found in file")

        sections = []
        for i, match in enumerate(matches):
            start = match.start()
            # End is start of next question, or end of file
            end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            section = content[start:end].strip()
            sections.append(section)

        return sections

    def _parse_question(self, section: str, week: int, question_number: int) -> Question:
        """
        Parse a single question section.

        Args:
            section: Markdown text for one question
            week: Week number
            question_number: Question number within week

        Returns:
            Question object

        Raises:
            ValueError: If section cannot be parsed
        """
        # Extract topic from header: ### Q1: Topic Name
        topic_match = re.search(r'###\s+Q\d+:\s*(.+)', section)
        if not topic_match:
            raise ValueError("Cannot find question topic in header")
        topic = topic_match.group(1).strip()

        # Extract question type (currently only Multiple Choice supported)
        type_match = re.search(r'\*\*Type:\*\*\s*(.+)', section)
        question_type = QuestionType.MULTIPLE_CHOICE
        if type_match and 'multiple choice' not in type_match.group(1).lower():
            raise ValueError(f"Unsupported question type: {type_match.group(1)}")

        # Extract Bloom's level (optional)
        bloom_level = self._extract_bloom_level(section)

        # Extract question text (text between Type: and first option A))
        question_text = self._extract_question_text(section)

        # Extract options
        options = self._extract_options(section)

        # Extract correct answer
        correct_answer = self._extract_answer(section)

        # Extract feedback
        feedback = self._extract_feedback(section, options, correct_answer)

        # Generate question ID
        question_id = f"W{week}-Q{question_number}-{self._slugify(topic)}"

        return Question(
            id=question_id,
            week=week,
            topic=topic,
            question_text=question_text,
            options=options,
            correct_answer=correct_answer,
            feedback=feedback,
            bloom_level=bloom_level,
            question_type=question_type
        )

    def _extract_bloom_level(self, section: str) -> BloomLevel:
        """Extract or infer Bloom's taxonomy level."""
        # Check for explicit annotation
        bloom_match = re.search(r'\*\*Bloom\'?s? Level:\*\*\s*(\w+)', section, re.IGNORECASE)
        if bloom_match:
            level_str = bloom_match.group(1).strip()
            try:
                return BloomLevel.from_string(level_str)
            except ValueError:
                pass  # Fall through to inference

        # Infer from question patterns
        if self.infer_bloom:
            return self._infer_bloom_level(section)

        # Default to Remembering
        return BloomLevel.REMEMBERING

    def _infer_bloom_level(self, section: str) -> BloomLevel:
        """
        Infer Bloom's level from question text patterns.

        Remembering: "What is...", "Define...", "List...", "Name...", "Identify..."
        Understanding: "Why...", "How...", "Explain...", "Compare...", scenario-based
        """
        text = section.lower()

        # Understanding indicators
        understanding_patterns = [
            r'\bwhy\b',
            r'\bhow\b',
            r'\bexplain\b',
            r'\bcompare\b',
            r'\bcontrast\b',
            r'\banalyze\b',
            r'\binterpret\b',
            r'\billustrate\b',
            r'\bdemonstrate\b',
            r'which.*would be',
            r'what.*best',
            r'scenario:',
            r'situation:',
            r'team|manager|client|employee|stakeholder',  # Scenario keywords
        ]

        for pattern in understanding_patterns:
            if re.search(pattern, text):
                return BloomLevel.UNDERSTANDING

        # Remembering indicators (explicit)
        remembering_patterns = [
            r'^what is\b',
            r'^what are\b',
            r'^define\b',
            r'^list\b',
            r'^name\b',
            r'^identify\b',
            r'^which.*definition',
            r'how many\b',
        ]

        for pattern in remembering_patterns:
            if re.search(pattern, text):
                return BloomLevel.REMEMBERING

        # Default: Check length and complexity
        # Longer questions (>100 chars) with multiple sentences likely Understanding
        question_text = self._extract_question_text(section)
        if len(question_text) > 100 and '.' in question_text:
            return BloomLevel.UNDERSTANDING

        # Default to Remembering
        return BloomLevel.REMEMBERING

    def _extract_question_text(self, section: str) -> str:
        """Extract the question text."""
        # Text is between Type: line and first option A)
        lines = section.split('\n')

        # Find start (after Type: line)
        start_idx = None
        for i, line in enumerate(lines):
            if '**Type:**' in line:
                start_idx = i + 1
                break

        if start_idx is None:
            # Fallback: start after header
            start_idx = 1

        # Find end (before first option)
        end_idx = None
        for i in range(start_idx, len(lines)):
            if re.match(r'^[A-D]\)', lines[i].strip()):
                end_idx = i
                break

        if end_idx is None:
            raise ValueError("Cannot find options in question")

        # Extract and clean question text
        question_lines = lines[start_idx:end_idx]
        question_text = '\n'.join(line.strip() for line in question_lines if line.strip())

        # Remove Bloom's level annotation if present
        question_text = re.sub(r'\*\*Bloom\'?s? Level:\*\*\s*\w+', '', question_text, flags=re.IGNORECASE)

        return question_text.strip()

    def _extract_options(self, section: str) -> Dict[str, str]:
        """Extract answer options A-D."""
        options = {}

        # Match options: A) Option text
        option_pattern = r'^([A-D])\)\s*(.+)$'

        for line in section.split('\n'):
            match = re.match(option_pattern, line.strip())
            if match:
                letter = match.group(1)
                text = match.group(2).strip()
                options[letter] = text

        if len(options) != 4:
            raise ValueError(
                f"Expected 4 options (A-D), found {len(options)}: {list(options.keys())}"
            )

        return options

    def _extract_answer(self, section: str) -> str:
        """Extract correct answer letter."""
        answer_match = re.search(r'\*\*Answer:\*\*\s*([A-D])', section)
        if not answer_match:
            raise ValueError("Cannot find **Answer:** field")

        return answer_match.group(1)

    def _extract_feedback(
        self,
        section: str,
        options: Dict[str, str],
        correct_answer: str
    ) -> Dict[str, str]:
        """
        Extract feedback for each option.

        Current format has combined feedback, so we split it intelligently
        or generate per-option feedback.
        """
        feedback_match = re.search(r'\*\*Feedback:\*\*\s*(.+)', section, re.DOTALL)
        if not feedback_match:
            raise ValueError("Cannot find **Feedback:** field")

        combined_feedback = feedback_match.group(1).strip()

        # Remove any trailing markdown separators
        combined_feedback = re.sub(r'\n---\s*$', '', combined_feedback).strip()

        # Try to parse per-option feedback if it exists
        # Format: "A is wrong because... B is correct because... C is wrong... D is wrong..."
        feedback = {}

        # Check if feedback mentions each option explicitly
        for letter in ['A', 'B', 'C', 'D']:
            # Pattern: "A is ...", "A) ...", "option A ...", etc.
            option_patterns = [
                rf'\b{letter}\s+is\b',
                rf'\b{letter}\)\s+',
                rf'\boption\s+{letter}\b',
                rf'\b{letter}\s+describes',
                rf'\b{letter}\s+shows',
            ]

            has_explicit_feedback = any(
                re.search(pattern, combined_feedback, re.IGNORECASE)
                for pattern in option_patterns
            )

            if has_explicit_feedback:
                # Try to extract specific feedback for this option
                # This is imperfect but handles many cases
                feedback[letter] = self._extract_option_feedback(
                    combined_feedback, letter, letter == correct_answer
                )
            else:
                # Generate feedback from combined text
                if letter == correct_answer:
                    feedback[letter] = f"Correct. {combined_feedback}"
                else:
                    feedback[letter] = f"Incorrect. {combined_feedback}"

        return feedback

    def _extract_option_feedback(
        self,
        combined_feedback: str,
        option_letter: str,
        is_correct: bool
    ) -> str:
        """Extract feedback specific to one option from combined text."""
        # Try to find sentences mentioning this option
        sentences = re.split(r'[.!?]+', combined_feedback)

        relevant_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            # Check if this sentence mentions the option
            patterns = [
                rf'\b{option_letter}\s+is\b',
                rf'\b{option_letter}\)\s+',
                rf'\boption\s+{option_letter}\b',
                rf'\b{option_letter}\s+describes',
            ]

            if any(re.search(pattern, sentence, re.IGNORECASE) for pattern in patterns):
                relevant_sentences.append(sentence)

        if relevant_sentences:
            feedback = '. '.join(relevant_sentences) + '.'
            # Add prefix if not present
            if not feedback.lower().startswith(('correct', 'incorrect')):
                prefix = "Correct" if is_correct else "Incorrect"
                feedback = f"{prefix}. {feedback}"
            return feedback

        # Fallback: Use combined feedback with prefix
        prefix = "Correct" if is_correct else "Incorrect"
        return f"{prefix}. {combined_feedback}"

    def _slugify(self, text: str) -> str:
        """Convert text to slug format for IDs."""
        # Remove special characters, replace spaces with hyphens
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')[:30]  # Limit length
