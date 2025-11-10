# Class Content Generator - Claude Code Workflows

This document describes workflows for generating world-class university course content using Claude Code with strict research validation and assessment alignment.

---

## Table of Contents

1. [Documentation Reference](#documentation-reference)
2. [Overview & Philosophy](#overview--philosophy)
3. [File Organization Rules](#file-organization-rules)
4. [Quick Start Guide](#quick-start-guide)
5. [Slash Commands Reference](#slash-commands-reference)
6. [Core Workflows](#core-workflows)
7. [Research & Validation Process](#research--validation-process)
8. [Quality Standards](#quality-standards)
9. [File Structure](#file-structure)
10. [Best Practices](#best-practices)

---

## Documentation Reference

### Quick Links by Purpose

**Getting Started:**
- **[README.md](../README.md)** - Project overview and quick start (5 minutes)
- **This document** - Complete course development workflows

**Creating Content:**
- **[lecture_content_instructions.md](../lecture_content_instructions.md)** - Lecture & tutorial generation rules
- **[docs/SLIDE-LAYOUTS.md](../docs/SLIDE-LAYOUTS.md)** - All 18 slide layouts with examples

**Technical Reference:**
- **[docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md)** - Converter architecture and design patterns
- **[docs/VALIDATION-GUIDE.md](../docs/VALIDATION-GUIDE.md)** - Quality checks and troubleshooting
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Development guidelines and code standards

**Complete Documentation Map:**
- **[docs/INDEX.md](../docs/INDEX.md)** - Central index of all documentation

### Documentation by Task

| I want to... | Primary Document | Time |
|--------------|------------------|------|
| **Understand the system** | [README.md](../README.md) | 5 min |
| **Create a new course** | [Slash Commands Reference](#slash-commands-reference) (this doc) | - |
| **Generate lecture content** | [lecture_content_instructions.md](../lecture_content_instructions.md) | - |
| **Choose slide layouts** | [docs/SLIDE-LAYOUTS.md](../docs/SLIDE-LAYOUTS.md) | - |
| **Research articles** | [Research & Validation Process](#research--validation-process) (this doc) | 30-50 min |
| **Troubleshoot slides** | [docs/VALIDATION-GUIDE.md](../docs/VALIDATION-GUIDE.md) | - |
| **Contribute code** | [CONTRIBUTING.md](../CONTRIBUTING.md) | - |
| **Understand architecture** | [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) | - |

---

## Overview & Philosophy

### Purpose

Generate comprehensive university course materials that:
- Are backed by research from top management schools (HBS, Stanford GSB, Wharton, MIT Sloan)
- Include only validated, openly accessible academic articles
- Align all content (lectures, tutorials, assessments) for student success
- Follow evidence-based pedagogical practices
- Maintain professional standards across all courses

### Core Principles

**1. Syllabus-First Approach**
- Create complete syllabus before generating weekly content
- Extract assessment schedule to drive tutorial alignment
- Use syllabus as single source of truth

**2. Strict Content Validation**
- Required articles must cover ALL key concepts (no partial matches)
- 4-stage research process ensures quality
- Only openly accessible articles (no paywalls)

**3. Assessment Alignment**
- Every tutorial directly prepares for specific graded work
- Rubrics introduced early and practiced throughout
- Students know exactly what they'll be graded on

**4. Research-Backed Content**
- Learn from top management schools
- Current examples (2023-2025)
- Peer-reviewed or top-tier practitioner sources only

**5. Quality Over Speed**
- Better to spend time finding perfect articles than settle
- Thorough validation ensures complete concept coverage
- World-class standards maintained across all courses

---

## File Organization Rules

**When creating files during workflows, follow these placement rules:**

- **Documentation** → `docs/` (technical guides, architecture, design references)
- **Development tools** → `tools/` (analysis scripts, utilities)
- **Converter handlers** → `html_to_pptx/handlers/` (new slide type handlers)
- **Sample files** → `samples/` (test HTML, demo PPTX files)
- **Generated courses** → `courses/[COURSE-CODE]/` (syllabus, weeks, assessments)
- **Root** → README, CONTRIBUTING, main scripts only

**Never create:** Test files, temporary files, or documentation in root directory.

---

## Quick Start Guide

### For a New Course

**Step 1: Create Course Structure**
```
/new-course [COURSE-CODE] [Course Name]
```
Creates complete directory structure with placeholders.

**Step 2: Generate Syllabus**
```
/generate-syllabus
```
Interactive process to create research-backed syllabus (3-4 hours for 10-week course).

**Step 3: Generate Weekly Content**
```
/generate-week [week-number]
```
Creates lecture and tutorial content for specific week (45-70 minutes per week).

**Step 4: Create Presentation Slides** (after content approval)
```
/export-slides [week-number]
```
Converts lecture content to presentation format.

### For Research Tasks

**Research Articles for Topic**
```
/research-topic "[Topic Name]" "[key concepts required]"
```
30-50 minutes for thorough, validated research.

**Validate Specific Article**
```
/validate-article-content [URL] "[key concepts]"
```
2-10 minutes for quick or detailed validation.

---

## Slash Commands Reference

### `/new-course [COURSE-CODE] [Course Name]`

**Purpose:** Scaffold complete course directory structure

**Usage:**
```
/new-course BUS101 Business Communication
```

**Creates:**
- Course folder with organized subdirectories
- Rubric templates
- Week folders with placeholders
- Course info and assessment schedule templates

**Time:** 2-3 minutes

**Next step:** Run `/generate-syllabus`

---

### `/generate-syllabus`

**Purpose:** Create comprehensive, research-backed course syllabus

**Interactive Process:**
1. Course basics + **research-backed course description**
   - Institution information (university, qualification, campus)
   - Course code, title, semester, weeks
   - Research top schools for course descriptions
   - Synthesize purpose, content, value proposition
   - Optional: Reference user-provided sample documents
2. Learning objectives (4 categories following Bloom's Taxonomy)
3. Assessment structure (portfolio+presentation+quiz or exam+project+quiz)
4. Course calendar with 4-stage article research per week
5. Rubric selection and customization
6. Final assembly and quality check

**Article Research (per week):**
- Stage 1: Discovery (10-15 candidates)
- Stage 2: Quick filter (5-6 accessible candidates)
- Stage 3: Content validation (2-3 finalists that cover ALL concepts)
- Stage 4: User selection (final 2 articles)

**Document Structure Options:**

During generation (Step 5.5), you'll choose between:

1. **Single Document** (Traditional):
   - All content in one syllabus.md file
   - All rubrics embedded inline
   - Best for: Simple courses with 2-3 assessments

2. **Two-Document Structure** (Recommended for Complex Courses):
   - **syllabus.md** (15-20 pages): Overview with course calendar, brief assessment descriptions, cross-references
   - **assessment-handbook.md** (25-40 pages): Complete instructions and rubrics for all assessments
   - Best for: Courses with 3+ assessments, detailed rubrics, complex requirements
   - Benefits: Syllabus remains scannable; handbook provides depth when needed

**Outputs:**

**Always created:**
- Complete syllabus saved to `courses/[COURSE-CODE]/syllabus.md`
- Research notes saved to `.working/research/`:
  - `course-description-research.md`
  - `learning-objectives-research.md`
  - `article-research-summary.md`

**If two-document structure chosen:**
- Also creates `courses/[COURSE-CODE]/assessment-handbook.md` with all detailed assessment information

**Time:** 3-4 hours for 10-week course (intensive but thorough)

**Next step:** Run `/generate-week [N]` for each week

---

### `/research-topic "[Topic]" "[Key Concepts]"`

**Purpose:** Standalone article research with strict validation

**Usage:**
```
/research-topic "Persuasive Communication" "Cialdini's principles, message structure, ethics, objections"
```

**4-Stage Process:**
1. **Discovery:** Search top schools + academic + practitioner sources (10-15 candidates)
2. **Quick Filter:** Check accessibility, quality, relevance (5-6 candidates)
3. **Content Validation:** Deep analysis against required concepts (2-3 finalists)
4. **Present Finalists:** Show content match analysis, user selects 2

**Validation Criteria:**
- ALL required concepts must be found
- ALL concepts have "Explained" or "In-depth" coverage
- Article is openly accessible (no paywall)

**Outputs:**
- 2-3 finalist articles with content match analysis
- Research documentation saved
- Formatted citations ready for syllabus

**Time:** 30-50 minutes per topic

---

### `/validate-article-content [URL] "[Key Concepts]"`

**Purpose:** Quick validation of specific article against required concepts

**Usage:**
```
/validate-article-content "https://hbr.org/article" "concept1, concept2, concept3"
```

**Process:**
1. Fetch article content
2. Extract frameworks and concepts covered
3. Validate against each required concept
4. Apply strict pass/fail criteria
5. Generate detailed or quick validation report

**Pass Criteria:**
- ✓ Every required concept found in article
- ✓ Every concept has minimum "Explained" depth
- ✓ Definitions and examples provided
- ✓ Article openly accessible

**Outputs:**
- PASS/FAIL decision with detailed reasoning
- Content mapping showing where each concept is covered
- Recommendations for next steps

**Time:** 2-10 minutes (quick or detailed)

---

### `/generate-week [week-number]`

**Purpose:** Generate complete weekly content (lecture + tutorial)

**Usage:**
```
/generate-week 3
```

**Prerequisites:**
- Syllabus must exist with weekly topics
- Assessment details documented (in assessment-handbook.md or syllabus/assessments folder)

**Document Structure Awareness:**
The command automatically detects and adapts to course structure:
- **Two-document**: Reads syllabus.md + assessment-handbook.md
- **Single-document**: Reads syllabus.md + assessments/ folder
- Tutorial content references correct document based on structure

**Generates:**

**1. Lecture Content (22-30 slides):**
- Opening (4-6 slides): Hook, objectives, assessment connection
- Core content (14-20 slides): 3-4 segments, theory→example→application
- Wrap-up (4-6 slides): Synthesis, tutorial preview, assessment bridge
- Speaker notes adapted to slide type
- Current examples with full citations

**2. Tutorial Content (90 minutes):**
- Opening (10 min): Quick review, assessment preview, simplified rubric
  - References: "See Assessment Handbook Section X" (or syllabus if single-doc)
- Main activity (55-60 min): ONE activity that mirrors actual assessment
  - Pulls criteria from assessment-handbook.md or rubrics folder
  - Includes references to where students find complete requirements
- Quiz prep (15-20 min): 5-8 practice questions
- Wrap-up (5-10 min): Self-assessment, next steps

**Assessment Alignment Logic:**
- Checks assessment-handbook.md (or assessment schedule if legacy) for due dates
- Extracts full rubric criteria from appropriate document
- Designs tutorial activity to practice exact assessment skills
- Uses simplified version (3-4 key criteria) of actual grading rubric
- Includes clear references to where students find complete rubrics

**Outputs:**
- `weeks/week-[N]/lecture-content.md`
- `weeks/week-[N]/tutorial-content.md`
- Updated course tracking

**Time:** 45-70 minutes per week

**Next step:** Review content, then `/export-slides [N]`

---

## Core Workflows

### Workflow 1: Complete Course Development

**Timeline: 5-7 days for 10-week course**

```
Day 1: Course Setup & Syllabus Structure
├─ /new-course [CODE] [Name]                    (5 min)
├─ /generate-syllabus - Steps 1-3               (30 min)
└─ Define learning objectives & assessments

Days 2-3: Syllabus Research (Most intensive)
├─ /generate-syllabus - Step 4 (Week 1-5)      (2.5 hrs)
│  └─ 4-stage research per week
└─ /generate-syllabus - Step 4 (Week 6-10)     (2.5 hrs)

Day 3: Syllabus Completion
├─ /generate-syllabus - Steps 5-6              (30 min)
└─ Review and finalize syllabus

Days 4-6: Weekly Content Generation
├─ /generate-week 1                             (60 min)
├─ /generate-week 2                             (60 min)
├─ /generate-week 3                             (60 min)
└─ ... continue for all weeks

Day 7: Slides & Final Review
├─ /export-slides for each week
└─ Final quality check across all materials
```

---

### Workflow 2: Syllabus-First Content Generation

**The recommended workflow:**

```
1. CREATE STRUCTURE
   └─ /new-course [CODE] [Name]

2. BUILD SYLLABUS (syllabus-first!)
   ├─ Define course basics
   ├─ Structure assessments
   ├─ Research articles for each week (4-stage validation)
   └─ Complete full syllabus before weekly content

3. GENERATE WEEKLY CONTENT
   ├─ Syllabus drives lecture topics
   ├─ Assessment schedule drives tutorial focus
   └─ /generate-week for each week sequentially

4. CREATE SLIDES
   └─ After lecture content is approved

5. ITERATE & IMPROVE
   └─ Update syllabus if needed, regenerate affected weeks
```

**Why syllabus-first?**
- Assessment schedule drives tutorial alignment
- Article research completed once, referenced throughout
- Consistent structure across all weeks
- Clear roadmap for content generation

---

### Workflow 3: Article Research & Validation

**The 4-Stage Research Process:**

```
STAGE 1: DISCOVERY (Cast Wide Net)
├─ Search top schools: HBS, Stanford GSB, Wharton, MIT Sloan
├─ Search academic: Google Scholar, peer-reviewed journals
├─ Search practitioner: HBR, MIT Sloan Review
└─ Result: 10-15 candidate articles

STAGE 2: QUICK FILTER (Reduce to Quality Candidates)
├─ Check accessibility (WebFetch each URL)
├─ Verify no paywall (STRICT)
├─ Review title + abstract for relevance
├─ Check publication quality & date
└─ Result: 5-6 accessible, high-quality candidates

STAGE 3: CONTENT VALIDATION (Deep Analysis)
├─ WebFetch full article content
├─ AI extraction of frameworks/concepts covered
├─ Validate EACH required concept:
│  ├─ Found? YES/NO
│  ├─ Coverage depth? Mentioned/Explained/In-depth
│  └─ STRICT: ALL concepts must be "Explained" or "In-depth"
├─ Reject if ANY concept missing or insufficient
└─ Result: 2-3 finalists that pass ALL validation

STAGE 4: PRESENT & SELECT
├─ Show content match analysis for each finalist
├─ Explain what each article covers and how
├─ User selects final 2 (ideally 1 theoretical + 1 applied)
└─ Result: 2 perfect articles with validated coverage
```

**Key Principle:** Better to spend extra time finding perfect articles than to settle for incomplete coverage.

---

## Research & Validation Process

### Web Research Sources

**Top Management Schools:**
```
site:hbs.edu [topic] syllabus
site:gsb.stanford.edu [topic] MBA course
site:wharton.upenn.edu [topic] syllabus
site:mitsloan.mit.edu [topic] course
```

**Academic Sources:**
```
[key concept] seminal article
[topic] peer reviewed highly cited
[concept] research article 2020..2025
```

**Practitioner Sources:**
```
site:hbr.org [topic]
site:sloanreview.mit.edu [topic]
[topic] Harvard Business Review
```

**Open Access:**
```
[concept] open access
[author] [topic] ResearchGate
[topic] arXiv / SSRN
```

### Content Validation Checklist

For each required concept:

```
□ Concept found in article? (YES/NO)
□ Coverage depth?
   □ Only mentioned (1-2 sentences) → INSUFFICIENT
   □ Explained (paragraph, defines concept) → ACCEPTABLE
   □ In-depth (multiple paragraphs, examples) → EXCELLENT
□ Definitions provided? (YES/NO)
□ Examples or applications included? (YES/NO)
□ Specific section(s): [Location in article]

VALIDATION RESULT:
- All concepts "Explained" or "In-depth"? → PASS
- Any concept missing or "Mentioned" only? → REJECT
```

### Accessibility Verification

**STRICT REQUIREMENT:** Articles must be openly accessible

```
✓ ACCEPTABLE:
- Freely available on publisher website
- Open access journal articles
- HBR articles (openly accessible)
- Author's website or ResearchGate versions
- Institutional repositories

✗ REJECT:
- Paywalled content
- Requires subscription
- Requires institutional login
- Abstract-only access
```

**Fallback strategies if paywall:**
1. Search for author's preprint (ResearchGate, personal website)
2. Look for open-access version on Google Scholar
3. Check institutional repositories
4. Find similar alternative that IS openly accessible
5. Check SSRN, arXiv, or discipline-specific repositories

---

## Quality Standards

### Lecture Content Quality

**Structure:**
- [ ] 22-30 content slides total
- [ ] Opening (4-6 slides) with hook, objectives, assessment connection
- [ ] Core content (14-20 slides) in 3-4 logical segments
- [ ] Wrap-up (4-6 slides) with synthesis and preview

**Citations & Research:**
- [ ] 3-5 verified sources minimum
- [ ] Inline citations for all statistics/research/frameworks (Author, Year)
- [ ] Full APA 7th references with DOI/URL after each slide
- [ ] Current examples (2023-2025)
- [ ] Vietnam-specific applications when relevant

**Pedagogical Quality:**
- [ ] Learning objectives clearly stated (3-5)
- [ ] Direct assessment connection explicit
- [ ] Engagement activities every 15-20 minutes
- [ ] Examples culturally diverse
- [ ] Speaker notes adapted to slide type

### Tutorial Content Quality

**Assessment Alignment:**
- [ ] ONE main activity directly mirrors actual assessment
- [ ] Simplified rubric provided (3-4 key criteria)
- [ ] Rubric language used in peer review
- [ ] Clear connection to upcoming graded work stated

**Structure:**
- [ ] Opening (10 min): Review, assessment preview, rubric
- [ ] Main activity (55-60 min): Setup, work, peer review, revision, debrief
- [ ] Quiz prep (15-20 min): 5-8 questions with review
- [ ] Wrap-up (5-10 min): Self-assessment, next steps

**Student Support:**
- [ ] Clear, numbered instructions
- [ ] Peer review sentence starters provided
- [ ] Cultural considerations for Vietnamese students
- [ ] Differentiation for struggling/advanced students

### Article Quality Standards

**Source Quality:**
- Peer-reviewed journals (top-tier preferred)
- Harvard Business Review, MIT Sloan Management Review
- Top management school publications
- Highly cited works (100+ citations for older works)

**Content Quality:**
- Covers ALL required key concepts (strict validation)
- Provides definitions and explanations
- Includes practical examples or applications
- Current or seminal (recent relevance proven)

**Accessibility:**
- Openly accessible without paywall (STRICT)
- Full text available (not just abstract)
- Verified URL working

---

## File Structure

```
class_content_generator/
├── .claude/
│   ├── commands/
│   │   ├── new-course.md
│   │   ├── generate-syllabus.md
│   │   ├── generate-week.md
│   │   ├── research-topic.md
│   │   └── validate-article-content.md
│   ├── CLAUDE.md (this file)
│   └── WORKING-DOCS-SYSTEM.md
│
├── templates/
│   ├── syllabus-base-template.md
│   ├── week-topic-specification.md
│   ├── syllabus-components/
│   │   ├── assessment-structures/
│   │   │   ├── portfolio-presentation-quiz.md
│   │   │   └── exam-project-quiz.md
│   │   └── rubric-structures/
│   │       ├── written-work-rubric.md
│   │       ├── presentation-rubric.md
│   │       └── project-rubric.md
│   └── research/
│
├── courses/
│   └── [COURSE-CODE]-[course-name]/
│       ├── .working/              # In-progress documents (hidden)
│       │   ├── course-info.md
│       │   ├── progress-summary.md
│       │   ├── syllabus-DRAFT.md
│       │   └── research/
│       │       ├── course-description-research.md
│       │       ├── learning-objectives-research.md
│       │       └── article-research-summary.md
│       │
│       ├── .archive/              # Completed documents (hidden)
│       │   ├── [date]-course-info.md
│       │   ├── [date]-syllabus-DRAFT.md
│       │   └── [date]-COMPLETION-REPORT.md
│       │
│       ├── syllabus.md            # FINAL published syllabus (always)
│       ├── assessment-handbook.md # OPTIONAL: Detailed assessment guide (2-doc structure)
│       ├── rubrics/               # OPTIONAL: Used if single-doc structure
│       ├── weeks/
│       │   └── week-[NN]/
│       │       ├── lecture-content.md
│       │       ├── tutorial-content.md
│       │       └── slides.md
│       ├── assessments/
│       │   └── assessment-schedule.md
│       └── resources/
│
├── shared/
│   ├── research/
│   │   ├── [course-topic]/
│   │   │   ├── article-research-summary.md
│   │   │   ├── course-description-research.md
│   │   │   └── learning-objectives-research.md
│   │   └── open-access-sources.md
│   ├── citation-library/
│   ├── vietnam-examples/
│   └── teaching-resources/
│
├── samples/
│   └── BUSINESS COMMUNICATION Syllabus Fall 2025.md
│
├── lecture_content_instructions.md
└── README.md
```

### Working Documents System

**See `.claude/WORKING-DOCS-SYSTEM.md` for complete documentation.**

**Key Principles:**
- `.working/` - In-progress documents created during syllabus generation
- `.archive/` - Completed documents kept for reference/audit trail
- Root level - Only final published deliverables (syllabus, weeks, assessments)

**Benefits:**
- Clean course directories (only finals visible)
- Recovery support (progress tracking if interrupted)
- Audit trail (research decisions documented)
- Version history (archive maintains evolution)

---

## Best Practices

### Research Best Practices

**1. Document Everything**
- Save research notes for transparency
- Track articles considered and why they passed/failed
- Create audit trail for quality assurance

**2. Be Strict with Validation**
- Never accept partial matches
- All required concepts must be fully covered
- If in doubt, REJECT and find better article

**3. Prioritize Accessibility**
- Students cannot learn from articles they cannot access
- Always verify URLs before including in syllabus
- Find open-access alternatives to paywalled content

**4. Learn from Top Schools**
- Research what HBS, Stanford, Wharton, MIT Sloan teach
- Extract best practices and innovative approaches
- Adapt to your context while maintaining quality

### Content Generation Best Practices

**1. Choose the Right Document Structure**

Use **Single Document** when:
- Course has 2-3 simple assessments
- Rubrics are short (1-2 pages each)
- All instructions can be explained briefly
- Total syllabus would be under 25 pages

Use **Two-Document Structure** when:
- Course has 3+ assessments
- Rubrics are detailed (2+ pages each)
- Complex requirements need extensive explanation
- Want syllabus to remain scannable overview
- Total content would exceed 30 pages

**Benefits of Two-Document Approach:**
- Syllabus stays 15-20 pages (quick reference for schedule/policies)
- Assessment Handbook provides depth (25-40 pages of detailed how-to)
- Clear separation: syllabus = "what/when", handbook = "how"
- Referential integrity through cross-references
- Students can focus on relevant sections as needed

**2. Syllabus First, Always**
- Complete syllabus before weekly content
- Let assessment schedule drive tutorial design
- Use syllabus as single source of truth

**3. Assessment Alignment is Critical**
- Every tutorial must prepare for specific graded work
- Practice with actual rubric criteria
- Students should never be surprised by assessments

**4. Cultural Adaptation**
- Include Vietnamese and regional examples
- Provide structured peer interaction frameworks
- Build confidence gradually for presentations
- Use local business context when possible

**5. Current + Timeless**
- Balance recent examples (2023-2025) with seminal works
- Update statistics and case studies regularly
- Classic frameworks with modern applications

### Quality Assurance

**Before Finalizing Syllabus:**
- [ ] Every week has 2 validated articles
- [ ] All URLs verified accessible
- [ ] Assessment structure complete with due dates
- [ ] Rubrics appropriate for all assessments
- [ ] Professional formatting throughout

**Before Releasing Weekly Content:**
- [ ] Lecture meets 22-30 slide requirement
- [ ] All sources properly cited with DOI/URLs
- [ ] Tutorial directly practices assessment skills
- [ ] Quiz prep questions align with quiz format
- [ ] Cultural adaptations included

**Periodic Review:**
- [ ] Check article URLs quarterly (links break)
- [ ] Update examples annually (keep current)
- [ ] Gather student feedback on materials
- [ ] Refine based on assessment results

---

## Coding Standards & Architecture

### Overview

All code in this project must follow SOLID principles, Python best practices (PEP 8), and maintain high quality standards. This section applies to **all Python code**, including:
- HTML to PPTX converter
- Content generation scripts
- Utilities and helpers
- Custom tools

### Core Principles

**1. SOLID Principles**
- **Single Responsibility:** Each class/function has one clear purpose
- **Open/Closed:** Open for extension (plugins), closed for modification
- **Liskov Substitution:** Subclasses fully interchangeable with base classes
- **Interface Segregation:** Small, focused interfaces
- **Dependency Inversion:** Depend on abstractions, not implementations

**2. DRY (Don't Repeat Yourself)**
- No duplicate code - extract to functions/classes
- No duplicate constants - use configuration
- No duplicate logic - use inheritance or composition

**3. Clean Code Principles**
- Descriptive names (no `x`, `y` - use `x_position`, `y_position`)
- Short functions (max 50 lines)
- Short files (max 500 lines - split into modules)
- Clear comments for non-obvious code
- Type hints on all functions
- Docstrings on all public methods

### File Organization

**Monolithic Files Are Not Acceptable**
- ✗ Single 3000+ line file
- ✓ Modular structure with focused files

**Proper Structure:**
```
project/
├── main_script.py           # CLI entry point (~200 lines max)
├── module_name/
│   ├── __init__.py
│   ├── core.py              # Main orchestrator (~300 lines max)
│   ├── parser.py            # Parsing logic (~400 lines max)
│   ├── config.py            # Configuration & constants
│   └── utils.py             # Utility functions
├── handlers/
│   ├── __init__.py
│   ├── base_handler.py      # Abstract base class
│   └── specific_handler.py  # Concrete implementations
└── tests/
    ├── test_parser.py
    └── test_handlers.py
```

### Constants & Configuration

**Magic Numbers Are Forbidden**
```python
# ✗ BAD: Magic numbers
y_start = 1.9
font_size = Pt(36)
gap = 0.57

# ✓ GOOD: Semantic constants
y_start = LayoutConfig.CONTENT_START_Y
font_size = FontConfig.TITLE_SIZE
gap = LayoutConfig.TITLE_CONTENT_GAP
```

**Configuration Classes:**
```python
class LayoutConfig:
    """Layout dimensions and spacing constants (all in inches)"""
    PADDING = 0.5
    TITLE_HEIGHT = 0.7
    TITLE_CONTENT_GAP = 0.6
    CONTENT_START_Y = PADDING + TITLE_HEIGHT + TITLE_CONTENT_GAP  # 1.9

class FontConfig:
    """Font sizes and families"""
    HEADER_FONT = 'Cal Sans'
    BODY_FONT = 'Plus Jakarta Sans'
    TITLE_SIZE = Pt(36)
    BODY_SIZE = Pt(14)
    BIG_NUMBER_SIZE = Pt(135)

class ColorConfig:
    """Semantic color names"""
    PRIMARY_TEXT = RGBColor(19, 19, 19)      # Dark gray
    ACCENT = RGBColor(237, 94, 41)            # Orange
    BACKGROUND_LIGHT = RGBColor(244, 243, 241) # Cream
    BACKGROUND_DARK = RGBColor(19, 19, 19)    # Dark
```

### Type Hints & Documentation

**All Functions Must Have:**
1. Type hints for parameters and return values
2. Docstring explaining purpose, args, returns
3. Examples for complex functions

```python
from typing import Optional, List, Dict, Tuple
from lxml import etree
from pptx.shapes.base import BaseShape

def create_text_box(
    slide: Any,  # pptx slide object
    x: float,
    y: float,
    width: float,
    height: float,
    text: str,
    font_size: Pt,
    color: RGBColor
) -> BaseShape:
    """
    Create a text box at specified position with styling.

    Args:
        slide: PowerPoint slide object to add text box to
        x: X position in inches from left edge
        y: Y position in inches from top edge
        width: Text box width in inches
        height: Text box height in inches
        text: Text content to display
        font_size: Font size as Pt object
        color: Text color as RGBColor object

    Returns:
        Created text box shape object

    Example:
        >>> title_box = create_text_box(
        ...     slide, 0.5, 0.5, 9.0, 0.7,
        ...     "My Title", Pt(36), ColorConfig.PRIMARY_TEXT
        ... )
    """
    # Implementation...
```

### Error Handling

**Custom Exceptions for Domain Errors:**
```python
class SlideConversionError(Exception):
    """Raised when slide conversion fails"""
    pass

class CSSParseError(Exception):
    """Raised when CSS parsing fails"""
    pass

class LayoutError(Exception):
    """Raised when layout calculation fails"""
    pass
```

**Proper Error Context:**
```python
# ✗ BAD: Generic errors with no context
raise Exception("Error")

# ✓ GOOD: Specific errors with context
raise CSSParseError(
    f"Failed to parse CSS rule: {rule_text}\n"
    f"Expected format: '.class {{ property: value; }}'"
)
```

### Testing Requirements

**All New Code Must Include Tests**
```python
# tests/test_css_parser.py
import pytest
from converters.css_parser import CSSStyleParser

def test_parse_color_hex():
    parser = CSSStyleParser()
    color = parser.parse_color('#ed5e29')
    assert color.red == 237
    assert color.green == 94
    assert color.blue == 41

def test_parse_color_with_css_var():
    parser = CSSStyleParser()
    parser.css_vars['--color-accent'] = '#ed5e29'
    color = parser.parse_color('var(--color-accent)')
    assert color == parser.parse_color('#ed5e29')
```

**Test Coverage Requirements:**
- New modules: 80%+ coverage
- Critical paths: 100% coverage
- All public APIs: Tested with examples

### Code Review Checklist

Before committing any code, verify:

**Structure:**
- [ ] No file over 500 lines
- [ ] No function over 50 lines
- [ ] No code duplication (DRY)
- [ ] Proper module organization

**Quality:**
- [ ] All functions have type hints
- [ ] All public methods have docstrings
- [ ] No magic numbers (all in config)
- [ ] Descriptive variable names
- [ ] PEP 8 compliant

**Testing:**
- [ ] Unit tests written
- [ ] Tests pass
- [ ] Edge cases covered
- [ ] Error cases tested

**Documentation:**
- [ ] README updated if needed
- [ ] CLAUDE.md updated if workflow changes
- [ ] Code comments for complex logic

### Refactoring Guidelines

**When to Refactor:**
- File exceeds 500 lines
- Function exceeds 50 lines
- Code duplicated 3+ times
- Magic numbers appear
- Adding new feature requires modifying existing code (not extending)

**How to Refactor:**
1. **Extract Method:** Pull out repeated code
2. **Extract Class:** Group related functions
3. **Extract Module:** Separate concerns
4. **Introduce Constants:** Replace magic numbers
5. **Use Design Patterns:** Factory, Strategy, Template Method as appropriate

**Refactoring Process:**
1. Create git branch: `refactor/description`
2. Create refactoring plan document
3. Keep existing tests passing (green)
4. Refactor one thing at a time
5. Commit after each successful change
6. Merge when complete and tested

### Current Refactoring Status

**HTML to PPTX Converter:**
- **Status:** Active refactoring in progress (see `REFACTORING_PLAN.md`)
- **Timeline:** 5 days (Jan 11-15, 2025)
- **Goal:** Transform 3200-line monolith into modular architecture
- **Progress:** See todo list in refactoring plan

**Future Modules:**
- Content generation scripts: Apply same standards
- Research validation tools: Follow patterns from refactored converter
- Any new Python code: Start with proper structure from day 1

---

## Troubleshooting

### "Cannot find articles covering all concepts"

**Solutions:**
1. Search for each concept individually first
2. Look for review articles or meta-analyses
3. Check if concepts known by alternative names
4. Consider using 3 articles instead of 2 (with user approval)
5. Ask user if alternative concepts would work

### "All good articles are paywalled"

**Solutions:**
1. Search for author's preprint versions
2. Check ResearchGate and Academia.edu
3. Look for institutional repository versions
4. Search for open-access alternatives
5. Use practitioner sources (HBR) which are often open

### "Tutorial activity doesn't align with assessment"

**Check:**
1. Is assessment schedule up to date?
2. Have assessments changed since syllabus created?
3. Is simplified rubric truly matching full rubric?
4. Can activity be adjusted to better mirror assessment?

### "Week content regeneration needed"

**Process:**
1. Update syllabus first if needed
2. Update assessment schedule if needed
3. Use `/generate-week [N]` to regenerate
4. Review changes carefully before overwriting
5. Update slides if lecture content changed

---

## Support & Resources

**Key Files:**
- This workflow guide: `.claude/CLAUDE.md`
- Working documents system: `.claude/WORKING-DOCS-SYSTEM.md`
- Content instructions: `lecture_content_instructions.md`
- Quick start: `README.md`
- Sample syllabus: `samples/BUSINESS COMMUNICATION Syllabus Fall 2025.md`

**Research Resources:**
- Top schools: HBS, Stanford GSB, Wharton, MIT Sloan
- Practitioner: HBR, MIT Sloan Review
- Academic: Google Scholar, peer-reviewed journals
- Open access: ResearchGate, SSRN, institutional repositories

**Quality Standards:**
- Lecture: 22-30 slides, 3-5 sources, assessment-aligned
- Tutorial: ONE assessment-mirroring activity, simplified rubric
- Articles: ALL concepts covered, openly accessible
- Citations: APA 7th with DOI/URL

---

## Version History

**v1.2** - Two-Document Structure for Complex Courses (January 6, 2025)
- Added Step 5.5 to `/generate-syllabus` command for document structure choice
- Introduced two-document structure option:
  - syllabus.md (15-20 pages): Overview with course calendar and brief descriptions
  - assessment-handbook.md (25-40 pages): Complete assessment instructions and rubrics
- Updated CLAUDE.md with guidance on when to use each structure
- Added cross-referencing pattern for referential integrity
- Quality checklist updated to verify cross-references
- File structure updated to show assessment-handbook.md as optional

**v1.1** - Working Documents System (January 5, 2025)
- Added `.working/` folder for in-progress documents
- Added `.archive/` folder for completed documents
- Clean course directories (only final deliverables in root)
- Complete documentation in `.claude/WORKING-DOCS-SYSTEM.md`
- Updated file structure in CLAUDE.md

**v1.0** - Initial system with research-enhanced workflows
- 5 slash commands created
- 4-stage research validation process
- Syllabus-first approach
- Strict content matching requirements

---

*For questions or improvements to this workflow, update this document and relevant command files.*
