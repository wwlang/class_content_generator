#!/usr/bin/env python3
"""
Strip course code and instructor metadata from lecture-content.md files.

Removes lines like:
- **Course:** PPDK66B Personal & Professional Development
- **Instructor:** William Winterton Lang, Le Huong Lan (PhD)
- **Instructors:** ...
"""

import re
from pathlib import Path
import sys


def strip_metadata(content: str) -> str:
    """Remove course code and instructor metadata."""
    lines = content.split('\n')
    cleaned_lines = []

    # Skip lines with course code and instructor metadata
    skip_patterns = [
        r'^\*\*Course:\*\*\s+[A-Z0-9]+\s+',  # **Course:** PPDK66B ...
        r'^\*\*Instructor',                    # **Instructor** or **Instructors**
    ]

    for line in lines:
        # Check if line matches any skip pattern
        should_skip = any(re.search(pattern, line) for pattern in skip_patterns)

        if not should_skip:
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python strip_lecture_metadata.py COURSE_CODE [week_number]")
        print("Examples:")
        print("  python strip_lecture_metadata.py PPDK66B      # All weeks")
        print("  python strip_lecture_metadata.py PPDK66B 5    # Week 5 only")
        sys.exit(1)

    course_code = sys.argv[1]

    # Parse week specification
    if len(sys.argv) >= 3:
        weeks = [int(sys.argv[2])]
    else:
        weeks = list(range(1, 13))

    # Find course directory
    courses_dir = Path(__file__).parent.parent / 'courses'
    course_dirs = list(courses_dir.glob(f'{course_code}*'))

    if not course_dirs:
        print(f"Error: Course {course_code} not found")
        sys.exit(1)

    course_dir = course_dirs[0]

    print(f"Stripping metadata from lecture-content.md files for {course_code}")
    print(f"Weeks: {weeks}")
    print()

    results = []

    for week_num in weeks:
        week_dir = course_dir / 'weeks' / f'week-{week_num:02d}'
        lecture_path = week_dir / 'lecture-content.md'

        if not lecture_path.exists():
            print(f"⚠ Week {week_num}: lecture-content.md not found - skipping")
            results.append((week_num, "MISSING"))
            continue

        # Read original content
        original_content = lecture_path.read_text()

        # Strip metadata
        cleaned_content = strip_metadata(original_content)

        # Check if anything changed
        if original_content == cleaned_content:
            print(f"  Week {week_num:2d}: No metadata found - skipping")
            results.append((week_num, "UNCHANGED"))
            continue

        # Write cleaned content back
        lecture_path.write_text(cleaned_content)

        print(f"✓ Week {week_num:2d}: Metadata stripped")
        results.append((week_num, "UPDATED"))

    print()
    print("=" * 80)
    print("Metadata Stripping Complete")
    print("=" * 80)
    print()

    updated_count = len([r for r in results if r[1] == "UPDATED"])
    print(f"Updated {updated_count} files")

    if updated_count > 0:
        print()
        print("Next steps:")
        print("1. Review changes: git diff")
        print("2. Regenerate Gemini prompts if needed: /gemini-handoff PPDK66B")


if __name__ == '__main__':
    main()
