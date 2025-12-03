# Class Content Generator

A comprehensive system for generating world-class university course materials using Claude Code with research validation and assessment alignment.

## Overview

This system helps you create complete course materials including:
- **Research-backed syllabi** with validated, accessible articles
- **Assessment handbooks** with scenarios, rubrics, and student guidance
- **Lecture content** (24-32 slides with speaker notes in XML format)
- **Tutorial activities** aligned to assessments
- **Quiz questions** in YAML format with GIFT export for Moodle
- **Presentation slides** via Gemini handoff

All content is generated following evidence-based pedagogical practices and validated against top management school standards (M7, UK Triple Crown).

## Key Features

### Parallel Agent Execution
- Week content generated using parallel agents for efficiency
- 10 weeks can be regenerated simultaneously
- Reduces generation time from hours to minutes

### Research-Enhanced Content
- 4-stage article validation process
- Only openly accessible, high-quality sources
- Strict content matching (no partial matches)
- Learn from top business schools

### Complete Course Materials
- Lecture content with citations and examples (XML slide format)
- Assessment-aligned tutorials with rubric criteria
- Quiz questions in YAML with automatic GIFT export
- Professional DOCX exports with branded footers

### Quality Assurance
- Every article covers ALL required concepts
- Accessibility verified (no paywalls)
- Current examples (2023-2025)
- Vietnamese cultural adaptations

## Quick Start

### 1. Create a New Course

```bash
/new-course BUS101 Business Communication
```

Creates the complete directory structure with templates.

### 2. Generate Course Syllabus

```bash
/generate-syllabus
```

Interactive process that researches and validates articles per week.

### 3. Generate Assessment Handbook

```bash
/generate-handbook BUS101
```

Creates scenarios, rubrics, and student guidance BEFORE weekly content.

### 4. Generate Weekly Content

```bash
# Single week
/generate-week 1

# All weeks (uses parallel agents)
/generate-course BUS101
```

Uses parallel agents to generate lecture, tutorial, tutor notes, and quiz simultaneously.

### 5. Create Presentation Slides

```bash
# Generate Gemini prompt
/gemini-handoff BUS101 1

# After downloading PPTX from Gemini:
/add-speaker-notes BUS101 1
```

### 6. Package Course

```bash
/package-course BUS101
```

Converts all markdown to DOCX and creates ZIP archive.

## Slash Commands

| Command | Purpose | Time |
|---------|---------|------|
| `/new-course [CODE] [Name]` | Create course structure | 2-3 min |
| `/generate-syllabus` | Build research-backed syllabus | 3-4 hrs |
| `/generate-handbook [CODE]` | Create assessment handbook | 30-45 min |
| `/generate-week [N]` | Create week content (parallel agents) | 15-25 min |
| `/generate-course [CODE]` | Batch generate all weeks | 2-4 hrs |
| `/gemini-handoff [CODE] [N]` | Generate Gemini slide prompt | 2-3 min |
| `/add-speaker-notes [CODE] [N]` | Insert notes into PPTX | 1-2 min |
| `/export-docx [CODE] [N]` | Convert markdown to DOCX | 1-3 min |
| `/package-course [CODE]` | Create delivery ZIP | 5-10 min |
| `/research-topic "[Topic]" "[Concepts]"` | Research articles | 30-50 min |

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
│       ├── course-info.md          # Status tracker
│       ├── weeks/week-[N]/
│       │   ├── lecture-content.md      # XML slides + speaker notes
│       │   ├── quiz-questions.md       # YAML format
│       │   ├── tutorial-content.md     # Student activities
│       │   ├── tutorial-tutor-notes.md # Facilitation guide
│       │   ├── gemini-prompt.md        # Ready-to-paste prompt
│       │   └── output/
│       │       ├── tutorial-content.docx
│       │       ├── tutorial-tutor-notes.docx
│       │       ├── week-N-quiz.gift
│       │       └── slides.pptx
│       └── .working/research/
│
├── tools/                  # Python automation scripts
│   ├── markdown_to_docx.py
│   ├── export_yaml_quiz_to_gift.py
│   ├── add_speaker_notes.py
│   └── package_course.py
│
└── docs/                   # Documentation
    ├── INDEX.md
    ├── ARCHITECTURE.md
    └── LAYOUT-VOCABULARY.md
```

## Workflow

```
1. /new-course [CODE] [Name]
2. /generate-syllabus
3. /generate-handbook [CODE]       # BEFORE weekly content
4. /generate-course [CODE]         # Uses parallel agents
   OR /generate-week [N]
5. /validate-content [CODE]
6. /gemini-handoff [CODE] [N]      # Generate slide prompt
7. /add-speaker-notes [CODE] [N]   # Merge notes into PPTX
8. /package-course [CODE]          # Create delivery ZIP
```

**Why this order:**
- Syllabus provides course structure and assessment overview
- Assessment Handbook uses syllabus to create scenarios and rubrics
- Tutorials reference Assessment Handbook scenarios and rubric criteria
- Weekly content aligns with specific assessment requirements

## Parallel Agent Architecture

The `/generate-week` command uses parallel agents for efficiency:

```
Phase 0: Pre-Flight (sequential)
    ↓
Phase 1: Content Generation (PARALLEL)
    ├── Lecture Agent → lecture-content.md
    └── Tutorial Agent → tutorial-content.md + tutorial-tutor-notes.md
    ↓
Phase 2: Lecture-Dependent (PARALLEL)
    ├── Quiz Agent → quiz-questions.md
    └── Gemini Agent → gemini-prompt.md
    ↓
Phase 3: Exports (sequential)
    ├── GIFT Export → output/week-N-quiz.gift
    └── DOCX Export → output/*.docx
```

**Key benefit:** Multiple weeks can be generated simultaneously using `/generate-course`.

## Quiz Format

Quizzes use YAML format with automatic GIFT export for Moodle:

```yaml
---
metadata:
  week: 1
  topic: "Introduction & Future of Work"
  prepares_for: "Personal Development Plan (Week 11)"
  source: "lecture-content.md"

questions:
  - id: "W1-Q1-framework"
    type: "multiple_choice"
    bloom_level: "remembering"
    topic: "Framework Name"

    question: |
      Question text here?

    options:
      - key: "A"
        text: "Option text"
        feedback: "Why correct/incorrect"
        correct: true
      - key: "B"
        text: "Option text"
        feedback: "Why incorrect"

    general_feedback: |
      Explanation with <b>term</b> (definition) format.
---
```

**Requirements:**
- File MUST start and end with `---`
- 12 questions per week (4 frameworks × 3 questions)
- Distribution: 4 Remembering + 8 Understanding
- Use HTML `<b>tags</b>` for bold (not markdown)

## Slide Workflow

Slides are created using Google Gemini for visual design:

1. **Claude generates** `lecture-content.md` with XML slides and speaker notes
2. **Claude creates** `gemini-prompt.md` with ready-to-paste prompt
3. **User sends to Gemini** → downloads PPTX file
4. **Claude inserts speaker notes:** `/add-speaker-notes [CODE] [N]`
5. **Final slides saved to** `output/slides.pptx`

## Core Principles

### 1. Syllabus-First Approach
Create complete syllabus before generating weekly content. The assessment schedule drives tutorial design.

### 2. Assessment Handbook Before Content
Generate assessment handbook BEFORE weekly content so tutorials can reference specific scenarios and rubric criteria.

### 3. Strict Content Validation
Articles must cover ALL required key concepts. No partial matches accepted.

### 4. YAML-Only Quiz Format
All quizzes in YAML format for consistent GIFT export. No markdown quiz format.

### 5. Parallel Agent Efficiency
Use parallel agents for week generation to maximize throughput.

## Quality Standards

### Lecture Content
- 24-32 slides in XML format
- Speaker notes for every slide
- Full APA 7th references
- Assessment connection explicit

### Tutorial Content
- ONE consolidated activity mirroring assessment
- Success criteria from rubric
- Class feedback with participation requirement
- ~80 lines, no inline timing

### Quiz Questions
- 12 questions in YAML format
- 4 Remembering + 8 Understanding
- No scenario/application questions (those belong in tutorials)
- ONE clearly correct answer per question

## Time Investment

### Per Course (12 weeks)
- Course setup: 5 minutes
- Syllabus generation: 3-4 hours
- Assessment handbook: 30-45 minutes
- Weekly content (parallel): 2-4 hours total
- Slides and review: 2-3 hours
- **Total: 8-12 hours for complete course**

### With Parallel Agents
- Single week: 15-25 minutes
- All weeks simultaneously: 30-45 minutes

## Documentation

- **Quick Start:** This README
- **Complete Workflows:** `.claude/CLAUDE.md`
- **All Documentation:** `docs/INDEX.md`
- **Layout Vocabulary:** `docs/LAYOUT-VOCABULARY.md`
- **System Architecture:** `docs/ARCHITECTURE.md`

## Version

**v3.0** - Parallel agent architecture with YAML quiz format

- Parallel agent execution for week generation
- YAML-only quiz format with GIFT export
- Assessment handbook generation before weekly content
- XML slide format with layout hints
- Package course command for delivery
- Standardized `gemini-prompt.md` naming
- Streamlined workflows with clear phase dependencies

---

**Ready to create world-class course content? Start with `/new-course`!**
