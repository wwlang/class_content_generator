#!/usr/bin/env python3
"""
Export quiz questions to Moodle GIFT format.

Reads quiz questions from quiz-questions.md (preferred) or falls back to
tutorial-content.md + tutorial-tutor-notes.md for legacy format.
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class QuizQuestion:
    """Represents a quiz question with options."""
    number: int
    topic: str
    question_text: str
    options: dict  # {letter: text} e.g., {'A': 'option text', 'B': ...}


@dataclass
class QuizAnswer:
    """Represents answer key with explanations."""
    number: int
    topic: str
    correct_letter: str
    correct_explanation: str
    wrong_explanations: dict  # {letter: explanation}
    common_confusion: Optional[str] = None
    teaching_tip: Optional[str] = None


class GIFTConfig:
    """Configuration for GIFT format export."""
    INCLUDE_FEEDBACK: bool = True
    INCLUDE_COMMON_CONFUSION: bool = False  # Too verbose for Moodle inline feedback
    FILE_ENCODING: str = 'utf-8'


class QuizParser:
    """Parse quiz questions and answers from tutorial markdown files."""

    def parse_questions(self, tutorial_content_path: str) -> List[QuizQuestion]:
        """Extract quiz questions from tutorial-content.md.

        Args:
            tutorial_content_path: Path to tutorial-content.md file

        Returns:
            List of QuizQuestion objects
        """
        with open(tutorial_content_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find quiz practice section
        quiz_section_match = re.search(
            r'## QUIZ PRACTICE.*?(?=^##|\Z)',
            content,
            re.MULTILINE | re.DOTALL
        )

        if not quiz_section_match:
            return []

        quiz_section = quiz_section_match.group(0)

        # Extract individual questions
        # Pattern: **Question N: Topic**\nQuestion text\n\nA) option\nB) option\nC) option\nD) option
        question_pattern = r'\*\*Question (\d+):\s*([^*]+)\*\*\s*\n\s*(.+?)\s*\n\s*A\)\s*(.+?)\s*\n\s*B\)\s*(.+?)\s*\n\s*C\)\s*(.+?)\s*\n\s*D\)\s*(.+?)(?=\n\s*\*\*Question|\n\s*---|\Z)'

        questions = []
        for match in re.finditer(question_pattern, quiz_section, re.DOTALL):
            number = int(match.group(1))
            topic = match.group(2).strip()
            question_text = match.group(3).strip()

            # Clean up question text (remove extra whitespace)
            question_text = ' '.join(question_text.split())

            options = {
                'A': match.group(4).strip(),
                'B': match.group(5).strip(),
                'C': match.group(6).strip(),
                'D': match.group(7).strip()
            }

            questions.append(QuizQuestion(
                number=number,
                topic=topic,
                question_text=question_text,
                options=options
            ))

        return questions

    def parse_answers(self, tutor_notes_path: str) -> List[QuizAnswer]:
        """Extract quiz answers from tutorial-tutor-notes.md.

        Args:
            tutor_notes_path: Path to tutorial-tutor-notes.md file

        Returns:
            List of QuizAnswer objects
        """
        with open(tutor_notes_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find quiz solutions section
        # Use negative lookahead (?!#) to ensure we match ## but not ###
        quiz_section_match = re.search(
            r'## Quiz Solutions.*?(?=^##(?!#)|\Z)',
            content,
            re.MULTILINE | re.DOTALL
        )

        if not quiz_section_match:
            return []

        quiz_section = quiz_section_match.group(0)

        # Extract individual answer explanations
        # Pattern: ### Question N: Topic\n**Correct: Letter**\n...
        answer_blocks = re.split(r'###\s*Question\s+(\d+):', quiz_section)[1:]  # Skip first empty split

        answers = []
        for i in range(0, len(answer_blocks), 2):
            number = int(answer_blocks[i].strip())
            block_content = answer_blocks[i + 1]

            # Extract topic (first line after question number)
            topic_match = re.match(r'\s*([^\n]+)', block_content)
            topic = topic_match.group(1).strip() if topic_match else ''

            # Extract correct answer letter
            correct_match = re.search(r'\*\*Correct:\s*([A-D])\*\*', block_content)
            if not correct_match:
                print(f"Warning: No correct answer found for Question {number}", file=sys.stderr)
                continue
            correct_letter = correct_match.group(1)

            # Extract "Why correct" explanation
            correct_exp_match = re.search(
                r'\*\*Why [A-D] is correct:\*\*\s*\n\s*(.+?)(?=\n\s*\*\*Why wrong:|\n\s*\*\*Common confusion:|\Z)',
                block_content,
                re.DOTALL
            )
            correct_explanation = correct_exp_match.group(1).strip() if correct_exp_match else ''
            correct_explanation = ' '.join(correct_explanation.split())  # Clean whitespace

            # Extract "Why wrong" explanations
            wrong_explanations = {}
            wrong_section_match = re.search(
                r'\*\*Why wrong:\*\*\s*\n((?:- [A-D]:.*?\n)+)',
                block_content,
                re.DOTALL
            )

            if wrong_section_match:
                wrong_section = wrong_section_match.group(1)
                # Parse each "- Letter: explanation" line
                for line_match in re.finditer(r'-\s*([A-D]):\s*(.+?)(?=\n-|\n\n|\Z)', wrong_section, re.DOTALL):
                    letter = line_match.group(1)
                    explanation = line_match.group(2).strip()
                    explanation = ' '.join(explanation.split())  # Clean whitespace
                    wrong_explanations[letter] = explanation

            # Extract common confusion (optional)
            confusion_match = re.search(
                r'\*\*Common confusion:\*\*\s*(.+?)(?=\n\s*\*\*Teaching tip:|\n\s*---|\Z)',
                block_content,
                re.DOTALL
            )
            common_confusion = confusion_match.group(1).strip() if confusion_match else None
            if common_confusion:
                common_confusion = ' '.join(common_confusion.split())

            # Extract teaching tip (optional)
            tip_match = re.search(
                r'\*\*Teaching tip:\*\*\s*(.+?)(?=\n\s*---|\Z)',
                block_content,
                re.DOTALL
            )
            teaching_tip = tip_match.group(1).strip() if tip_match else None
            if teaching_tip:
                teaching_tip = ' '.join(teaching_tip.split())

            answers.append(QuizAnswer(
                number=number,
                topic=topic,
                correct_letter=correct_letter,
                correct_explanation=correct_explanation,
                wrong_explanations=wrong_explanations,
                common_confusion=common_confusion,
                teaching_tip=teaching_tip
            ))

        return answers

    def validate_quiz(self, questions: List[QuizQuestion], answers: List[QuizAnswer]) -> bool:
        """Validate that questions and answers match properly.

        Args:
            questions: List of parsed questions
            answers: List of parsed answers

        Returns:
            True if valid, raises ValueError otherwise
        """
        if len(questions) != len(answers):
            raise ValueError(f"Question count mismatch: {len(questions)} questions vs {len(answers)} answers")

        for q, a in zip(questions, answers):
            if q.number != a.number:
                raise ValueError(f"Question number mismatch: Q{q.number} vs A{a.number}")

            if a.correct_letter not in q.options:
                raise ValueError(f"Question {q.number}: Correct answer '{a.correct_letter}' not in options")

            # Check all options have A, B, C, D
            if set(q.options.keys()) != {'A', 'B', 'C', 'D'}:
                raise ValueError(f"Question {q.number}: Missing options (need A, B, C, D)")

        return True

    def parse_quiz_questions_file(self, quiz_path: str) -> List[Tuple[QuizQuestion, QuizAnswer]]:
        """Parse the new quiz-questions.md format where Q&A are in same file.

        Format expected:
        ### Q1: Topic Name
        **Type:** Multiple Choice

        Question text here?

        A) Option A text
        B) Option B text
        C) Option C text
        D) Option D text

        **Answer:** C
        **Feedback:** Explanation text...

        Args:
            quiz_path: Path to quiz-questions.md file

        Returns:
            List of (QuizQuestion, QuizAnswer) tuples
        """
        with open(quiz_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split by question headers
        question_pattern = r'###\s*Q(\d+):\s*(.+?)(?=\n)'
        question_blocks = re.split(r'(?=###\s*Q\d+:)', content)

        results = []
        for block in question_blocks:
            if not block.strip() or not re.match(r'###\s*Q\d+:', block):
                continue

            # Extract question number and topic
            header_match = re.match(r'###\s*Q(\d+):\s*(.+?)(?=\n)', block)
            if not header_match:
                continue

            number = int(header_match.group(1))
            topic = header_match.group(2).strip()

            # Extract question text (between **Type:** line and options)
            question_match = re.search(
                r'\*\*Type:\*\*[^\n]*\n\s*\n(.+?)(?=\n\s*A\))',
                block,
                re.DOTALL
            )
            question_text = question_match.group(1).strip() if question_match else ''
            question_text = ' '.join(question_text.split())

            # Extract options A-D
            options = {}
            for letter in ['A', 'B', 'C', 'D']:
                opt_match = re.search(
                    rf'{letter}\)\s*(.+?)(?=\n\s*[B-D]\)|\n\s*\*\*Answer|\n\s*---|\Z)',
                    block,
                    re.DOTALL
                )
                if opt_match:
                    options[letter] = ' '.join(opt_match.group(1).strip().split())

            # Extract answer
            answer_match = re.search(r'\*\*Answer:\*\*\s*([A-D])', block)
            correct_letter = answer_match.group(1) if answer_match else 'A'

            # Extract feedback
            feedback_match = re.search(
                r'\*\*Feedback:\*\*\s*(.+?)(?=\n\s*---|\Z)',
                block,
                re.DOTALL
            )
            feedback = feedback_match.group(1).strip() if feedback_match else ''
            feedback = ' '.join(feedback.split())

            # Create QuizQuestion
            question = QuizQuestion(
                number=number,
                topic=topic,
                question_text=question_text,
                options=options
            )

            # Create QuizAnswer with feedback as correct_explanation
            # Wrong explanations extracted from feedback if possible
            answer = QuizAnswer(
                number=number,
                topic=topic,
                correct_letter=correct_letter,
                correct_explanation=feedback,
                wrong_explanations={}
            )

            results.append((question, answer))

        return results


class GIFTFormatter:
    """Format quiz data into Moodle GIFT format."""

    @staticmethod
    def escape_gift_text(text: str) -> str:
        """Escape special characters for GIFT format.

        Args:
            text: Text to escape

        Returns:
            Escaped text safe for GIFT format
        """
        # Order matters: escape backslash first
        text = text.replace('\\', '\\\\')
        text = text.replace('{', '\\{')
        text = text.replace('}', '\\}')
        text = text.replace('=', '\\=')
        text = text.replace('~', '\\~')
        text = text.replace('#', '\\#')
        text = text.replace(':', '\\:')
        return text

    def format_question(self, question: QuizQuestion, answer: QuizAnswer,
                       include_feedback: bool = True) -> str:
        """Convert single question/answer pair to GIFT format.

        Args:
            question: QuizQuestion object
            answer: QuizAnswer object
            include_feedback: Whether to include explanations as feedback

        Returns:
            GIFT formatted string for this question
        """
        # Question title and text
        title = self.escape_gift_text(question.topic)
        q_text = self.escape_gift_text(question.question_text)

        gift_lines = [f'::{title}::{q_text}{{']

        # Add options with feedback
        for letter in ['A', 'B', 'C', 'D']:
            option_text = self.escape_gift_text(question.options[letter])

            if letter == answer.correct_letter:
                # Correct answer
                prefix = '='
                if include_feedback and answer.correct_explanation:
                    feedback = self.escape_gift_text(answer.correct_explanation)
                    gift_lines.append(f'{prefix}{option_text} #{feedback}')
                else:
                    gift_lines.append(f'{prefix}{option_text}')
            else:
                # Wrong answer (distractor)
                prefix = '~'
                if include_feedback and letter in answer.wrong_explanations:
                    feedback = self.escape_gift_text(answer.wrong_explanations[letter])
                    gift_lines.append(f'{prefix}{option_text} #{feedback}')
                else:
                    gift_lines.append(f'{prefix}{option_text}')

        gift_lines.append('}')

        return '\n'.join(gift_lines)

    def format_quiz(self, quiz_data: List[Tuple[QuizQuestion, QuizAnswer]],
                   week_number: int, week_title: str,
                   include_feedback: bool = True) -> str:
        """Convert full quiz to GIFT file content.

        Args:
            quiz_data: List of (QuizQuestion, QuizAnswer) tuples
            week_number: Week number for category
            week_title: Week title for header
            include_feedback: Whether to include explanations

        Returns:
            Complete GIFT file content
        """
        lines = []

        # Add header comment
        lines.append(f'// Week {week_number} Quiz: {week_title}')
        lines.append(f'// Generated from tutorial quiz practice questions')
        lines.append(f'// Questions: {len(quiz_data)}')
        lines.append('')

        # Add category (for Moodle organization)
        lines.append(f'$CATEGORY: Week {week_number}')
        lines.append('')

        # Add each question
        for question, answer in quiz_data:
            gift_question = self.format_question(question, answer, include_feedback)
            lines.append(gift_question)
            lines.append('')  # Blank line between questions

        return '\n'.join(lines)


def export_quiz_gift(week_folder: str, week_number: int = None) -> str:
    """Export quiz to GIFT format.

    Prefers quiz-questions.md (new format) over tutorial-content.md (legacy).

    Args:
        week_folder: Path to week folder (e.g., courses/COURSE/weeks/week-1)
        week_number: Week number (optional, extracted from folder if not provided)

    Returns:
        Path to generated GIFT file

    Raises:
        FileNotFoundError: If required files don't exist
        ValueError: If quiz validation fails
    """
    week_path = Path(week_folder)

    if not week_path.exists():
        raise FileNotFoundError(f"Week folder not found: {week_folder}")

    # Extract week number from folder name if not provided
    if week_number is None:
        folder_name = week_path.name
        week_match = re.search(r'week-(\d+)', folder_name)
        if week_match:
            week_number = int(week_match.group(1))
        else:
            week_number = 0  # Fallback

    parser = QuizParser()

    # Check for new format first (quiz-questions.md)
    quiz_questions_file = week_path / 'quiz-questions.md'
    tutorial_content = week_path / 'tutorial-content.md'

    if quiz_questions_file.exists():
        # New format: quiz-questions.md has Q&A in same file
        print(f"Using quiz-questions.md format")
        quiz_pairs = parser.parse_quiz_questions_file(str(quiz_questions_file))

        if not quiz_pairs:
            raise ValueError(f"No quiz questions found in {quiz_questions_file}")

        # Extract week title from quiz file
        with open(quiz_questions_file, 'r', encoding='utf-8') as f:
            first_lines = f.read(500)
            topic_match = re.search(r'\*\*Topic:\*\*\s*(.+)', first_lines)
            week_title = topic_match.group(1).strip() if topic_match else 'Quiz'

    else:
        # Legacy format: separate tutorial-content.md and tutor-notes.md
        print(f"Using legacy tutorial format")
        tutor_notes = week_path / 'tutorial-tutor-notes.md'

        if not tutorial_content.exists():
            raise FileNotFoundError(f"Neither quiz-questions.md nor tutorial-content.md found")
        if not tutor_notes.exists():
            raise FileNotFoundError(f"Tutor notes not found: {tutor_notes}")

        questions = parser.parse_questions(str(tutorial_content))
        answers = parser.parse_answers(str(tutor_notes))

        if not questions:
            raise ValueError(f"No quiz questions found in {tutorial_content}")
        if not answers:
            raise ValueError(f"No quiz answers found in {tutor_notes}")

        parser.validate_quiz(questions, answers)
        quiz_pairs = list(zip(questions, answers))

        # Extract week title from tutorial content
        with open(tutorial_content, 'r', encoding='utf-8') as f:
            first_lines = f.read(500)
            title_match = re.search(r'#\s*Week\s*\d+[:\s]+(.+)', first_lines)
            week_title = title_match.group(1).strip() if title_match else 'Tutorial Quiz'

    # Format to GIFT
    formatter = GIFTFormatter()
    gift_content = formatter.format_quiz(
        quiz_pairs,
        week_number,
        week_title,
        include_feedback=GIFTConfig.INCLUDE_FEEDBACK
    )

    # Write GIFT file to output/ folder
    output_folder = week_path / 'output'
    output_folder.mkdir(exist_ok=True)
    output_path = output_folder / f'week-{week_number}-quiz.gift'
    with open(output_path, 'w', encoding=GIFTConfig.FILE_ENCODING) as f:
        f.write(gift_content)

    return str(output_path)


def main():
    """Command-line interface for quiz export."""
    if len(sys.argv) < 2:
        print("Usage: python export_quiz_to_gift.py <week_folder> [week_number]")
        print("Example: python export_quiz_to_gift.py courses/BCI2AU/weeks/week-1")
        sys.exit(1)

    week_folder = sys.argv[1]
    week_number = int(sys.argv[2]) if len(sys.argv) > 2 else None

    try:
        output_path = export_quiz_gift(week_folder, week_number)
        print(f"✓ Quiz exported to: {output_path}")

        # Count questions
        with open(output_path, 'r') as f:
            content = f.read()
            question_count = content.count('::')

        print(f"  Questions: {question_count}")
        print(f"  Ready for Moodle import")

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
