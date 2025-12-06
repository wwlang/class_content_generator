"""
Content Structure Validators

Validates generated course content against quality standards:
- Lectures: Structure, slide count (XML formats), citations
- Tutorials: Alignment with assessments, timing
- Quizzes: GIFT format, content match
- Gemini: Slide count matches lecture content
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


class LectureValidator:
    """Validates lecture content structure and quality."""

    # Check for structural elements via layout hints
    REQUIRED_LAYOUTS = ["title", "section-break"]  # Must have title + sections
    MIN_SLIDES = 24
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

        # Check for structural layout/type elements (support both formats)
        for layout in self.REQUIRED_LAYOUTS:
            has_layout = (
                f'layout="{layout}"' in content.lower()
                or f'type="{layout}"' in content.lower()
                or f'type="section_title"' in content.lower()
                and layout == "section-break"
            )
            if not has_layout:
                issues.append(f"Missing required layout: {layout}")

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
        # XML format: <slide number="N" ...> or <slide id="N.N" ...>
        xml_pattern = r'<slide\s+(?:number|id)="[\d.]+"'
        xml_count = len(re.findall(xml_pattern, content))
        if xml_count > 0:
            return xml_count

        # Fallback: markdown format like "## Slide 1:" or "### Slide 1"
        slide_pattern = r'(?:##\s+Slide\s+\d+|###\s+Slide\s+\d+|\*\*Slide\s+\d+)'
        return len(re.findall(slide_pattern, content, re.IGNORECASE))

    def _count_citations(self, content: str) -> int:
        """Count sources via References section or in-text citations."""
        # Count APA references: lines starting with Author and containing (Year)
        ref_pattern = r'^[A-Z][^(\n]+\(\d{4}'
        ref_matches = re.findall(ref_pattern, content, re.MULTILINE)
        if len(ref_matches) >= 3:
            return len(ref_matches)

        # Fallback: count in-text (Author, Year) patterns
        citation_pattern = r'\([A-Z][a-z]+(?:\s+&\s+[A-Z][a-z]+)?,\s+\d{4}\)'
        citations = re.findall(citation_pattern, content)
        return max(len(set(citations)), len(ref_matches))


class TutorialValidator:
    """Validates tutorial content structure and alignment."""

    # Updated to match current format
    REQUIRED_SECTIONS = ["Quick Review", "Main Activity", "Before Next Class"]
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

        # Check timing (look for Duration in header)
        duration_match = re.search(r'Duration[:\s]*(\d+)', content, re.IGNORECASE)
        if duration_match:
            duration = int(duration_match.group(1))
            if abs(duration - self.TARGET_DURATION) > 15:
                issues.append(
                    f"Duration {duration}min differs from target "
                    f"{self.TARGET_DURATION}min"
                )

        # Check assessment connection
        if "assessment" not in content.lower() and "rubric" not in content.lower():
            issues.append("No assessment connection found")

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


class GeminiValidator:
    """Validates Gemini prompt matches lecture content."""

    def validate(
        self, gemini_path: Path, lecture_path: Path
    ) -> Tuple[bool, List[str]]:
        """
        Validate Gemini prompt matches lecture slide count.

        Args:
            gemini_path: Path to gemini-prompt.md
            lecture_path: Path to lecture-content.md

        Returns:
            (is_valid, list_of_issues)
        """
        issues = []

        if not gemini_path.exists():
            return False, ["Gemini prompt not found"]

        if not lecture_path.exists():
            return False, ["Lecture content not found (needed for comparison)"]

        gemini_content = gemini_path.read_text()
        lecture_content = lecture_path.read_text()

        lecture_slides = self._count_slides(lecture_content)
        gemini_slides = self._count_slides(gemini_content)

        if gemini_slides == 0:
            issues.append("No slides found in Gemini prompt")
        elif lecture_slides != gemini_slides:
            issues.append(
                f"Slide count mismatch: lecture={lecture_slides}, "
                f"gemini={gemini_slides}"
            )

        return len(issues) == 0, issues

    def _count_slides(self, content: str) -> int:
        """Count slides in various formats."""
        # XML format: <slide number="N" or <slide id="N.N"
        xml_count = len(re.findall(r'<slide\s+(?:number|id)="[\d.]+"', content))
        if xml_count > 0:
            return xml_count

        # Markdown format: **Slide N: or ### Slide N
        md_count = max(
            len(re.findall(r'\*\*Slide\s+\d+:', content)),
            len(re.findall(r'###\s+Slide\s+\d+', content)),
        )
        return md_count


class QuizValidator:
    """Validates quiz GIFT format and content."""

    MIN_QUESTIONS = 10
    MAX_QUESTIONS = 15  # Standard is 12 questions per week

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

        # Count questions (each question starts with ::Title:: pattern)
        # Format is ::Title::Question{...} so divide by 2
        questions = content.count('::') // 2
        if questions < self.MIN_QUESTIONS:
            issues.append(f"Too few questions: {questions} (minimum {self.MIN_QUESTIONS})")
        elif questions > self.MAX_QUESTIONS:
            issues.append(f"Too many questions: {questions} (maximum {self.MAX_QUESTIONS})")

        # Check for feedback (should have # markers for feedback)
        if content.count('#') < questions:
            issues.append("Missing feedback for some questions")

        # Check for answer markers (= for correct, ~ for incorrect in GIFT)
        # GIFT format uses { =correct ~incorrect } or just =text and ~text
        if not re.search(r'[{]\s*=|^=', content, re.MULTILINE):
            issues.append("No correct answers marked (missing = prefix)")

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

    # Validate quiz (check both locations)
    quiz_path = week_dir / "output" / f"week-{week_num:02d}-quiz.gift"
    if not quiz_path.exists():
        quiz_path = week_dir / f"week-{week_num}-quiz.gift"  # Fallback
    if quiz_path.exists():
        validator = QuizValidator()
        lecture_content = lecture_path.read_text() if lecture_path.exists() else None
        results["quiz"] = validator.validate(quiz_path, lecture_content)
    else:
        results["quiz"] = (False, ["Quiz file not found"])

    # Validate Gemini prompt
    gemini_path = week_dir / "gemini-prompt.md"
    gemini_validator = GeminiValidator()
    results["gemini"] = gemini_validator.validate(gemini_path, lecture_path)

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
