# /generate-week [week-number]

Generate complete weekly content: lecture, tutorial, tutor notes, and quiz.

## Prerequisites

- Syllabus exists with weekly topics
- Assessment schedule documented
- Research imported (check `.working/research/week-N-research.md`)

## Workflow

### Step 0: Pre-Flight (Before generating)

1. **Create TODO list** using TodoWrite tool to track progress
2. **Read required files:**
   - `syllabus.md` - Week topic, key concepts, learning objectives
   - `.working/research/week-N-research.md` - 4 articles (2 seminal + 2 recent)
   - `assessment-handbook.md` - Rubric details for tutorial alignment
3. **Load skills:**
   - `content-generation/lecture-structure.md`
   - `content-generation/speaker-notes.md`
   - `assessment-design/tutorial-activities.md`
   - `assessment-design/quiz-questions.md`

### Step 1: Validate Research
```
IF .week-N-ready flag exists:
  → Validate research format and content
  → Delete flag if valid, stop if invalid
ELSE:
  → Check for week-N-research.md
  → Warn if missing, offer to research now
```

### Step 2: Generate Lecture (22-30 slides)

**Load skill:** `content-generation/lecture-structure.md`

**Structure:**
- Opening: 4-6 slides (hook, objectives, roadmap)
- Core: 14-20 slides (3-4 segments)
- Wrap-up: 4-6 slides (synthesis, preview)

**Per slide include:**
- Slide content (150-200 words max)
- Speaker notes (see `content-generation/speaker-notes.md`)
- Layout hint if non-standard (see `content-generation/layout-variety.md`)
- Citations inline (see `content-generation/citations.md`)

**Output:** `lecture-content.md`

### Step 3: Generate Quiz Questions

**Load skill:** `assessment-design/quiz-questions.md`

**Inputs:**
- lecture-content.md (key concepts, frameworks)
- syllabus.md (week learning objectives)
- Assessment schedule (which quiz this prepares for)

**Structure:**
- 5-8 questions covering lecture concepts
- Mix of question types (MC, T/F, matching)
- Scenario-based when possible
- Full feedback for all answer options

**Output:** `quiz-questions.md`

### Step 4: Generate Tutorial (90 min)

**Load skill:** `assessment-design/tutorial-activities.md`

**Structure:**
| Phase | Time | Content |
|-------|------|---------|
| Quick Review | 5 min | Lecture recap + success criteria |
| Main activity | 75 min | ONE task with deliverable + class feedback |
| Before Next Class | 10 min | 3 items: quiz, prereading, save work |

**Key rules:**
- NO inline timing (timing in tutor-notes only)
- NO separate Assessment Connection section (in header)
- NO Quiz Prep section (online via LMS)
- Reference Assessment Handbook for full rubric

**Output:** `tutorial-content.md` (student-facing, ~80 lines)

### Step 5: Generate Tutor Notes

**Include:**
- **Timing table at top** (phase breakdowns with flex notes)
- 3-5 valid student approaches
- Facilitation guidance per activity phase
- Cultural tips for Vietnamese students
- Common misconceptions to address

**Do NOT include:**
- Quiz answer key (now in quiz-questions.md)

**Output:** `tutorial-tutor-notes.md`

### Step 6: Export Quiz (GIFT Format)

Convert quiz-questions.md to Moodle GIFT format.

**Output:** `output/week-N-quiz.gift`

### Step 7: Generate Gemini Handoff

Create ready-to-paste prompt for Gemini slide creation.

**Template:** `.claude/templates/gemini-slide-handoff-prompt.md`

**Include:**
- Course details (code, name, week, topic, instructor)
- Batch structure (Slides 1-10, 11-20, 21-N)
- Layout hints interpreted for Gemini
- First 10 slides of lecture content
- Troubleshooting section

**Output:** `gemini-handoff.md`

### Step 8: Export DOCX Files

Convert tutorial files to professional DOCX in `output/` subfolder.

**Run:**
```bash
source venv/bin/activate && python3 tools/markdown_to_docx.py [CODE] [N]
```

**Converts:**
- `tutorial-content.md` → `output/tutorial-content.docx`
- `tutorial-tutor-notes.md` → `output/tutorial-tutor-notes.docx`

**Footer format:** `CODE | University | Campus | Instructor | Page X of Y`

## Output Files

```
courses/[CODE]/weeks/week-[N]/
├── lecture-content.md        # Source: slides + speaker notes
├── quiz-questions.md         # Source: human-readable quiz
├── tutorial-content.md       # Source: student activities (~80 lines)
├── tutorial-tutor-notes.md   # Source: timing table + facilitation
├── gemini-handoff.md         # Handoff: ready-to-paste Gemini prompt
└── output/                   # Deliverables folder
    ├── tutorial-content.docx
    ├── tutorial-tutor-notes.docx
    ├── week-N-quiz.gift
    └── slides.pptx           # (after Gemini + speaker notes)
```

## Quality Checklist

- [ ] 22-30 slides with layout variety (see skill)
- [ ] Speaker notes for every slide
- [ ] Citations with working URLs
- [ ] Quiz questions (5-8) in quiz-questions.md
- [ ] Tutorial has consolidated activity with deliverable
- [ ] Tutorial has participation warning for class feedback
- [ ] Tutorial references Assessment Handbook for rubric
- [ ] Tutor notes has timing table at top
- [ ] Vietnamese cultural adaptations included
- [ ] Gemini handoff has correct slide count and batches
- [ ] DOCX exports created for tutorial files

## Time Estimate

45-70 minutes per week
