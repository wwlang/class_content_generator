# /generate-week [week-number]

Generate complete weekly content using parallel agents for efficiency.

## Prerequisites

- Syllabus exists with weekly topics
- Assessment handbook documented
- Research imported (check `.working/research/week-N-research.md`)

## Workflow Overview

```
Phase 0: Pre-Flight (sequential)
    ↓
Phase 1: Content Generation (PARALLEL)
    ├── Lecture Agent → lecture-content.md
    └── Tutorial Agent → tutorial-content.md + tutorial-tutor-notes.md
    ↓
Phase 2: Lecture-Dependent (PARALLEL, after Phase 1)
    ├── Quiz Agent → quiz-questions.md
    └── Gemini Agent → gemini-prompt.md
    ↓
Phase 3: Exports (sequential)
    ├── GIFT Export → output/week-N-quiz.gift
    └── DOCX Export → output/*.docx
```

---

## Phase 0: Pre-Flight (Sequential)

**Do NOT spawn agents yet.** First gather all context:

### 0.1 Read Required Files

```
courses/[CODE]/syllabus.md
courses/[CODE]/assessment-handbook.md
courses/[CODE]/.working/research/week-N-research.md
```

### 0.2 Validate Research

```
IF week-N-research.md missing:
  → Warn user, offer to run /research-topic
  → STOP (cannot generate without research)
ELSE:
  → Extract key sources for agent prompts
```

### 0.3 Extract Week Context

From syllabus, extract for Week N:
- Topic title
- Key concepts (bullet list)
- Learning objectives
- Required readings

From assessment-handbook, extract:
- Which assessment this week prepares for
- Relevant rubric criteria
- Scenario types if applicable

---

## Phase 1: Parallel Content Generation

**Spawn TWO agents in parallel:**

### Agent 1: Lecture Generation

```
Prompt template:
---
You are generating lecture content for Week [N]: [Topic]

COURSE: [Course Name] (do NOT include course code in slides)
WEEK: [N]
TOPIC: [Topic Title]

CONTEXT:
- Key concepts: [from syllabus]
- Learning objectives: [from syllabus]
- Assessment connection: [from assessment-handbook]

RESEARCH SOURCES:
[Paste validated sources from week-N-research.md]

SKILL INSTRUCTIONS:
[Paste content from .claude/skills/content-generation/lecture-structure.md]

OUTPUT REQUIREMENTS:
- 24-32 slides in XML format
- Opening (5-7 slides): title, hook, objectives, assessment connection, roadmap
- Core (14-20 slides): 3-4 segments with examples
- Wrap-up (5-7 slides): takeaways, preview, resources, references
- Speaker notes for EVERY slide
- Layout hints where appropriate

Write the complete lecture-content.md file.
---
```

**Output:** `lecture-content.md`

### Agent 2: Tutorial Generation

```
Prompt template:
---
You are generating tutorial content for Week [N]: [Topic]

COURSE: [Course Name]
WEEK: [N]
TOPIC: [Topic Title]

CONTEXT:
- Key concepts: [from syllabus]
- Target assessment: [from assessment-handbook]
- Rubric criteria: [relevant criteria for success metrics]

SKILL INSTRUCTIONS:
[Paste content from .claude/skills/assessment-design/tutorial-activities.md]

GENERATE TWO FILES:

FILE 1: tutorial-content.md (~80 lines, student-facing)
Structure:
- Quick Review (5 min): lecture recap + success criteria
- Main Activity (75 min): ONE task with deliverable + class feedback
- Before Next Class (10 min): 3 items only

FILE 2: tutorial-tutor-notes.md
Structure:
- Timing table at top
- 3-5 valid student approaches
- Facilitation guidance
- Cultural tips for Vietnamese students
- Common misconceptions

Write both files completely.
---
```

**Output:** `tutorial-content.md`, `tutorial-tutor-notes.md`

---

## Phase 2: Lecture-Dependent Generation (Parallel)

**Wait for Phase 1 Lecture Agent to complete.** Then spawn TWO agents in parallel:

### Agent 3: Quiz Generation

```
Prompt template:
---
You are generating quiz questions for Week [N]: [Topic]

LECTURE CONTENT:
[Paste the generated lecture-content.md]

CONTEXT:
- Week learning objectives: [from syllabus]
- Assessment this prepares for: [from assessment-handbook]

SKILL INSTRUCTIONS:
[Paste content from .claude/skills/assessment-design/quiz-questions.md]

OUTPUT REQUIREMENTS:
- 12 questions total (4 frameworks × 3 questions each)
- Distribution: 4 Remembering + 8 Understanding
- YAML format per skill template
- NO scenario/application questions (those belong in tutorials)
- ONE clearly correct answer per question

Write the complete quiz-questions.md file.
---
```

**Output:** `quiz-questions.md`

### Agent 4: Gemini Handoff Generation

```
Prompt template:
---
You are generating a Gemini slide creation prompt for Week [N]: [Topic]

LECTURE CONTENT:
[Paste the generated lecture-content.md]

COURSE DETAILS:
- Code: [CODE]
- Name: [Course Name]
- Week: [N]
- Topic: [Topic]
- Instructor: [from course-info.md]

TEMPLATE:
[Paste content from .claude/templates/gemini-slide-handoff-prompt.md]

OUTPUT REQUIREMENTS:
- Ready-to-paste prompt for Google Gemini
- Include all slides (no batching)
- Layout hints interpreted for Gemini
- Troubleshooting section

Write the complete gemini-prompt.md file.
---
```

**Output:** `gemini-prompt.md`

---

## Phase 3: Exports (Sequential)

After all content files exist, run exports:

### 3.1 GIFT Export

```bash
source venv/bin/activate && python3 tools/export_yaml_quiz_to_gift.py [CODE] [N]
```

**Output:** `output/week-N-quiz.gift`

### 3.2 DOCX Export

```bash
source venv/bin/activate && python3 tools/markdown_to_docx.py [CODE] [N]
```

**Output:**
- `output/tutorial-content.docx`
- `output/tutorial-tutor-notes.docx`

---

## Execution Summary

When running `/generate-week [N]`:

1. **Pre-flight:** Read syllabus, assessment-handbook, research (sequential)
2. **Phase 1:** Spawn Lecture Agent + Tutorial Agent (parallel)
3. **Wait:** Until both Phase 1 agents complete
4. **Phase 2:** Spawn Quiz Agent + Gemini Agent (parallel)
5. **Wait:** Until both Phase 2 agents complete
6. **Phase 3:** Run GIFT export + DOCX export (sequential bash commands)
7. **Validate:** Check all output files exist

---

## Output Files

```
courses/[CODE]/weeks/week-[N]/
├── lecture-content.md        # Phase 1: Lecture Agent
├── tutorial-content.md       # Phase 1: Tutorial Agent
├── tutorial-tutor-notes.md   # Phase 1: Tutorial Agent
├── quiz-questions.md         # Phase 2: Quiz Agent
├── gemini-prompt.md          # Phase 2: Gemini Agent
└── output/
    ├── week-N-quiz.gift      # Phase 3: GIFT export
    ├── tutorial-content.docx # Phase 3: DOCX export
    └── tutorial-tutor-notes.docx
```

---

## Quality Checklist

After all phases complete, verify:

**Lecture:**
- [ ] 24-32 slides with layout variety
- [ ] Title slide as slide 1 (topic only, no course code)
- [ ] References slide as final slide
- [ ] Speaker notes for every slide

**Quiz:**
- [ ] 12 questions in YAML format
- [ ] 4 Remembering + 8 Understanding distribution
- [ ] No ambiguous "MOST/PRIMARY" questions

**Tutorial:**
- [ ] ~80 lines, student-facing
- [ ] ONE main activity with deliverable
- [ ] Class feedback section with participation warning
- [ ] Tutor notes has timing table at top

**Exports:**
- [ ] GIFT file imports cleanly to Moodle
- [ ] DOCX files have correct footer format

---

## Time Estimate

15-25 minutes per week (parallel agents reduce from 45-70 minutes)
