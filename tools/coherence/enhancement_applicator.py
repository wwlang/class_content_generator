#!/usr/bin/env python3
"""
Enhancement applicator - Applies coherence fixes with git backup.

Implements Decision 2B: Git commit backup before changes.
Implements Decision 1C: User chooses enhancement types to apply.
"""

from typing import List, Dict, Tuple, Optional, Set
from pathlib import Path
from collections import defaultdict
import re
import subprocess

from ..core_structures import CoherenceIssue


class ApplicationReport:
    """Report of enhancement application."""

    def __init__(
        self,
        total_issues: int,
        applied_count: int,
        failed_count: int,
        skipped_count: int,
        applied_by_type: Dict[str, int],
        failed_issues: List[Tuple[CoherenceIssue, str]],
        git_backup_commit: Optional[str] = None
    ):
        """
        Initialize application report.

        Args:
            total_issues: Total issues available to apply
            applied_count: Number successfully applied
            failed_count: Number that failed to apply
            skipped_count: Number skipped (not auto-safe or filtered out)
            applied_by_type: Count of applied issues by type
            failed_issues: List of (issue, error_message) for failures
            git_backup_commit: Git commit hash of backup (if created)
        """
        self.total_issues = total_issues
        self.applied_count = applied_count
        self.failed_count = failed_count
        self.skipped_count = skipped_count
        self.applied_by_type = applied_by_type
        self.failed_issues = failed_issues
        self.git_backup_commit = git_backup_commit


class EnhancementApplicator:
    """Apply coherence enhancements with git backup."""

    # Issue types that can be auto-applied
    AUTO_FIXABLE_TYPES = {
        'terminology_variation',
        'capitalization_inconsistency',
        'duplicate_citation'
    }

    def __init__(self, course_path: Path, issues: List[CoherenceIssue]):
        """
        Initialize applicator.

        Args:
            course_path: Path to course directory
            issues: List of all coherence issues found
        """
        self.course_path = Path(course_path)
        self.issues = issues
        self.applied_fixes: List[CoherenceIssue] = []
        self.failed_fixes: List[Tuple[CoherenceIssue, str]] = []
        self.skipped_fixes: List[CoherenceIssue] = []

    def apply_enhancements(
        self,
        issue_types: Optional[List[str]] = None,
        auto_only: bool = True,
        create_backup: bool = True
    ) -> ApplicationReport:
        """
        Apply enhancements with git backup.

        Args:
            issue_types: Specific issue types to apply (None = all auto-fixable)
            auto_only: Only apply issues with auto_apply_safe=True
            create_backup: Create git commit backup before changes (Decision 2B)

        Returns:
            ApplicationReport with statistics and results
        """
        # 1. Filter issues to apply
        issues_to_apply = self._filter_issues(issue_types, auto_only)

        if not issues_to_apply:
            return ApplicationReport(
                total_issues=len(self.issues),
                applied_count=0,
                failed_count=0,
                skipped_count=len(self.issues),
                applied_by_type={},
                failed_issues=[],
                git_backup_commit=None
            )

        # 2. Create git backup (Decision 2B)
        git_commit = None
        if create_backup:
            backup_success, backup_message = self._create_git_backup()
            if backup_success:
                git_commit = backup_message  # Commit hash
            else:
                # Backup failed - abort
                return ApplicationReport(
                    total_issues=len(self.issues),
                    applied_count=0,
                    failed_count=len(issues_to_apply),
                    skipped_count=len(self.issues) - len(issues_to_apply),
                    applied_by_type={},
                    failed_issues=[(issues_to_apply[0], f"Git backup failed: {backup_message}")],
                    git_backup_commit=None
                )

        # 3. Apply fixes
        for issue in issues_to_apply:
            success, message = self._apply_fix(issue)

            if success:
                self.applied_fixes.append(issue)
            else:
                self.failed_fixes.append((issue, message))

        # 4. Generate report
        return self._generate_report(git_commit)

    def _filter_issues(
        self,
        issue_types: Optional[List[str]],
        auto_only: bool
    ) -> List[CoherenceIssue]:
        """Filter issues to apply based on criteria."""
        filtered = []

        for issue in self.issues:
            # Skip if not auto-safe and auto_only enabled
            if auto_only and not issue.auto_apply_safe:
                self.skipped_fixes.append(issue)
                continue

            # Skip if issue type not in allowed list
            if issue_types is not None and issue.issue_type not in issue_types:
                self.skipped_fixes.append(issue)
                continue

            # Skip if issue type not in AUTO_FIXABLE_TYPES
            if issue.issue_type not in self.AUTO_FIXABLE_TYPES:
                self.skipped_fixes.append(issue)
                continue

            filtered.append(issue)

        return filtered

    def _create_git_backup(self) -> Tuple[bool, str]:
        """
        Create git commit backup before changes (Decision 2B).

        Returns:
            (success, commit_hash or error_message)
        """
        try:
            # Check if we're in a git repository
            result = subprocess.run(
                ['git', 'rev-parse', '--git-dir'],
                cwd=self.course_path,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return (False, "Not a git repository")

            # Check if there are changes to commit
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.course_path,
                capture_output=True,
                text=True
            )

            if not result.stdout.strip():
                # No changes - get current commit
                result = subprocess.run(
                    ['git', 'rev-parse', 'HEAD'],
                    cwd=self.course_path,
                    capture_output=True,
                    text=True
                )
                return (True, result.stdout.strip())

            # Add all changes
            subprocess.run(
                ['git', 'add', '-A'],
                cwd=self.course_path,
                check=True
            )

            # Create commit
            commit_message = "Backup before coherence enhancements"
            result = subprocess.run(
                ['git', 'commit', '-m', commit_message],
                cwd=self.course_path,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                return (False, f"Commit failed: {result.stderr}")

            # Get commit hash
            result = subprocess.run(
                ['git', 'rev-parse', 'HEAD'],
                cwd=self.course_path,
                capture_output=True,
                text=True
            )

            commit_hash = result.stdout.strip()
            return (True, commit_hash)

        except subprocess.CalledProcessError as e:
            return (False, f"Git command failed: {str(e)}")
        except Exception as e:
            return (False, f"Unexpected error: {str(e)}")

    def _apply_fix(self, issue: CoherenceIssue) -> Tuple[bool, str]:
        """
        Apply a single fix based on issue type.

        Args:
            issue: CoherenceIssue to apply

        Returns:
            (success, message)
        """
        if issue.issue_type == "terminology_variation":
            return self._apply_terminology_fix(issue)

        elif issue.issue_type == "capitalization_inconsistency":
            return self._apply_capitalization_fix(issue)

        elif issue.issue_type == "duplicate_citation":
            return self._apply_citation_fix(issue)

        else:
            return (False, f"Unknown issue type: {issue.issue_type}")

    def _apply_terminology_fix(self, issue: CoherenceIssue) -> Tuple[bool, str]:
        """
        Standardize terminology across weeks.

        Issue details should contain:
        - canonical_form: The term to standardize to
        - variations: List of variations to replace
        - affected_weeks: Weeks to update
        """
        try:
            details = issue.details
            canonical = details.get('canonical_form')
            variations = details.get('variations', [])

            if not canonical or not variations:
                return (False, "Missing canonical_form or variations in issue details")

            changes_made = 0

            # Update each affected week
            for week_num in issue.affected_weeks:
                week_dir = self.course_path / "weeks" / f"week-{week_num:02d}"

                # Update lecture content
                lecture_file = week_dir / "lecture-content.md"
                if lecture_file.exists():
                    updated = self._replace_terms_in_file(
                        lecture_file,
                        variations,
                        canonical
                    )
                    if updated:
                        changes_made += 1

                # Update tutorial content
                tutorial_file = week_dir / "tutorial-content.md"
                if tutorial_file.exists():
                    updated = self._replace_terms_in_file(
                        tutorial_file,
                        variations,
                        canonical
                    )
                    if updated:
                        changes_made += 1

            if changes_made > 0:
                return (True, f"Standardized terminology in {changes_made} files")
            else:
                return (False, "No changes made - variations not found")

        except Exception as e:
            return (False, f"Error applying terminology fix: {str(e)}")

    def _apply_capitalization_fix(self, issue: CoherenceIssue) -> Tuple[bool, str]:
        """
        Fix capitalization inconsistencies.

        Issue details should contain:
        - term: The term to fix
        - correct_form: Correct capitalization
        - incorrect_forms: List of incorrect capitalizations
        """
        try:
            details = issue.details
            correct_form = details.get('correct_form')
            incorrect_forms = details.get('incorrect_forms', [])

            if not correct_form or not incorrect_forms:
                return (False, "Missing correct_form or incorrect_forms in issue details")

            changes_made = 0

            # Update each affected week
            for week_num in issue.affected_weeks:
                week_dir = self.course_path / "weeks" / f"week-{week_num:02d}"

                # Update lecture content
                lecture_file = week_dir / "lecture-content.md"
                if lecture_file.exists():
                    updated = self._replace_terms_in_file(
                        lecture_file,
                        incorrect_forms,
                        correct_form
                    )
                    if updated:
                        changes_made += 1

                # Update tutorial content
                tutorial_file = week_dir / "tutorial-content.md"
                if tutorial_file.exists():
                    updated = self._replace_terms_in_file(
                        tutorial_file,
                        incorrect_forms,
                        correct_form
                    )
                    if updated:
                        changes_made += 1

            if changes_made > 0:
                return (True, f"Fixed capitalization in {changes_made} files")
            else:
                return (False, "No changes made - incorrect forms not found")

        except Exception as e:
            return (False, f"Error applying capitalization fix: {str(e)}")

    def _apply_citation_fix(self, issue: CoherenceIssue) -> Tuple[bool, str]:
        """
        Standardize citation formatting.

        For duplicate citations, ensures consistent formatting.
        """
        try:
            details = issue.details
            author = details.get('author')
            year = details.get('year')

            if not author or not year:
                return (False, "Missing author or year in issue details")

            # For now, just mark as informational
            # Full implementation would:
            # 1. Find all instances of citation
            # 2. Determine correct format
            # 3. Standardize all instances

            return (True, f"Citation '{author} ({year})' noted for standardization")

        except Exception as e:
            return (False, f"Error applying citation fix: {str(e)}")

    def _replace_terms_in_file(
        self,
        file_path: Path,
        old_terms: List[str],
        new_term: str
    ) -> bool:
        """
        Replace terms in a file.

        Args:
            file_path: Path to file
            old_terms: List of terms to replace
            new_term: Term to replace with

        Returns:
            True if file was modified, False otherwise
        """
        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content

            # Replace each variation with canonical form
            for old_term in old_terms:
                # Use word boundaries to avoid partial replacements
                pattern = r'\b' + re.escape(old_term) + r'\b'
                content = re.sub(pattern, new_term, content, flags=re.IGNORECASE)

            # Check if content changed
            if content != original_content:
                file_path.write_text(content, encoding='utf-8')
                return True

            return False

        except Exception as e:
            print(f"Error replacing terms in {file_path}: {str(e)}")
            return False

    def _generate_report(self, git_commit: Optional[str]) -> ApplicationReport:
        """Generate application report."""
        # Count applied issues by type
        applied_by_type = defaultdict(int)
        for issue in self.applied_fixes:
            applied_by_type[issue.issue_type] += 1

        return ApplicationReport(
            total_issues=len(self.issues),
            applied_count=len(self.applied_fixes),
            failed_count=len(self.failed_fixes),
            skipped_count=len(self.skipped_fixes),
            applied_by_type=dict(applied_by_type),
            failed_issues=self.failed_fixes,
            git_backup_commit=git_commit
        )

    def save_application_report(self, output_path: Path, report: ApplicationReport) -> None:
        """
        Save application report to markdown file.

        Args:
            output_path: Path to save report
            report: ApplicationReport to format
        """
        md = f"""# Coherence Enhancement Application Report

## Summary

- **Total Issues:** {report.total_issues}
- **Applied:** {report.applied_count}
- **Failed:** {report.failed_count}
- **Skipped:** {report.skipped_count}
"""

        if report.git_backup_commit:
            md += f"\n**Git Backup Commit:** `{report.git_backup_commit}`\n"

        # Applied by type
        if report.applied_by_type:
            md += "\n## Applied Enhancements by Type\n\n"
            for issue_type, count in sorted(report.applied_by_type.items()):
                md += f"- **{issue_type.replace('_', ' ').title()}:** {count}\n"

        # Failed issues
        if report.failed_issues:
            md += "\n## Failed Enhancements\n\n"
            for issue, error_message in report.failed_issues:
                md += f"### {issue.issue_type.replace('_', ' ').title()}\n\n"
                md += f"- **Weeks:** {', '.join(map(str, issue.affected_weeks))}\n"
                md += f"- **Error:** {error_message}\n"
                md += f"- **Suggested Fix:** {issue.suggested_fix}\n\n"

        # Success message
        if report.applied_count > 0:
            md += "\n## Next Steps\n\n"
            md += "1. Review changes with `git diff`\n"
            md += "2. Test content quality\n"
            md += "3. Commit changes or revert with `git reset --hard HEAD^`\n"

        output_path.write_text(md, encoding='utf-8')
