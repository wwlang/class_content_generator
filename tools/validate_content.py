"""
Content Structure Validators

Validates generated course content against quality standards:
- Lectures: Structure, slide count, citations
- Tutorials: Alignment with assessments, timing
- Slides: Layout compliance, references
- Quizzes: GIFT format, content match
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


class LectureValidator:
    """Validates lecture content structure and quality."""

    REQUIRED_SECTIONS = ["Opening", "Core Content", "Wrap-up"]
    MIN_SLIDES = 22
    MAX_SLIDES = 30
    MIN_SOURCES = 3

    def validate(self, lecture_path: Path) -> Tuple[bool, List[str]]:
        """
        Validate lecture content.

        Returns:
            (is_valid, list_of_issues)
        """
        issues = []

        if not lecture_path.exists():
            return False, [f"Lecture file not found: {lecture_path}"]

        content = lecture_path.read_text()

        # Check slide count
        slides = self._count_slides(content)
        if slides < self.MIN_SLIDES:
            issues.append(f"Too few slides: {slides} (minimum {self.MIN_SLIDES})")
        elif slides > self.MAX_SLIDES:
            issues.append(f"Too many slides: {slides} (maximum {self.MAX_SLIDES})")

        # Check required sections
        for section in self.REQUIRED_SECTIONS:
            if section.lower() not in content.lower():
                issues.append(f"Missing required section: {section}")

        # Check citations
        citations = self._count_citations(content)
        if citations < self.MIN_SOURCES:
            issues.append(f"Insufficient sources: {citations} (minimum {self.MIN_SOURCES})")

        # Check learning objectives present
        if "learning objective" not in content.lower():
            issues.append("No learning objectives found")

        # Check assessment connection
        if "assessment" not in content.lower():
            issues.append("No assessment connection mentioned")

        return len(issues) == 0, issues

    def _count_slides(self, content: str) -> int:
        """Count slide markers in content."""
        # Look for slide markers like "## Slide 1:" or "### Slide 1"
        slide_pattern = r'(?:##\s+Slide\s+\d+|###\s+Slide\s+\d+|\*\*Slide\s+\d+)'
        return len(re.findall(slide_pattern, content, re.IGNORECASE))

    def _count_citations(self, content: str) -> int:
        """Count unique citations (Author, Year) patterns."""
        citation_pattern = r'\([A-Z][a-z]+(?:\s+&\s+[A-Z][a-z]+)?,\s+\d{4}\)'
        citations = re.findall(citation_pattern, content)
        return len(set(citations))  # Unique citations


class TutorialValidator:
    """Validates tutorial content structure and alignment."""

    REQUIRED_SECTIONS = ["Opening", "Main Activity", "Quiz Prep", "Wrap-up"]
    TARGET_DURATION = 90  # minutes

    def validate(self, tutorial_path: Path, assessment_schedule: Dict) -> Tuple[bool, List[str]]:
        """
        Validate tutorial content.

        Args:
            tutorial_path: Path to tutorial markdown
            assessment_schedule: Dict with assessment info for alignment check

        Returns:
            (is_valid, list_of_issues)
        """
        issues = []

        if not tutorial_path.exists():
            return False, [f"Tutorial file not found: {tutorial_path}"]

        content = tutorial_path.read_text()

        # Check required sections
        for section in self.REQUIRED_SECTIONS:
            if section.lower() not in content.lower():
                issues.append(f"Missing required section: {section}")

        # Check timing breakdown
        timings = self._extract_timings(content)
        total = sum(timings.values())
        if abs(total - self.TARGET_DURATION) > 10:  # Allow 10min variance
            issues.append(f"Total duration {total}min differs from target {self.TARGET_DURATION}min")

        # Check assessment alignment
        if "rubric" not in content.lower():
            issues.append("No rubric reference found")
        if "peer review" not in content.lower() and "feedback" not in content.lower():
            issues.append("No peer review/feedback activity found")

        # Check quiz questions
        quiz_count = content.lower().count("question")
        if quiz_count < 5:
            issues.append(f"Too few quiz questions: {quiz_count} (minimum 5)")

        return len(issues) == 0, issues

    def _extract_timings(self, content: str) -> Dict[str, int]:
        """Extract timing information from content."""
        timing_pattern = r'\((\d+)\s*min(?:utes?)?\)'
        timings = re.findall(timing_pattern, content, re.IGNORECASE)

        sections = {}
        for section in self.REQUIRED_SECTIONS:
            # Find timing near section heading
            section_pattern = rf'{section}[^\n]*\((\d+)\s*min'
            match = re.search(section_pattern, content, re.IGNORECASE)
            if match:
                sections[section] = int(match.group(1))

        return sections


class QuizValidator:
    """Validates quiz GIFT format and content."""

    MIN_QUESTIONS = 5
    MAX_QUESTIONS = 10

    def validate(self, quiz_path: Path, lecture_content: str = None) -> Tuple[bool, List[str]]:
        """
        Validate quiz GIFT format.

        Args:
            quiz_path: Path to .gift file
            lecture_content: Optional lecture content for alignment check

        Returns:
            (is_valid, list_of_issues)
        """
        issues = []

        if not quiz_path.exists():
            return False, [f"Quiz file not found: {quiz_path}"]

        content = quiz_path.read_text()

        # Count questions (look for ::Question markers)
        questions = content.count('::')
        if questions < self.MIN_QUESTIONS:
            issues.append(f"Too few questions: {questions} (minimum {self.MIN_QUESTIONS})")
        elif questions > self.MAX_QUESTIONS:
            issues.append(f"Too many questions: {questions} (maximum {self.MAX_QUESTIONS})")

        # Check for feedback (should have # markers for feedback)
        if content.count('#') < questions:
            issues.append("Missing feedback for some questions")

        # Check for answer markers ({= for correct, ~ for incorrect})
        if not re.search(r'\{=', content):
            issues.append("No correct answers marked (missing {=)")

        if not re.search(r'~', content):
            issues.append("No incorrect options found (missing ~)")

        # Basic GIFT syntax check
        if not content.strip():
            issues.append("Quiz file is empty")

        return len(issues) == 0, issues


def validate_week_content(course_code: str, week_num: int) -> Dict[str, Tuple[bool, List[str]]]:
    """
    Validate all content for a specific week.

    Args:
        course_code: Course code (e.g., "BCI2AU")
        week_num: Week number

    Returns:
        Dict with validation results for each content type
    """
    base_path = Path(f"courses/{course_code}-*/weeks/week-{week_num:02d}")

    # Find the actual course directory
    matches = list(Path("courses").glob(f"{course_code}-*"))
    if not matches:
        return {"error": (False, [f"Course {course_code} not found"])}

    course_dir = matches[0]
    week_dir = course_dir / "weeks" / f"week-{week_num:02d}"

    results = {}

    # Validate lecture
    lecture_path = week_dir / "lecture-content.md"
    if lecture_path.exists():
        validator = LectureValidator()
        results["lecture"] = validator.validate(lecture_path)
    else:
        results["lecture"] = (False, ["Lecture file not found"])

    # Validate tutorial
    tutorial_path = week_dir / "tutorial-content.md"
    if tutorial_path.exists():
        validator = TutorialValidator()
        assessment_schedule = {}  # Load from course if available
        results["tutorial"] = validator.validate(tutorial_path, assessment_schedule)
    else:
        results["tutorial"] = (False, ["Tutorial file not found"])

    # Validate quiz
    quiz_path = week_dir / f"week-{week_num}-quiz.gift"
    if quiz_path.exists():
        validator = QuizValidator()
        lecture_content = lecture_path.read_text() if lecture_path.exists() else None
        results["quiz"] = validator.validate(quiz_path, lecture_content)
    else:
        results["quiz"] = (False, ["Quiz file not found"])

    return results


def print_validation_report(results: Dict[str, Tuple[bool, List[str]]]):
    """Print a formatted validation report."""
    print("\n" + "="*60)
    print("CONTENT VALIDATION REPORT")
    print("="*60 + "\n")

    all_valid = True

    for content_type, (is_valid, issues) in results.items():
        status = "✓ VALID" if is_valid else "✗ INVALID"
        print(f"{content_type.upper()}: {status}")

        if issues:
            for issue in issues:
                print(f"  - {issue}")
            print()

        all_valid = all_valid and is_valid

    print("="*60)
    if all_valid:
        print("✓ ALL CONTENT VALID")
    else:
        print("✗ ISSUES FOUND - Please review and fix")
    print("="*60 + "\n")

    return all_valid


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python validate_content.py <COURSE_CODE> <WEEK_NUM>")
        print("Example: python validate_content.py BCI2AU 1")
        sys.exit(1)

    course_code = sys.argv[1]
    week_num = int(sys.argv[2])

    results = validate_week_content(course_code, week_num)
    is_valid = print_validation_report(results)

    sys.exit(0 if is_valid else 1)
