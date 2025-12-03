#!/usr/bin/env python3
"""
Export YAML-format quiz questions to Moodle GIFT format.

Simple standalone script that directly parses YAML and generates GIFT format.

Usage:
    python3 tools/export_yaml_quiz_to_gift.py <course_code> <week_number>

Example:
    python3 tools/export_yaml_quiz_to_gift.py BCI2AU 1
"""

import sys
import re
from pathlib import Path
import yaml


def escape_gift_text(text: str) -> str:
    """
    Escape special characters for GIFT format and convert markdown bold to HTML.

    GIFT special characters that need escaping:
    - Backslash, braces, equals, tilde, hash, colon

    Also converts **text** to <b>text</b>
    """
    # Convert markdown bold to HTML BEFORE escaping
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)

    # Escape special GIFT characters
    text = text.replace('\\', '\\\\')
    text = text.replace('{', '\\{')
    text = text.replace('}', '\\}')
    text = text.replace('=', '\\=')
    text = text.replace('~', '\\~')
    text = text.replace('#', '\\#')
    text = text.replace(':', '\\:')

    return text


def parse_yaml_quiz(file_path: Path) -> dict:
    """Parse YAML quiz file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---\s*$', content, re.DOTALL)
    if not match:
        raise ValueError("No YAML frontmatter found")

    yaml_content = match.group(1)
    data = yaml.safe_load(yaml_content)

    return data


def export_to_gift(quiz_data: dict, week_number: int, course_code: str) -> str:
    """Convert quiz data to GIFT format."""
    lines = []

    # Header comments
    metadata = quiz_data.get('metadata', {})
    topic = metadata.get('topic', 'Quiz')
    lines.append(f'// Week {week_number}: {topic}')
    lines.append(f'// Questions: {len(quiz_data.get("questions", []))}')
    lines.append('')

    # Category
    lines.append(f'$CATEGORY: {course_code} - Week {week_number}')
    lines.append('')

    # Export each question
    for q in quiz_data.get('questions', []):
        gift_q = export_question(q)
        lines.append(gift_q)
        lines.append('')

    return '\n'.join(lines)


def export_question(q: dict) -> str:
    """Export single question to GIFT format."""
    # Question title and text
    title = escape_gift_text(q['topic'])
    q_text = escape_gift_text(q['question'].strip())

    lines = [f'::{title}::{q_text}{{']

    # Find correct answer
    correct_key = None
    for opt in q['options']:
        if opt.get('correct', False):
            correct_key = opt['key']
            break

    # Add options
    for opt in q['options']:
        opt_text = escape_gift_text(opt['text'])
        feedback = escape_gift_text(opt.get('feedback', ''))

        if opt['key'] == correct_key:
            # Correct answer
            if feedback:
                lines.append(f'={opt_text} #{feedback}')
            else:
                lines.append(f'={opt_text}')
        else:
            # Wrong answer
            if feedback:
                lines.append(f'~{opt_text} #{feedback}')
            else:
                lines.append(f'~{opt_text}')

    # General feedback
    general_fb = q.get('general_feedback', '').strip()
    if general_fb:
        general_fb = escape_gift_text(general_fb)
        lines.append(f'####{general_fb}}}')
    else:
        lines.append('}')

    return '\n'.join(lines)


def export_quiz(course_code: str, week_number: int) -> Path:
    """
    Export quiz questions from YAML format to GIFT format.

    Args:
        course_code: Course code (e.g., BCI2AU)
        week_number: Week number

    Returns:
        Path to generated GIFT file
    """
    # Find course directory
    courses_dir = Path("courses")
    course_dirs = list(courses_dir.glob(f"{course_code}*"))

    if not course_dirs:
        raise FileNotFoundError(f"No course directory found matching '{course_code}'")

    course_dir = course_dirs[0]

    # Find week directory
    week_dir = course_dir / "weeks" / f"week-{week_number:02d}"

    if not week_dir.exists():
        raise FileNotFoundError(f"Week directory not found: {week_dir}")

    # Parse quiz questions
    quiz_file = week_dir / "quiz-questions.md"

    if not quiz_file.exists():
        raise FileNotFoundError(f"Quiz questions file not found: {quiz_file}")

    print(f"Parsing {quiz_file.name}...")
    quiz_data = parse_yaml_quiz(quiz_file)

    questions = quiz_data.get('questions', [])
    if not questions:
        raise ValueError("No questions found in quiz file")

    print(f"✓ Parsed {len(questions)} questions")

    # Convert to GIFT
    print(f"Exporting to GIFT format...")
    gift_content = export_to_gift(quiz_data, week_number, course_code)

    # Write output
    output_dir = week_dir / "output"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"week-{week_number:02d}-quiz.gift"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(gift_content)

    print(f"✓ Exported to: {output_file}")
    print(f"  Questions: {len(questions)}")

    # Count Bloom levels
    bloom_counts = {}
    for q in questions:
        level = q.get('bloom_level', 'unknown')
        bloom_counts[level] = bloom_counts.get(level, 0) + 1

    print(f"  Bloom's: {bloom_counts.get('remembering', 0)} Remembering, {bloom_counts.get('understanding', 0)} Understanding")

    return output_file


def main():
    """Command-line interface."""
    if len(sys.argv) < 3:
        print("Usage: python3 export_yaml_quiz_to_gift.py <course_code> <week_number>")
        print("Example: python3 export_yaml_quiz_to_gift.py BCI2AU 1")
        sys.exit(1)

    course_code = sys.argv[1]
    week_number = int(sys.argv[2])

    try:
        export_quiz(course_code, week_number)
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
