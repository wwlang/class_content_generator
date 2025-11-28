# Documentation Index

**Central directory for the Class Content Generator**

Last Updated: November 2025

---

## Quick Start

| I want to... | Go to |
|--------------|-------|
| **Create a new course** | `.claude/CLAUDE.md` |
| **Generate weekly content** | `/generate-week` command |
| **Understand layout vocabulary** | `docs/LAYOUT-VOCABULARY.md` |
| **Set up Desktop research** | `docs/RESEARCH-HANDOFF-GUIDE.md` |
| **Fix common issues** | `docs/TROUBLESHOOTING.md` |
| **Contribute code** | `CONTRIBUTING.md` |

---

## Documentation Map

### Core Workflows

| Document | Purpose | Audience |
|----------|---------|----------|
| **[.claude/CLAUDE.md](../.claude/CLAUDE.md)** | Master workflow guide | Course developers |
| **[README.md](../README.md)** | Project overview | Everyone |
| **[CONTRIBUTING.md](../CONTRIBUTING.md)** | Development guide | Developers |

### Skills (Domain Guidance)

Focused, ~400-token guidance files loaded on demand:

```
.claude/skills/
├── content-generation/    # Lecture, speaker notes, layouts, citations
├── assessment-design/     # Quiz questions, tutorial activities
└── research/              # Article validation
```

### Commands

Compact workflow definitions:

| Command | Purpose |
|---------|---------|
| `/new-course` | Create course structure |
| `/generate-syllabus` | Build research-backed syllabus |
| `/generate-handbook` | Create Assessment Handbook |
| `/generate-week` | Create lecture + tutorial + quiz |
| `/generate-course` | Batch generate all weeks |
| `/validate-content` | AI-powered quality validation |
| `/gemini-handoff` | Generate Gemini slide prompt |
| `/add-speaker-notes` | Merge speaker notes into PPTX |
| `/research-topic` | Find validated articles |

### Technical Reference

| Document | Purpose |
|----------|---------|
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System architecture |
| **[LAYOUT-VOCABULARY.md](LAYOUT-VOCABULARY.md)** | Layout vocabulary for Gemini workflow |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Common issues and solutions |
| **[CONTENT-VALIDATION.md](CONTENT-VALIDATION.md)** | AI-powered quality validation (8 validators) |
| **[VALIDATION-GUIDE.md](VALIDATION-GUIDE.md)** | Structural validation checks |
| **[QUESTION-AMBIGUITY-VALIDATION.md](QUESTION-AMBIGUITY-VALIDATION.md)** | Ambiguity detection and auto-rewording |
| **[RESEARCH-HANDOFF-GUIDE.md](RESEARCH-HANDOFF-GUIDE.md)** | Desktop research workflow |
| **[TESTING.md](TESTING.md)** | Unit testing guide (82% coverage) |
| **[FONT-EMBEDDING.md](FONT-EMBEDDING.md)** | Font embedding for PPTX |

---

## Archived Documentation

Historical reports and redundant docs moved to `.archive/`:

```
docs/.archive/
├── historical/           # Phase reports, session summaries
├── full-reference/       # Archived FULL-REFERENCE files (version history)
├── slide-technical/      # HTML/CSS converter details (fallback workflow)
├── redundant-skills/     # Old skill docs (now in skills/)
└── layout-consolidation/ # Old layout analysis docs
```

---

## Workflow Summary

### Standard Course Creation

```
1. /new-course [CODE] [Name]           → Creates structure
2. /generate-syllabus                  → Research + syllabus (2-3 hrs)
3. /generate-handbook [CODE]           → Assessment Handbook (1-2 hrs)
4. /generate-course [CODE]             → All weeks (7-12 hrs)
   OR /generate-week [N]               → Per week (45-70 min)
5. /validate-content [CODE]            → AI quality checks (5-10 min)
6. /enhance-coherence [CODE]           → Quality polish (15-30 min)
7. /gemini-handoff [CODE] [N]          → Generate prompt, paste into Gemini
8. /add-speaker-notes [CODE] [N]       → Merge speaker notes into PPTX
9. /export-docx [CODE] [N]             → Tutorial/quiz Word exports
```

### Gemini Hybrid Slide Workflow

```
Claude Code → lecture-content.md (content + speaker notes)
     ↓
Gemini      → visual slides in batches (images, infographics)
     ↓
Claude Code → merge batches + insert speaker notes (/finalize-slides)
```

---

## File Organization

```
class_content_generator/
├── .claude/
│   ├── CLAUDE.md           # Main workflow guide (compact)
│   ├── commands/           # Slash commands (~60-90 lines each)
│   ├── skills/             # Domain guidance (~40-70 lines each)
│   └── templates/          # Handoff prompts
│
├── docs/
│   ├── INDEX.md            # This file
│   ├── ARCHITECTURE.md     # Technical deep-dive
│   ├── LAYOUT-VOCABULARY.md # Layout catalog
│   └── .archive/           # Historical docs
│
├── courses/[CODE]/
│   ├── syllabus.md
│   └── weeks/week-[N]/
│
└── tools/                  # Python utilities
```

---

## Update Policy

| Document | Update When |
|----------|-------------|
| CLAUDE.md | Workflow changes |
| Skills | Domain rules change |
| Commands | Command behavior changes |
| ARCHITECTURE.md | System refactoring |
| LAYOUT-VOCABULARY.md | New layouts added |

**Principle:** Add to existing docs, don't create new ones.

---

*For questions, update the relevant document or `.claude/CLAUDE.md`.*
