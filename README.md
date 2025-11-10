# Class Content Generator

A comprehensive system for generating world-class university course materials using Claude Code with research validation and assessment alignment.

## Overview

This system helps you create complete course materials including:
- **Research-backed syllabi** with validated, accessible articles
- **Lecture content** (22-30 slides with speaker notes)
- **Tutorial activities** aligned to assessments
- **Rubrics and assessment materials**
- **Presentation slides**

All content is generated following evidence-based pedagogical practices and validated against top management school standards (Harvard Business School, Stanford GSB, Wharton, MIT Sloan).

## Key Features

### 🔬 Research-Enhanced Syllabus Generation
- 4-stage article validation process
- Only openly accessible, high-quality sources
- Strict content matching (no partial matches)
- Learn from top business schools

### 📚 Complete Course Materials
- Lecture content with citations and examples
- Assessment-aligned tutorials
- Professional rubrics
- Quiz preparation materials

### ✅ Quality Assurance
- Every article covers ALL required concepts
- Accessibility verified (no paywalls)
- Current examples (2023-2025)
- Vietnam-specific adaptations

### 🤖 Automated Workflows
- Slash commands for efficiency
- Syllabus-first approach
- Assessment alignment logic
- Cultural adaptations built-in

## Quick Start

### 1. Create a New Course

```bash
/new-course BUS101 Business Communication
```

This creates the complete directory structure with templates and placeholders.

### 2. Generate Course Syllabus

```bash
/generate-syllabus
```

Interactive process (3-4 hours for 10-week course) that:
- Guides you through course structure
- Researches and validates 2 articles per week
- Learns from top management schools
- Creates professional, comprehensive syllabus

### 3. Generate Weekly Content

```bash
/generate-week 1
```

Creates lecture and tutorial content (45-70 minutes per week) with:
- 22-30 lecture slides with speaker notes
- Assessment-aligned tutorial activities
- Quiz preparation questions
- Current, cited examples

### 4. Create Presentation Slides

```bash
/export-slides 1
```

Converts lecture content to presentation format (after content approval).

## Slash Commands

| Command | Purpose | Time |
|---------|---------|------|
| `/new-course [CODE] [Name]` | Create course structure | 2-3 min |
| `/generate-syllabus` | Build research-backed syllabus | 3-4 hrs |
| `/generate-week [N]` | Create lecture + tutorial content | 45-70 min |
| `/research-topic "[Topic]" "[Concepts]"` | Research articles for topic | 30-50 min |
| `/validate-article-content [URL] "[Concepts]"` | Validate article quality | 2-10 min |

## Project Structure

```
class_content_generator/
├── .claude/
│   ├── commands/          # Slash command definitions
│   └── CLAUDE.md          # Complete workflow documentation
│
├── templates/             # Reusable templates
│   ├── syllabus-base-template.md
│   ├── week-topic-specification.md
│   └── syllabus-components/
│
├── courses/               # Generated course content
│   └── [COURSE-CODE]-[name]/
│       ├── syllabus.md
│       ├── weeks/
│       ├── rubrics/
│       └── assessments/
│
├── shared/                # Shared resources
│   ├── research/          # Research documentation
│   ├── citation-library/  # Reusable citations
│   └── vietnam-examples/  # Local context examples
│
└── lecture_content_instructions.md  # Content generation guide
```

## HTML to PPTX Converter

The `/export-slides` command uses a **modular, handler-based converter** that transforms HTML slides into professional PowerPoint presentations.

### Key Features

- **18 specialized slide layouts** (title, quote, framework, comparison, etc.)
- **Prescriptive layout hints** for guaranteed formatting  
- **Automated validation** of conversion quality
- **Clean architecture** following SOLID principles and Python best practices

### Architecture Highlights

The converter is organized into focused modules:

- **`config.py`** - Configuration constants (layouts, fonts, colors)
- **`css_parser.py`** - CSS parsing with variable resolution
- **`handlers/`** - Slide-type specific rendering logic (Strategy pattern)
- **Automated validation** - Quality checks on every conversion

### Supported Layouts

**Core:** Title, Section Break, Standard Content, Dark Background  
**Data:** Big Number, Stats Banner, Vocabulary Table, Learning Objectives  
**Interactive:** Activity, Checklist, Card Layout  
**Comparison:** 2-Column, Comparison Table  
**Academic:** Quote, References, Framework/Diagram, Reflection Prompt

**Prescriptive Control:** Use layout hints to guarantee formatting:
```markdown
<!-- LAYOUT: quote -->
"Your quote text"
— Attribution
```

### Documentation

- **Quick Reference:** See [docs/SLIDE-LAYOUTS.md](docs/SLIDE-LAYOUTS.md) for all layouts with examples
- **Technical Details:** See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for complete architecture
- **Validation:** See [docs/VALIDATION-GUIDE.md](docs/VALIDATION-GUIDE.md) for quality checks
- **Contributing:** See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines

## Core Principles

### 1. Syllabus-First Approach
Create complete syllabus before generating weekly content. The assessment schedule drives tutorial design, ensuring perfect alignment.

### 2. Strict Content Validation
Articles must cover **ALL** required key concepts. The 4-stage research process ensures:
- Stage 1: Discovery (10-15 candidates)
- Stage 2: Quick filter (5-6 quality candidates)
- Stage 3: Content validation (2-3 finalists)
- Stage 4: User selection (final 2 articles)

### 3. Assessment Alignment
Every tutorial directly prepares students for specific graded work using simplified versions of actual rubrics.

### 4. Quality Sources Only
- Peer-reviewed journals
- Harvard Business Review, MIT Sloan Management Review
- Top management school publications
- Highly cited works
- **Must be openly accessible (no paywalls)**

## Example Workflow

**Creating a complete 10-week course:**

```
Day 1: Setup
  └─ /new-course ECON201 Microeconomic Theory

Days 2-3: Syllabus (Most intensive)
  ├─ /generate-syllabus
  │  ├─ Define basics and structure
  │  └─ Research 2 articles × 10 weeks = 20 articles
  └─ Quality check and finalize

Days 4-6: Weekly Content
  ├─ /generate-week 1
  ├─ /generate-week 2
  └─ ... continue for all weeks

Day 7: Slides and Review
  ├─ /export-slides for each week
  └─ Final quality check
```

**Result:** Complete, professional course ready to teach

## Quality Standards

### Lecture Content ✓
- 22-30 content slides
- 3-5 verified sources with DOI/URLs
- Current examples (2023-2025)
- Assessment connection explicit
- Speaker notes for teaching

### Tutorial Content ✓
- ONE activity mirroring actual assessment
- Simplified rubric (3-4 criteria)
- 5-8 quiz practice questions
- Structured peer review
- Clear time allocations

### Article Selection ✓
- Covers ALL required concepts (strict)
- Openly accessible (verified)
- High-quality source (peer-reviewed or top-tier)
- Current or seminal (relevance proven)

## Research Process

### Sources Prioritized

**Top Management Schools:**
- Harvard Business School
- Stanford Graduate School of Business
- Wharton School
- MIT Sloan

**Peer-Reviewed Journals:**
- Top-tier academic publications
- 100+ citations for older works

**Practitioner Publications:**
- Harvard Business Review
- MIT Sloan Management Review

**All articles must be:**
- Openly accessible (no paywalls)
- Validated for content match
- Current or proven relevant

### 4-Stage Validation

Every article goes through:

1. **Discovery:** Find 10-15 candidates from multiple sources
2. **Quick Filter:** Check accessibility, quality, relevance → 5-6 candidates
3. **Content Validation:** Deep analysis of concept coverage → 2-3 finalists
4. **Selection:** User chooses final 2 with full justification

**Strict Rule:** Article must cover ALL required concepts or it's rejected.

## Documentation

- **Quick Start:** This README
- **Complete Workflows:** `.claude/CLAUDE.md`
- **Content Guidelines:** `lecture_content_instructions.md`
- **Sample Syllabus:** `samples/BUSINESS COMMUNICATION Syllabus Fall 2025.md`

## Assessment Alignment

Tutorials are designed using backward design:

```
Upcoming Assessment
    ↓
Extract Rubric Criteria
    ↓
Simplify to 3-4 Key Criteria
    ↓
Design Tutorial Activity that Mirrors Assessment
    ↓
Students Practice with Rubric
    ↓
Peer Review Using Rubric Language
    ↓
Students Ready for Real Assessment
```

**Result:** Students practice exactly what they'll be graded on, using the same criteria.

## Cultural Adaptations

Content is adapted for Vietnamese university context:

**Lectures:**
- Vietnamese business examples
- Regional (ASEAN) context
- Culturally relevant scenarios
- Local business practices

**Tutorials:**
- Structured peer interaction
- Sentence starters for feedback
- Gradual confidence building
- Local case discussions

## Time Investment

### One-Time Setup
- Project structure: Already complete
- Understanding workflows: 30 minutes

### Per Course (10 weeks)
- Course setup: 5 minutes
- Syllabus generation: 3-4 hours (research-intensive)
- Weekly content (×10): 7-12 hours
- Slides and review: 2-3 hours
- **Total: 12-20 hours for complete course**

### Ongoing
- Article validation: 30-50 min per topic
- Content updates: As needed
- Quality checks: Built into process

**ROI:** 12-20 hours of work produces world-class course materials that can be used for multiple semesters with minor updates.

## Getting Help

- **Workflows:** See `.claude/CLAUDE.md` for complete documentation
- **Commands:** See `.claude/commands/` for detailed command instructions
- **Content Guidelines:** See `lecture_content_instructions.md`
- **Troubleshooting:** See "Troubleshooting" section in `.claude/CLAUDE.md`

## Best Practices

1. **Always start with `/new-course`** to create proper structure
2. **Complete syllabus first** before weekly content
3. **Be strict with article validation** - quality over convenience
4. **Check assessment alignment** - tutorials must mirror assessments
5. **Document research decisions** - maintain quality audit trail
6. **Update regularly** - verify URLs, refresh examples
7. **Gather feedback** - improve based on student and instructor experience

## System Philosophy

**Quality Over Speed**
Better to spend time finding perfect articles than settle for incomplete coverage.

**Evidence-Based**
Learn from top schools, use peer-reviewed research, validate thoroughly.

**Student-Centered**
Every decision serves student learning and assessment preparation.

**Professionally Rigorous**
Maintain high standards across all courses and materials.

**Culturally Relevant**
Adapt content for Vietnamese and regional context.

## Version

**v1.0** - Research-enhanced course content generation system

- ✅ 5 slash commands
- ✅ 4-stage research validation
- ✅ Syllabus-first workflow
- ✅ Assessment alignment logic
- ✅ Cultural adaptations
- ✅ Quality assurance built-in

---

## Next Steps

1. **Understand the System:** Read `.claude/CLAUDE.md` for complete workflows
2. **Create Your First Course:** Run `/new-course [CODE] [Name]`
3. **Build Syllabus:** Run `/generate-syllabus` for research-backed syllabus
4. **Generate Content:** Run `/generate-week [N]` for each week
5. **Teach Great Courses:** Use materials with confidence

---

**Ready to create world-class course content? Start with `/new-course`!**
