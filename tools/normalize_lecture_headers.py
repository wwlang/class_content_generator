#!/usr/bin/env python3
"""
Normalize lecture-content.md headers to standard XML format.

Standard format:
<?xml version="1.0" encoding="UTF-8"?>
<lecture>
<metadata>
<course>CODE Course Name</course>
<week>N</week>
<topic>Topic Name</topic>
<duration>90 minutes</duration>
</metadata>

<slide number="1" ...>
"""

import re
import sys
from pathlib import Path


# Topic mapping from syllabus
TOPICS = {
    'BCI2AU': {
        1: 'Communication Strategy Foundations',
        2: 'Audience Analysis & Stakeholder Mapping',
        3: 'Structured Business Writing',
        4: 'Persuasive Written Communication',
        5: 'Oral Communication Fundamentals',
        6: 'Visual Communication & Slide Design',
        7: 'Persuasive Presentations',
        8: 'High-Stakes Communication',
        9: 'Cross-Cultural & Team Communication',
        10: 'Integration & Capstone',
    },
    'PPDK66B': {
        1: 'Introduction & Future of Work',
        2: 'Career Skills in the AI Era',
        3: 'Reflection & Reflective Learning',
        4: 'Self-Managed Learning',
        5: 'Self-Discovery Through Assessment',
        7: 'Transferable Skills & Emotional Intelligence',
        8: 'Time, Energy & Habit Management',
        9: 'Growth Mindset & Adaptability',
        11: 'Designing Your Development Plan',
        12: 'Integration & Continuous Growth',
    }
}

COURSE_NAMES = {
    'BCI2AU': 'Business Communication',
    'PPDK66B': 'Personal & Professional Development',
}


def extract_first_slide(content: str) -> str:
    """Extract everything from first <slide> tag onwards."""
    match = re.search(r'(<slide\s+[^>]+>.*)', content, re.DOTALL)
    return match.group(1) if match else content


def count_slides(content: str) -> int:
    """Count number of slides."""
    return len(re.findall(r'<slide\s+[^>]+>', content))


def normalize_file(file_path: Path, course_code: str, week_num: int, dry_run: bool = False) -> bool:
    """Normalize a single lecture-content.md file."""
    content = file_path.read_text(encoding='utf-8')

    # Get topic from mapping
    topic = TOPICS.get(course_code, {}).get(week_num, f'Week {week_num}')
    course_name = COURSE_NAMES.get(course_code, 'Course')

    # Extract slides content (everything from first <slide> onwards)
    slides_content = extract_first_slide(content)
    slide_count = count_slides(slides_content)

    # Escape ampersands in topic for XML
    topic_xml = topic.replace('&', '&amp;')

    # Build standard header
    header = f'''<?xml version="1.0" encoding="UTF-8"?>
<lecture>
<metadata>
<course>{course_code} {course_name}</course>
<week>{week_num}</week>
<topic>{topic_xml}</topic>
<duration>90 minutes</duration>
<slides>{slide_count}</slides>
</metadata>

'''

    # Combine header with slides
    new_content = header + slides_content

    if dry_run:
        print(f"  Would normalize: {file_path.name}")
        print(f"    Topic: {topic}")
        print(f"    Slides: {slide_count}")
        return True

    # Write normalized content
    file_path.write_text(new_content, encoding='utf-8')
    print(f"  ✓ Normalized: Week {week_num:02d} - {topic} ({slide_count} slides)")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python normalize_lecture_headers.py COURSE_CODE [--dry-run]")
        print("Example: python normalize_lecture_headers.py BCI2AU")
        sys.exit(1)

    course_code = sys.argv[1]
    dry_run = '--dry-run' in sys.argv

    # Find course directory
    courses_dir = Path(__file__).parent.parent / 'courses'
    course_dirs = list(courses_dir.glob(f'{course_code}*'))

    if not course_dirs:
        print(f"Error: Course {course_code} not found")
        sys.exit(1)

    course_dir = course_dirs[0]
    weeks_dir = course_dir / 'weeks'

    print(f"Normalizing lecture headers for {course_code}")
    if dry_run:
        print("(DRY RUN - no changes will be made)")
    print()

    normalized = 0
    for week_dir in sorted(weeks_dir.glob('week-*')):
        week_num = int(week_dir.name.split('-')[1])
        lecture_file = week_dir / 'lecture-content.md'

        if lecture_file.exists():
            if normalize_file(lecture_file, course_code, week_num, dry_run):
                normalized += 1

    print()
    print(f"Normalized {normalized} files")


if __name__ == '__main__':
    main()
