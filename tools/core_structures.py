#!/usr/bin/env python3
"""
Core data structures for Phase 3 implementation.

Provides foundational classes used by both /generate-course and /enhance-coherence.
"""

import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum


class ResearchStatus(Enum):
    """Status of research for a week."""
    NOT_FOUND = "not_found"
    FLAG_EXISTS = "flag_exists"
    IMPORTED = "imported"
    VALIDATION_FAILED = "validation_failed"
    VALID = "valid"


@dataclass
class GenerationConfig:
    """Configuration for course generation."""
    course_code: str
    course_path: Path
    total_weeks: int
    resume_from_week: Optional[int] = None
    export_slides: bool = True  # Decision 3A: Always export slides
    skip_on_validation_failure: bool = True  # Decision 2B: Skip failed, continue
    regenerate_interrupted_week: bool = True  # Decision 1A: Regenerate current week

    def __post_init__(self):
        """Ensure course_path is Path object."""
        if isinstance(self.course_path, str):
            self.course_path = Path(self.course_path)


@dataclass
class GenerationProgress:
    """Track generation progress for recovery support."""
    course_code: str
    total_weeks: int
    completed_weeks: List[int] = field(default_factory=list)
    skipped_weeks: List[int] = field(default_factory=list)
    current_week: int = 1
    last_updated: str = field(default_factory=lambda: datetime.now().isoformat())
    estimated_remaining_hours: float = 0.0
    week_times: List[float] = field(default_factory=list)  # Time per week in minutes

    def to_json(self) -> str:
        """Serialize to JSON."""
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_json(cls, json_str: str) -> 'GenerationProgress':
        """Deserialize from JSON."""
        data = json.loads(json_str)
        return cls(**data)

    def save(self, file_path: Path) -> None:
        """Save progress to file."""
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(self.to_json(), encoding='utf-8')

    @classmethod
    def load(cls, file_path: Path) -> Optional['GenerationProgress']:
        """Load progress from file."""
        if not file_path.exists():
            return None
        try:
            return cls.from_json(file_path.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"Warning: Could not load progress file: {e}")
            return None


@dataclass
class GenerationResult:
    """Result of generating a single week."""
    week_number: int
    success: bool
    files_created: List[Path] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    time_elapsed_minutes: float = 0.0
    research_status: ResearchStatus = ResearchStatus.NOT_FOUND
    validation_flag_deleted: bool = False

    def add_error(self, error: str) -> None:
        """Add an error message."""
        self.errors.append(error)
        self.success = False

    def add_warning(self, warning: str) -> None:
        """Add a warning message."""
        self.warnings.append(warning)


@dataclass
class SkippedWeek:
    """Information about a skipped week."""
    week_number: int
    topic: str
    reason: str
    errors: List[str]
    fix_instructions: str


@dataclass
class GenerationReport:
    """Final generation report."""
    course_code: str
    total_weeks: int
    completed_weeks: List[int]
    skipped_weeks: List[SkippedWeek]
    total_files: int
    total_time_hours: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    results: List[GenerationResult] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Generate markdown report."""
        lines = []

        # Header
        lines.append("═" * 65)
        lines.append("COURSE GENERATION COMPLETE")
        lines.append(f"Course: {self.course_code}")
        lines.append(f"Total time: {self.total_time_hours:.1f} hours")
        lines.append("═" * 65)
        lines.append("")

        # Summary
        lines.append(f"WEEKS GENERATED: {len(self.completed_weeks)}/{self.total_weeks}")

        for week_num in self.completed_weeks:
            result = self._get_result(week_num)
            if result:
                lines.append(f"✓ Week {week_num}: Generated successfully ({result.time_elapsed_minutes:.0f} min)")

        if self.skipped_weeks:
            lines.append("")
            lines.append(f"SKIPPED WEEKS: {len(self.skipped_weeks)}")
            for skipped in self.skipped_weeks:
                lines.append(f"✗ Week {skipped.week_number}: {skipped.topic}")
                lines.append(f"  Reason: {skipped.reason}")
                for error in skipped.errors[:3]:  # Show first 3 errors
                    lines.append(f"  - {error}")
                lines.append(f"  Fix: {skipped.fix_instructions}")
                lines.append("")

        # Outputs
        lines.append("OUTPUTS PER WEEK:")
        lines.append("├─ lecture-content.md (22-30 slides)")
        lines.append("├─ tutorial-content.md (90 min structured)")
        lines.append("├─ tutorial-tutor-notes.md (keys + guidance)")
        lines.append("├─ week-N-quiz.gift (Moodle-ready)")
        lines.append("└─ slides.html (presentation ready)")
        lines.append("")

        lines.append(f"TOTAL FILES CREATED: {self.total_files} files")

        # Next steps
        lines.append("")
        lines.append("NEXT STEPS:")
        if self.skipped_weeks:
            lines.append("1. Fix skipped weeks (see errors above)")
            lines.append("2. Run /generate-week [N] for each skipped week")
            lines.append("3. Run /enhance-coherence for quality polish")
        else:
            lines.append("1. Review generated content")
            lines.append("2. Run /enhance-coherence for quality polish")
            lines.append("3. Deploy course!")

        lines.append("")
        lines.append("═" * 65)

        return "\n".join(lines)

    def _get_result(self, week_num: int) -> Optional[GenerationResult]:
        """Get result for specific week."""
        for result in self.results:
            if result.week_number == week_num:
                return result
        return None

    def save(self, output_path: Path) -> None:
        """Save report to file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self.to_markdown(), encoding='utf-8')


@dataclass
class ValidationResult:
    """Result of validation check."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)

    def add_error(self, error: str) -> None:
        """Add error and mark as invalid."""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str) -> None:
        """Add warning (doesn't affect validity)."""
        self.warnings.append(warning)


# Coherence Analysis Data Structures

@dataclass
class TermUsage:
    """Where and how a term is used."""
    week: int
    file: str  # "lecture" or "tutorial"
    line_number: int
    context: str  # Surrounding text
    is_definition: bool = False


@dataclass
class Term:
    """A term found in content."""
    text: str
    normalized: str  # Lowercase, stripped version for comparison
    variations: List[str] = field(default_factory=list)
    first_use_week: int = 0
    uses: List[TermUsage] = field(default_factory=list)

    def add_variation(self, variation: str) -> None:
        """Add a variation of this term."""
        if variation not in self.variations and variation != self.text:
            self.variations.append(variation)


@dataclass
class Concept:
    """A concept taught in course."""
    name: str
    introduced_week: int
    definition: str = ""
    dependencies: List[str] = field(default_factory=list)
    referenced_weeks: List[int] = field(default_factory=list)
    framework_type: Optional[str] = None  # e.g., "model", "theory", "principle"


@dataclass
class Example:
    """An example used in content."""
    text: str
    week: int
    file: str  # "lecture" or "tutorial"
    domain: str  # Industry/sector (e.g., "technology", "finance")
    context: str  # Geographic/cultural (e.g., "Vietnamese", "US", "global")
    usage_type: str  # "case_study", "illustration", "exercise"
    company_name: Optional[str] = None


@dataclass
class Citation:
    """A citation in content."""
    text: str
    week: int
    file: str
    format_type: str  # "inline", "reference_list", "speaker_notes"
    is_apa_7th: bool = False
    article_key: Optional[str] = None  # Which syllabus article
    author: Optional[str] = None
    year: Optional[str] = None


@dataclass
class Framework:
    """A framework or model presented."""
    name: str
    week: int
    type: str  # "model", "theory", "principle", "framework"
    components: List[str] = field(default_factory=list)
    source_citation: Optional[str] = None


@dataclass
class WeekContent:
    """Extracted content from a single week."""
    week_number: int
    topic: str
    lecture_path: Path
    tutorial_path: Path
    terms: List[Term] = field(default_factory=list)
    concepts: List[Concept] = field(default_factory=list)
    examples: List[Example] = field(default_factory=list)
    citations: List[Citation] = field(default_factory=list)
    frameworks: List[Framework] = field(default_factory=list)
    word_count_lecture: int = 0
    word_count_tutorial: int = 0


@dataclass
class CoherenceIssue:
    """Base class for coherence issues."""
    issue_id: str
    issue_type: str
    quality_score: int  # 1-10 (Decision 3C)
    affected_weeks: List[int]
    suggested_fix: str
    auto_apply_safe: bool
    category: str  # "terminology", "scaffolding", "examples", "cross_references", "citations"

    def get_priority(self) -> str:
        """Get priority based on score."""
        if self.quality_score >= 9:
            return "CRITICAL"
        elif self.quality_score >= 7:
            return "IMPORTANT"
        elif self.quality_score >= 4:
            return "MEDIUM"
        else:
            return "MINOR"


@dataclass
class EnhancementConfig:
    """Configuration for enhancement (Decision 1C - user chooses per type)."""
    apply_terminology: bool = False
    apply_scaffolding: bool = False
    apply_examples: bool = False
    apply_cross_references: bool = False
    apply_citations: bool = False
    create_git_backup: bool = True  # Decision 2B
    dry_run: bool = False  # Preview changes without applying


@dataclass
class EnhancementResult:
    """Result of applying a single enhancement."""
    issue_id: str
    success: bool
    file_modified: Optional[Path] = None
    changes_made: str = ""
    error: Optional[str] = None


@dataclass
class CoherenceReport:
    """Complete coherence analysis report."""
    course_code: str
    total_issues: int
    issues_by_category: Dict[str, List['CoherenceIssue']] = field(default_factory=dict)
    critical_issues: List['CoherenceIssue'] = field(default_factory=list)  # Score 9-10
    important_issues: List['CoherenceIssue'] = field(default_factory=list)  # Score 7-8
    medium_issues: List['CoherenceIssue'] = field(default_factory=list)  # Score 4-6
    minor_issues: List['CoherenceIssue'] = field(default_factory=list)  # Score 1-3
    auto_fixable_count: int = 0
    manual_review_count: int = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
