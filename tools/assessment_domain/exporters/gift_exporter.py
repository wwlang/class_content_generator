"""
GIFT format exporter for quiz banks.

Exports QuizBank objects to Moodle GIFT format for LMS import.
"""

from pathlib import Path
from typing import Optional
from ..models import Question, QuizBank


class GIFTExporter:
    """
    Export quiz banks to Moodle GIFT format.

    GIFT (General Import Format Technology) is Moodle's text-based format
    for importing quiz questions with multiple choice, feedback, and categories.

    Features:
    - Escapes special GIFT characters
    - Includes per-option feedback
    - Organizes by category
    - Adds metadata headers

    Usage:
        exporter = GIFTExporter()
        gift_content = exporter.export_quiz_bank(quiz_bank)
        exporter.write_to_file(gift_content, "output/quiz-1.gift")
    """

    def __init__(self, include_feedback: bool = True):
        """
        Initialize exporter.

        Args:
            include_feedback: Whether to include answer feedback in export
        """
        self.include_feedback = include_feedback

    def export_quiz_bank(
        self,
        quiz_bank: QuizBank,
        category: Optional[str] = None
    ) -> str:
        """
        Export quiz bank to GIFT format string.

        Args:
            quiz_bank: QuizBank to export
            category: Optional Moodle category name (defaults to quiz title)

        Returns:
            GIFT formatted string ready for Moodle import

        Example:
            gift = exporter.export_quiz_bank(quiz_bank)
            print(gift)  # See formatted GIFT output
        """
        lines = []

        # Header comments
        lines.append(f'// {quiz_bank.title}')
        lines.append(f'// Quiz ID: {quiz_bank.quiz_id}')
        lines.append(f'// Questions: {len(quiz_bank.questions)}')
        lines.append(f'// Weeks covered: {", ".join(str(w) for w in quiz_bank.weeks_covered)}')

        # Bloom distribution info
        validation = quiz_bank.validate_distribution()
        lines.append(
            f'// Bloom distribution: '
            f'{validation["remembering_count"]} Remembering, '
            f'{validation["understanding_count"]} Understanding'
        )
        lines.append('')

        # Category for Moodle organization
        # Note: Don't escape the category text - Moodle handles it as-is
        if category is None:
            category = quiz_bank.title
        lines.append(f'$CATEGORY: {category}')
        lines.append('')

        # Export each question
        for question in quiz_bank.questions:
            gift_question = self._export_question(question)
            lines.append(gift_question)
            lines.append('')  # Blank line between questions

        return '\n'.join(lines)

    def _export_question(self, question: Question) -> str:
        """
        Export single question to GIFT format.

        Args:
            question: Question to export

        Returns:
            GIFT formatted question block
        """
        # Question title and text
        title = self._escape_gift_text(question.topic)
        q_text = self._escape_gift_text(question.question_text)

        lines = [f'::{title}::{q_text}{{']

        # Add options with feedback
        for letter in ['A', 'B', 'C', 'D']:
            option_text = self._escape_gift_text(question.options[letter])

            if letter == question.correct_answer:
                # Correct answer (= prefix)
                if self.include_feedback and letter in question.feedback:
                    feedback = self._escape_gift_text(question.feedback[letter])
                    lines.append(f'={option_text} #{feedback}')
                else:
                    lines.append(f'={option_text}')
            else:
                # Wrong answer/distractor (~ prefix)
                if self.include_feedback and letter in question.feedback:
                    feedback = self._escape_gift_text(question.feedback[letter])
                    lines.append(f'~{option_text} #{feedback}')
                else:
                    lines.append(f'~{option_text}')

        # Add general feedback if available (uses #### syntax in GIFT)
        # Note: #### and } must be on the same line
        if self.include_feedback and question.general_feedback:
            general_fb = self._escape_gift_text(question.general_feedback.strip())
            lines.append(f'####{general_fb}}}')  # Double }} to escape in f-string
        else:
            lines.append('}')

        return '\n'.join(lines)

    def _escape_gift_text(self, text: str) -> str:
        r"""
        Escape special characters for GIFT format and convert markdown to HTML.

        GIFT special characters that need escaping:
        - Backslash (\)
        - Braces ({})
        - Equals (=)
        - Tilde (~)
        - Hash (#)
        - Colon (:)

        Also converts markdown bold (**text**) to HTML (<b>text</b>) since
        GIFT format supports HTML but not markdown.

        Args:
            text: Text to escape

        Returns:
            Escaped text safe for GIFT format with HTML formatting

        Example:
            >>> _escape_gift_text("Use {braces} = special")
            "Use \\{braces\\} \\= special"
            >>> _escape_gift_text("The **term** (definition) here")
            "The <b>term</b> (definition) here"
        """
        import re

        # Convert markdown bold to HTML BEFORE escaping
        # (so we don't escape the < and > we're adding)
        text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)

        # Order matters: escape backslash first to avoid double-escaping
        text = text.replace('\\', '\\\\')
        text = text.replace('{', '\\{')
        text = text.replace('}', '\\}')
        text = text.replace('=', '\\=')
        text = text.replace('~', '\\~')
        text = text.replace('#', '\\#')
        text = text.replace(':', '\\:')
        return text

    def write_to_file(
        self,
        gift_content: str,
        output_path: str,
        encoding: str = 'utf-8'
    ) -> Path:
        """
        Write GIFT content to file.

        Args:
            gift_content: GIFT formatted string
            output_path: Path to output file
            encoding: File encoding (default: utf-8)

        Returns:
            Path object for written file

        Example:
            path = exporter.write_to_file(gift_content, "output/quiz-1.gift")
            print(f"Wrote {path}")
        """
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, 'w', encoding=encoding) as f:
            f.write(gift_content)

        return output

    def export_to_file(
        self,
        quiz_bank: QuizBank,
        output_path: str,
        category: Optional[str] = None
    ) -> Path:
        """
        Export quiz bank directly to file.

        Convenience method combining export_quiz_bank() and write_to_file().

        Args:
            quiz_bank: QuizBank to export
            output_path: Path to output file
            category: Optional Moodle category

        Returns:
            Path to written file

        Example:
            path = exporter.export_to_file(quiz_bank, "output/quiz-1.gift")
        """
        gift_content = self.export_quiz_bank(quiz_bank, category)
        return self.write_to_file(gift_content, output_path)
