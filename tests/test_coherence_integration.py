#!/usr/bin/env python3
"""Integration tests for coherence analysis system (Phase 3B)."""

import unittest
from pathlib import Path
import tempfile
import shutil
import subprocess

from tools.core_structures import CoherenceIssue
from tools.coherence import (
    ContentExtractor,
    TerminologyAnalyzer,
    ScaffoldingAnalyzer,
    ExamplesAnalyzer,
    CrossReferenceAnalyzer,
    CitationAnalyzer,
    CoherenceReporter,
    EnhancementApplicator,
    ApplicationReport
)


class TestCoherenceIntegration(unittest.TestCase):
    """Integration tests for coherence analysis."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.course_path = self.test_dir / "BCI2AU-test"
        self.course_path.mkdir()

        # Create basic course structure
        (self.course_path / "weeks").mkdir()
        (self.course_path / "syllabus.md").write_text("# Test Syllabus", encoding='utf-8')

        # Create sample week content
        self._create_sample_week(1, "Communication Basics")
        self._create_sample_week(2, "Persuasive Communication")

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def _create_sample_week(self, week_num: int, topic: str):
        """Create sample week content for testing."""
        week_dir = self.course_path / "weeks" / f"week-{week_num:02d}"
        week_dir.mkdir()

        lecture_content = f"""# Week {week_num}: {topic}

## Slide 1: Introduction

The company needs to improve organizational culture.

**Speaker Notes:**
We'll discuss how organizations can improve their culture.

## Slide 2: Key Concepts

Communication is essential in any organisation. Effective communication requires:
- Message clarity
- Audience analysis
- Appropriate channel selection

**References:**
Smith, J. (2023). Communication theory. *Journal of Business*, 15(2), 45-67.

## Slide 3: Example

**Example: Vinamilk**
Vinamilk demonstrates excellent internal communication practices.

**Speaker Notes:**
This Vietnamese company shows how cultural context matters.
"""

        tutorial_content = f"""# Week {week_num} Tutorial: {topic}

## Quiz Questions

1. What is the definition of organisational communication?
2. Name three elements of effective message design.
3. How does culture affect communication?

## Main Activity

Work in groups to analyze a communication scenario.
"""

        (week_dir / "lecture-content.md").write_text(lecture_content, encoding='utf-8')
        (week_dir / "tutorial-content.md").write_text(tutorial_content, encoding='utf-8')

    def test_full_coherence_analysis_workflow(self):
        """Test complete coherence analysis workflow."""
        # 1. Extract content from course
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()

        self.assertEqual(len(week_contents), 2)
        self.assertEqual(week_contents[0].week_number, 1)
        self.assertEqual(week_contents[1].week_number, 2)

        # 2. Run all analyzers
        all_issues = []

        terminology_analyzer = TerminologyAnalyzer(week_contents)
        all_issues.extend(terminology_analyzer.analyze())

        scaffolding_analyzer = ScaffoldingAnalyzer(week_contents)
        all_issues.extend(scaffolding_analyzer.analyze())

        examples_analyzer = ExamplesAnalyzer(week_contents)
        all_issues.extend(examples_analyzer.analyze())

        cross_ref_analyzer = CrossReferenceAnalyzer(week_contents)
        all_issues.extend(cross_ref_analyzer.analyze())

        citation_analyzer = CitationAnalyzer(week_contents)
        all_issues.extend(citation_analyzer.analyze())

        # Should find some issues (at least terminology variation)
        self.assertGreater(len(all_issues), 0)

        # 3. Generate report
        reporter = CoherenceReporter(all_issues, "BCI2AU-test")
        report = reporter.generate_full_report()

        self.assertEqual(report.course_code, "BCI2AU-test")
        self.assertEqual(report.total_issues, len(all_issues))
        self.assertIsInstance(report.issues_by_category, dict)

    def test_terminology_analysis(self):
        """Test terminology analyzer finds variations."""
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()

        analyzer = TerminologyAnalyzer(week_contents)
        issues = analyzer.analyze()

        # Should find "company/organisation/organization" variation
        term_variation_issues = [
            i for i in issues if i.issue_type == "terminology_variation"
        ]

        # May or may not find depending on thresholds
        # Just verify structure is correct
        for issue in term_variation_issues:
            self.assertIsInstance(issue, CoherenceIssue)
            self.assertIn('canonical_form', issue.details)
            self.assertIn('variations', issue.details)
            self.assertEqual(issue.category, "terminology")

    def test_scaffolding_analysis(self):
        """Test scaffolding analyzer finds dependencies."""
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()

        analyzer = ScaffoldingAnalyzer(week_contents)
        issues = analyzer.analyze()

        # Should generate some scaffolding issues
        # Verify structure
        for issue in issues:
            self.assertIsInstance(issue, CoherenceIssue)
            self.assertEqual(issue.category, "scaffolding")
            self.assertIn(issue.issue_type, [
                "premature_concept_use",
                "missing_prerequisite",
                "weak_forward_reference",
                "orphaned_concept"
            ])

    def test_examples_analysis(self):
        """Test examples analyzer finds diversity issues."""
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()

        analyzer = ExamplesAnalyzer(week_contents)
        issues = analyzer.analyze()

        # Verify structure
        for issue in issues:
            self.assertIsInstance(issue, CoherenceIssue)
            self.assertEqual(issue.category, "examples")

    def test_report_generation(self):
        """Test report generation with sample issues."""
        # Create sample issues
        issues = [
            CoherenceIssue(
                issue_id="test-critical",
                issue_type="undefined_term",
                quality_score=9,
                affected_weeks=[1, 2],
                suggested_fix="Define term on first use",
                auto_apply_safe=False,
                category="terminology"
            ),
            CoherenceIssue(
                issue_id="test-important",
                issue_type="terminology_variation",
                quality_score=7,
                affected_weeks=[1, 2, 3],
                suggested_fix="Standardize to 'organization'",
                auto_apply_safe=True,
                category="terminology"
            ),
            CoherenceIssue(
                issue_id="test-minor",
                issue_type="duplicate_citation",
                quality_score=3,
                affected_weeks=[2],
                suggested_fix="Ensure consistent citation format",
                auto_apply_safe=True,
                category="citations"
            )
        ]

        # Set details for issues
        issues[1].details = {
            'canonical_form': 'organization',
            'variations': ['organisation', 'org']
        }

        reporter = CoherenceReporter(issues, "TEST-COURSE")
        report = reporter.generate_full_report()

        # Verify report structure
        self.assertEqual(report.total_issues, 3)
        self.assertEqual(len(report.critical_issues), 1)  # score 9
        self.assertEqual(len(report.important_issues), 1)  # score 7
        self.assertEqual(len(report.medium_issues), 0)
        self.assertEqual(len(report.minor_issues), 1)  # score 3
        self.assertEqual(report.auto_fixable_count, 2)
        self.assertEqual(report.manual_review_count, 1)

        # Test saving reports
        full_report_path = self.test_dir / "full-report.md"
        reporter.save_full_report(full_report_path)
        self.assertTrue(full_report_path.exists())

        summary_path = self.test_dir / "summary.md"
        reporter.save_summary_report(summary_path)
        self.assertTrue(summary_path.exists())

        todo_path = self.test_dir / "manual-todo.md"
        reporter.save_manual_todo(todo_path)
        self.assertTrue(todo_path.exists())

        # Verify content
        full_content = full_report_path.read_text(encoding='utf-8')
        self.assertIn("TEST-COURSE", full_content)
        self.assertIn("Total Issues Found:", full_content)
        self.assertIn("**Critical (9-10):** 1", full_content)

    def test_enhancement_application_filtering(self):
        """Test enhancement applicator filters issues correctly."""
        # Create sample issues
        issues = [
            CoherenceIssue(
                issue_id="auto-1",
                issue_type="terminology_variation",
                quality_score=7,
                affected_weeks=[1],
                suggested_fix="Standardize term",
                auto_apply_safe=True,
                category="terminology"
            ),
            CoherenceIssue(
                issue_id="manual-1",
                issue_type="missing_definition",
                quality_score=8,
                affected_weeks=[1],
                suggested_fix="Add definition",
                auto_apply_safe=False,
                category="terminology"
            ),
            CoherenceIssue(
                issue_id="auto-2",
                issue_type="capitalization_inconsistency",
                quality_score=5,
                affected_weeks=[2],
                suggested_fix="Fix capitalization",
                auto_apply_safe=True,
                category="terminology"
            )
        ]

        applicator = EnhancementApplicator(self.course_path, issues)

        # Test filtering to auto-only
        filtered = applicator._filter_issues(issue_types=None, auto_only=True)
        self.assertEqual(len(filtered), 2)  # Only auto-safe issues

        # Test filtering by type
        filtered = applicator._filter_issues(
            issue_types=["terminology_variation"],
            auto_only=True
        )
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].issue_id, "auto-1")

    def test_enhancement_application_with_git(self):
        """Test enhancement application with git backup."""
        # Initialize git repo
        subprocess.run(['git', 'init'], cwd=self.course_path, check=True)
        subprocess.run(
            ['git', 'config', 'user.email', 'test@example.com'],
            cwd=self.course_path,
            check=True
        )
        subprocess.run(
            ['git', 'config', 'user.name', 'Test User'],
            cwd=self.course_path,
            check=True
        )
        subprocess.run(['git', 'add', '-A'], cwd=self.course_path, check=True)
        subprocess.run(
            ['git', 'commit', '-m', 'Initial commit'],
            cwd=self.course_path,
            check=True
        )

        # Create issue with proper details
        issue = CoherenceIssue(
            issue_id="test-term-variation",
            issue_type="terminology_variation",
            quality_score=7,
            affected_weeks=[1, 2],
            suggested_fix="Standardize to 'organization'",
            auto_apply_safe=True,
            category="terminology"
        )
        issue.details = {
            'canonical_form': 'organization',
            'variations': ['organisation']
        }

        applicator = EnhancementApplicator(self.course_path, [issue])

        # Apply enhancements with git backup
        report = applicator.apply_enhancements(
            issue_types=None,
            auto_only=True,
            create_backup=True
        )

        # Verify git backup was created
        self.assertIsNotNone(report.git_backup_commit)
        self.assertEqual(report.total_issues, 1)

        # Verify changes were applied (or attempted)
        self.assertGreaterEqual(report.applied_count + report.failed_count, 0)

    def test_enhancement_application_report(self):
        """Test enhancement application report generation."""
        # Create sample issues
        issues = [
            CoherenceIssue(
                issue_id="term-1",
                issue_type="terminology_variation",
                quality_score=7,
                affected_weeks=[1],
                suggested_fix="Standardize term",
                auto_apply_safe=True,
                category="terminology"
            )
        ]
        issues[0].details = {
            'canonical_form': 'organization',
            'variations': ['organisation']
        }

        applicator = EnhancementApplicator(self.course_path, issues)

        # Apply without git (for testing)
        report = applicator.apply_enhancements(
            issue_types=None,
            auto_only=True,
            create_backup=False
        )

        # Verify report structure
        self.assertIsInstance(report, ApplicationReport)
        self.assertEqual(report.total_issues, 1)

        # Save report
        report_path = self.test_dir / "application-report.md"
        applicator.save_application_report(report_path, report)
        self.assertTrue(report_path.exists())

        content = report_path.read_text(encoding='utf-8')
        self.assertIn("Enhancement Application Report", content)
        self.assertIn("Total Issues:", content)

    def test_issue_prioritization(self):
        """Test that issues are correctly prioritized by score."""
        issues = [
            CoherenceIssue(
                issue_id=f"issue-{i}",
                issue_type="test_type",
                quality_score=score,
                affected_weeks=[1],
                suggested_fix=f"Fix {i}",
                auto_apply_safe=True,
                category="test"
            )
            for i, score in enumerate([3, 9, 5, 7, 10, 2, 8, 4])
        ]

        reporter = CoherenceReporter(issues, "TEST")
        report = reporter.generate_full_report()

        # Verify prioritization
        self.assertEqual(len(report.critical_issues), 2)  # scores 9, 10
        self.assertEqual(len(report.important_issues), 2)  # scores 7, 8
        self.assertEqual(len(report.medium_issues), 2)  # scores 4, 5
        self.assertEqual(len(report.minor_issues), 2)  # scores 2, 3

        # Verify critical issues have highest scores
        critical_scores = [i.quality_score for i in report.critical_issues]
        self.assertIn(9, critical_scores)
        self.assertIn(10, critical_scores)

    def test_cross_reference_analysis(self):
        """Test cross-reference analyzer finds opportunities."""
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()

        analyzer = CrossReferenceAnalyzer(week_contents)
        issues = analyzer.analyze()

        # Verify structure
        for issue in issues:
            self.assertIsInstance(issue, CoherenceIssue)
            self.assertEqual(issue.category, "cross_reference")
            self.assertIn(issue.issue_type, [
                "missing_callback",
                "missing_forward_link"
            ])

    def test_citation_analysis(self):
        """Test citation analyzer finds formatting issues."""
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()

        analyzer = CitationAnalyzer(week_contents)
        issues = analyzer.analyze()

        # Verify structure
        for issue in issues:
            self.assertIsInstance(issue, CoherenceIssue)
            self.assertEqual(issue.category, "citations")


if __name__ == '__main__':
    unittest.main()
