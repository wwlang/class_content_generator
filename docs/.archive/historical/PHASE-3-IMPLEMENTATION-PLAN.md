# Phase 3 Implementation Plan

**Commands:** `/generate-course` (Phase 3A) and `/enhance-coherence` (Phase 3B)

**Goal:** End-to-end automation + professional quality enhancement

---

## Architecture Overview

### Component Structure

```
Phase 3 Components:
├── tools/
│   ├── generate_course.py          # Phase 3A: Batch generation orchestrator
│   ├── enhance_coherence.py        # Phase 3B: Coherence analysis & enhancement
│   └── coherence/                  # Phase 3B: Analysis modules
│       ├── __init__.py
│       ├── analyzer.py             # Content extraction and analysis
│       ├── terminology.py          # Terminology consistency analysis
│       ├── scaffolding.py          # Concept scaffolding analysis
│       ├── examples.py             # Example diversity analysis
│       ├── cross_references.py     # Cross-reference opportunities
│       ├── citations.py            # Citation formatting analysis
│       ├── scorer.py               # Issue scoring system (1-10)
│       ├── enhancer.py             # Enhancement application engine
│       └── reporter.py             # Report generation
│
├── tests/
│   ├── test_generate_course.py    # Unit tests for batch generation
│   ├── test_coherence_analyzer.py # Unit tests for coherence analysis
│   ├── test_coherence_enhancer.py # Unit tests for enhancement
│   ├── integration/
│   │   ├── test_phase3_integration.py  # Integration tests
│   │   └── fixtures/                    # Test fixtures (sample courses)
│   └── e2e/
│       ├── test_full_workflow.py        # End-to-end workflow tests
│       └── test_course_generation.py    # Complete course generation test
│
└── .claude/commands/
    ├── generate-course.md          # Command specification (DONE)
    └── enhance-coherence.md        # Command specification (DONE)
```

---

## Phase 3A: `/generate-course` Implementation

### Core Modules

#### 1. `tools/generate_course.py` - Main Orchestrator

**Purpose:** Batch generate all weeks with progress tracking and recovery

**Key Classes:**

```python
@dataclass
class GenerationConfig:
    """Configuration for course generation."""
    course_code: str
    course_path: Path
    total_weeks: int
    resume_from_week: Optional[int] = None
    export_slides: bool = True  # Decision 3A
    skip_on_validation_failure: bool = True  # Decision 2B
    regenerate_interrupted_week: bool = True  # Decision 1A

@dataclass
class GenerationProgress:
    """Track generation progress for recovery."""
    course_code: str
    total_weeks: int
    completed_weeks: List[int]
    skipped_weeks: List[int]
    current_week: int
    last_updated: str
    estimated_remaining: str

@dataclass
class GenerationResult:
    """Result of generating a single week."""
    week_number: int
    success: bool
    files_created: List[Path]
    errors: List[str]
    warnings: List[str]
    time_elapsed: float

class CourseGenerator:
    """Main orchestrator for batch course generation."""

    def __init__(self, config: GenerationConfig):
        self.config = config
        self.progress = self._load_or_create_progress()
        self.results: List[GenerationResult] = []

    def generate(self) -> GenerationReport:
        """Execute batch generation with progress tracking."""
        # Pre-flight validation
        # Generation loop
        # Post-generation report
        pass

    def _validate_prerequisites(self) -> ValidationResult:
        """Pre-flight checks: syllabus, research, etc."""
        pass

    def _generate_week(self, week_num: int) -> GenerationResult:
        """Generate single week with validation."""
        pass

    def _save_progress(self) -> None:
        """Save progress for recovery."""
        pass

    def _create_report(self) -> GenerationReport:
        """Create final generation report."""
        pass
```

**Key Functions:**

```python
def validate_syllabus(course_path: Path) -> Tuple[bool, int, List[str]]:
    """
    Validate syllabus exists and count weeks.

    Returns:
        (is_valid, week_count, errors)
    """
    pass

def check_research_availability(course_path: Path, week_num: int) -> ResearchStatus:
    """
    Check if research exists for week (validation flag or imported).

    Returns:
        ResearchStatus(exists, has_flag, is_valid, errors)
    """
    pass

def validate_research(course_path: Path, week_num: int) -> Tuple[bool, List[str]]:
    """
    Validate research for week (Phase 2 integration).
    Uses same logic as /import-research validation.
    """
    pass

def generate_week_content(course_path: Path, week_num: int) -> GenerationResult:
    """
    Generate all content for week.
    Calls existing /generate-week logic.
    """
    pass

def export_week_slides(course_path: Path, week_num: int) -> Tuple[bool, List[str]]:
    """
    Export slides for week.
    Calls existing /export-slides logic.
    """
    pass

def estimate_time_remaining(completed: int, total: int, avg_time: float) -> str:
    """Calculate estimated time remaining."""
    pass
```

**Progress Tracking:**

```python
class ProgressTracker:
    """Track and display generation progress."""

    def __init__(self, total_weeks: int):
        self.total_weeks = total_weeks
        self.completed = 0
        self.start_time = time.time()
        self.week_times: List[float] = []

    def update(self, week_num: int, success: bool, elapsed: float) -> None:
        """Update progress after week completion."""
        pass

    def display_progress(self, week_num: int) -> str:
        """Generate progress display string."""
        # ═══════════════════════════════════════════
        # Week 5/10: Topic Name
        # Progress: [█████░░░░░] 50%
        # ═══════════════════════════════════════════
        pass

    def get_summary(self) -> Dict[str, Any]:
        """Get progress summary for reporting."""
        pass
```

**Recovery Support (Decision 1A):**

```python
class RecoveryManager:
    """Handle interruption and recovery."""

    @staticmethod
    def detect_interrupted_generation(course_path: Path) -> Optional[GenerationProgress]:
        """Check for interrupted generation."""
        progress_file = course_path / ".working" / "generation-progress.json"
        if progress_file.exists():
            return GenerationProgress.from_json(progress_file.read_text())
        return None

    @staticmethod
    def prompt_resume(progress: GenerationProgress) -> bool:
        """Ask user if they want to resume."""
        # Display what was completed
        # Show what will be regenerated (current week)
        # Get user confirmation
        pass

    @staticmethod
    def cleanup_progress(course_path: Path) -> None:
        """Remove progress file after completion."""
        pass
```

**Report Generation:**

```python
@dataclass
class GenerationReport:
    """Final generation report."""
    course_code: str
    total_weeks: int
    completed_weeks: List[int]
    skipped_weeks: List[Dict[str, Any]]  # {week, reason, errors}
    total_files: int
    total_time: float
    timestamp: str

    def to_markdown(self) -> str:
        """Generate markdown report."""
        # See command spec for report format
        pass

    def save(self, output_path: Path) -> None:
        """Save report to file."""
        pass
```

### Integration Points

**1. Phase 2 Validation Integration:**
```python
def integrate_phase2_validation(course_path: Path, week_num: int) -> Tuple[bool, Optional[Path], List[str]]:
    """
    Check for validation flag and validate research.

    Process:
    1. Look for .week-[N]-ready flag
    2. If found: Validate research
    3. If valid: Delete flag, return True
    4. If invalid: Return False with errors
    5. If no flag: Check for imported research

    Returns:
        (is_valid, flag_path, errors)
    """
    flag_path = course_path / ".working" / "research" / f".week-{week_num}-ready"

    if flag_path.exists():
        # Validate research
        is_valid, errors = validate_research(course_path, week_num)

        if is_valid:
            flag_path.unlink()  # Delete flag after successful validation
            return (True, flag_path, [])
        else:
            return (False, flag_path, errors)

    # No flag - check for imported research
    research_file = course_path / ".working" / "research" / "article-research-summary.md"
    if research_file.exists():
        # Check if this week's research is in the file
        # Return validation result
        pass

    return (False, None, ["No research found"])
```

**2. Existing Week Generation Integration:**
```python
def call_generate_week(course_path: Path, week_num: int) -> GenerationResult:
    """
    Call existing /generate-week logic.

    This doesn't create a new implementation - it reuses existing logic.
    We'll need to refactor /generate-week command to be callable as a function.
    """
    # Import or call existing generation logic
    # Return standardized result
    pass
```

**3. Slide Export Integration:**
```python
def call_export_slides(course_path: Path, week_num: int) -> Tuple[bool, List[str]]:
    """
    Call existing /export-slides logic.

    Uses slide-exporter skill or calls convert_lecture_to_slides.py.
    """
    # Import existing slide export logic
    # Return success and any errors
    pass
```

### Testing Strategy

**Unit Tests (`tests/test_generate_course.py`):**

```python
class TestCourseGenerator:
    """Unit tests for CourseGenerator."""

    def test_validate_syllabus_exists(self):
        """Test syllabus validation with valid syllabus."""
        pass

    def test_validate_syllabus_missing(self):
        """Test syllabus validation with missing syllabus."""
        pass

    def test_count_weeks_from_syllabus(self):
        """Test week counting from syllabus."""
        pass

    def test_check_research_with_flag(self):
        """Test research detection with validation flag."""
        pass

    def test_check_research_without_flag(self):
        """Test research detection from imported research file."""
        pass

    def test_progress_tracking(self):
        """Test progress tracking updates correctly."""
        pass

    def test_recovery_detection(self):
        """Test detection of interrupted generation."""
        pass

    def test_skip_on_validation_failure(self):
        """Test Decision 2B: skip failed week, continue."""
        pass

    def test_regenerate_interrupted_week(self):
        """Test Decision 1A: resume regenerates current week."""
        pass

class TestProgressTracker:
    """Unit tests for ProgressTracker."""

    def test_progress_display(self):
        """Test progress bar formatting."""
        pass

    def test_time_estimation(self):
        """Test time remaining calculation."""
        pass

class TestRecoveryManager:
    """Unit tests for RecoveryManager."""

    def test_detect_interrupted(self):
        """Test interrupted generation detection."""
        pass

    def test_resume_from_week(self):
        """Test resuming from specific week."""
        pass
```

---

## Phase 3B: `/enhance-coherence` Implementation

### Core Modules

#### 1. `tools/coherence/analyzer.py` - Content Extraction

**Purpose:** Extract and parse all week content for analysis

```python
@dataclass
class WeekContent:
    """Extracted content from a single week."""
    week_number: int
    topic: str
    lecture_path: Path
    tutorial_path: Path
    terms: List[Term]
    concepts: List[Concept]
    examples: List[Example]
    citations: List[Citation]
    frameworks: List[Framework]

@dataclass
class Term:
    """A term found in content."""
    text: str
    variations: List[str]  # Different ways same term is written
    first_use_week: int
    uses: List[TermUsage]  # Where and how term is used

@dataclass
class Concept:
    """A concept taught in course."""
    name: str
    introduced_week: int
    dependencies: List[str]  # Other concepts this depends on
    references: List[int]  # Weeks where referenced

@dataclass
class Example:
    """An example used in content."""
    text: str
    week: int
    domain: str  # Industry/sector
    context: str  # Vietnamese, US, global, etc.
    usage_type: str  # Case study, illustration, exercise

@dataclass
class Citation:
    """A citation in content."""
    text: str
    week: int
    format: str  # APA, inline, reference list
    article_key: str  # Which syllabus article

class ContentExtractor:
    """Extract content from all weeks."""

    def extract_all_weeks(self, course_path: Path) -> List[WeekContent]:
        """Extract content from all generated weeks."""
        pass

    def extract_terms(self, markdown_content: str) -> List[Term]:
        """Extract key terms from markdown."""
        # Look for bolded terms, defined terms, etc.
        pass

    def extract_concepts(self, markdown_content: str) -> List[Concept]:
        """Extract concepts and frameworks."""
        # Look for heading patterns, definition patterns
        pass

    def extract_examples(self, markdown_content: str) -> List[Example]:
        """Extract examples and case studies."""
        # Pattern match for example markers
        # Classify by domain
        pass

    def extract_citations(self, markdown_content: str) -> List[Citation]:
        """Extract all citations."""
        # Find inline citations (Author, Year)
        # Find reference lists
        # Classify format
        pass
```

#### 2. `tools/coherence/terminology.py` - Terminology Analysis

**Purpose:** Analyze terminology consistency

```python
@dataclass
class TerminologyIssue:
    """An issue with terminology consistency."""
    issue_id: str
    issue_type: str  # "inconsistent_usage", "undefined_jargon", "term_drift"
    quality_score: int  # 1-10 (Decision 3C)
    term: str
    variations: List[str]
    affected_weeks: List[int]
    suggested_standard: str
    suggested_fix: str
    auto_apply_safe: bool

class TerminologyAnalyzer:
    """Analyze terminology consistency across weeks."""

    def analyze(self, weeks: List[WeekContent]) -> List[TerminologyIssue]:
        """Find all terminology issues."""
        pass

    def find_inconsistent_usage(self, weeks: List[WeekContent]) -> List[TerminologyIssue]:
        """Find same concept with different terms."""
        # "value proposition" vs "value prop"
        # Score based on frequency and weeks affected
        pass

    def find_undefined_jargon(self, weeks: List[WeekContent]) -> List[TerminologyIssue]:
        """Find jargon used without definition."""
        # Terms used before defined
        # Acronyms without expansion
        # High score (8-10) for critical terms
        pass

    def find_term_drift(self, weeks: List[WeekContent]) -> List[TerminologyIssue]:
        """Find terminology that drifts across weeks."""
        # "audience analysis" → "reader analysis" → "stakeholder analysis"
        # Score based on confusion potential
        pass
```

#### 3. `tools/coherence/scaffolding.py` - Scaffolding Analysis

**Purpose:** Analyze concept prerequisites and progression

```python
@dataclass
class ScaffoldingIssue:
    """An issue with concept scaffolding."""
    issue_id: str
    issue_type: str  # "used_before_introduced", "missing_reference", "prerequisite_gap"
    quality_score: int  # 1-10
    concept: str
    first_used_week: int
    introduced_week: Optional[int]
    suggested_fix: str
    auto_apply_safe: bool

class ScaffoldingAnalyzer:
    """Analyze concept scaffolding and dependencies."""

    def analyze(self, weeks: List[WeekContent]) -> List[ScaffoldingIssue]:
        """Find all scaffolding issues."""
        pass

    def find_concepts_used_before_introduced(self, weeks: List[WeekContent]) -> List[ScaffoldingIssue]:
        """Find concepts used before proper introduction."""
        # Week 2 uses "persuasion principles" but Week 5 introduces them
        # High score (7-10) for significant concepts
        pass

    def find_missing_references(self, weeks: List[WeekContent]) -> List[ScaffoldingIssue]:
        """Find opportunities for backward/forward references."""
        # Week 7 could reference Week 2's framework
        # Score based on connection strength
        pass

    def find_prerequisite_gaps(self, weeks: List[WeekContent]) -> List[ScaffoldingIssue]:
        """Find weeks assuming knowledge not taught."""
        # Week 8 assumes slide design, but never taught
        # Critical score (9-10)
        pass
```

#### 4. `tools/coherence/examples.py` - Example Diversity Analysis

**Purpose:** Analyze example diversity and duplication

```python
@dataclass
class ExampleIssue:
    """An issue with example diversity."""
    issue_id: str
    issue_type: str  # "duplicate", "domain_clustering", "vietnamese_gap"
    quality_score: int  # 1-10
    examples: List[Example]
    affected_weeks: List[int]
    suggested_fix: str
    auto_apply_safe: bool

class ExampleAnalyzer:
    """Analyze example diversity across weeks."""

    def analyze(self, weeks: List[WeekContent]) -> List[ExampleIssue]:
        """Find all example issues."""
        pass

    def find_duplicates(self, weeks: List[WeekContent]) -> List[ExampleIssue]:
        """Find same example used multiple times."""
        # Low score (3-4) unless critical example
        pass

    def find_domain_clustering(self, weeks: List[WeekContent]) -> List[ExampleIssue]:
        """Find over-representation of certain industries."""
        # 39% tech examples → Medium score (6)
        # Suggest diversification
        pass

    def find_vietnamese_gaps(self, weeks: List[WeekContent]) -> List[ExampleIssue]:
        """Find weeks missing Vietnamese context."""
        # High score (8) for cultural relevance
        pass
```

#### 5. `tools/coherence/cross_references.py` - Cross-Reference Analysis

**Purpose:** Find opportunities to link concepts across weeks

```python
@dataclass
class CrossReferenceOpportunity:
    """An opportunity to add cross-reference."""
    issue_id: str
    opportunity_type: str  # "forward", "backward", "lateral"
    quality_score: int  # 1-10
    source_week: int
    target_week: int
    concept: str
    suggested_text: str
    auto_apply_safe: bool

class CrossReferenceAnalyzer:
    """Find cross-reference opportunities."""

    def analyze(self, weeks: List[WeekContent]) -> List[CrossReferenceOpportunity]:
        """Find all cross-reference opportunities."""
        pass

    def find_forward_references(self, weeks: List[WeekContent]) -> List[CrossReferenceOpportunity]:
        """Find places to preview upcoming concepts."""
        # Week 2 could preview Week 5
        # Medium score (5-6)
        pass

    def find_backward_references(self, weeks: List[WeekContent]) -> List[CrossReferenceOpportunity]:
        """Find places to reinforce prior concepts."""
        # Week 7 could reference Week 1 foundations
        # High score (8-9) for reinforcement
        pass

    def find_lateral_references(self, weeks: List[WeekContent]) -> List[CrossReferenceOpportunity]:
        """Find places to connect parallel concepts."""
        # Week 4 persuasion + Week 7 emails = persuasive emails
        # High score (8-9) for practical integration
        pass
```

#### 6. `tools/coherence/citations.py` - Citation Analysis

**Purpose:** Ensure citation consistency

```python
@dataclass
class CitationIssue:
    """An issue with citation formatting."""
    issue_id: str
    issue_type: str  # "format_variation", "duplicate_format", "unused_article"
    quality_score: int  # 1-10
    citation: Citation
    correct_format: str
    affected_weeks: List[int]
    auto_apply_safe: bool

class CitationAnalyzer:
    """Analyze citation consistency."""

    def analyze(self, weeks: List[WeekContent]) -> List[CitationIssue]:
        """Find all citation issues."""
        pass

    def find_format_variations(self, weeks: List[WeekContent]) -> List[CitationIssue]:
        """Find inconsistent citation formats."""
        # "Cialdini, R. (2021)" vs "Cialdini (2021)" vs "R. Cialdini, 2021"
        # Low score (3) but easy auto-fix
        pass

    def find_duplicate_formats(self, weeks: List[WeekContent]) -> List[CitationIssue]:
        """Find same article cited differently."""
        # Same article, two different citation strings
        # Low score (3) but easy auto-fix
        pass

    def find_unused_articles(self, weeks: List[WeekContent]) -> List[CitationIssue]:
        """Find syllabus articles not cited."""
        # Medium score (5) - wasted research
        pass
```

#### 7. `tools/coherence/scorer.py` - Issue Scoring System (Decision 3C)

**Purpose:** Score all issues 1-10 for quality impact

```python
class IssueScorer:
    """Score issues for quality impact (1-10)."""

    @staticmethod
    def score_terminology_issue(issue: TerminologyIssue) -> int:
        """
        Score terminology issues.

        Criteria:
        - 9-10: Critical jargon undefined, high confusion potential
        - 7-8: Inconsistent usage across many weeks
        - 4-6: Minor inconsistencies or term drift
        - 1-3: Cosmetic improvements
        """
        pass

    @staticmethod
    def score_scaffolding_issue(issue: ScaffoldingIssue) -> int:
        """
        Score scaffolding issues.

        Criteria:
        - 9-10: Missing prerequisite, breaks learning sequence
        - 7-8: Concept used before introduced, missed reinforcement
        - 4-6: Reference opportunity, helpful but not critical
        - 1-3: Nice-to-have connections
        """
        pass

    @staticmethod
    def score_example_issue(issue: ExampleIssue) -> int:
        """
        Score example issues.

        Criteria:
        - 9-10: Critical cultural gap (no Vietnamese context)
        - 7-8: Significant domain clustering
        - 4-6: Duplicate examples
        - 1-3: Minor variety improvements
        """
        pass

    @staticmethod
    def score_cross_reference(issue: CrossReferenceOpportunity) -> int:
        """
        Score cross-reference opportunities.

        Criteria:
        - 9-10: Critical skill integration (lateral references)
        - 7-8: Strong reinforcement (backward references)
        - 4-6: Preview opportunities (forward references)
        - 1-3: Nice-to-have connections
        """
        pass

    @staticmethod
    def score_citation_issue(issue: CitationIssue) -> int:
        """
        Score citation issues.

        Criteria:
        - 9-10: (None - citations are formatting)
        - 7-8: (None)
        - 4-6: Unused articles (wasted research)
        - 1-3: Format inconsistencies (cosmetic)
        """
        pass
```

#### 8. `tools/coherence/enhancer.py` - Enhancement Application (Decision 1C, 2B)

**Purpose:** Apply selected enhancements with git backup

```python
class EnhancementApplicator:
    """Apply enhancements to week files."""

    def __init__(self, course_path: Path):
        self.course_path = course_path
        self.git_backup: Optional[str] = None

    def create_git_backup(self) -> Optional[str]:
        """
        Create git commit backup (Decision 2B).

        Returns:
            Commit hash or None if not git repo
        """
        import subprocess

        # Check if git repo
        try:
            subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.course_path,
                check=True,
                capture_output=True
            )
        except:
            return None

        # Create commit
        try:
            subprocess.run(
                ["git", "add", "weeks/"],
                cwd=self.course_path,
                check=True
            )

            commit_msg = f"Pre-coherence-enhancement backup - {datetime.now()}"
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=self.course_path,
                check=True,
                capture_output=True,
                text=True
            )

            # Get commit hash
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.course_path,
                check=True,
                capture_output=True,
                text=True
            )

            return result.stdout.strip()
        except:
            return None

    def apply_enhancement(self, issue: Any) -> Tuple[bool, str]:
        """
        Apply a single enhancement.

        Returns:
            (success, message)
        """
        # Dispatch to specific applier based on issue type
        if isinstance(issue, TerminologyIssue):
            return self._apply_terminology(issue)
        elif isinstance(issue, ScaffoldingIssue):
            return self._apply_scaffolding(issue)
        # ... etc
        pass

    def _apply_terminology(self, issue: TerminologyIssue) -> Tuple[bool, str]:
        """Apply terminology enhancement."""
        # Read file, find term, replace with standard
        # Return success and details
        pass

    def _apply_scaffolding(self, issue: ScaffoldingIssue) -> Tuple[bool, str]:
        """Apply scaffolding enhancement."""
        # Add reference text at specified location
        pass

    def _apply_cross_reference(self, issue: CrossReferenceOpportunity) -> Tuple[bool, str]:
        """Apply cross-reference enhancement."""
        # Insert suggested text at appropriate location
        pass
```

#### 9. `tools/coherence/reporter.py` - Report Generation

**Purpose:** Generate comprehensive coherence reports

```python
class CoherenceReporter:
    """Generate coherence analysis reports."""

    def generate_full_report(
        self,
        terminology_issues: List[TerminologyIssue],
        scaffolding_issues: List[ScaffoldingIssue],
        example_issues: List[ExampleIssue],
        cross_ref_opportunities: List[CrossReferenceOpportunity],
        citation_issues: List[CitationIssue]
    ) -> str:
        """
        Generate full coherence report (8,000-10,000 words).

        Sections:
        - Overall coherence score
        - Critical issues (9-10) with details
        - Important issues (7-8) with details
        - Medium issues (4-6) with details
        - Minor issues (1-3) with details
        - Enhancement summary by type
        - Auto-apply summary
        """
        pass

    def generate_summary(self, full_report_data: Dict) -> str:
        """Generate executive summary (500-800 words)."""
        pass

    def generate_manual_todo(self, issues: List[Any]) -> str:
        """Generate manual enhancement todo list."""
        # Checklist format
        # File paths and line numbers
        # Suggested fixes
        pass
```

### Testing Strategy

**Unit Tests (`tests/test_coherence_analyzer.py`):**

```python
class TestContentExtractor:
    """Test content extraction."""

    def test_extract_terms(self):
        """Test term extraction from markdown."""
        pass

    def test_extract_concepts(self):
        """Test concept extraction."""
        pass

    def test_extract_examples(self):
        """Test example extraction and classification."""
        pass

class TestTerminologyAnalyzer:
    """Test terminology analysis."""

    def test_find_inconsistent_usage(self):
        """Test finding term variations."""
        pass

    def test_find_undefined_jargon(self):
        """Test jargon detection."""
        pass

class TestIssueScorer:
    """Test scoring system."""

    def test_score_critical_issues(self):
        """Test 9-10 scoring."""
        pass

    def test_score_minor_issues(self):
        """Test 1-3 scoring."""
        pass
```

**Unit Tests (`tests/test_coherence_enhancer.py`):**

```python
class TestEnhancementApplicator:
    """Test enhancement application."""

    def test_git_backup_creation(self):
        """Test git commit backup."""
        pass

    def test_apply_terminology_enhancement(self):
        """Test terminology fix application."""
        pass

    def test_revert_on_error(self):
        """Test rollback on enhancement error."""
        pass
```

---

## Integration Tests

**File: `tests/integration/test_phase3_integration.py`**

```python
class TestPhase3Integration:
    """Integration tests for Phase 3 commands."""

    def test_generate_course_with_valid_research(self):
        """Test batch generation with all research ready."""
        pass

    def test_generate_course_with_validation_flags(self):
        """Test Phase 2 integration (validation flags)."""
        pass

    def test_generate_course_with_failures(self):
        """Test skip-on-failure behavior (Decision 2B)."""
        pass

    def test_generate_course_recovery(self):
        """Test interruption and recovery (Decision 1A)."""
        pass

    def test_enhance_coherence_analysis(self):
        """Test full coherence analysis pipeline."""
        pass

    def test_enhance_coherence_application(self):
        """Test enhancement application."""
        pass

    def test_enhance_coherence_git_backup(self):
        """Test git backup (Decision 2B)."""
        pass
```

---

## End-to-End Tests

**File: `tests/e2e/test_full_workflow.py`**

```python
class TestFullWorkflow:
    """End-to-end tests for complete workflows."""

    @pytest.fixture
    def sample_course(self):
        """Create a complete sample course for testing."""
        # 3-week mini course with all components
        pass

    def test_complete_phase3_workflow(self, sample_course):
        """
        Test complete Phase 3 workflow:
        1. /generate-course
        2. /enhance-coherence
        3. Verify all files created
        4. Verify quality improvements
        """
        pass

    def test_workflow_with_interruption_recovery(self, sample_course):
        """
        Test workflow with interruption:
        1. Start /generate-course
        2. Simulate interruption at week 2
        3. Resume /generate-course
        4. Verify recovery works (Decision 1A)
        """
        pass

    def test_workflow_with_validation_failures(self, sample_course):
        """
        Test workflow with bad research:
        1. Set up course with 1 invalid research
        2. Run /generate-course
        3. Verify skip behavior (Decision 2B)
        4. Verify other weeks still generated
        """
        pass

    def test_enhancement_revert(self, sample_course):
        """
        Test enhancement rollback:
        1. Generate course
        2. Apply enhancements
        3. Simulate issue
        4. Verify git revert works
        """
        pass
```

---

## Test Fixtures

**File: `tests/integration/fixtures/sample_course/`**

Structure:
```
sample_course/
├── syllabus.md                     # 3-week sample syllabus
├── .working/
│   └── research/
│       ├── article-research-summary.md  # Research for all 3 weeks
│       ├── .week-1-ready           # Validation flag
│       ├── .week-2-ready
│       └── .week-3-ready
├── weeks/
│   ├── week-01/
│   │   ├── lecture-content.md      # Pre-generated for enhancement testing
│   │   └── tutorial-content.md
│   ├── week-02/
│   │   ├── lecture-content.md
│   │   └── tutorial-content.md
│   └── week-03/
│       ├── lecture-content.md
│       └── tutorial-content.md
└── expected-outputs/
    ├── coherence-report.md         # Expected report for validation
    └── enhancement-summary.md      # Expected summary
```

---

## Implementation Sequence

### Phase 1: Core Infrastructure (Week 1)
1. ✅ Command specifications (DONE)
2. Create project structure (`tools/coherence/`)
3. Implement `ContentExtractor` (basic version)
4. Implement `ProgressTracker`
5. Implement `RecoveryManager`
6. Write unit tests for infrastructure

### Phase 2: Batch Generation (Week 1-2)
1. Implement `CourseGenerator` main logic
2. Integrate Phase 2 validation
3. Integrate existing `/generate-week` logic
4. Integrate slide export
5. Implement report generation
6. Write unit tests
7. Write integration tests for generation

### Phase 3: Coherence Analysis (Week 2-3)
1. Implement all analyzer modules:
   - `TerminologyAnalyzer`
   - `ScaffoldingAnalyzer`
   - `ExampleAnalyzer`
   - `CrossReferenceAnalyzer`
   - `CitationAnalyzer`
2. Implement `IssueScorer`
3. Implement `CoherenceReporter`
4. Write unit tests for each analyzer
5. Write integration tests for analysis

### Phase 4: Enhancement Application (Week 3)
1. Implement `EnhancementApplicator`
2. Implement git backup
3. Implement per-type enhancement logic
4. Implement manual todo generation
5. Write unit tests
6. Write integration tests

### Phase 5: End-to-End Testing (Week 4)
1. Create test fixtures
2. Write e2e workflow tests
3. Write recovery tests
4. Write enhancement tests
5. Run full test suite
6. Fix any failures

### Phase 6: Documentation & Polish (Week 4)
1. Update implementation notes in CLAUDE.md
2. Create user guide additions
3. Add troubleshooting section
4. Code review and refactor
5. Performance optimization
6. Final testing

---

## Success Criteria

### Functional Requirements
- ✅ `/generate-course` generates all weeks successfully
- ✅ `/generate-course` handles interruptions and recovers correctly (1A)
- ✅ `/generate-course` skips failed weeks and continues (2B)
- ✅ `/generate-course` always exports slides (3A)
- ✅ `/enhance-coherence` analyzes all 5 categories
- ✅ `/enhance-coherence` scores all issues 1-10 (3C)
- ✅ `/enhance-coherence` allows per-type selection (1C)
- ✅ `/enhance-coherence` creates git backup (2B)

### Quality Requirements
- ✅ 80%+ test coverage for all new code
- ✅ All unit tests pass
- ✅ All integration tests pass
- ✅ All e2e tests pass
- ✅ No regressions in existing functionality
- ✅ Clean code following SOLID principles
- ✅ Type hints on all functions
- ✅ Comprehensive docstrings

### Performance Requirements
- ✅ `/generate-course` 10-week course: 7-12 hours (acceptable for overnight run)
- ✅ `/enhance-coherence` 10-week course: 15-30 minutes
- ✅ Memory usage reasonable (<2GB for typical course)
- ✅ Progress updates every 30 seconds or less

### User Experience Requirements
- ✅ Clear progress tracking with time estimates
- ✅ Helpful error messages with recovery guidance
- ✅ Reports are readable and actionable
- ✅ Manual todo lists have specific file locations
- ✅ Git backup makes rollback easy

---

## Dependencies

### Python Packages (add to requirements.txt)
```
pytest>=7.0.0           # Testing framework
pytest-cov>=4.0.0       # Coverage reporting
pytest-mock>=3.10.0     # Mocking support
```

### Internal Dependencies
- Existing `/generate-week` logic (need to refactor to callable function)
- Existing `/export-slides` logic (slide-exporter skill)
- Phase 2 validation logic from `/import-research`
- Markdown parsing utilities
- APA citation formatting utilities

---

## Risk Mitigation

### Risk 1: Integration with existing code
**Mitigation:** Create adapter layer for existing commands, test thoroughly

### Risk 2: Large codebases may be slow to analyze
**Mitigation:** Implement caching, optimize parsers, show progress

### Risk 3: Enhancement application may break markdown
**Mitigation:** Comprehensive tests, git backup, dry-run mode

### Risk 4: Recovery mechanism may fail
**Mitigation:** Robust progress file format, validation on load, fallback options

---

*This implementation plan provides complete architecture and testing strategy for Phase 3. Ready to begin implementation.*
