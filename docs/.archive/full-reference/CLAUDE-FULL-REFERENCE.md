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

| I want to... | Primary Document |
|--------------|------------------|
| **Understand the system** | [README.md](../README.md) (5 min) |
| **Create a new course** | [Slash Commands Reference](#slash-commands-reference) (this doc) |
| **Generate lecture content** | `.claude/skills/content-generation/` |
| **Choose slide layouts** | [docs/SLIDE-LAYOUTS.md](../docs/SLIDE-LAYOUTS.md) |
| **Research articles** | [Research & Validation](#research--validation-process) (this doc) |
| **Use Claude Desktop research** | [docs/RESEARCH-HANDOFF-GUIDE.md](../docs/RESEARCH-HANDOFF-GUIDE.md) |
| **Troubleshoot slides** | [docs/VALIDATION-GUIDE.md](../docs/VALIDATION-GUIDE.md) |
| **Contribute code** | [CONTRIBUTING.md](../CONTRIBUTING.md) |
| **View all documentation** | [docs/INDEX.md](../docs/INDEX.md) |

---

## Overview & Philosophy

### Purpose

Generate comprehensive university course materials that:
- Are backed by research from top management schools (US: M7 + Berkeley, Yale, Tuck; UK: LBS, Oxford, Cambridge, LSE, Imperial, Warwick, Edinburgh, Manchester, Cranfield)
- Include only validated academic articles (open access preferred; paywalls acceptable if seminal + content validated)
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
- Paywalls acceptable ONLY if: (1) seminal work AND (2) Claude highly confident of contents

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
Interactive process to create research-backed syllabus.

**IMPORTANT - Research Method Choice:**
- **Claude Desktop (RECOMMENDED):** Superior research quality, 7-10.5 hours total (2-2.5 hrs Code + 5-8 hrs Desktop)
- **Direct in Code (Fallback):** All in one session, 6-9.5 hours (if Desktop unavailable)

The workflow will ask which method you prefer and guide you accordingly.

**Step 3: Generate Weekly Content**

**Option A: Batch Generation (Phase 3A - Recommended)**
```
/generate-course [COURSE-CODE]
```
Generate all weeks + slides in one command (7-12 hours for 10-week course).

**Option B: Individual Weeks**
```
/generate-week [week-number]
```
Creates lecture and tutorial content for specific week (45-70 minutes per week).

**Step 4: Polish Course Quality (Phase 3B - Recommended)**
```
/enhance-coherence [COURSE-CODE]
```
Cross-week quality enhancement for professional polish (15-30 minutes).

**Step 5: Create Presentation Slides** (if not using batch generation)
```
/export-slides [week-number]
```
Converts lecture content to presentation format.

### For Research Tasks

**Import Research from Claude Desktop** (Recommended for Best Quality)
```
/import-research [course-code] [week-number]
```
Import pre-researched articles from Claude Desktop.
- **Auto-write (NEW):** 1-2 minutes (validation only, MCP required)
- **Manual paste:** 3-7 minutes (copy/paste + validation)

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

Creates complete course directory structure with templates.

**Example:** `/new-course BUS101 Business Communication`
**Time:** 2-3 minutes
**Next:** `/generate-syllabus`

---

### `/generate-syllabus`

Creates comprehensive, research-backed course syllabus through interactive 6-step process.

**Process:**
1. Course basics + research-backed description (references top schools)
2. Learning objectives (4 categories, Bloom's Taxonomy)
3. Assessment structure (portfolio+presentation+quiz OR exam+project+quiz)
4. Course calendar with **4-stage article research per week** (30-50 min/week)
   - Discovery (10-15) → Quick filter (5-6) → Content validation (2-3) → User selects (2)
5. Rubric selection and customization
6. Final assembly and quality check

**Document Structure (Step 5.5):**
- **Single-doc** (2-3 assessments): All in syllabus.md
- **Two-doc** (3+ assessments): syllabus.md (overview) + assessment-handbook.md (detailed)

**Outputs:**
- `syllabus.md` (always)
- `assessment-handbook.md` (if two-doc chosen)
- Research notes in `.working/research/`

**Time:** 3-4 hours for 10-week course
**Next:** `/generate-week [N]` for each week

---

### `/research-topic "[Topic]" "[Key Concepts]"`

Standalone article research with strict validation (4-stage process).

**Example:** `/research-topic "Persuasive Communication" "Cialdini's principles, message structure, ethics"`

**Pass Criteria:** ALL concepts found with "Explained" or "In-depth" coverage, openly accessible

**Outputs:** 2-3 validated finalists with content match analysis
**Time:** 30-50 minutes

---

### `/validate-article-content [URL] "[Key Concepts]"`

Quick validation of specific article against required concepts.

**Example:** `/validate-article-content "https://hbr.org/article" "concept1, concept2, concept3"`

**Pass Criteria:** Every concept found with minimum "Explained" depth + definitions + examples + accessible

**Outputs:** PASS/FAIL with content mapping
**Time:** 2-10 minutes

---

### `/import-research [course-code] [week-number]`

Import pre-researched articles from Claude Desktop into Claude Code for content generation.

**Purpose:** Leverage Claude Desktop's superior research capabilities while using Claude Code for content generation.

**Example:** `/import-research BCI2AU 5`

**Two Import Methods:**
- **Auto-write with validation flags (Phase 2):** Claude Desktop writes research + creates `.week-[N]-ready` flag → `/generate-week` auto-validates
- **Auto-write without flags (Phase 1):** Claude Desktop writes research directly to file system via MCP
- **Manual paste:** Copy/paste research output from Claude Desktop

**Prerequisites:**
- Course structure exists (via `/new-course`)
- **Auto-write:** MCP filesystem server configured (one-time setup, see guide)
  - Template: `.claude/templates/desktop-research-with-autowrite.md`
- **Manual paste:** Research copied from Claude Desktop
  - Template: `.claude/templates/research-output-format.md` (if exists)

**Process (Auto-write):**
1. Claude Desktop writes research directly to `.working/research/article-research-summary.md`
2. Run `/import-research [course-code] [week-number]`
3. Claude Code detects existing research
4. Choose: "Validate existing research"
5. Claude Code validates and confirms ready

**Process (Manual paste):**
1. User provides research output (paste or file path)
2. Claude Code validates format, content, quality, accessibility
3. Saves to `.working/research/article-research-summary.md`
4. Ready for `/generate-week` or `/generate-syllabus`

**Validation Checks:**
- Format compliance (all sections present)
- Content completeness (all concepts with ✓ checkmarks)
- Quality (2 articles, APA citations, rationales)
- Accessibility (no obvious paywalls)

**Batch Import:**
```
/import-research [course-code] all
```
Import multiple weeks at once (both methods supported).

**MCP Setup:**
- Configuration: `.claude/mcp-config/desktop-commander-research.json`
- One-time setup: 15 minutes
- Time saved: 2-5 min/week → 20-50 min per 10-week course

**Outputs:** Validated research saved to `.working/research/`
**Time:**
- Auto-write: 1-2 minutes per week (validation only)
- Manual paste: 3-7 minutes per week (validation + paste)

**See:** [docs/RESEARCH-HANDOFF-GUIDE.md](../docs/RESEARCH-HANDOFF-GUIDE.md) for complete workflow and MCP setup

---

### `/generate-week [week-number]`

Generates complete weekly content (lecture + tutorial + quiz export). Auto-detects document structure.

**Prerequisites:** Syllabus with weekly topics, assessment details documented

**Auto-Validation (Phase 2 - NEW):**
- Checks for `.week-[N]-ready` flag file from Claude Desktop auto-write
- If found: Automatically validates research before generating content
- If valid: Deletes flag and proceeds
- If invalid: Shows errors and stops (prevents wasting 45-70 min on bad research)
- If no flag: Proceeds normally

**Generates:**
1. **Lecture (22-30 slides):** Opening (4-6) + Core (14-20) + Wrap-up (4-6), with citations
2. **Tutorial (90 min):** Opening (10) + Main activity (55-60) mirrors assessment + Quiz prep (15-20) + Wrap-up (5-10)
3. **Tutor Notes:** Quiz answer keys, facilitation guidance, expected student approaches
4. **GIFT Quiz Export:** Moodle-ready quiz file with feedback (MANDATORY)

**Assessment Alignment:** Tutorial uses simplified rubric (3-4 criteria) from actual grading rubric

**Outputs:**
- `lecture-content.md` (slides with speaker notes)
- `tutorial-content.md` (student-facing activities)
- `tutorial-tutor-notes.md` (answer keys and facilitation guidance)
- `week-[N]-quiz.gift` (Moodle GIFT format with feedback)

**Time:** 45-70 minutes
**Next:** `/export-slides [N]`

---

### `/generate-course [COURSE-CODE]` (Phase 3A - NEW)

End-to-end batch generation: Generates all weeks + slides in one command.

**Purpose:** True automation from research → finished course materials

**Example:** `/generate-course BCI2AU`

**Prerequisites:**
- Course structure exists (`/new-course`)
- Syllabus complete (`/generate-syllabus`)
- Research imported for all weeks (auto-write or manual)

**Process:**
1. **Pre-flight validation:** Verifies syllabus, counts weeks, checks research
2. **Batch generation loop:** For each week:
   - Auto-validates research (Phase 2 integration)
   - Generates lecture + tutorial + tutor notes + quiz
   - Exports slides
   - Saves progress (recovery support)
3. **Completion report:** Summary of all generated files, any skipped weeks

**Features:**
- **Progress tracking:** "Week 5/10 complete (50%)..."
- **Recovery support (Decision 1A):** Resume from interrupted week (regenerates that week)
- **Validation failures (Decision 2B):** Skip failed week, continue with others, report at end
- **Always exports slides (Decision 3A):** Complete slide decks for all weeks

**Outputs:**
- All files for each week (lecture, tutorial, tutor notes, quiz, slides)
- `generation-report.md` - Complete summary with any skipped weeks
- **Total:** ~45 files for 10-week course

**Time:** 7-12 hours for 10-week course (can run overnight)
**Time savings:** 1 command vs. 20 commands (10× `/generate-week` + 10× `/export-slides`)
**Next:** `/enhance-coherence [COURSE-CODE]` for quality polish

---

### `/enhance-coherence [COURSE-CODE]` (Phase 3B - NEW)

Cross-week quality enhancement for professional polish and unified course experience.

**Purpose:** Transform generated content into cohesive, professional course

**Example:** `/enhance-coherence BCI2AU`

**Prerequisites:**
- All (or most) weeks generated via `/generate-course` or `/generate-week`
- At least 3 weeks needed for meaningful analysis

**Analysis Performed:**
1. **Terminology Consistency** - Standardize terms, define jargon
2. **Concept Scaffolding** - Fix prerequisites, add references
3. **Example Diversity** - Remove duplicates, add Vietnamese context
4. **Cross-References** - Link concepts across weeks
5. **Citation Formatting** - Standardize to APA 7th

**Enhancement Types (Decision 1C - User chooses per type):**
- Terminology (auto-apply: 83%)
- Scaffolding (auto-apply: 75%)
- Examples (auto-apply: 20%, mostly manual)
- Cross-references (auto-apply: 83%)
- Citations (auto-apply: 100%)

**Scoring System (Decision 3C):**
- Each issue scored 1-10 for quality impact
- Critical (9-10), Important (7-8), Medium (4-6), Minor (1-3)
- User can prioritize by score

**Backup Strategy (Decision 2B):**
- Creates git commit before changes
- Easy revert if needed: `git reset --hard [commit]`

**Outputs:**
- `coherence-report.md` - Full analysis (~8,000-10,000 words)
- `enhancement-summary.md` - Executive overview
- `manual-enhancements-todo.md` - Items needing manual review
- Modified week files (with git backup)

**Time:** 15-30 minutes for 10-week course
**Quality improvement:** Typically +1.0 to +1.5 coherence score improvement
**Next:** Review manual items, deploy course

---

## Core Workflows

### Complete Course Development

**Phase 3 Workflow (RECOMMENDED - Full Automation):**

```
Time: 12-20 hours total for 10-week world-class course

1. CREATE STRUCTURE → /new-course [CODE] [Name]                    (5 min)

2. BUILD SYLLABUS → /generate-syllabus                             (7-10.5 hrs)

   WORKFLOW NOW USES DESKTOP-FIRST APPROACH:

   ├─ Step 1: Course basics & research-backed description           (20-30 min)
   ├─ Step 1.5: Extract description promises (validation)           (5 min)
   ├─ Step 2: Learning objectives & course structure                (20-30 min)
   │          (validates against description promises)
   ├─ Step 3: RESEARCH ARTICLES FIRST (Desktop recommended)         (5-8 hrs)
   │   │
   │   ├─ Option 1 (RECOMMENDED): Claude Desktop Handoff
   │   │   • Superior research capabilities
   │   │   • Time: 5-8 hours in Desktop
   │   │   • Quality: More thorough validation
   │   │   • Process: Code creates prompts → Desktop researches → Import back
   │   │
   │   └─ Option 2 (Fallback): Direct research in Code
   │       • Time: 8-10 hours in one session
   │       • Use if Desktop unavailable
   │
   └─ Step 4: DESIGN ASSESSMENTS (based on actual content)          (20-30 min)
       • Now knows specific frameworks/content being taught
       • Assessments align with researched articles
       • Pedagogically sound: assess what you teach

3. BATCH GENERATE → /generate-course [CODE]                        (7-12 hrs)
   ├─ Auto-validates all research (Phase 2)
   ├─ Generates all weeks (lecture + tutorial + tutor notes + quiz)
   ├─ Exports all slides automatically
   ├─ Recovery support (can run overnight)
   └─ Skip failed weeks, continue, report at end

4. POLISH QUALITY → /enhance-coherence [CODE]                      (15-30 min)
   ├─ Terminology consistency
   ├─ Concept scaffolding
   ├─ Cross-references between weeks
   ├─ Example diversity (Vietnamese context)
   └─ Citation formatting

5. REVIEW & DEPLOY
   ├─ Complete manual enhancements (30-60 min)
   ├─ Quality check sample weeks
   └─ Ready for students!

Benefits:
• 1 command for all weeks (vs. 20 commands manually)
• Professional coherence across entire course
• Time saved: ~40% vs. manual week-by-week
```

**Individual Week Workflow (Alternative):**

```
Use when you want control over each week, or only generating select weeks.

1-2. Same as above (structure + syllabus)

3. GENERATE WEEKLY CONTENT → /generate-week [N] for each week     (45-70 min each)
   ├─ Auto-validates research if flag exists (Phase 2)
   ├─ Syllabus drives lecture topics
   └─ Assessment schedule drives tutorial focus

4. CREATE SLIDES → /export-slides [N] for each week               (3-5 min each)
   └─ After lecture content is approved

5. OPTIONAL: POLISH → /enhance-coherence [CODE]                    (15-30 min)
   └─ Run after generating 3+ weeks for cross-week improvements

6. ITERATE & IMPROVE
   └─ Update syllabus if needed, regenerate affected weeks
```

### Article Research & Validation (4-Stage Process)

**RECOMMENDED: Perform in Claude Desktop for Superior Quality**

Claude Desktop has better research capabilities. The 4-stage process works the same, but Desktop:
- Finds more comprehensive sources
- Provides more thorough validation
- Saves overall time (5-8 hrs vs 8-10 hrs in Code)
- Better handles large-scale research

**Process (works in both Desktop and Code):**

```
STAGE 1: DISCOVERY → 10-15 candidates
├─ Top schools: site:hbs.edu, site:gsb.stanford.edu, site:wharton.upenn.edu, site:mitsloan.mit.edu
├─ Academic: Google Scholar, peer-reviewed journals
└─ Practitioner: HBR, MIT Sloan Review

STAGE 2: QUICK FILTER → 5-6 candidates
├─ WebFetch to check accessibility (prefer open access, paywalls OK if seminal + validated)
├─ Review title + abstract for relevance
└─ Check publication quality & date

STAGE 3: CONTENT VALIDATION → 2-3 finalists
├─ WebFetch full article content
├─ Extract frameworks/concepts covered (AI-assisted)
├─ Validate EACH required concept: Found? Coverage depth?
└─ STRICT: ALL concepts must be "Explained" or "In-depth" (reject if any missing)

STAGE 4: PRESENT & SELECT → Final 2 articles
├─ Show content match analysis for each finalist
└─ User selects (ideally 1 theoretical + 1 applied)
```

**Key Principles:**
- Better to spend extra time finding perfect articles than settle for incomplete coverage
- **Use Desktop for research when available** - better quality, better time management
- Direct research in Code only if Desktop unavailable

---

## Research & Validation Process

### Web Research Sources

**Top Management Schools (US - M7 + Top Tier):**
```
site:hbs.edu [topic] syllabus
site:gsb.stanford.edu [topic] MBA course
site:wharton.upenn.edu [topic] syllabus
site:mitsloan.mit.edu [topic] course
site:chicagobooth.edu [topic] syllabus
site:gsb.columbia.edu [topic] course
site:kellogg.northwestern.edu [topic] MBA
site:haas.berkeley.edu [topic] syllabus
site:som.yale.edu [topic] course
site:tuck.dartmouth.edu [topic] syllabus
```

**Top Management Schools (UK - Triple Crown Accredited):**
```
site:london.edu [topic] syllabus
site:sbs.ox.ac.uk [topic] MBA course
site:jbs.cam.ac.uk [topic] syllabus
site:imperial.ac.uk/business-school [topic] course
site:wbs.ac.uk [topic] syllabus
site:lse.ac.uk [topic] business management
site:business-school.ed.ac.uk [topic] MBA
site:mbs.ac.uk [topic] course
site:cranfield.ac.uk/som [topic] syllabus
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

**UPDATED POLICY:** Paywalls acceptable for seminal works if content validation possible

```
✓ ACCEPTABLE:
- Freely available on publisher website
- Open access journal articles
- HBR articles (openly accessible)
- Author's website or ResearchGate versions
- Institutional repositories
- Paywalled SEMINAL articles IF Claude is highly confident of contents

✓ PAYWALLED ACCEPTABLE IF ALL conditions met:
- Article is HIGH-QUALITY SEMINAL work:
  - Highly cited (1000+ citations for established works, 100+ for recent)
  - Foundational to the field or topic
  - Published in top-tier journal (A*/A ranked)
  - Field-defining or paradigm-shifting
- Comprehensive abstract covers all key concepts
- Google Scholar preview shows sufficient content
- Cached/archived versions available for full validation
- Multiple sources confirm article contents
- High confidence in concept coverage validation

⚠ REJECT paywalled articles that are:
- Recent but not highly cited yet
- Mid-tier journal publications
- Incremental research (not foundational)
- Lower quality even if behind paywall
```

**Content confidence requirements for paywalled seminal articles:**
1. Can extract ALL required concepts from available previews/abstracts
2. Can verify coverage depth (explained/in-depth, not just mentioned)
3. Can identify specific frameworks, models, or methodologies
4. Can confirm examples and applications are present
5. Multiple sources corroborate the article's contents

**Preferred strategies (in order):**
1. Use open-access articles when equally high quality
2. Use paywalled SEMINAL articles ONLY if:
   - Significantly better quality/coverage than open alternatives
   - Truly foundational to the topic (not replaceable)
   - Full content validation possible
3. Mix: Open-access for applied + paywalled seminal for theoretical foundation

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

**Tutor Notes Quality:**
- [ ] Complete quiz answer key with explanations
- [ ] 3-5 valid student approaches documented
- [ ] Facilitation guidance for each activity phase
- [ ] Quality indicators clearly stated
- [ ] Cultural considerations woven into guidance

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
- Open access strongly preferred
- Paywalls acceptable ONLY for HIGH-QUALITY SEMINAL works:
  - 1000+ citations (established) or 100+ (recent)
  - Top-tier journal (A*/A ranked)
  - Foundational/field-defining
  - Claude highly confident of full contents via abstracts/previews/cached
- Verified URL working
- Note: Students with institutional access can access paywalled articles

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
│   │   ├── validate-article-content.md
│   │   └── import-research.md
│   ├── mcp-config/
│   │   └── desktop-commander-research.json
│   ├── templates/
│   │   └── desktop-research-with-autowrite.md
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
│       │       ├── tutorial-tutor-notes.md
│       │       ├── week-[NN]-quiz.gift
│       │       └── slides.html
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
- Research what leading US schools (M7: HBS, Stanford, Wharton, MIT Sloan, Chicago Booth, Columbia, Kellogg + Berkeley, Yale, Tuck) and UK schools (LBS, Oxford, Cambridge, LSE, Imperial, Warwick, Edinburgh, Manchester, Cranfield) teach
- Extract best practices and innovative approaches
- Adapt to your context while maintaining quality

### Content Generation Best Practices

**1. Document Structure**
- **Single-doc** (2-3 assessments, <25 pages): All rubrics inline in syllabus
- **Two-doc** (3+ assessments, >30 pages): syllabus.md + assessment-handbook.md
- Two-doc benefits: Scannable syllabus, detailed handbook, clear separation of "what/when" vs "how"

**2. Syllabus First** - Complete before weekly content; drives tutorial design

**3. Assessment Alignment** - Every tutorial practices actual rubric criteria for upcoming graded work

**4. Cultural Adaptation** - Vietnamese examples, structured peer interaction, gradual confidence building

**5. Current + Timeless** - Balance recent examples (2023-2025) with seminal frameworks

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
- [ ] Tutor notes complete with answer keys and facilitation guidance
- [ ] GIFT quiz file generated and validated (Moodle-ready)
- [ ] Cultural adaptations included

**Periodic Review:**
- [ ] Check article URLs quarterly (links break)
- [ ] Update examples annually (keep current)
- [ ] Gather student feedback on materials
- [ ] Refine based on assessment results

### Documentation Best Practices

**IMPORTANT: Update Existing Docs, Don't Create New Ones**

The documentation has been consolidated to maintain a single source of truth. Before creating new documentation:

**1. Check [docs/INDEX.md](../docs/INDEX.md) First**

| Your Content | Add It To |
|--------------|-----------|
| Slide layout | docs/SLIDE-LAYOUTS.md |
| Validation check | docs/VALIDATION-GUIDE.md |
| Architecture change | docs/ARCHITECTURE.md |
| Workflow improvement | .claude/CLAUDE.md |
| Content rule | `.claude/skills/content-generation/` |
| Code standards | CONTRIBUTING.md |

**2. When New Docs Are Acceptable**

- **Major feature** (>1,000 lines of docs): `docs/FEATURE-NAME.md`
- **New system component**: Separate reference doc in `docs/`
- **Temporary task tracking**: Use `.working/` (will be archived)
- **Project planning**: In `docs/` (archive when complete)

**3. Quick Review Checklist**

Before committing documentation:
- [ ] Checked INDEX.md - does this fit in existing doc?
- [ ] Won't create duplicate information?
- [ ] Updated INDEX.md if creating new doc?
- [ ] All cross-references still valid?

**4. Documentation Locations**

```
Root:      README.md, CONTRIBUTING.md
.claude/:  CLAUDE.md, WORKING-DOCS-SYSTEM.md, commands/*.md
docs/:     INDEX.md, SLIDE-LAYOUTS.md, VALIDATION-GUIDE.md, ARCHITECTURE.md
```

**Remember:** Add to existing docs rather than creating new ones. The consolidation effort reduced volume by 40% while losing zero information.

---

## Coding Standards & Architecture

**All Python code must follow SOLID principles, PEP 8, and maintain high quality standards.**

**See [CONTRIBUTING.md](../CONTRIBUTING.md) for complete coding standards, including:**
- SOLID principles and Clean Code guidelines
- File organization requirements (max 500 lines per file)
- Constants and configuration patterns
- Type hints and documentation requirements
- Error handling and testing standards
- Code review checklist
- Refactoring guidelines

**Quick Reference:**
- **No magic numbers** - Use config classes (LayoutConfig, FontConfig, ColorConfig)
- **No files >500 lines** - Split into modules
- **No functions >50 lines** - Extract methods
- **Type hints required** - All function parameters and returns
- **Tests required** - 80%+ coverage for new code
- **No monolithic files** - Modular architecture only

**Current Refactoring:**
- HTML to PPTX Converter: See `docs/REFACTORING_PLAN.md` for status
- Apply same standards to all content generation scripts

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
- Content instructions: `.claude/skills/content-generation/`
- Quick start: `README.md`
- Sample syllabus: `samples/BUSINESS COMMUNICATION Syllabus Fall 2025.md`

**Research Resources:**
- Top schools (US - 10 total): HBS, Stanford GSB, Wharton, MIT Sloan, Chicago Booth, Columbia, Kellogg, Berkeley Haas, Yale SOM, Dartmouth Tuck
- Top schools (UK - 9 total): LBS, Oxford Saïd, Cambridge Judge, Imperial, Warwick, LSE, Edinburgh, Manchester Alliance MBS, Cranfield
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

**v1.7** - Phase 3: Batch Generation & Quality Enhancement (January 20, 2025)
- Implemented Phase 3A: End-to-end batch generation
  - New command: `/generate-course [COURSE-CODE]`
  - Generates all weeks + slides in one command (7-12 hours for 10-week course)
  - Progress tracking with recovery support (Decision 1A: resume from interrupted week)
  - Validation failures skip week, continue with others (Decision 2B)
  - Always exports slides automatically (Decision 3A)
  - Time savings: 1 command vs. 20 commands (10× weeks + 10× slides)
- Implemented Phase 3B: Cross-week quality enhancement
  - New command: `/enhance-coherence [COURSE-CODE]`
  - Analyzes: Terminology, scaffolding, examples, cross-references, citations
  - Scores all issues 1-10 for quality impact (Decision 3C)
  - User chooses enhancement types to apply (Decision 1C)
  - Git commit backup before changes (Decision 2B)
  - Typical improvement: +1.0 to +1.5 coherence score (15-30 min)
- Created `.claude/commands/generate-course.md` - Full batch generation spec
- Created `.claude/commands/enhance-coherence.md` - Full coherence enhancement spec
- Updated CLAUDE.md with Phase 3 workflow (recommended approach)
- Updated Quick Start Guide with batch generation options
- Benefits: 40% time savings, professional coherence, true end-to-end automation

**v1.6** - Validation Flags for Proactive Error Detection (January 20, 2025)
- Implemented Phase 2: Validation flags system
- Claude Desktop creates `.week-[N]-ready` flag files after writing research
- `/generate-week` automatically detects and validates flagged research
- Prevents wasting 45-70 min generating content with invalid research
- Auto-deletes flags after successful validation
- Updated `desktop-research-with-autowrite.md` with flag creation step
- Updated `/generate-week` command with Step 0.0 flag check
- Comprehensive documentation in `RESEARCH-HANDOFF-GUIDE.md`
- Fully backward compatible (works with or without flags)

**v1.5** - MCP Auto-Write for Research Import (January 20, 2025)
- Added MCP-based auto-write capability for research handoff from Claude Desktop
- Created `.claude/mcp-config/desktop-commander-research.json` for MCP filesystem configuration
- Created `.claude/templates/desktop-research-with-autowrite.md` for auto-write research workflow
- Updated `/import-research` command to detect and validate auto-imported research
- Enhanced `docs/RESEARCH-HANDOFF-GUIDE.md` with MCP setup instructions and dual-method workflow
- Time savings: 2-5 min/week (20-50 min per 10-week course) vs manual copy/paste
- Benefits: Zero copy/paste errors, format guaranteed, seamless handoff
- Backward compatible: Manual paste still fully supported as fallback

**v1.4** - GIFT Quiz Export Automation (January 19, 2025)
- Added `week-[N]-quiz.gift` as fourth mandatory output file for `/generate-week`
- Automated export of tutorial quiz questions to Moodle GIFT format
- Quiz export includes feedback for correct and incorrect answers
- New tool: `tools/export_quiz_to_gift.py` for automated conversion
- Updated file structure to show GIFT file in week folders
- Updated quality standards checklist to include GIFT validation
- Step 3.6 added to `/generate-week` command documentation

**v1.3** - Separate Tutor Notes Files (January 19, 2025)
- Added `tutorial-tutor-notes.md` as third output file for `/generate-week`
- Separation of student-facing (`tutorial-content.md`) and tutor-facing (`tutorial-tutor-notes.md`) materials
- Tutor notes include: quiz answer keys, expected student approaches, facilitation guidance
- Updated file structure, quality standards, and documentation throughout CLAUDE.md
- Cleaner student materials without instructor guidance or answers

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
