#!/usr/bin/env python3
"""
Export Week 2 quiz with structured feedback to GIFT format.

Handles the new format where each option has individual feedback.
"""

import re
from pathlib import Path


def escape_gift_text(text: str) -> str:
    """Escape special characters for GIFT format."""
    text = text.replace('\\', '\\\\')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('=', '\\=')
    text = text.replace('~', '\\~')
    text = text.replace('#', '\\#')
    text = text.replace(':', '\\:')
    # Remove markdown bold formatting
    text = text.replace('**', '')
    return text


def parse_structured_quiz(file_path: str):
    """Parse quiz with structured option-specific feedback."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by question headers
    question_blocks = re.split(r'(?=###\s*Q\d+:)', content)

    quiz_data = []

    for block in question_blocks:
        if not block.strip() or not re.match(r'###\s*Q\d+:', block):
            continue

        # Extract question number and topic
        header_match = re.match(r'###\s*Q(\d+):\s*(.+?)(?=\n)', block)
        if not header_match:
            continue

        number = int(header_match.group(1))
        topic = header_match.group(2).strip()

        # Extract question type and category
        type_match = re.search(r'\*\*Type:\*\*\s*(.+)', block)
        question_type = type_match.group(1).strip() if type_match else 'Multiple Choice'

        category_match = re.search(r'\*\*Category:\*\*\s*(.+)', block)
        category = category_match.group(1).strip() if category_match else ''

        # Handle different question types
        if question_type == 'Matching':
            # Parse matching question
            question_text_match = re.search(
                r'\*\*Category:\*\*[^\n]*\n\s*\n(.+?)(?=\n\s*\d+\.)',
                block,
                re.DOTALL
            )
            question_text = question_text_match.group(1).strip() if question_text_match else ''

            # For matching, extract the items and options
            items = []
            for i in range(1, 5):  # Assuming 4 items
                item_match = re.search(rf'{i}\.\s*(.+?)(?=\n)', block)
                if item_match:
                    items.append(item_match.group(1).strip())

            options = {}
            for letter in ['A', 'B', 'C', 'D']:
                opt_match = re.search(rf'{letter}\)\s*(.+?)(?=\n)', block)
                if opt_match:
                    options[letter] = opt_match.group(1).strip()

            # Extract answer
            answer_match = re.search(r'\*\*Answer:\*\*\s*\n(.+?)(?=\n\s*\*\*Feedback:)', block, re.DOTALL)
            answer_text = answer_match.group(1).strip() if answer_match else ''

            # Extract feedback
            feedback_match = re.search(r'\*\*Feedback:\*\*\s*\n(.+?)(?=\n\s*---|\Z)', block, re.DOTALL)
            feedback = feedback_match.group(1).strip() if feedback_match else ''

            quiz_data.append({
                'number': number,
                'topic': topic,
                'type': 'matching',
                'question_text': question_text,
                'items': items,
                'options': options,
                'answer_text': answer_text,
                'feedback': feedback,
                'category': category
            })

        elif question_type == 'True/False':
            # Parse True/False question
            question_text_match = re.search(
                r'\*\*Category:\*\*[^\n]*\n\s*\n(.+?)(?=\n\s*\*\*Answer:)',
                block,
                re.DOTALL
            )
            question_text = question_text_match.group(1).strip() if question_text_match else ''
            question_text = ' '.join(question_text.split())

            # Extract answer
            answer_match = re.search(r'\*\*Answer:\*\*\s*(True|False)', block)
            answer = answer_match.group(1) if answer_match else 'True'

            # Extract feedback
            feedback_match = re.search(r'\*\*Feedback:\*\*\s*\n(.+?)(?=\n\s*---|\Z)', block, re.DOTALL)
            feedback_text = feedback_match.group(1).strip() if feedback_match else ''

            # Extract the correct answer feedback (starts with answer + " is correct")
            correct_feedback_match = re.search(
                rf'\*\*{answer} is correct\.\*\*\s*(.+?)(?=\n\s*\*\*If you answered|\Z)',
                feedback_text,
                re.DOTALL
            )
            correct_feedback = correct_feedback_match.group(1).strip() if correct_feedback_match else feedback_text
            correct_feedback = ' '.join(correct_feedback.split())

            # Extract wrong answer feedback
            wrong_answer = 'False' if answer == 'True' else 'True'
            wrong_feedback_match = re.search(
                rf'\*\*If you answered {wrong_answer}:\*\*\s*(.+?)(?=\Z)',
                feedback_text,
                re.DOTALL
            )
            wrong_feedback = wrong_feedback_match.group(1).strip() if wrong_feedback_match else f"Incorrect. {correct_feedback}"
            wrong_feedback = ' '.join(wrong_feedback.split())

            quiz_data.append({
                'number': number,
                'topic': topic,
                'type': 'truefalse',
                'question_text': question_text,
                'answer': answer,
                'correct_feedback': correct_feedback,
                'wrong_feedback': wrong_feedback,
                'category': category
            })

        else:  # Multiple Choice
            # Extract question text
            question_text_match = re.search(
                r'\*\*Category:\*\*[^\n]*\n\s*\n(.+?)(?=\n\s*A\))',
                block,
                re.DOTALL
            )
            question_text = question_text_match.group(1).strip() if question_text_match else ''
            question_text = ' '.join(question_text.split())

            # Extract options A-D
            options = {}
            for letter in ['A', 'B', 'C', 'D']:
                opt_match = re.search(
                    rf'{letter}\)\s*(.+?)(?=\n\s*[B-D]\)|\n\s*\*\*Answer:|\n\s*---|\Z)',
                    block,
                    re.DOTALL
                )
                if opt_match:
                    options[letter] = ' '.join(opt_match.group(1).strip().split())

            # Extract answer
            answer_match = re.search(r'\*\*Answer:\*\*\s*([A-D])', block)
            correct_letter = answer_match.group(1) if answer_match else 'A'

            # Extract structured feedback for each option
            feedback_section = re.search(
                r'\*\*Feedback:\*\*\s*\n(.+?)(?=\n\s*---|\Z)',
                block,
                re.DOTALL
            )

            option_feedback = {}
            if feedback_section:
                feedback_text = feedback_section.group(1)

                # Extract feedback for each option
                for letter in ['A', 'B', 'C', 'D']:
                    # Pattern: - **A) Incorrect.** text or - **B) Correct!** text
                    pattern = rf'-\s*\*\*{letter}\)\s*(Incorrect|Correct!)?\.*\*\*\s*(.+?)(?=\n\s*-\s*\*\*[A-D]\)|\Z)'
                    match = re.search(pattern, feedback_text, re.DOTALL)
                    if match:
                        feedback = match.group(2).strip()
                        feedback = ' '.join(feedback.split())
                        option_feedback[letter] = feedback

            quiz_data.append({
                'number': number,
                'topic': topic,
                'type': 'multichoice',
                'question_text': question_text,
                'options': options,
                'correct_letter': correct_letter,
                'feedback': option_feedback,
                'category': category
            })

    return quiz_data


def format_to_gift(quiz_data, week_number: int, week_title: str) -> str:
    """Convert parsed quiz data to GIFT format."""
    lines = []

    # Header
    lines.append(f'// Week {week_number} Quiz: {week_title}')
    lines.append(f'// Questions: {len(quiz_data)}')
    lines.append('')
    lines.append(f'$CATEGORY: Week {week_number}')
    lines.append('')

    for q in quiz_data:
        if q['type'] == 'multichoice':
            # Multiple choice question
            title = escape_gift_text(q['topic'])
            q_text = escape_gift_text(q['question_text'])

            lines.append(f'::{title}::{q_text}{{')

            for letter in ['A', 'B', 'C', 'D']:
                option_text = escape_gift_text(q['options'][letter])

                if letter == q['correct_letter']:
                    prefix = '='
                else:
                    prefix = '~'

                # Add feedback if available
                if letter in q['feedback']:
                    feedback = escape_gift_text(q['feedback'][letter])
                    lines.append(f'{prefix}{option_text} #{feedback}')
                else:
                    lines.append(f'{prefix}{option_text}')

            lines.append('}')
            lines.append('')

        elif q['type'] == 'truefalse':
            # True/False question
            title = escape_gift_text(q['topic'])
            q_text = escape_gift_text(q['question_text'])

            lines.append(f'::{title}::{q_text}{{')

            if q['answer'] == 'True':
                correct_feedback = escape_gift_text(q['correct_feedback'])
                wrong_feedback = escape_gift_text(q['wrong_feedback'])
                lines.append(f'TRUE#{correct_feedback}')
                lines.append(f'FALSE#{wrong_feedback}')
            else:
                correct_feedback = escape_gift_text(q['correct_feedback'])
                wrong_feedback = escape_gift_text(q['wrong_feedback'])
                lines.append(f'FALSE#{correct_feedback}')
                lines.append(f'TRUE#{wrong_feedback}')

            lines.append('}')
            lines.append('')

        elif q['type'] == 'matching':
            # Matching question
            title = escape_gift_text(q['topic'])
            q_text = escape_gift_text(q['question_text'])

            lines.append(f'::{title}::{q_text}{{')

            # Parse answer format (e.g., "1 → B, 2 → C, 3 → D, 4 → A")
            answer_pairs = re.findall(r'(\d+)\s*→\s*([A-D])', q['answer_text'])

            for item_num, option_letter in answer_pairs:
                item_idx = int(item_num) - 1
                if item_idx < len(q['items']):
                    item_text = escape_gift_text(q['items'][item_idx])
                    match_text = escape_gift_text(q['options'][option_letter])
                    lines.append(f'={item_text} -> {match_text}')

            lines.append('}')
            lines.append('')

    return '\n'.join(lines)


def main():
    """Export Week 2 quiz to GIFT format."""
    quiz_file = Path('courses/BCI2AU-business-communication/weeks/week-02/quiz-questions.md')
    output_file = Path('courses/BCI2AU-business-communication/weeks/week-02/output/week-02-quiz.gift')

    # Parse quiz
    quiz_data = parse_structured_quiz(str(quiz_file))

    # Extract week title from file
    with open(quiz_file, 'r', encoding='utf-8') as f:
        first_lines = f.read(500)
        topic_match = re.search(r'\*\*Topic:\*\*\s*(.+)', first_lines)
        week_title = topic_match.group(1).strip() if topic_match else 'Quiz'

    # Format to GIFT
    gift_content = format_to_gift(quiz_data, 2, week_title)

    # Write output
    output_file.parent.mkdir(exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(gift_content)

    print(f"✓ Quiz exported to: {output_file}")
    print(f"  Questions: {len(quiz_data)}")

    # Print Bloom's distribution
    remembering = sum(1 for q in quiz_data if q.get('category') == 'Remembering')
    understanding = sum(1 for q in quiz_data if q.get('category') == 'Understanding')
    print(f"  Remembering: {remembering}")
    print(f"  Understanding: {understanding}")


if __name__ == '__main__':
    main()
