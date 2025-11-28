#!/usr/bin/env python3
"""
Simplified end-to-end tests for Phase 3.

Tests core workflows that are fully implemented and working.
"""

import unittest
from pathlib import Path
import tempfile
import shutil
import subprocess
import time

from tools.course_generator import CourseGenerator
from tools.coherence import (
    ContentExtractor,
    TerminologyAnalyzer,
    ScaffoldingAnalyzer,
    ExamplesAnalyzer,
    CrossReferenceAnalyzer,
    CitationAnalyzer,
    CoherenceReporter,
    EnhancementApplicator
)
from tools.core_structures import CoherenceIssue


class TestPhase3CoreWorkflows(unittest.TestCase):
    """Test core Phase 3 workflows."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.course_path = self.test_dir / "TEST-COURSE"
        self.course_path.mkdir()

        # Initialize git (required for enhancements)
        subprocess.run(['git', 'init'], cwd=self.course_path, check=True, capture_output=True)
        subprocess.run(
            ['git', 'config', 'user.email', 'test@test.com'],
            cwd=self.course_path,
            check=True,
            capture_output=True
        )
        subprocess.run(
            ['git', 'config', 'user.name', 'Test'],
            cwd=self.course_path,
            check=True,
            capture_output=True
        )

    def tearDown(self):
        """Clean up test fixtures."""
        shutil.rmtree(self.test_dir)

    def test_coherence_full_workflow(self):
        """Test complete coherence analysis workflow."""
        # Create sample course content
        (self.course_path / "weeks").mkdir()

        # Create 3 weeks of content
        for week_num in range(1, 4):
            self._create_sample_week(week_num)

        # 1. Extract content
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()

        self.assertEqual(len(week_contents), 3)

        # 2. Run all analyzers
        all_issues = []
        all_issues.extend(TerminologyAnalyzer(week_contents).analyze())
        all_issues.extend(ScaffoldingAnalyzer(week_contents).analyze())
        all_issues.extend(ExamplesAnalyzer(week_contents).analyze())
        all_issues.extend(CrossReferenceAnalyzer(week_contents).analyze())
        all_issues.extend(CitationAnalyzer(week_contents).analyze())

        # Should find issues (at least terminology variations)
        self.assertGreater(len(all_issues), 0)

        # 3. Generate reports
        reporter = CoherenceReporter(all_issues, "TEST-COURSE")
        report = reporter.generate_full_report()

        self.assertEqual(report.course_code, "TEST-COURSE")
        self.assertEqual(report.total_issues, len(all_issues))

        # 4. Save all report types
        output_dir = self.test_dir / "reports"
        output_dir.mkdir()

        reporter.save_full_report(output_dir / "full-report.md")
        reporter.save_summary_report(output_dir / "summary.md")
        reporter.save_manual_todo(output_dir / "manual-todo.md")

        # Verify files created
        self.assertTrue((output_dir / "full-report.md").exists())
        self.assertTrue((output_dir / "summary.md").exists())
        self.assertTrue((output_dir / "manual-todo.md").exists())

    def test_coherence_enhancement_with_git_backup(self):
        """Test enhancement application with git backup."""
        # Create sample content
        (self.course_path / "weeks").mkdir()
        self._create_sample_week(1)

        # Create initial git commit
        subprocess.run(['git', 'add', '-A'], cwd=self.course_path, check=True, capture_output=True)
        subprocess.run(
            ['git', 'commit', '-m', 'Initial'],
            cwd=self.course_path,
            check=True,
            capture_output=True
        )

        # Extract and analyze
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()
        issues = TerminologyAnalyzer(week_contents).analyze()

        # Apply enhancements with git backup
        applicator = EnhancementApplicator(self.course_path, issues)
        report = applicator.apply_enhancements(
            issue_types=None,
            auto_only=True,
            create_backup=True
        )

        # Verify report structure
        self.assertIsNotNone(report)
        self.assertEqual(report.total_issues, len(issues))

        # If there were auto-fixable issues, should have git commit
        auto_fixable = [i for i in issues if i.auto_apply_safe]
        if len(auto_fixable) > 0:
            self.assertIsNotNone(report.git_backup_commit)

    def test_coherence_issue_prioritization(self):
        """Test that issues are properly prioritized by score."""
        # Create test issues with different scores
        issues = [
            self._create_test_issue("critical-1", 10),
            self._create_test_issue("critical-2", 9),
            self._create_test_issue("important-1", 8),
            self._create_test_issue("important-2", 7),
            self._create_test_issue("medium-1", 6),
            self._create_test_issue("medium-2", 4),
            self._create_test_issue("minor-1", 3),
            self._create_test_issue("minor-2", 1)
        ]

        # Generate report
        reporter = CoherenceReporter(issues, "TEST")
        report = reporter.generate_full_report()

        # Verify prioritization
        self.assertEqual(len(report.critical_issues), 2)  # 9-10
        self.assertEqual(len(report.important_issues), 2)  # 7-8
        self.assertEqual(len(report.medium_issues), 2)  # 4-6
        self.assertEqual(len(report.minor_issues), 2)  # 1-3

    def test_coherence_analyzer_performance(self):
        """Test that coherence analysis completes quickly."""
        # Create 10 weeks of content
        (self.course_path / "weeks").mkdir()
        for week_num in range(1, 11):
            self._create_sample_week(week_num)

        # Measure extraction time
        start = time.time()
        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()
        extraction_time = time.time() - start

        self.assertEqual(len(week_contents), 10)
        self.assertLess(extraction_time, 5.0, "Should extract 10 weeks in < 5s")

        # Measure analysis time
        start = time.time()
        analyzer = TerminologyAnalyzer(week_contents)
        issues = analyzer.analyze()
        analysis_time = time.time() - start

        self.assertLess(analysis_time, 3.0, "Should analyze in < 3s")

    def test_report_generation_performance(self):
        """Test that report generation is fast."""
        # Create 100 test issues
        issues = [self._create_test_issue(f"issue-{i}", 5) for i in range(100)]

        # Measure report generation time
        start = time.time()
        reporter = CoherenceReporter(issues, "TEST")
        report = reporter.generate_full_report()
        report_time = time.time() - start

        self.assertLess(report_time, 1.0, "Should generate report in < 1s")
        self.assertEqual(report.total_issues, 100)

    def test_course_generator_initialization(self):
        """Test CourseGenerator initializes correctly."""
        generator = CourseGenerator("TEST", self.course_path)

        self.assertEqual(generator.course_code, "TEST")
        self.assertEqual(generator.course_path, self.course_path)
        self.assertEqual(len(generator.completed_weeks), 0)
        self.assertEqual(len(generator.skipped_weeks), 0)

    def test_content_extractor_handles_missing_weeks(self):
        """Test ContentExtractor gracefully handles missing weeks."""
        # Create only weeks 1 and 3 (skip 2)
        (self.course_path / "weeks").mkdir()
        self._create_sample_week(1)
        self._create_sample_week(3)

        extractor = ContentExtractor(self.course_path)
        week_contents = extractor.extract_all_weeks()

        # Should only extract existing weeks
        self.assertEqual(len(week_contents), 2)
        week_numbers = [w.week_number for w in week_contents]
        self.assertIn(1, week_numbers)
        self.assertIn(3, week_numbers)
        self.assertNotIn(2, week_numbers)

    def test_enhancement_applicator_filtering(self):
        """Test enhancement applicator filters correctly."""
        # Create mix of auto and manual issues
        issues = [
            self._create_test_issue("auto-1", 7, auto_safe=True, type="terminology_variation"),
            self._create_test_issue("manual-1", 8, auto_safe=False, type="missing_definition"),
            self._create_test_issue("auto-2", 5, auto_safe=True, type="capitalization_inconsistency")
        ]

        applicator = EnhancementApplicator(self.course_path, issues)

        # Test auto-only filtering
        filtered = applicator._filter_issues(issue_types=None, auto_only=True)
        self.assertEqual(len(filtered), 2)

        # Test type filtering
        filtered = applicator._filter_issues(
            issue_types=["terminology_variation"],
            auto_only=True
        )
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].issue_id, "auto-1")

    def _create_sample_week(self, week_num: int):
        """Create sample week content."""
        week_dir = self.course_path / "weeks" / f"week-{week_num:02d}"
        week_dir.mkdir(parents=True)

        lecture = f"""# Week {week_num}: Business Communication

## Slide 1: Introduction

The company needs better communication. Organizations must communicate effectively.

**Speaker Notes:**
We'll discuss how organisations improve messaging.

## Slide 2: Concepts

Communication requires:
- Clarity
- Consistency
- Cultural awareness

**References:**
Smith, J. (2023). Communication. *Journal*, 15(2), 45-67.

## Slide 3: Example

**Example: Vinamilk**
Vietnamese company with strong communication practices.
"""

        tutorial = f"""# Week {week_num} Tutorial

## Quiz
1. What is communication?
2. Name three principles.

## Activity
Analyze communication scenarios.
"""

        (week_dir / "lecture-content.md").write_text(lecture, encoding='utf-8')
        (week_dir / "tutorial-content.md").write_text(tutorial, encoding='utf-8')

    def _create_test_issue(self, issue_id: str, score: int, auto_safe: bool = True, type: str = "test_type") -> CoherenceIssue:
        """Create test issue."""
        issue = CoherenceIssue(
            issue_id=issue_id,
            issue_type=type,
            quality_score=score,
            affected_weeks=[1],
            suggested_fix=f"Fix {issue_id}",
            auto_apply_safe=auto_safe,
            category="test"
        )
        issue.details = {"test": "data"}
        return issue


if __name__ == '__main__':
    unittest.main()
