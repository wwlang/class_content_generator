#!/usr/bin/env python3
"""
Course Quality Validator CLI

AI-powered validation for university teaching content quality.
Runs all validators and generates comprehensive report.

Usage:
    python validate_course_quality.py <course_path> [options]
    python validate_course_quality.py courses/BCI2AU-business-communication --report

Options:
    --report        Generate markdown report file
    --phase1        Run only Phase 1 validators (critical alignment)
    --phase2        Run only Phase 2 validators (quality checks)
    --validator X   Run specific validator only
    --fix           Auto-fix suggestions where possible (coming soon)
"""

import argparse
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.content_validators import (
    ValidationReport,
    ValidationResult,
    IssueSeverity,
    # Phase 1
    BloomLevelValidator,
    TutorialAssessmentValidator,
    LectureQuizValidator,
    FrameworkScaffoldingValidator,
    # Phase 2
    LearningObjectiveValidator,
    RubricValidator,
    TerminologyValidator,
    CulturalSensitivityValidator,
)


PHASE1_VALIDATORS = [
    BloomLevelValidator,
    TutorialAssessmentValidator,
    LectureQuizValidator,
    FrameworkScaffoldingValidator,
]

PHASE2_VALIDATORS = [
    LearningObjectiveValidator,
    RubricValidator,
    TerminologyValidator,
    CulturalSensitivityValidator,
]

ALL_VALIDATORS = PHASE1_VALIDATORS + PHASE2_VALIDATORS

VALIDATOR_MAP = {
    'bloom': BloomLevelValidator,
    'tutorial': TutorialAssessmentValidator,
    'lecture-quiz': LectureQuizValidator,
    'scaffolding': FrameworkScaffoldingValidator,
    'learning-objectives': LearningObjectiveValidator,
    'rubric': RubricValidator,
    'terminology': TerminologyValidator,
    'cultural': CulturalSensitivityValidator,
}


def print_header(text: str):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_result(result: ValidationResult):
    """Print validation result with formatting."""
    status = "PASSED" if result.passed else "FAILED"
    status_color = "\033[92m" if result.passed else "\033[91m"
    reset = "\033[0m"

    print(f"\n{result.validator_name}: {status_color}{status}{reset}")
    print(f"  {result.summary}")
    print(f"  Duration: {result.duration_seconds:.2f}s | Items checked: {result.items_checked}")

    # Count issues by severity
    critical = sum(1 for i in result.issues if i.severity == IssueSeverity.CRITICAL)
    warnings = sum(1 for i in result.issues if i.severity == IssueSeverity.WARNING)
    suggestions = sum(1 for i in result.issues if i.severity == IssueSeverity.SUGGESTION)

    if result.issues:
        print(f"  Issues: {critical} critical, {warnings} warnings, {suggestions} suggestions")

        # Show critical issues
        for issue in result.issues:
            if issue.severity == IssueSeverity.CRITICAL:
                print(f"\n    \033[91mCRITICAL\033[0m: {issue.message}")
                print(f"      Location: {issue.location}")
                if issue.suggestion:
                    print(f"      Suggestion: {issue.suggestion}")

        # Show first few warnings
        warning_issues = [i for i in result.issues if i.severity == IssueSeverity.WARNING]
        for issue in warning_issues[:3]:
            print(f"\n    \033[93mWARNING\033[0m: {issue.message}")
            print(f"      Location: {issue.location}")

        if len(warning_issues) > 3:
            print(f"\n    ... and {len(warning_issues) - 3} more warnings")


def run_validators(
    course_path: Path,
    validators: List,
    verbose: bool = True
) -> ValidationReport:
    """Run specified validators and collect results."""
    # Extract course code from path (e.g., "BCI2AU" from "BCI2AU-business-communication")
    course_code = course_path.name.split('-')[0] if '-' in course_path.name else course_path.name
    report = ValidationReport(course_code=course_code, timestamp=datetime.now())

    for validator_class in validators:
        try:
            validator = validator_class()
            if verbose:
                print(f"Running {validator.name}...", end=" ", flush=True)

            result = validator.validate(course_path)
            report.add_result(result)

            if verbose:
                status = "\033[92mOK\033[0m" if result.passed else "\033[91mISSUES\033[0m"
                print(f"{status} ({len(result.issues)} issues)")

        except Exception as e:
            if verbose:
                print(f"\033[91mERROR\033[0m: {str(e)}")
            # Create error result
            from tools.content_validators.base import ValidationIssue
            error_result = ValidationResult(
                validator_name=validator_class.__name__,
                passed=False,
                issues=[ValidationIssue(
                    validator=validator_class.__name__,
                    severity=IssueSeverity.CRITICAL,
                    message=f"Validator failed: {str(e)}",
                    location="System"
                )],
                summary=f"Error: {str(e)}",
                duration_seconds=0,
                items_checked=0
            )
            report.add_result(error_result)

    return report


def main():
    parser = argparse.ArgumentParser(
        description="Validate university course content quality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python validate_course_quality.py courses/BCI2AU-business-communication
    python validate_course_quality.py courses/BCI2AU-business-communication --report
    python validate_course_quality.py courses/BCI2AU-business-communication --phase1
    python validate_course_quality.py courses/BCI2AU-business-communication --validator bloom
        """
    )

    parser.add_argument(
        'course_path',
        type=Path,
        help='Path to course directory'
    )
    parser.add_argument(
        '--report',
        action='store_true',
        help='Generate markdown report file'
    )
    parser.add_argument(
        '--phase1',
        action='store_true',
        help='Run only Phase 1 validators (critical alignment)'
    )
    parser.add_argument(
        '--phase2',
        action='store_true',
        help='Run only Phase 2 validators (quality checks)'
    )
    parser.add_argument(
        '--validator',
        choices=list(VALIDATOR_MAP.keys()),
        help='Run specific validator only'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output for all issues'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Minimal output, only show summary'
    )

    args = parser.parse_args()

    # Validate course path
    if not args.course_path.exists():
        print(f"Error: Course path '{args.course_path}' does not exist")
        sys.exit(1)

    if not (args.course_path / 'syllabus.md').exists():
        print(f"Error: No syllabus.md found in '{args.course_path}'")
        print("Make sure you're pointing to a valid course directory")
        sys.exit(1)

    # Determine which validators to run
    if args.validator:
        validators = [VALIDATOR_MAP[args.validator]]
    elif args.phase1:
        validators = PHASE1_VALIDATORS
    elif args.phase2:
        validators = PHASE2_VALIDATORS
    else:
        validators = ALL_VALIDATORS

    # Print header
    if not args.quiet:
        print_header(f"Course Quality Validation")
        print(f"Course: {args.course_path}")
        print(f"Validators: {len(validators)}")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    # Run validators
    report = run_validators(args.course_path, validators, verbose=not args.quiet)

    # Print results
    if not args.quiet:
        print_header("Validation Results")

        for result in report.results:
            print_result(result)

        # Summary
        print_header("Summary")
        print(f"Total validators: {len(report.results)}")
        print(f"Passed: {sum(1 for r in report.results if r.passed)}")
        print(f"Failed: {sum(1 for r in report.results if not r.passed)}")
        print(f"Total duration: {report.total_duration:.2f}s")

        total_issues = sum(len(r.issues) for r in report.results)
        critical = sum(
            sum(1 for i in r.issues if i.severity == IssueSeverity.CRITICAL)
            for r in report.results
        )
        warnings = sum(
            sum(1 for i in r.issues if i.severity == IssueSeverity.WARNING)
            for r in report.results
        )

        print(f"\nTotal issues: {total_issues}")
        print(f"  Critical: {critical}")
        print(f"  Warnings: {warnings}")
        print(f"  Suggestions: {total_issues - critical - warnings}")

    # Generate report file if requested
    if args.report:
        report_path = args.course_path / f"VALIDATION-REPORT-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        report_content = report.to_markdown()

        with open(report_path, 'w') as f:
            f.write(report_content)

        print(f"\nReport saved to: {report_path}")

    # Exit code based on critical issues
    critical_count = sum(
        sum(1 for i in r.issues if i.severity == IssueSeverity.CRITICAL)
        for r in report.results
    )

    if critical_count > 0:
        if not args.quiet:
            print(f"\n\033[91mValidation FAILED with {critical_count} critical issues\033[0m")
        sys.exit(1)
    else:
        if not args.quiet:
            print(f"\n\033[92mValidation PASSED\033[0m")
        sys.exit(0)


if __name__ == '__main__':
    main()
