#!/usr/bin/env python3
"""
Validate lecture-content XML files.

Checks:
- XML slide structure and syntax
- Required attributes (number, title)
- Slide numbering sequence
- Speaker notes presence
- Content completeness
- Comparison against original markdown (if available)

Usage:
    python tools/validate_lecture_xml.py COURSE_CODE [OPTIONS]

Options:
    --week N        Validate only week N
    --strict        Fail on warnings (missing speaker notes, etc.)
    --compare       Compare against original markdown files
    --all-courses   Validate all courses

Examples:
    python tools/validate_lecture_xml.py BCI2AU
    python tools/validate_lecture_xml.py BCI2AU --week 1 --compare
    python tools/validate_lecture_xml.py --all-courses
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

from lecture_parser import create_parser, XMLParser, MarkdownParser


@dataclass
class ValidationIssue:
    """A single validation issue."""
    level: str  # ERROR, WARNING, INFO
    message: str
    slide_number: Optional[int] = None


@dataclass
class ValidationResult:
    """Result of validating a single file."""
    week_num: int
    file_path: Path
    is_valid: bool
    format_detected: str
    slide_count: int
    issues: List[ValidationIssue] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return len([i for i in self.issues if i.level == "ERROR"])

    @property
    def warning_count(self) -> int:
        return len([i for i in self.issues if i.level == "WARNING"])


@dataclass
class ValidationReport:
    """Summary report for batch validation."""
    course_code: str
    results: List[ValidationResult]

    @property
    def total_files(self) -> int:
        return len(self.results)

    @property
    def valid_count(self) -> int:
        return len([r for r in self.results if r.is_valid])

    @property
    def total_errors(self) -> int:
        return sum(r.error_count for r in self.results)

    @property
    def total_warnings(self) -> int:
        return sum(r.warning_count for r in self.results)


def validate_xml_structure(content: str) -> List[ValidationIssue]:
    """Validate XML slide structure."""
    issues = []

    # Check for slide tags
    slide_tags = re.findall(r'<slide\s+([^>]+)>', content)
    if not slide_tags:
        issues.append(ValidationIssue("ERROR", "No <slide> tags found"))
        return issues

    # Check each slide tag for required attributes
    for i, attrs in enumerate(slide_tags):
        slide_num = i + 1

        # Check number attribute
        number_match = re.search(r'number="(\d+)"', attrs)
        if not number_match:
            issues.append(ValidationIssue(
                "ERROR",
                f"Missing 'number' attribute",
                slide_num
            ))
        else:
            actual_num = int(number_match.group(1))
            if actual_num != slide_num:
                issues.append(ValidationIssue(
                    "WARNING",
                    f"Slide number mismatch: expected {slide_num}, found {actual_num}",
                    slide_num
                ))

        # Check title attribute
        if 'title="' not in attrs:
            issues.append(ValidationIssue(
                "ERROR",
                f"Missing 'title' attribute",
                slide_num
            ))

    # Check for closing tags
    open_count = len(re.findall(r'<slide\s+[^>]+>', content))
    close_count = len(re.findall(r'</slide>', content))
    if open_count != close_count:
        issues.append(ValidationIssue(
            "ERROR",
            f"Mismatched slide tags: {open_count} opening, {close_count} closing"
        ))

    # Check speaker-notes tags
    open_notes = len(re.findall(r'<speaker-notes>', content))
    close_notes = len(re.findall(r'</speaker-notes>', content))
    if open_notes != close_notes:
        issues.append(ValidationIssue(
            "ERROR",
            f"Mismatched speaker-notes tags: {open_notes} opening, {close_notes} closing"
        ))

    return issues


def validate_content_completeness(content: str) -> List[ValidationIssue]:
    """Check for content completeness issues."""
    issues = []

    parser = create_parser(content)
    if not isinstance(parser, XMLParser):
        issues.append(ValidationIssue("INFO", "File is not in XML format"))
        return issues

    try:
        lecture = parser.parse(content)
    except Exception as e:
        issues.append(ValidationIssue("ERROR", f"Parse error: {e}"))
        return issues

    # Check slide count
    if lecture.slide_count < 22:
        issues.append(ValidationIssue(
            "WARNING",
            f"Low slide count: {lecture.slide_count} (minimum 22 recommended)"
        ))
    elif lecture.slide_count > 30:
        issues.append(ValidationIssue(
            "WARNING",
            f"High slide count: {lecture.slide_count} (maximum 30 recommended)"
        ))

    # Check each slide
    for slide in lecture.slides:
        # Check for empty content
        if not slide.content.strip():
            issues.append(ValidationIssue(
                "WARNING",
                f"Empty content",
                slide.number
            ))

        # Check for missing speaker notes
        if not slide.speaker_notes.strip():
            issues.append(ValidationIssue(
                "WARNING",
                f"Missing speaker notes",
                slide.number
            ))

        # Check for very short content (likely incomplete)
        if len(slide.content.strip()) < 20:
            issues.append(ValidationIssue(
                "WARNING",
                f"Very short content ({len(slide.content.strip())} chars)",
                slide.number
            ))

    return issues


def compare_with_original(
    xml_path: Path,
    md_path: Path
) -> List[ValidationIssue]:
    """Compare XML file against original markdown."""
    issues = []

    if not md_path.exists():
        issues.append(ValidationIssue(
            "INFO",
            f"Original markdown not found: {md_path.name}"
        ))
        return issues

    try:
        xml_content = xml_path.read_text(encoding='utf-8')
        md_content = md_path.read_text(encoding='utf-8')
    except Exception as e:
        issues.append(ValidationIssue("ERROR", f"Read error: {e}"))
        return issues

    # Count slides in both
    xml_parser = create_parser(xml_content)
    md_parser = create_parser(md_content)

    xml_count = xml_parser.count_slides(xml_content)
    md_count = md_parser.count_slides(md_content)

    if xml_count != md_count:
        issues.append(ValidationIssue(
            "ERROR",
            f"Slide count mismatch: XML has {xml_count}, markdown has {md_count}"
        ))

    # Parse both and compare titles
    try:
        xml_lecture = xml_parser.parse(xml_content)
        md_lecture = md_parser.parse(md_content)

        for xml_slide, md_slide in zip(xml_lecture.slides, md_lecture.slides):
            if xml_slide.title != md_slide.title:
                issues.append(ValidationIssue(
                    "WARNING",
                    f"Title mismatch: '{xml_slide.title}' vs '{md_slide.title}'",
                    xml_slide.number
                ))
    except Exception as e:
        issues.append(ValidationIssue(
            "WARNING",
            f"Could not compare slide details: {e}"
        ))

    return issues


def validate_file(
    file_path: Path,
    week_num: int,
    strict: bool = False,
    compare: bool = False
) -> ValidationResult:
    """Validate a single lecture content file."""
    issues = []

    # Check file exists
    if not file_path.exists():
        return ValidationResult(
            week_num=week_num,
            file_path=file_path,
            is_valid=False,
            format_detected="N/A",
            slide_count=0,
            issues=[ValidationIssue("ERROR", "File not found")]
        )

    # Read content
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return ValidationResult(
            week_num=week_num,
            file_path=file_path,
            is_valid=False,
            format_detected="N/A",
            slide_count=0,
            issues=[ValidationIssue("ERROR", f"Read error: {e}")]
        )

    # Detect format
    parser = create_parser(content)
    format_detected = type(parser).__name__

    # Get slide count
    slide_count = parser.count_slides(content)

    # Run validations
    if isinstance(parser, XMLParser):
        issues.extend(validate_xml_structure(content))

    issues.extend(validate_content_completeness(content))

    # Compare with original if requested
    if compare and file_path.name == 'lecture-content-xml.md':
        original_path = file_path.parent / 'lecture-content.md'
        issues.extend(compare_with_original(file_path, original_path))

    # Determine validity
    error_count = len([i for i in issues if i.level == "ERROR"])
    warning_count = len([i for i in issues if i.level == "WARNING"])

    is_valid = error_count == 0
    if strict and warning_count > 0:
        is_valid = False

    return ValidationResult(
        week_num=week_num,
        file_path=file_path,
        is_valid=is_valid,
        format_detected=format_detected,
        slide_count=slide_count,
        issues=issues
    )


def validate_course(
    course_code: str,
    weeks: Optional[List[int]] = None,
    strict: bool = False,
    compare: bool = False,
    prefer_xml: bool = True
) -> ValidationReport:
    """Validate all lecture content files for a course."""
    # Find course directory
    courses_dir = Path(__file__).parent.parent / 'courses'
    course_dirs = list(courses_dir.glob(f'{course_code}*'))

    if not course_dirs:
        return ValidationReport(course_code=course_code, results=[])

    course_dir = course_dirs[0]

    # Default to all weeks
    if weeks is None:
        weeks = list(range(1, 13))

    results = []

    for week_num in weeks:
        week_dir = course_dir / 'weeks' / f'week-{week_num:02d}'

        # Prefer XML if available, otherwise use markdown
        if prefer_xml:
            xml_path = week_dir / 'lecture-content-xml.md'
            md_path = week_dir / 'lecture-content.md'
            file_path = xml_path if xml_path.exists() else md_path
        else:
            file_path = week_dir / 'lecture-content.md'

        result = validate_file(
            file_path=file_path,
            week_num=week_num,
            strict=strict,
            compare=compare
        )
        results.append(result)

    return ValidationReport(course_code=course_code, results=results)


def print_report(report: ValidationReport, verbose: bool = False):
    """Print a formatted validation report."""
    print()
    print("=" * 70)
    print(f"VALIDATION REPORT: {report.course_code}")
    print("=" * 70)
    print()

    for result in report.results:
        if result.is_valid:
            status = "✓"
        elif result.error_count > 0:
            status = "✗"
        else:
            status = "⚠"

        format_short = "XML" if "XML" in result.format_detected else "MD"
        print(f"{status} Week {result.week_num:2d}: {result.slide_count:2d} slides [{format_short}]", end="")

        if result.error_count > 0:
            print(f" - {result.error_count} error(s)", end="")
        if result.warning_count > 0:
            print(f" - {result.warning_count} warning(s)", end="")
        print()

        # Print issues if verbose or if there are errors
        if verbose or result.error_count > 0:
            for issue in result.issues:
                if issue.level == "ERROR" or verbose:
                    slide_ref = f" (slide {issue.slide_number})" if issue.slide_number else ""
                    print(f"    [{issue.level}]{slide_ref} {issue.message}")

    print()
    print("-" * 70)
    print(f"Summary: {report.valid_count}/{report.total_files} valid, "
          f"{report.total_errors} errors, {report.total_warnings} warnings")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Validate lecture-content XML files"
    )
    parser.add_argument(
        'course_code',
        nargs='?',
        help="Course code (e.g., BCI2AU)"
    )
    parser.add_argument(
        '--week',
        type=int,
        help="Validate only this week number"
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help="Fail on warnings (missing speaker notes, etc.)"
    )
    parser.add_argument(
        '--compare',
        action='store_true',
        help="Compare against original markdown files"
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help="Show all issues including warnings"
    )
    parser.add_argument(
        '--all-courses',
        action='store_true',
        help="Validate all courses"
    )
    parser.add_argument(
        '--markdown',
        action='store_true',
        help="Validate markdown files instead of XML"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.course_code and not args.all_courses:
        parser.print_help()
        print("\nError: Either COURSE_CODE or --all-courses is required")
        sys.exit(1)

    weeks = [args.week] if args.week else None
    prefer_xml = not args.markdown

    if args.all_courses:
        # Validate all courses
        courses_dir = Path(__file__).parent.parent / 'courses'
        course_dirs = [d for d in courses_dir.iterdir() if d.is_dir()]

        all_valid = True
        for course_dir in sorted(course_dirs):
            course_code = course_dir.name.split('-')[0]
            report = validate_course(
                course_code=course_code,
                weeks=weeks,
                strict=args.strict,
                compare=args.compare,
                prefer_xml=prefer_xml
            )
            print_report(report, verbose=args.verbose)
            if report.total_errors > 0:
                all_valid = False

        sys.exit(0 if all_valid else 1)
    else:
        # Validate single course
        report = validate_course(
            course_code=args.course_code,
            weeks=weeks,
            strict=args.strict,
            compare=args.compare,
            prefer_xml=prefer_xml
        )
        print_report(report, verbose=args.verbose)
        sys.exit(0 if report.total_errors == 0 else 1)


if __name__ == '__main__':
    main()
