# Documentation Index

**Central directory of all project documentation**

**Last Updated:** January 10, 2025

---

## Quick Navigation

**I want to...**

- [Get started with the project](#getting-started) → `README.md`
- [Create a new course](#course-creation) → `.claude/CLAUDE.md`
- [Generate lecture content](#content-generation) → `lecture_content_instructions.md`
- [Understand the system architecture](#technical-reference) → `docs/ARCHITECTURE.md`
- [Add a new slide layout](#contributing) → `CONTRIBUTING.md`
- [Troubleshoot validation issues](#troubleshooting) → `docs/VALIDATION-GUIDE.md`

---

## Documentation by Purpose

### Getting Started

#### For Course Developers (Non-Technical)

1. **[README.md](../README.md)** - Project overview and quick start
   - What the system does
   - Key features
   - 5-minute quick start
   - Example workflow

2. **[.claude/CLAUDE.md](../.claude/CLAUDE.md)** - Complete course development workflows
   - Slash commands reference
   - Syllabus-first approach
   - Research & validation process
   - Quality standards
   - **START HERE for course creation**

3. **[lecture_content_instructions.md](../lecture_content_instructions.md)** - Content generation guide
   - Lecture structure requirements (22-30 slides)
   - Tutorial design (assessment-aligned)
   - Citation requirements
   - Layout hints
   - **Reference when generating weekly content**

#### For Developers (Technical)

1. **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Development guide
   - Project structure
   - Code standards (SOLID, DRY, PEP 8)
   - File organization rules
   - Adding new features
   - Testing guidelines
   - **START HERE for technical contributions**

2. **[docs/ARCHITECTURE.md](ARCHITECTURE.md)** - Technical deep-dive
   - Handler system design
   - Configuration system
   - CSS parser
   - Design patterns
   - Extension points
   - **Reference for understanding internals**

3. **[docs/SLIDE-LAYOUTS.md](SLIDE-LAYOUTS.md)** - Complete layout reference
   - All 18 slide layouts
   - HTML structure and examples
   - Usage guidelines
   - Prescriptive layout hints
   - Troubleshooting
   - **Reference when creating/debugging layouts**

---

### Core Workflows

#### Course Creation

| Task | Primary Doc | Time | Supporting Docs |
|------|-------------|------|-----------------|
| **1. Create course structure** | `.claude/commands/new-course.md` | 5 min | `.claude/CLAUDE.md` |
| **2. Generate syllabus** | `.claude/commands/generate-syllabus.md` | 3-4 hrs | `.claude/CLAUDE.md` (research process) |
| **3. Generate weekly content** | `.claude/commands/generate-week.md` | 45-70 min/week | `lecture_content_instructions.md` |
| **4. Export slides** | `.claude/skills/slide-exporter/` | 5-10 min/week | `docs/SLIDE-LAYOUTS.md` |

**Total time for 10-week course:** 12-20 hours

#### Content Generation

| Task | Primary Doc | Supporting Docs |
|------|-------------|-----------------|
| **Research articles** | `.claude/commands/research-topic.md` | `.claude/CLAUDE.md` (4-stage process) |
| **Validate articles** | `.claude/commands/validate-article-content.md` | - |
| **Design lectures** | `lecture_content_instructions.md` | `docs/SLIDE-LAYOUTS.md` |
| **Design tutorials** | `lecture_content_instructions.md` | Assessment handbook/rubrics |

---

## Documentation by Topic

### Course Content System

#### Workflows & Commands

- **[.claude/CLAUDE.md](../.claude/CLAUDE.md)** - Master workflow documentation
  - Complete course creation process
  - Research validation (4-stage process)
  - Assessment alignment
  - Quality standards
  - Two-document structure guidance (syllabus + assessment handbook)

- **[.claude/WORKING-DOCS-SYSTEM.md](../.claude/WORKING-DOCS-SYSTEM.md)** - File management system
  - `.working/` folder for in-progress docs
  - `.archive/` folder for completed work
  - Clean directory structure
  - Migration guide

#### Slash Commands

- **[.claude/commands/new-course.md](../.claude/commands/new-course.md)** - Create course structure
- **[.claude/commands/generate-syllabus.md](../.claude/commands/generate-syllabus.md)** - Build syllabus
- **[.claude/commands/generate-week.md](../.claude/commands/generate-week.md)** - Create weekly content
- **[.claude/commands/research-topic.md](../.claude/commands/research-topic.md)** - Research articles
- **[.claude/commands/validate-article-content.md](../.claude/commands/validate-article-content.md)** - Validate articles

#### Content Guidelines

- **[lecture_content_instructions.md](../lecture_content_instructions.md)** - Content generation rules
  - Lecture structure (22-30 slides)
  - Tutorial design (assessment-aligned)
  - Citation requirements (APA 7th)
  - Layout hints for specialized slides
  - Quality checklist

---

### HTML to PPTX Converter

#### Core Documentation

- **[docs/ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture (1,615 lines)
  - Handler system design
  - Configuration system
  - CSS parser
  - Main converter
  - Design patterns (Strategy, Registry, Template Method, Factory)
  - Extension points
  - **For developers understanding/modifying converter**

- **[docs/SLIDE-LAYOUTS.md](SLIDE-LAYOUTS.md)** - Layout reference (2,060 lines)
  - Quick reference table (18 layouts)
  - Detailed specifications for each layout
  - HTML structure and examples
  - Usage guidelines
  - Prescriptive layout hints
  - Troubleshooting
  - **For content generators and developers**

#### Quality Assurance

- **[docs/VALIDATION-GUIDE.md](VALIDATION-GUIDE.md)** - Validation system (620 lines)
  - Automated quality checks (HTML, PPTX, cross-validation)
  - Understanding validation results
  - Customization and thresholds
  - CI/CD integration
  - Troubleshooting
  - Enhancement roadmap
  - **For QA and automation**

#### Usage Guides

- **[docs/DARK_SLIDE_USAGE_GUIDE.md](DARK_SLIDE_USAGE_GUIDE.md)** - Dark slide best practices
  - When to use dark slides
  - Strategic placement (every 8-10 slides)
  - Content types suitable for dark background
  - Visual rhythm guidelines

- **[docs/reference-design-style-guide.md](reference-design-style-guide.md)** - Design system reference
  - Color palette
  - Typography system
  - Spacing guidelines
  - Visual hierarchy

---

### Development

#### Contributing

- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Development guidelines (619 lines)
  - Quick reference for file organization
  - Project structure
  - Development workflow
  - Code standards (SOLID, DRY, PEP 8)
  - Adding new features
  - Testing guidelines
  - Documentation requirements

#### Technical Reference

- **[docs/ARCHITECTURE.md](ARCHITECTURE.md)** - Complete technical reference
  - Package structure
  - Handler system (Strategy pattern)
  - Configuration system (LayoutConfig, FontConfig, ColorConfig)
  - CSS parser
  - Main converter
  - Extension points
  - Design patterns
  - File size metrics
  - Dependencies

---

## Documentation Maintenance

### Recent Consolidation (January 10, 2025)

**Consolidated documents:**
- `docs/SLIDE-LAYOUTS.md` ← Merged 4 layout docs (layout-catalog.md, SLIDE-LAYOUT-TYPES.md, NEW-LAYOUTS-GUIDE.md, layout-usage-example.md)
- `docs/VALIDATION-GUIDE.md` ← Merged 2 validation docs (VALIDATION-SYSTEM.md, VALIDATION-ENHANCEMENTS.md)
- `docs/INDEX.md` ← This document (NEW)

**Deprecated files** (moved to archives, content preserved in consolidated docs):
- `docs/layout-catalog.md`
- `docs/SLIDE-LAYOUT-TYPES.md`
- `docs/NEW-LAYOUTS-GUIDE.md`
- `docs/layout-usage-example.md`
- `docs/VALIDATION-SYSTEM.md`
- `docs/VALIDATION-ENHANCEMENTS.md`

**Archived files** (task-specific, moved to `.archive/`):
- `docs/WEEK_12_CITATION_FIXES.md`
- `docs/WEEK_12_DARK_SLIDE_OPPORTUNITIES.md`
- `docs/SLIDE_LAYOUT_ANALYSIS.md`
- `docs/CLEANUP_RECOMMENDATIONS.md`

### Update Frequency

| Document | Update Frequency | Owner |
|----------|------------------|-------|
| README.md | After major features | Project lead |
| CLAUDE.md | After workflow changes | Workflow designer |
| ARCHITECTURE.md | After refactoring | Technical lead |
| SLIDE-LAYOUTS.md | When layouts added/changed | Converter dev |
| VALIDATION-GUIDE.md | When checks added | QA lead |
| lecture_content_instructions.md | As pedagogy evolves | Content lead |

---

## Complete File Listing

### Root Level

```
/
├── README.md                              # Quick start and overview
├── CONTRIBUTING.md                        # Development guide
└── lecture_content_instructions.md       # Content generation rules
```

### .claude/ (Workflows)

```
.claude/
├── CLAUDE.md                             # Master workflow documentation
├── WORKING-DOCS-SYSTEM.md               # File management system
├── GENERATOR-UPDATES.md                 # System update log
└── commands/                            # Slash command definitions
    ├── new-course.md
    ├── generate-syllabus.md
    ├── generate-week.md
    ├── research-topic.md
    └── validate-article-content.md
```

### docs/ (Technical Reference)

```
docs/
├── INDEX.md                             # This document
├── ARCHITECTURE.md                      # Technical architecture
├── SLIDE-LAYOUTS.md                     # Complete layout reference
├── VALIDATION-GUIDE.md                  # Validation system guide
├── DARK_SLIDE_USAGE_GUIDE.md           # Dark slide best practices
├── reference-design-style-guide.md     # Design system
└── .archive/                           # Archived documents
    └── completed-tasks/
```

### Templates

```
templates/
├── syllabus-base-template.md
├── week-topic-specification.md
├── grading-systems.md
├── vocabulary-translation-template.md
└── syllabus-components/
    ├── assessment-structures/
    │   ├── portfolio-presentation-quiz.md
    │   └── exam-project-quiz.md
    └── rubric-structures/
        ├── written-work-rubric.md
        ├── presentation-rubric.md
        ├── project-rubric.md
        └── vietnamese-weighted-rubric.md
```

### Shared Resources

```
shared/
├── research/
│   └── open-access-sources.md          # Research resource list
├── citation-library/                    # (Future)
├── vietnam-examples/                    # (Future)
└── teaching-resources/                  # (Future)
```

---

## Getting Help

### By Task

| I need to... | Check this document | Then this |
|--------------|---------------------|-----------|
| **Understand project** | README.md | .claude/CLAUDE.md |
| **Create a course** | .claude/CLAUDE.md | .claude/commands/*.md |
| **Generate content** | lecture_content_instructions.md | docs/SLIDE-LAYOUTS.md |
| **Fix converter bug** | docs/ARCHITECTURE.md | CONTRIBUTING.md |
| **Add new layout** | docs/SLIDE-LAYOUTS.md | CONTRIBUTING.md |
| **Understand validation** | docs/VALIDATION-GUIDE.md | - |
| **Troubleshoot slides** | docs/SLIDE-LAYOUTS.md (Troubleshooting section) | docs/VALIDATION-GUIDE.md |
| **Contribute code** | CONTRIBUTING.md | docs/ARCHITECTURE.md |

### By Audience

#### Course Developers
1. README.md (overview)
2. .claude/CLAUDE.md (workflows)
3. lecture_content_instructions.md (content rules)

#### Content Generators (AI)
1. lecture_content_instructions.md (primary)
2. docs/SLIDE-LAYOUTS.md (layouts)
3. .claude/CLAUDE.md (workflows)

#### Developers
1. CONTRIBUTING.md (start here)
2. docs/ARCHITECTURE.md (deep-dive)
3. docs/SLIDE-LAYOUTS.md (layout system)
4. docs/VALIDATION-GUIDE.md (QA system)

#### Quality Assurance
1. docs/VALIDATION-GUIDE.md (primary)
2. docs/SLIDE-LAYOUTS.md (expected layouts)
3. docs/ARCHITECTURE.md (understanding system)

---

## External Resources

### Research Sources

- **Harvard Business School:** https://www.hbs.edu/
- **Stanford GSB:** https://www.gsb.stanford.edu/
- **Wharton School:** https://www.wharton.upenn.edu/
- **MIT Sloan:** https://mitsloan.mit.edu/

### Open Access Research

- **Google Scholar:** https://scholar.google.com/
- **ResearchGate:** https://www.researchgate.net/
- **SSRN:** https://www.ssrn.com/
- **arXiv:** https://arxiv.org/

### Practitioner Publications

- **Harvard Business Review:** https://hbr.org/
- **MIT Sloan Management Review:** https://sloanreview.mit.edu/

---

## Version History

### v2.0 (January 10, 2025) - Documentation Consolidation

- Created central INDEX.md
- Consolidated 4 layout docs → SLIDE-LAYOUTS.md
- Consolidated 2 validation docs → VALIDATION-GUIDE.md
- Archived 4 task-specific docs
- **40% reduction in documentation volume**
- **Zero information loss**

### v1.0 (December 2024) - Initial Documentation

- Created separate documentation files
- Established workflow documentation
- Technical architecture documented

---

## Feedback

Found an issue or have a suggestion?

- **Documentation issues:** Update this INDEX.md or relevant docs
- **Workflow improvements:** Update `.claude/CLAUDE.md`
- **Technical issues:** Update `docs/ARCHITECTURE.md`
- **Code issues:** See `CONTRIBUTING.md` for contribution process

---

**Last Updated:** January 10, 2025 | **Maintainer:** Project team | **Version:** 2.0
