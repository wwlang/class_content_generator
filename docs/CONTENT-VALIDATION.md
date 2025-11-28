# Content Validation Guide

AI-powered validation for university teaching content quality.

## Overview

The content validation system checks 8 aspects of course quality:

| Phase | Validator | Purpose | Severity |
|-------|-----------|---------|----------|
| 1 | Bloom's Level | Quiz questions match stated cognitive level | CRITICAL |
| 1 | Tutorial-Assessment | Tutorials prepare for graded work | CRITICAL |
| 1 | Lecture-Quiz | Quizzes test taught content | CRITICAL |
| 1 | Framework Scaffolding | Concepts introduced before referenced | CRITICAL |
| 2 | Learning Objectives | All LOs taught and assessed | CRITICAL/WARNING |
| 2 | Rubric Specificity | Criteria are measurable | WARNING |
| 2 | Terminology | Same terms used throughout | WARNING |
| 2 | Cultural/ESL | Appropriate for Vietnamese students | WARNING/SUGGESTION |

---

## Quick Start

### Using Claude Code (Recommended)

```
/validate-content BCI2AU
/validate-content BCI2AU --phase1
/validate-content BCI2AU --phase2
```

This uses Claude Code directly with the content-validation skill - no separate API key needed.

### Using Python CLI (Optional)

For programmatic/automated use with your own API key:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
python3 tools/validate_course_quality.py courses/BCI2AU-business-communication
python3 tools/validate_course_quality.py courses/BCI2AU-business-communication --phase1
python3 tools/validate_course_quality.py courses/BCI2AU-business-communication --report
```

Available CLI validators: `bloom`, `tutorial`, `lecture-quiz`, `scaffolding`, `learning-objectives`, `rubric`, `terminology`, `cultural`

---

## Phase 1 Validators (Critical Alignment)

### 1. Bloom's Level Validator

**What it checks:** Quiz questions actually match their stated Bloom's taxonomy level.

**Common issues:**
- Questions labeled "Remembering" that require application/analysis
- Scenario-based questions marked as "Understanding"
- Definition recall questions labeled higher than "Remembering"

**Bloom's Level Definitions for Quizzes:**

| Level | Appropriate For | Question Types |
|-------|-----------------|----------------|
| Remembering | Recall facts, definitions | "What is...", "Name the...", "Which of..." |
| Understanding | Explain why, distinguish concepts | "Why does...", "What is the difference...", "What is the purpose..." |
| Applying | Use in scenarios | "Given this situation...", "Apply X to..." |

**Fix guidance:**
- Relabel questions to match actual cognitive demand
- Or rewrite questions to match intended level
- Remembering questions should NOT include scenarios

---

### 2. Tutorial-Assessment Validator

**What it checks:** Tutorials explicitly prepare students for specific assessments.

**Required elements:**
1. **Assessment Connection statement** - Explicit link to specific assessment
2. **Scaled activity** - Practices same skill/format as assessment, but smaller
3. **Success criteria from rubric** - Not invented, pulled from Assessment Handbook

**Common issues:**
- Generic activities not tied to any assessment
- Success criteria invented instead of rubric-based
- Missing "Assessment Connection" statement

**Fix guidance:**
- Add "Assessment Connection" header linking to Assessment Handbook section
- Rewrite activities as scaled-down versions of assessment tasks
- Copy success criteria from rubric, not invent new ones

---

### 3. Lecture-Quiz Validator

**What it checks:** Quiz questions test concepts actually taught in the lecture.

**Analysis method:**
- Extracts lecture concepts (headings, bolded terms, frameworks)
- Checks each quiz question against lecture content
- Flags questions testing untaught material

**Severity levels:**
- **CRITICAL**: Question tests concept NOT in lecture
- **WARNING**: Question tests detail only briefly mentioned

**Fix guidance:**
- Add missing content to lecture
- Or move question to appropriate week
- Or rewrite question to test covered content

---

### 4. Framework Scaffolding Validator

**What it checks:** Frameworks/models are introduced before being referenced.

**Rules:**
- Lectures can forward-reference (SUGGESTION level)
- Tutorials/quizzes cannot use un-introduced frameworks (CRITICAL)
- Tracks: Pyramid Principle, SCQA, Shannon-Weaver, Hofstede, etc.

**Common issues:**
- Quiz asking about framework not yet taught
- Tutorial referencing model from future week
- Framework used throughout but never formally defined

**Fix guidance:**
- Add framework introduction to earlier lecture
- Or move reference to later week
- Add forward-reference if previewing ("We'll explore X in Week 5")

---

## Phase 2 Validators (Quality Checks)

### 5. Learning Objective Coverage Validator

**What it checks:** All stated LOs are covered in lectures AND assessed.

**Extracts LOs from syllabus, then checks:**
1. Content coverage (in lectures)
2. Assessment coverage (in assignments/quizzes)

**Status levels:**
- COVERED / PARTIALLY_COVERED / NOT_COVERED
- ASSESSED / PARTIALLY_ASSESSED / NOT_ASSESSED

**Fix guidance:**
- Add lecture content for uncovered LOs
- Add assessment targeting unassessed LOs
- Expand partial coverage

---

### 6. Rubric Specificity Validator

**What it checks:** Rubric criteria are specific, measurable, actionable.

**Pattern checks for vague phrases:**
- "appropriate", "adequate", "sufficient"
- "good", "excellent", "acceptable"
- "demonstrates understanding", "shows knowledge"

**Claude analyzes for:**
1. **Specificity** - Not vague descriptors
2. **Measurability** - Can students verify achievement?
3. **Differentiation** - Are levels clearly distinguished?
4. **Actionability** - Does it tell students HOW to succeed?

**Bad example:**
> "Good organization" / "Demonstrates understanding"

**Good example:**
> "Pyramid structure with main point in first paragraph"
> "Correctly identifies 3+ stakeholders using Freeman's categories"

---

### 7. Terminology Validator

**What it checks:** Same terms used consistently across all weeks.

**Process:**
1. Collects all bolded terms from lectures/tutorials/quizzes
2. Normalizes and groups similar terms
3. Flags groups with multiple surface forms
4. Uses Claude to determine if genuinely inconsistent

**Example issues:**
- "Pyramid Principle" vs "Minto Pyramid" vs "The Pyramid Method"
- "SCQA" vs "Situation-Complication-Question-Answer"
- Inconsistent capitalization of technical terms

---

### 8. Cultural Sensitivity & ESL Validator

**What it checks:** Content appropriate for Vietnamese ESL students.

**Pattern checks:**
- Complex idioms ("hit the ground running", "low-hanging fruit")
- Western-specific references (Thanksgiving, Super Bowl)
- Very long sentences (40+ words)
- High passive voice density

**Claude analyzes for:**
1. **Cultural assumptions** - Western norms as universal
2. **ESL barriers** - Unnecessarily complex vocabulary
3. **Example diversity** - All Western names/companies
4. **Implicit bias** - Gendered language, stereotypes

---

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **CRITICAL** | Must fix before course delivery | Blocks validation pass |
| **WARNING** | Should fix, may cause student confusion | Review and fix |
| **SUGGESTION** | Nice to have improvement | Consider fixing |
| **INFO** | Informational only | No action needed |

---

## Integration with Workflow

Validation is step 5 in the standard workflow:

```
1. /new-course [CODE] [Name]
2. /generate-syllabus
3. /generate-handbook [CODE]       ← Assessment Handbook FIRST
4. /generate-course [CODE]
5. /validate-content [CODE]        ← AI validation
6. /enhance-coherence [CODE]       ← Fix issues THEN polish
7. /finalize-slides [CODE] [N]
```

**Why before coherence:** Fix structural/alignment issues before spending time on polish.

---

## Programmatic Usage

```python
from tools.content_validators import (
    BloomLevelValidator,
    ValidationReport,
    IssueSeverity
)

# Run single validator
validator = BloomLevelValidator()
result = validator.validate(Path("courses/BCI2AU-business-communication"))

# Check results
if not result.passed:
    for issue in result.issues:
        if issue.severity == IssueSeverity.CRITICAL:
            print(f"CRITICAL: {issue.message}")
            print(f"  Location: {issue.location}")
            print(f"  Fix: {issue.suggestion}")
```

---

## Extending Validators

To add a new validator:

1. Create `tools/content_validators/my_validator.py`
2. Inherit from `BaseValidator`
3. Implement `name`, `description` properties
4. Implement `validate(course_path)` method
5. Add to `__init__.py` exports
6. Add to CLI `VALIDATOR_MAP`

```python
from .base import BaseValidator, ValidationResult, ValidationIssue, IssueSeverity

class MyValidator(BaseValidator):
    @property
    def name(self) -> str:
        return "My Validator"

    @property
    def description(self) -> str:
        return "Checks for something specific"

    def validate(self, course_path: Path, **kwargs) -> ValidationResult:
        issues = []
        # ... validation logic ...
        # Use self._call_claude(prompt) for AI analysis
        return ValidationResult(
            validator_name=self.name,
            passed=len([i for i in issues if i.severity == IssueSeverity.CRITICAL]) == 0,
            issues=issues,
            summary="Checked X items",
            duration_seconds=duration,
            items_checked=count
        )
```

---

## Cost Considerations

Each validator makes Claude API calls. Approximate costs per course:

| Validator | API Calls | Est. Tokens |
|-----------|-----------|-------------|
| Bloom's Level | 1 per week with quizzes | ~1000/call |
| Tutorial-Assessment | 1 per week | ~1500/call |
| Lecture-Quiz | 1 per week | ~2000/call |
| Framework Scaffolding | 1 per flagged issue | ~500/call |
| Learning Objectives | 1 per course | ~3000 |
| Rubric | 1 per rubric | ~1500/call |
| Terminology | 1 per term group | ~500/call |
| Cultural | 1 per lecture | ~1500/call |

**Estimated total for 10-week course:** ~50-80 API calls, ~50K-100K tokens

---

## Troubleshooting

### "ANTHROPIC_API_KEY not found" (Python CLI only)
The Python CLI requires: `export ANTHROPIC_API_KEY=sk-ant-...`
Use `/validate-content` command instead to avoid this.

### "Assessment Handbook not found"
Run `/generate-handbook [CODE]` before validation.

### "No learning objectives found"
Ensure syllabus has numbered LO list with bolded verbs:
```
1. **Analyze** business communication...
2. **Apply** frameworks to...
```

### Validator taking too long
- Use `--phase1` for critical checks only
- Use `--validator X` for specific check
- Large courses (15+ weeks) may take 5-10 minutes
