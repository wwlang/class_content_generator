#!/usr/bin/env python3
"""
Renumber slides in lecture-content XML files.

Automatically fixes slide numbering after inserting or deleting slides.
Works with both XML format (<slide number="N">) and markdown format (## Slide N:).

Usage:
    python tools/renumber_slides.py COURSE_CODE WEEK_NUMBER
    python tools/renumber_slides.py COURSE_CODE WEEK_NUMBER --dry-run

Examples:
    python tools/renumber_slides.py BCI2AU 1
    python tools/renumber_slides.py BCI2AU 1 --dry-run
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

from lecture_parser import create_parser, XMLParser


def renumber_xml_slides(content: str) -> Tuple[str, List[Tuple[int, int]]]:
    """
    Renumber XML slides sequentially starting from 1.

    Returns: (updated_content, list of (old_num, new_num) changes)
    """
    changes = []
    current_num = 0

    def replace_number(match):
        nonlocal current_num
        current_num += 1
        old_num = int(match.group(1))
        if old_num != current_num:
            changes.append((old_num, current_num))
        return f'<slide number="{current_num}"'

    # Replace all slide number attributes
    updated = re.sub(
        r'<slide\s+number="(\d+)"',
        replace_number,
        content
    )

    return updated, changes


def renumber_markdown_slides(content: str) -> Tuple[str, List[Tuple[int, int]]]:
    """
    Renumber markdown slides sequentially starting from 1.

    Returns: (updated_content, list of (old_num, new_num) changes)
    """
    changes = []
    current_num = 0

    def replace_number(match):
        nonlocal current_num
        current_num += 1
        old_num = int(match.group(2))
        hashes = match.group(1)
        title = match.group(3)
        if old_num != current_num:
            changes.append((old_num, current_num))
        return f'{hashes} Slide {current_num}: {title}'

    # Replace all slide headers (##, ###, or ####)
    updated = re.sub(
        r'^(#{2,4})\s+Slide\s+(\d+):\s*(.+)$',
        replace_number,
        content,
        flags=re.MULTILINE
    )

    return updated, changes


def renumber_file(
    file_path: Path,
    dry_run: bool = False
) -> Tuple[bool, int, List[Tuple[int, int]]]:
    """
    Renumber slides in a file.

    Returns: (success, slide_count, changes)
    """
    if not file_path.exists():
        return False, 0, []

    content = file_path.read_text(encoding='utf-8')

    # Detect format
    parser = create_parser(content)
    is_xml = isinstance(parser, XMLParser)

    # Get original slide count
    original_count = parser.count_slides(content)

    # Renumber based on format
    if is_xml:
        updated_content, changes = renumber_xml_slides(content)
    else:
        updated_content, changes = renumber_markdown_slides(content)

    # Write if not dry run and there are changes
    if changes and not dry_run:
        file_path.write_text(updated_content, encoding='utf-8')

    return True, original_count, changes


def main():
    parser = argparse.ArgumentParser(
        description="Renumber slides in lecture-content files"
    )
    parser.add_argument(
        'course_code',
        help="Course code (e.g., BCI2AU)"
    )
    parser.add_argument(
        'week_number',
        type=int,
        help="Week number"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Preview changes without writing"
    )

    args = parser.parse_args()

    # Find course directory
    courses_dir = Path(__file__).parent.parent / 'courses'
    course_dirs = list(courses_dir.glob(f'{args.course_code}*'))

    if not course_dirs:
        print(f"Error: Course {args.course_code} not found")
        sys.exit(1)

    course_dir = course_dirs[0]
    week_dir = course_dir / 'weeks' / f'week-{args.week_number:02d}'

    # Prefer XML format
    xml_path = week_dir / 'lecture-content-xml.md'
    md_path = week_dir / 'lecture-content.md'
    file_path = xml_path if xml_path.exists() else md_path

    if not file_path.exists():
        print(f"Error: No lecture content found in {week_dir}")
        sys.exit(1)

    print(f"Renumbering slides in: {file_path.name}")
    if args.dry_run:
        print("(DRY RUN - no changes will be written)")
    print()

    success, slide_count, changes = renumber_file(file_path, args.dry_run)

    if not success:
        print("Error: Failed to process file")
        sys.exit(1)

    print(f"Total slides: {slide_count}")

    if changes:
        print(f"\nChanges ({len(changes)}):")
        for old_num, new_num in changes:
            print(f"  Slide {old_num} → Slide {new_num}")

        if args.dry_run:
            print("\nRun without --dry-run to apply changes.")
        else:
            print("\nChanges applied successfully.")
    else:
        print("\nNo renumbering needed - slides are already sequential.")


if __name__ == '__main__':
    main()
