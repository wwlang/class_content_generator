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
# Copy gemini-handoff.md content to Gemini, download PPTX, then:
/add-speaker-notes BUS101 1
```

Inserts speaker notes into Gemini-created PPTX (saves to `output/slides.pptx`).

## Slash Commands

| Command | Purpose | Time |
|---------|---------|------|
| `/new-course [CODE] [Name]` | Create course structure | 2-3 min |
| `/generate-syllabus` | Build research-backed syllabus | 7-10 hrs |
| `/generate-week [N]` | Create lecture + tutorial + quiz | 45-70 min |
| `/generate-course [CODE]` | Batch generate all weeks | 7-12 hrs |
| `/add-speaker-notes [CODE] [N]` | Insert notes into Gemini PPTX | 1-2 min |
| `/export-docx [CODE] [N]` | Convert markdown to DOCX | 1-3 min |
| `/research-topic "[Topic]" "[Concepts]"` | Research articles for topic | 30-50 min |

## Project Structure

```
class_content_generator/
├── .claude/
│   ├── commands/           # Slash command definitions
│   ├── skills/             # Domain-specific guidance
│   │   ├── content-generation/
│   │   ├── assessment-design/
│   │   └── research/
│   ├── templates/          # Handoff prompts
│   └── CLAUDE.md           # Complete workflow documentation
│
├── courses/                # Generated course content
│   └── [COURSE-CODE]-[name]/
│       ├── syllabus.md
│       ├── assessment-handbook.md
│       ├── weeks/week-[N]/
│       │   ├── lecture-content.md      # Source: slides + speaker notes
│       │   ├── quiz-questions.md       # Source: quiz Q&A
│       │   ├── tutorial-content.md     # Source: student activities
│       │   ├── tutorial-tutor-notes.md # Source: facilitation guide
│       │   ├── gemini-handoff.md       # Handoff: Gemini prompt
│       │   └── output/                 # Deliverables
│       │       ├── tutorial-content.docx
│       │       ├── tutorial-tutor-notes.docx
│       │       ├── week-N-quiz.gift
│       │       └── slides.pptx
│       └── .working/research/
│
├── tools/                  # Python automation scripts
│   ├── markdown_to_docx.py
│   ├── export_quiz_to_gift.py
│   └── add_speaker_notes.py
│
└── docs/                   # Documentation
    ├── INDEX.md
    ├── ARCHITECTURE.md
    └── LAYOUT-VOCABULARY.md
```

## Slide Workflow

Slides are created using Google Gemini for visual design, with Claude handling content and speaker notes:

### Workflow

1. **Claude generates** `lecture-content.md` with slide content and speaker notes
2. **Claude creates** `gemini-handoff.md` with ready-to-paste Gemini prompt
3. **User sends to Gemini** → downloads PPTX file to week folder
4. **Claude inserts speaker notes:** `/add-speaker-notes [CODE] [N]`
5. **Final slides saved to** `output/slides.pptx`

### Why This Approach?

- **Gemini excels** at visual slide design and layout
- **Claude excels** at content structure, speaker notes, and automation
- **Combined result:** Professional slides with comprehensive teaching notes

### Documentation

- **Layout Vocabulary:** See [docs/LAYOUT-VOCABULARY.md](docs/LAYOUT-VOCABULARY.md) for layout hints
- **Architecture:** See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
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
  └─ /new-course BUS101 Business Communication

Days 2-3: Syllabus (Most intensive)
  ├─ /generate-syllabus
  │  ├─ Define basics and structure
  │  └─ Research 2 articles × 10 weeks = 20 articles
  └─ /export-docx BUS101 syllabus

Days 4-6: Weekly Content
  ├─ /generate-week 1  (creates lecture, tutorial, quiz → output/)
  ├─ /generate-week 2
  └─ ... or use /generate-course BUS101 for batch

Day 7: Slides
  ├─ Copy gemini-handoff.md to Gemini for each week
  ├─ Download PPTX to week folder
  └─ /add-speaker-notes BUS101 [N] for each week
```

**Result:** Complete course with DOCX tutorials, GIFT quizzes, and PPTX slides

## Quality Standards

### Lecture Content ✓
- 22-30 content slides
- 3-5 verified sources with DOI/URLs
- Current examples (2023-2025)
- Assessment connection explicit
- Speaker notes for teaching

### Tutorial Content ✓
- ONE consolidated activity mirroring assessment
- Quick Review with success criteria
- Class feedback with participation requirement
- Timing in tutor-notes only (not inline)
- Separate quiz-questions.md file (5-8 questions)

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
- **All Documentation:** `docs/INDEX.md`
- **Layout Vocabulary:** `docs/LAYOUT-VOCABULARY.md`
- **System Architecture:** `docs/ARCHITECTURE.md`

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
- **All Docs:** See `docs/INDEX.md` for documentation index
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

**v2.0** - Streamlined course content generation with output folder structure

- ✅ 7 slash commands (new: `/add-speaker-notes`, `/export-docx`, `/generate-course`)
- ✅ Gemini slide workflow with speaker notes insertion
- ✅ Output folder structure (sources separate from deliverables)
- ✅ Standalone quiz-questions.md with GIFT export
- ✅ Streamlined tutorials (~80 lines, no inline timing)
- ✅ DOCX export with branded footers
- ✅ 4-stage research validation
- ✅ Assessment alignment logic

---

## Next Steps

1. **Understand the System:** Read `.claude/CLAUDE.md` for complete workflows
2. **Create Your First Course:** Run `/new-course [CODE] [Name]`
3. **Build Syllabus:** Run `/generate-syllabus` for research-backed syllabus
4. **Generate Content:** Run `/generate-week [N]` or `/generate-course [CODE]`
5. **Create Slides:** Use Gemini handoff + `/add-speaker-notes`
6. **Export Deliverables:** All outputs in `output/` folder ready for LMS

---

**Ready to create world-class course content? Start with `/new-course`!**
