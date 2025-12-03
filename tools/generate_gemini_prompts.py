#!/usr/bin/env python3
"""
Generate Gemini handoff prompts for all weeks of a course.
"""

import re
from pathlib import Path
import sys
from lecture_parser import create_parser


def strip_speaker_notes(content: str) -> str:
    """Remove speaker notes sections from lecture content (XML format)."""
    # Remove XML <speaker-notes>...</speaker-notes> tags and their content
    content = re.sub(
        r'<speaker-notes>.*?</speaker-notes>\s*',
        '',
        content,
        flags=re.DOTALL
    )
    return content


def strip_metadata(content: str) -> str:
    """Remove XML metadata block (provided separately in template header)."""
    # Remove entire XML <metadata>...</metadata> block
    content = re.sub(
        r'<metadata>.*?</metadata>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove <?xml ...?> declaration if present
    content = re.sub(r'<\?xml[^>]*\?>\s*', '', content)

    return content.strip()


def consolidate_blank_lines(content: str) -> str:
    """Consolidate multiple consecutive blank lines into single blank lines."""
    return re.sub(r'\n{3,}', '\n\n', content)


def count_slides(content: str) -> int:
    """Count number of slides in lecture content (supports both markdown and XML)."""
    parser = create_parser(content)
    return parser.count_slides(content)


def extract_topic(content: str, week_num: int) -> str:
    """Extract week topic from lecture content (supports both markdown and XML)."""
    parser = create_parser(content)
    try:
        lecture_data = parser.parse(content)
        return lecture_data.topic
    except Exception:
        # Fallback to regex if parsing fails
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            topic = h1_match.group(1).strip()
            topic = re.sub(r'^Week\s+\d+:\s*', '', topic, count=1, flags=re.IGNORECASE)
            return topic
        return f"Week {week_num} Topic"


def load_template() -> str:
    """Load Gemini prompt template from .claude/templates/."""
    template_path = Path(__file__).parent.parent / '.claude' / 'templates' / 'gemini-slide-handoff-prompt.md'
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text()


def generate_prompt(course_name: str, university: str, campus: str, week_num: int,
                   topic: str, slide_count: int, lecture_content: str) -> str:
    """Generate complete Gemini prompt by loading template and substituting placeholders."""

    # Load template from file
    template = load_template()

    # Substitute placeholders
    prompt_content = template.replace('{{COURSE_NAME}}', course_name)
    prompt_content = prompt_content.replace('{{WEEK_NUMBER}}', f'{week_num:02d}')
    prompt_content = prompt_content.replace('{{TOPIC}}', topic)
    prompt_content = prompt_content.replace('{{UNIVERSITY}}', university)
    prompt_content = prompt_content.replace('{{CAMPUS}}', campus)
    prompt_content = prompt_content.replace('{{SLIDE_COUNT}}', str(slide_count))
    prompt_content = prompt_content.replace('{{LECTURE_CONTENT}}', lecture_content)

    return prompt_content


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_gemini_prompts.py COURSE_CODE [week_range]")
        print("Examples:")
        print("  python generate_gemini_prompts.py PPDK66B")
        print("  python generate_gemini_prompts.py PPDK66B 1-12")
        print("  python generate_gemini_prompts.py BCI2AU 5")
        sys.exit(1)

    course_code = sys.argv[1]

    # Parse week range
    if len(sys.argv) >= 3:
        week_arg = sys.argv[2]
        if '-' in week_arg:
            start, end = map(int, week_arg.split('-'))
            weeks = list(range(start, end + 1))
        else:
            weeks = [int(week_arg)]
    else:
        # Default: all weeks (1-12)
        weeks = list(range(1, 13))

    # Find course directory
    courses_dir = Path(__file__).parent.parent / 'courses'
    course_dirs = list(courses_dir.glob(f'{course_code}*'))

    if not course_dirs:
        print(f"Error: Course {course_code} not found")
        sys.exit(1)

    course_dir = course_dirs[0]

    # Read course-info.md for course metadata (canonical source)
    course_info_path = course_dir / 'course-info.md'
    if course_info_path.exists():
        course_info = course_info_path.read_text()
    else:
        course_info = ""

    # Extract course name from course-info.md
    course_name_match = re.search(r'\*\*Course Name:\*\*\s*(.+)', course_info)
    course_name = course_name_match.group(1).strip() if course_name_match else "Course"

    # Extract university from course-info.md
    university_match = re.search(r'\*\*University:\*\*\s*(.+)', course_info)
    university = university_match.group(1).strip() if university_match else "University"

    # Extract campus from course-info.md
    campus_match = re.search(r'\*\*Campus:\*\*\s*(.+)', course_info)
    campus = campus_match.group(1).strip() if campus_match else ""

    print(f"Generating Gemini prompts for {course_name}")
    print(f"Institution: {university}")
    print(f"Weeks: {weeks}")
    print()

    results = []

    for week_num in weeks:
        week_dir = course_dir / 'weeks' / f'week-{week_num:02d}'

        # Prefer XML format if available, otherwise use markdown
        xml_path = week_dir / 'lecture-content-xml.md'
        md_path = week_dir / 'lecture-content.md'
        lecture_path = xml_path if xml_path.exists() else md_path

        if not lecture_path.exists():
            print(f"⚠ Week {week_num}: lecture-content.md not found - skipping")
            results.append((week_num, "MISSING", 0))
            continue

        # Read lecture content
        lecture_content = lecture_path.read_text()

        # Extract info
        topic = extract_topic(lecture_content, week_num)
        slide_count = count_slides(lecture_content)

        # Validate slide count (24+ minimum from lecture-structure.md)
        if slide_count < 24:
            print(f"⚠ Week {week_num}: Only {slide_count} slides (minimum 24 required)")
            print(f"   → Check for merged concepts; each idea needs its own slide")

        # Strip speaker notes, metadata, and consolidate blank lines
        clean_content = strip_speaker_notes(lecture_content)
        clean_content = strip_metadata(clean_content)
        clean_content = consolidate_blank_lines(clean_content)

        # Generate prompt
        prompt = generate_prompt(
            course_name, university, campus, week_num, topic, slide_count, clean_content
        )

        # Save prompt
        output_path = week_dir / 'gemini-prompt.md'
        output_path.write_text(prompt)

        print(f"✓ Week {week_num:2d}: {topic[:50]:<50} ({slide_count:2d} slides)")
        results.append((week_num, topic, slide_count))

    print()
    print("=" * 80)
    print("Gemini Handoff Ready - All Weeks")
    print("=" * 80)
    print()
    print(f"Generated {len([r for r in results if r[1] != 'MISSING'])} prompts")
    print()
    print("Next steps:")
    print("1. Open gemini-prompt.md in each week folder")
    print("2. Copy entire contents → Paste into Google Gemini")
    print("3. Download as week-NN.pptx")
    print("4. Run: /add-speaker-notes [CODE] [N]")
    print()
    print("Summary:")
    for week_num, topic, slides in results:
        if topic == "MISSING":
            print(f"  Week {week_num:2d}: MISSING")
        else:
            print(f"  Week {week_num:2d}: {slides:2d} slides - {topic}")


if __name__ == '__main__':
    main()
