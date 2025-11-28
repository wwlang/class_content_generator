#!/usr/bin/env python3
"""
Command-line interface for assessment automation.

Provides subcommands for quiz consolidation, GIFT export, and PDF brief generation.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from assessment_domain import (
    QuestionRepository,
    AssessmentRepository,
    QuizConsolidationService,
    GIFTExporter,
    PDFExporter,
)


def consolidate_quiz_command(args):
    """Consolidate quiz questions into a quiz bank."""
    print(f"Consolidating quiz {args.quiz_id} from weeks {args.weeks}...")

    # Initialize
    repo = QuestionRepository(base_path=args.base_path)
    service = QuizConsolidationService(repo)

    # Preview first
    if args.preview:
        print("\n=== Preview ===")
        preview = service.preview_consolidation(
            args.course_code,
            weeks=args.weeks,
            target_total=args.target_total
        )
        print(f"Available questions: {preview['available']}")
        print(f"Remembering: {preview['remembering']}")
        print(f"Understanding: {preview['understanding']}")
        print(f"Can consolidate: {preview['can_consolidate']}")
        print(f"Average quality: {preview['avg_quality']:.1f}")
        print(f"By week: {preview['by_week']}")

        if not preview['can_consolidate']:
            print("\n✗ Not enough questions to consolidate")
            return 1

        if not args.yes:
            response = input("\nProceed with consolidation? (y/n): ")
            if response.lower() != 'y':
                print("Cancelled")
                return 0

    # Consolidate
    result = service.consolidate_quiz(
        course_code=args.course_code,
        quiz_id=args.quiz_id,
        weeks=args.weeks,
        target_total=args.target_total,
        target_remembering=args.target_remembering,
        target_understanding=args.target_understanding
    )

    if not result.success:
        print("\n✗ Consolidation failed:")
        for warning in result.warnings:
            print(f"  - {warning}")
        return 1

    # Success
    print(f"\n✓ Consolidated {len(result.selected_questions)} questions")

    dist = result.get_bloom_distribution()
    print(f"Bloom distribution: {dist['remembering']} Remembering, {dist['understanding']} Understanding")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"  - {warning}")

    # Export to GIFT if requested
    if args.export_gift:
        output_path = args.output or f"{args.course_code}-{args.quiz_id}.gift"
        exporter = GIFTExporter(include_feedback=True)
        path = exporter.export_to_file(result.quiz_bank, output_path)
        print(f"\n✓ Exported to GIFT: {path}")

    return 0


def export_gift_command(args):
    """Export quiz bank to GIFT format."""
    print(f"Exporting quiz {args.quiz_id} to GIFT format...")

    # Initialize
    repo = QuestionRepository(base_path=args.base_path)
    service = QuizConsolidationService(repo)

    # Consolidate
    result = service.consolidate_quiz(
        course_code=args.course_code,
        quiz_id=args.quiz_id,
        weeks=args.weeks,
        target_total=args.target_total,
        target_remembering=args.target_remembering,
        target_understanding=args.target_understanding
    )

    if not result.success:
        print("\n✗ Consolidation failed:")
        for warning in result.warnings:
            print(f"  - {warning}")
        return 1

    # Export
    exporter = GIFTExporter(include_feedback=args.include_feedback)
    output_path = args.output or f"{args.course_code}-{args.quiz_id}.gift"

    path = exporter.export_to_file(
        result.quiz_bank,
        output_path,
        category=args.category
    )

    print(f"\n✓ Exported to: {path}")
    print(f"  Questions: {len(result.quiz_bank.questions)}")
    print(f"  File size: {path.stat().st_size} bytes")

    return 0


def generate_brief_command(args):
    """Generate assessment brief PDF."""
    print(f"Generating brief for assessment: {args.assessment_id}...")

    # Initialize
    repo = AssessmentRepository(base_path=args.base_path)

    # Load assessment
    assessment = repo.get_assessment(args.course_code, args.assessment_id)

    if not assessment:
        print(f"\n✗ Assessment not found: {args.assessment_id}")
        print(f"Available assessments:")
        assessments = repo.get_all_assessments(args.course_code)
        for aid, a in assessments.items():
            print(f"  - {aid}: {a.name}")
        return 1

    print(f"Assessment: {assessment.name}")
    print(f"Type: {assessment.type.value}")
    print(f"Weight: {assessment.weight * 100}%")
    print(f"Due: Week {assessment.due_week}")

    # Export
    exporter = PDFExporter()

    if args.format == 'html':
        output_path = args.output or f"{args.assessment_id}.html"
        path = exporter.export_html_to_file(
            assessment,
            output_path,
            course_code=args.course_code
        )
        print(f"\n✓ Exported HTML to: {path}")
    else:  # pdf
        output_path = args.output or f"{args.assessment_id}.pdf"
        try:
            path = exporter.export_to_pdf(
                assessment,
                output_path,
                course_code=args.course_code
            )
            print(f"\n✓ Exported PDF to: {path}")
            print(f"  File size: {path.stat().st_size} bytes")
        except ImportError as e:
            print(f"\n✗ {e}")
            print("Falling back to HTML export...")
            output_path = args.output or f"{args.assessment_id}.html"
            path = exporter.export_html_to_file(
                assessment,
                output_path,
                course_code=args.course_code
            )
            print(f"✓ Exported HTML to: {path}")

    return 0


def list_questions_command(args):
    """List available questions."""
    print(f"Listing questions for {args.course_code}...")

    repo = QuestionRepository(base_path=args.base_path)

    # Get statistics
    stats = repo.get_statistics(args.course_code, weeks=args.weeks)

    print(f"\n=== Question Statistics ===")
    print(f"Total questions: {stats['total']}")
    print(f"Valid questions: {stats['valid']}")
    print(f"Scenario-based: {stats['scenario_based']}")
    print(f"Average quality: {stats['avg_quality']:.1f}")

    print(f"\nBy Bloom level:")
    print(f"  Remembering: {stats['by_bloom']['remembering']}")
    print(f"  Understanding: {stats['by_bloom']['understanding']}")

    print(f"\nBy week:")
    for week, count in sorted(stats['by_week'].items()):
        print(f"  Week {week}: {count} questions")

    return 0


def list_assessments_command(args):
    """List available assessments."""
    print(f"Listing assessments for {args.course_code}...")

    repo = AssessmentRepository(base_path=args.base_path)

    try:
        assessments = repo.get_all_assessments(args.course_code)
    except FileNotFoundError as e:
        print(f"\n✗ {e}")
        return 1

    print(f"\n=== Assessments ({len(assessments)}) ===")
    for aid, assessment in assessments.items():
        print(f"\n{aid}:")
        print(f"  Name: {assessment.name}")
        print(f"  Type: {assessment.type.value}")
        print(f"  Weight: {assessment.weight * 100}%")
        print(f"  Due: Week {assessment.due_week}")
        print(f"  Rubric: {'Yes' if assessment.rubric else 'No'}")
        print(f"  Scenarios: {len(assessment.scenarios)}")

    # Statistics
    stats = repo.get_statistics(args.course_code)
    print(f"\n=== Statistics ===")
    print(f"Total weight: {stats['total_weight'] * 100:.0f}%")
    print(f"Portfolio: {stats['by_type']['portfolio']}")
    print(f"Presentation: {stats['by_type']['presentation']}")
    print(f"With rubrics: {stats['with_rubrics']}")
    print(f"With scenarios: {stats['with_scenarios']}")

    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Assessment automation tools for quiz consolidation and brief generation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview consolidation
  python assessment_cli.py consolidate BCI2AU quiz-1 --weeks 1 2 3 --preview

  # Consolidate and export to GIFT
  python assessment_cli.py consolidate BCI2AU quiz-1 --weeks 1 2 3 --export-gift

  # Generate PDF brief
  python assessment_cli.py brief BCI2AU persuasive-proposal -o proposal.pdf

  # List questions
  python assessment_cli.py list-questions BCI2AU --weeks 1 2 3

  # List assessments
  python assessment_cli.py list-assessments BCI2AU
"""
    )

    parser.add_argument(
        '--base-path',
        default='courses',
        help='Base path to courses directory (default: courses)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Consolidate command
    consolidate_parser = subparsers.add_parser(
        'consolidate',
        help='Consolidate quiz questions into a quiz bank'
    )
    consolidate_parser.add_argument('course_code', help='Course code (e.g., BCI2AU)')
    consolidate_parser.add_argument('quiz_id', help='Quiz identifier (e.g., quiz-1)')
    consolidate_parser.add_argument('--weeks', nargs='+', type=int, required=True,
                                   help='Week numbers to consolidate')
    consolidate_parser.add_argument('--target-total', type=int, default=30,
                                   help='Target total questions (default: 30)')
    consolidate_parser.add_argument('--target-remembering', type=int, default=15,
                                   help='Target Remembering questions (default: 15)')
    consolidate_parser.add_argument('--target-understanding', type=int, default=15,
                                   help='Target Understanding questions (default: 15)')
    consolidate_parser.add_argument('--preview', action='store_true',
                                   help='Preview before consolidating')
    consolidate_parser.add_argument('--export-gift', action='store_true',
                                   help='Export to GIFT after consolidation')
    consolidate_parser.add_argument('--output', '-o', help='Output file path')
    consolidate_parser.add_argument('--yes', '-y', action='store_true',
                                   help='Skip confirmation prompts')
    consolidate_parser.set_defaults(func=consolidate_quiz_command)

    # Export GIFT command
    gift_parser = subparsers.add_parser(
        'export-gift',
        help='Export quiz bank to GIFT format'
    )
    gift_parser.add_argument('course_code', help='Course code')
    gift_parser.add_argument('quiz_id', help='Quiz identifier')
    gift_parser.add_argument('--weeks', nargs='+', type=int, required=True,
                            help='Week numbers')
    gift_parser.add_argument('--target-total', type=int, default=30)
    gift_parser.add_argument('--target-remembering', type=int, default=15)
    gift_parser.add_argument('--target-understanding', type=int, default=15)
    gift_parser.add_argument('--output', '-o', help='Output GIFT file')
    gift_parser.add_argument('--category', help='Moodle category name')
    gift_parser.add_argument('--no-feedback', dest='include_feedback',
                            action='store_false', default=True,
                            help='Exclude feedback from export')
    gift_parser.set_defaults(func=export_gift_command)

    # Generate brief command
    brief_parser = subparsers.add_parser(
        'brief',
        help='Generate assessment brief'
    )
    brief_parser.add_argument('course_code', help='Course code')
    brief_parser.add_argument('assessment_id', help='Assessment ID (e.g., persuasive-proposal)')
    brief_parser.add_argument('--output', '-o', help='Output file path')
    brief_parser.add_argument('--format', choices=['pdf', 'html'], default='pdf',
                             help='Output format (default: pdf)')
    brief_parser.set_defaults(func=generate_brief_command)

    # List questions command
    list_q_parser = subparsers.add_parser(
        'list-questions',
        help='List available questions'
    )
    list_q_parser.add_argument('course_code', help='Course code')
    list_q_parser.add_argument('--weeks', nargs='+', type=int,
                              help='Filter by weeks')
    list_q_parser.set_defaults(func=list_questions_command)

    # List assessments command
    list_a_parser = subparsers.add_parser(
        'list-assessments',
        help='List available assessments'
    )
    list_a_parser.add_argument('course_code', help='Course code')
    list_a_parser.set_defaults(func=list_assessments_command)

    # Parse and execute
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    try:
        return args.func(args)
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        return 130
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        if '--debug' in sys.argv:
            raise
        return 1


if __name__ == '__main__':
    sys.exit(main())
