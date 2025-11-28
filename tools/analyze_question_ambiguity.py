#!/usr/bin/env python3
"""
Analyze Question Ambiguity

Command-line tool to detect and fix ambiguous multiple-choice questions.
Supports batch analysis, automatic rewording, and manual review workflows.

Usage:
    # Analyze all questions in a week
    python tools/analyze_question_ambiguity.py BCI2AU 1

    # Analyze specific quiz
    python tools/analyze_question_ambiguity.py BCI2AU --quiz quiz-1

    # Analyze without auto-rewording (manual review only)
    python tools/analyze_question_ambiguity.py BCI2AU 1 --no-reword

    # Export analysis report
    python tools/analyze_question_ambiguity.py BCI2AU 1 --export ambiguity-report.md
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional
import json

from tools.assessment_domain.repositories import QuestionRepository
from tools.assessment_domain.services.question_ambiguity_analyzer import (
    QuestionAmbiguityAnalyzer,
    AmbiguityReport,
    PlausibilityLevel
)
from tools.assessment_domain.models import Question


class AmbiguityAnalysisWorkflow:
    """Workflow for analyzing and fixing question ambiguity."""

    def __init__(self, course_code: str, base_path: Optional[Path] = None):
        """
        Initialize workflow.

        Args:
            course_code: Course code (e.g., BCI2AU)
            base_path: Base path to course content (defaults to courses/)
        """
        self.course_code = course_code
        self.base_path = base_path or Path("courses")
        self.course_path = self.base_path / course_code

        if not self.course_path.exists():
            raise ValueError(f"Course {course_code} not found at {self.course_path}")

        self.repository = QuestionRepository(base_path=str(self.base_path))
        self.analyzer = QuestionAmbiguityAnalyzer()

    def analyze_week(
        self,
        week: int,
        reword_ambiguous: bool = True,
        manual_review_threshold: float = 0.7
    ) -> List[AmbiguityReport]:
        """
        Analyze all questions in a week.

        Args:
            week: Week number
            reword_ambiguous: Whether to auto-reword ambiguous questions
            manual_review_threshold: Quality score below which manual review is needed

        Returns:
            List of ambiguity reports
        """
        # Load questions
        questions = self.repository.get_questions_by_week(self.course_code, week)

        if not questions:
            print(f"No questions found for {self.course_code} week {week}")
            return []

        # Load course context
        context = self._load_course_context(week)

        # Analyze questions
        print(f"\nAnalyzing {len(questions)} questions from week {week}...")
        reports = []

        for i, question in enumerate(questions, 1):
            print(f"  [{i}/{len(questions)}] {question.id}...", end=" ")

            if reword_ambiguous:
                report = self.analyzer.analyze_and_reword(question, context)
            else:
                report = self.analyzer.analyze_question(question, context)

            reports.append(report)

            # Check if manual review needed
            quality_score = question.calculate_quality_score()
            needs_review = (
                report.is_ambiguous or
                quality_score < manual_review_threshold
            )

            if needs_review:
                print(f"⚠️  NEEDS REVIEW (quality: {quality_score:.2f})")
            elif report.is_ambiguous:
                print("✓ Reworded")
            else:
                print("✓ OK")

        return reports

    def analyze_quiz(
        self,
        quiz_id: str,
        reword_ambiguous: bool = True
    ) -> List[AmbiguityReport]:
        """
        Analyze questions in a specific quiz.

        Args:
            quiz_id: Quiz identifier
            reword_ambiguous: Whether to auto-reword

        Returns:
            List of ambiguity reports
        """
        # Load quiz questions from consolidated file
        quiz_file = self.course_path / f"{quiz_id}-consolidated.json"

        if not quiz_file.exists():
            raise ValueError(f"Quiz {quiz_id} not found at {quiz_file}")

        with open(quiz_file, 'r') as f:
            quiz_data = json.load(f)

        questions = [Question.from_dict(q) for q in quiz_data['questions']]
        context = f"Quiz {quiz_id}"

        print(f"\nAnalyzing {len(questions)} questions from {quiz_id}...")
        reports = []

        for i, question in enumerate(questions, 1):
            print(f"  [{i}/{len(questions)}] {question.id}...", end=" ")

            if reword_ambiguous:
                report = self.analyzer.analyze_and_reword(question, context)
            else:
                report = self.analyzer.analyze_question(question, context)

            reports.append(report)

            if report.is_ambiguous:
                print("⚠️  Ambiguous" if not report.reworded_question else "✓ Reworded")
            else:
                print("✓ OK")

        return reports

    def export_report(
        self,
        reports: List[AmbiguityReport],
        output_path: Path,
        include_reworded: bool = True
    ):
        """
        Export analysis report to markdown.

        Args:
            reports: List of ambiguity reports
            output_path: Path to save report
            include_reworded: Whether to include reworded questions
        """
        total = len(reports)
        ambiguous = sum(1 for r in reports if r.is_ambiguous)
        reworded = sum(1 for r in reports if r.reworded_question is not None)

        markdown = f"""# Question Ambiguity Analysis Report

**Course:** {self.course_code}
**Date:** {Path().absolute()}
**Total Questions:** {total}
**Ambiguous Questions:** {ambiguous} ({ambiguous/total*100:.1f}%)
**Questions Reworded:** {reworded}

---

## Summary

"""

        if ambiguous == 0:
            markdown += "✅ All questions have one clearly correct answer.\n\n"
        else:
            markdown += f"⚠️ Found {ambiguous} questions with potential ambiguity.\n\n"

        # Ambiguous questions details
        if ambiguous > 0:
            markdown += "## Ambiguous Questions\n\n"

            for report in reports:
                if not report.is_ambiguous:
                    continue

                markdown += f"### {report.question_id}\n\n"
                markdown += f"**Correct Answer:** {report.correct_answer}  \n"
                markdown += f"**Plausible Options:** {', '.join(report.plausible_options)}  \n"
                markdown += f"**Recommendation:** {report.recommendation}\n\n"

                markdown += "**Plausibility Analysis:**\n\n"
                for analysis in report.analyses:
                    emoji = "✓" if analysis.plausibility == PlausibilityLevel.CLEARLY_WRONG else "⚠️"
                    markdown += f"- {emoji} **Option {analysis.option_key}** ({analysis.plausibility.value})\n"
                    markdown += f"  - {analysis.option_text}\n"
                    markdown += f"  - *Reasoning:* {analysis.reasoning}\n\n"

                if include_reworded and report.reworded_question:
                    markdown += "**Reworded Version:**\n\n"
                    markdown += f"**Question:** {report.reworded_question.question_text}\n\n"
                    markdown += "**Options:**\n"
                    for key, text in report.reworded_question.options.items():
                        marker = "✓" if key == report.correct_answer else " "
                        markdown += f"- {marker} {key}. {text}\n"
                    markdown += "\n"

                    markdown += "**Feedback:**\n"
                    for key, fb in report.reworded_question.feedback.items():
                        markdown += f"- {key}: {fb}\n"
                    markdown += "\n---\n\n"

        # Clear questions summary
        clear_questions = [r for r in reports if not r.is_ambiguous]
        if clear_questions:
            markdown += f"## Clear Questions ({len(clear_questions)})\n\n"
            markdown += "The following questions have one clearly correct answer:\n\n"
            for report in clear_questions:
                markdown += f"- ✅ {report.question_id}\n"

        # Write report
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown)
        print(f"\n✓ Report exported to {output_path}")

    def apply_reworded_questions(
        self,
        reports: List[AmbiguityReport],
        week: int,
        backup: bool = True
    ):
        """
        Apply reworded questions back to source files.

        Args:
            reports: Ambiguity reports with reworded questions
            week: Week number
            backup: Whether to backup original file
        """
        reworded_count = sum(1 for r in reports if r.reworded_question)

        if reworded_count == 0:
            print("No reworded questions to apply.")
            return

        quiz_file = self.course_path / f"weeks/week-{week}/quiz-questions.md"

        if not quiz_file.exists():
            print(f"Quiz file not found: {quiz_file}")
            return

        # Backup original
        if backup:
            backup_path = quiz_file.with_suffix('.md.backup')
            backup_path.write_text(quiz_file.read_text())
            print(f"✓ Backed up original to {backup_path.name}")

        # Load original content
        content = quiz_file.read_text()

        # Replace questions
        for report in reports:
            if not report.reworded_question:
                continue

            original_id = report.question_id
            reworded = report.reworded_question

            # Find and replace question block
            # This is a simplified implementation - would need more robust parsing
            print(f"  ⚠️  Manual replacement needed for {original_id}")
            print(f"      Original question needs manual review and replacement")

        print(f"\n⚠️  Automatic replacement not yet implemented.")
        print(f"   Please review the analysis report and manually update quiz-questions.md")

    def flag_for_manual_review(
        self,
        reports: List[AmbiguityReport],
        quality_threshold: float = 0.7
    ) -> List[str]:
        """
        Flag questions needing manual review.

        Args:
            reports: Ambiguity reports
            quality_threshold: Quality score threshold

        Returns:
            List of question IDs flagged for review
        """
        flagged = []

        for report in reports:
            # Get original question
            # Note: This is simplified - would need to load from repository
            needs_review = report.is_ambiguous

            if needs_review:
                flagged.append(report.question_id)

        return flagged

    def _load_course_context(self, week: int) -> str:
        """Load course context for better analysis."""
        syllabus_path = self.course_path / "syllabus.md"
        week_path = self.course_path / f"weeks/week-{week}/lecture-content.md"

        context_parts = []

        # Add course info
        if syllabus_path.exists():
            syllabus = syllabus_path.read_text()
            # Extract course title and description
            lines = syllabus.split('\n')[:20]  # First 20 lines
            context_parts.append(' '.join(lines))

        # Add week topic
        if week_path.exists():
            lecture = week_path.read_text()
            # Extract first few headings
            lines = [l for l in lecture.split('\n') if l.startswith('#')][:5]
            context_parts.append(' '.join(lines))

        return ' '.join(context_parts)[:500]  # Limit context length


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze question ambiguity and suggest rewording"
    )

    parser.add_argument(
        "course_code",
        help="Course code (e.g., BCI2AU)"
    )

    parser.add_argument(
        "week",
        type=int,
        nargs='?',
        help="Week number to analyze"
    )

    parser.add_argument(
        "--quiz",
        help="Analyze specific quiz instead of week"
    )

    parser.add_argument(
        "--no-reword",
        action="store_true",
        help="Disable automatic rewording (analysis only)"
    )

    parser.add_argument(
        "--export",
        type=Path,
        help="Export analysis report to file"
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Apply reworded questions to source files"
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="Quality score threshold for manual review (default: 0.7)"
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.week and not args.quiz:
        parser.error("Either week number or --quiz must be provided")

    # Initialize workflow
    try:
        workflow = AmbiguityAnalysisWorkflow(args.course_code)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Run analysis
    reword = not args.no_reword

    try:
        if args.quiz:
            reports = workflow.analyze_quiz(args.quiz, reword_ambiguous=reword)
        else:
            reports = workflow.analyze_week(
                args.week,
                reword_ambiguous=reword,
                manual_review_threshold=args.threshold
            )

        # Print summary
        print("\n" + "=" * 60)
        print(workflow.analyzer.generate_report_summary(reports))

        # Export report if requested
        if args.export:
            workflow.export_report(reports, args.export)

        # Apply reworded questions if requested
        if args.apply and args.week:
            workflow.apply_reworded_questions(reports, args.week)

        # Flag for manual review
        flagged = workflow.flag_for_manual_review(reports, args.threshold)
        if flagged:
            print(f"\n⚠️  Questions flagged for manual review: {len(flagged)}")
            for qid in flagged:
                print(f"  - {qid}")

    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
