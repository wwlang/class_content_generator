# /generate-syllabus

Create a research-backed course syllabus through interactive steps.

## Step 1: Course Setup

**Gather from user:**
- University, qualification, campus
- Course code and title
- Semester/year
- Grading system (US 60% / UK 40% / Vietnamese)
- Any existing documents to reference

**Course Structure (Standard):**
- **All courses: 12 weeks total**
  - Weeks 1-10: Content delivery
  - Week 11: Assignment prep lecture + in-class quiz during tutorial
  - Week 12: Final presentations

**Create directories:**
```
courses/[COURSE-CODE]/
├── .working/
│   └── research/          ← Desktop saves here
├── assessments/
├── rubrics/
└── weeks/
```

**Output:** `course-info.md`

## Step 2: Research (Desktop or Direct)

**Ask:** "Use Claude Desktop for research? (recommended)"

### Option A: Claude Desktop (recommended)

1. **Generate research prompt** from template:
   - Read `.claude/templates/desktop-course-research-template.md`
   - Fill in placeholders with course info
   - Set output path: `[PROJECT-ROOT]/courses/[COURSE-CODE]/.working/research/`

2. **User copies prompt to Desktop** and completes research

3. **Desktop outputs** (saved via MCP filesystem):
   - `syllabus-research.md` - Course description, learning objectives (5-8), weekly structure
   - `week-01-research.md` through `week-10-research.md` - Articles per week

4. **Import and validate:**
   ```
   /import-research [COURSE-CODE]
   ```

### Option B: Direct Research (fallback)

- Load skill: `research/SKILL.md`
- Research course description from top schools
- Draft 5-8 learning objectives (best practice per Cornell/UC Berkeley)
- 4-stage article research per week (30-50 min each)

**Article balance:** 2 seminal + 2 recent per week

---

### Learning Objectives Best Practice

**Target:** 5-8 course-level outcomes total

**Draft outcomes that:**
1. Span Bloom's levels (knowledge → synthesis) without rigid categories
2. Are measurable and assessable
3. Align with course description promises
4. Match what top schools emphasize for this subject
5. Use strong action verbs (apply, analyze, create, evaluate, design)

**Optional grouping** by theme (e.g., Written, Oral, Analytical) rather than Bloom levels.

**Anti-pattern:** Do NOT create 3-5 per Bloom category (12-20 total). Exceeds best practice.

## Step 3: Assessment Design

**After research complete** (so assessments match actual content):

**Ask:** "Which structure?"
- Portfolio + Presentation + Quiz
- Exam + Project + Quiz
- Custom mix

Design assessments aligned to researched frameworks.

**Output:** `assessments/assessment-schedule.md`

## Step 4: Rubrics

Load appropriate templates:
- `written-work-rubric.md`
- `presentation-rubric.md`
- `project-rubric.md`

Customize for specific assignments.

## Step 5: Document Structure

**Ask:** "Single or two-document structure?"

| Option | When to Use |
|--------|-------------|
| Single syllabus | 2-3 assessments, <25 pages |
| Syllabus + Handbook | 3+ assessments, >30 pages |

## Step 6: Synthesize Syllabus

- Combine all sections
- Verify all URLs accessible
- Quality check against checklist
- Save final documents

**General Information Format:** Use table with proper headers:

| Field | Value |
|-------|-------|
| **Course Code** | [CODE] |
| **Course Title** | [TITLE] |
| **Program** | [PROGRAM] |
| **Duration** | 12 weeks |
| **Instructor** | [NAME] |
| **Email** | [EMAIL] |
| **Phone** | [PHONE] |

**Course Calendar Format:** Use table format with FULL detail preserved:

| Week | Topic | Key Concepts | Foundational Frameworks | Required Reading | Assessment Due |
|------|-------|--------------|------------------------|------------------|----------------|
| 1 | **Topic Name**: Theme description | - **Key term/phrase**: elaboration text<br>- **Another key concept**: explanation<br>- **Third concept**: details<br>- **Fourth concept**: more detail | - Framework (Author, Year)<br>- Framework (Author, Year) | - Author, A. B., & Author, C. D. (Year). *Book title* (edition, Ch. X-Y). Publisher.<br>- Author, E. F. (Year). Article title. *Journal Name*, *Volume*(Issue), pages. | Assessment name (%) |

**IMPORTANT:**
- Topic column format: **Topic Name**: Theme description (on same line)
- Use bulleted lists (with `<br>` tags) for Key Concepts, Frameworks, and Readings - NOT semicolons
- Each item on its own line starting with `-`
- **Bold the key term/phrase** in each Key Concept for easy scanning
- Include ALL key concepts (3-5 per week) - never summarize or abbreviate
- Include ALL foundational frameworks with full citations
- **Required Reading format**: Full APA 7th edition citations (2-3 per week)
  - Books: Author, A. B. (Year). *Title* (edition, Ch. X-Y). Publisher.
  - Articles: Author, A. B. (Year). Title. *Journal*, *Volume*(Issue), pages.
  - Use italics for book/journal titles (markdown `*asterisks*`)
- Include assessment due dates where applicable

**Standard Course Policies (use simplified versions):**

**Group Work:**
- All portfolio assignments and presentations are completed in groups of 2-4 members
- Groups must be formed by **Week 3** and remain consistent throughout the semester
- Inform instructor of group composition via email by end of Week 3 for LMS records

**Participation Policy (10%):**

Attendance (5%):
- Attendance is mandatory and taken within the first 10 minutes of each class
- Students arriving after attendance is marked absent
- 2 absences allowed without penalty; each additional absence reduces participation grade

Active Participation (5%):
- Complete all in-class quizzes and activities
- Deductions for incomplete or missing in-class work
- Professional conduct during class sessions

**Do NOT include:**
- Attribution lines like "Course design informed by syllabi analysis from Harvard Business School..."
- AI and Technology Use Policy sections (still under discussion)
- Detailed group work expectations, conflict resolution procedures, or non-contributing member policies
- Subjective participation criteria ("engaged in discussions," "quality over quantity," etc.)

**Outputs:**
- `syllabus.md` (always)
- `assessment-handbook.md` (if two-doc)
- Research notes in `.working/research/`

## Step 7: Export

**After user approves syllabus:**

Auto-export syllabus to professional DOCX format:

```bash
source venv/bin/activate && python tools/markdown_to_docx.py [COURSE-CODE] syllabus
```

**Features:**
- Professional footer: `Course Code | University | Campus | Instructor | Page X of Y`
- Formatted headings, tables, lists
- Ready for distribution to students

**Output:** `syllabus.docx` (in course folder)

## Time Estimate

| Method | Code Time | Total Time |
|--------|-----------|------------|
| Desktop | 2-2.5 hrs | 7-10.5 hrs |
| Direct | 6-9.5 hrs | 6-9.5 hrs |
