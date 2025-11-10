# Create New Course Structure

Scaffolds a complete directory structure for a new course with all necessary folders and placeholder files.

## Your Task

Create an organized course directory with all necessary subdirectories and template files to support course content generation.

## Usage

**User provides:**
1. Course code (e.g., BUS101, ECON201, MGT301)
2. Course name (e.g., "Business Communication", "Microeconomic Theory")
3. Number of weeks (typically 10-11, but can vary)

**You create:**
- Complete directory structure
- Placeholder files
- Course info document
- Assessment schedule template

## Step-by-Step Process

### Step 1: Gather Information

**Ask user:**
```
I'll create a new course structure for you.

1. Course Code: [e.g., BUS101]
2. Course Name: [e.g., Business Communication]
3. Number of weeks: [e.g., 11]
```

**Parse inputs:**
- Course code: Uppercase, no spaces
- Course name: Title case, convert to slug for folder (e.g., "Business Communication" → "business-communication")
- Number of weeks: Integer

### Step 2: Create Directory Structure

**Create the following structure:**

```
courses/
└── [COURSE-CODE]-[course-name-slug]/
    ├── syllabus.md (placeholder)
    ├── course-info.md (template with user inputs)
    ├── rubrics/
    │   ├── written-work-rubric.md (copy from templates)
    │   ├── presentation-rubric.md (copy from templates)
    │   └── project-rubric.md (copy from templates)
    ├── weeks/
    │   ├── week-01/
    │   │   ├── lecture-content.md (placeholder)
    │   │   ├── tutorial-content.md (placeholder)
    │   │   └── slides.md (placeholder)
    │   ├── week-02/ [same structure]
    │   ├── week-03/ [same structure]
    │   └── ... [continue to week-N]
    ├── assessments/
    │   ├── assessment-schedule.md (template)
    │   └── portfolio-guidelines.md (placeholder)
    └── resources/
        ├── case-studies/
        └── examples/
```

**Use Bash commands:**
```bash
mkdir -p courses/[COURSE-CODE]-[slug]/rubrics
mkdir -p courses/[COURSE-CODE]-[slug]/weeks/week-{01..N}
mkdir -p courses/[COURSE-CODE]-[slug]/assessments
mkdir -p courses/[COURSE-CODE]-[slug]/resources/case-studies
mkdir -p courses/[COURSE-CODE]-[slug]/resources/examples
```

### Step 3: Create Course Info File

**File:** `courses/[COURSE-CODE]-[slug]/course-info.md`

**Content:**
```markdown
# {{COURSE_CODE}}: {{COURSE_NAME}}

## Course Metadata

**Course Code:** {{COURSE_CODE}}
**Course Name:** {{COURSE_NAME}}
**Instructor:** William Winterton Lang
**Email:** wil.hoang@gmail.com
**Telephone:** (+84) 344 347 703

**Structure:**
- Number of weeks: {{NUMBER_OF_WEEKS}}
- Course type: [To be determined during syllabus generation]
- Assessment structure: [To be determined during syllabus generation]

**Status:**
- [ ] Syllabus created
- [ ] Week topics defined
- [ ] Articles researched
- [ ] Lecture content generated
- [ ] Tutorial content generated
- [ ] Slides created

## Quick Links

- Syllabus: [syllabus.md](./syllabus.md)
- Assessment Schedule: [assessments/assessment-schedule.md](./assessments/assessment-schedule.md)
- Rubrics: [rubrics/](./rubrics/)

## Week Overview

| Week | Topic | Status | Lecture | Tutorial | Slides |
|------|-------|--------|---------|----------|--------|
| 1 | TBD | Not started | ☐ | ☐ | ☐ |
| 2 | TBD | Not started | ☐ | ☐ | ☐ |
| 3 | TBD | Not started | ☐ | ☐ | ☐ |
[... repeat for all weeks ...]

## Notes

[Add course-specific notes, context, or reminders here]
```

### Step 4: Copy Rubric Templates

**Copy these files from templates to course rubrics folder:**

```bash
cp templates/syllabus-components/rubric-structures/written-work-rubric.md \
   courses/[COURSE-CODE]-[slug]/rubrics/written-work-rubric.md

cp templates/syllabus-components/rubric-structures/presentation-rubric.md \
   courses/[COURSE-CODE]-[slug]/rubrics/presentation-rubric.md

cp templates/syllabus-components/rubric-structures/project-rubric.md \
   courses/[COURSE-CODE]-[slug]/rubrics/project-rubric.md
```

### Step 5: Create Assessment Schedule Template

**File:** `courses/[COURSE-CODE]-[slug]/assessments/assessment-schedule.md`

**Content:**
```markdown
# Assessment Schedule: {{COURSE_CODE}}

## Overview

This document tracks all graded assessments for {{COURSE_NAME}}.

**Total Assessments:** [To be filled during syllabus generation]
**Assessment Types:** [To be filled during syllabus generation]

## Assessment Calendar

| Assessment | Type | Weight | Due Week | Due Date | Status |
|------------|------|--------|----------|----------|--------|
| TBD | TBD | TBD% | TBD | TBD | Not created |

## Assessment Details

### Assessment 1: [Name]
- **Type:** [Portfolio piece / Presentation / Quiz / Exam / Project]
- **Weight:** [X%]
- **Due:** Week [X]
- **Requirements:** [To be defined]
- **Rubric:** [Link to rubric]

[Add more assessments as defined in syllabus]

## Quiz Schedule

| Quiz | Covers Weeks | Due Week | Status |
|------|--------------|----------|--------|
| Quiz 1 | TBD | TBD | Not created |
| Quiz 2 | TBD | TBD | Not created |
| Quiz 3 | TBD | TBD | Not created |

## Preparation Tracking

### Weeks Before Each Assessment

Track which weeks prepare students for each assessment:

**[Assessment Name]:**
- Week [X]: [Skill/concept practiced]
- Week [Y]: [Skill/concept practiced]
- Week [Z]: [Final preparation / due date]

[Repeat for each major assessment]
```

### Step 6: Create Week Placeholder Files

**For each week folder, create these placeholder files:**

**`lecture-content.md`:**
```markdown
# Week {{N}}: [Topic TBD]

**Status:** Not started

This lecture content will be generated using the /generate-week or /create-lecture command after the syllabus is complete.

## Planned Content

**Topic:** [To be determined]
**Key Concepts:** [To be determined]
**Required Readings:** [To be researched]

---

*Use /create-lecture {{N}} to generate content for this week*
```

**`tutorial-content.md`:**
```markdown
# Tutorial Week {{N}}: [Topic TBD]

**Status:** Not started

This tutorial content will be generated using the /generate-week or /create-tutorial command after the syllabus is complete.

## Planned Focus

**Assessment Connection:** [To be determined]
**Main Activity:** [To be designed]
**Quiz Prep:** [To be created]

---

*Use /create-tutorial {{N}} to generate content for this week*
```

**`slides.md`:**
```markdown
# Week {{N}} Slides: [Topic TBD]

**Status:** Not started

Presentation slides will be created after lecture content is approved.

---

*Slides are generated last, after lecture content is finalized*
```

### Step 7: Create Syllabus Placeholder

**File:** `courses/[COURSE-CODE]-[slug]/syllabus.md`

**Content:**
```markdown
# {{COURSE_CODE}}: {{COURSE_NAME}} - Syllabus

**Status:** Not yet created

Use the `/generate-syllabus` command to create a complete, research-backed syllabus for this course.

The syllabus will include:
- Course description and learning objectives
- Assessment structure and grading distribution
- Complete course calendar with researched readings
- Rubrics for all assessments
- Course policies and support resources

---

**Next step:** Run `/generate-syllabus` to begin creating this course syllabus.
```

### Step 8: Confirm Creation

**Output to user:**

```markdown
✓ Course structure created successfully!

## Created Directory Structure

📁 courses/{{COURSE_CODE}}-{{COURSE_NAME_SLUG}}/
   ├── 📄 syllabus.md (placeholder - run /generate-syllabus to create)
   ├── 📄 course-info.md (course metadata and tracking)
   ├── 📁 rubrics/ (3 rubric templates copied)
   │   ├── written-work-rubric.md
   │   ├── presentation-rubric.md
   │   └── project-rubric.md
   ├── 📁 weeks/ ({{NUMBER_OF_WEEKS}} week folders created)
   │   ├── week-01/ (lecture, tutorial, slides placeholders)
   │   ├── week-02/
   │   └── ... [week-{{NUMBER_OF_WEEKS}}]
   ├── 📁 assessments/
   │   └── assessment-schedule.md (template)
   └── 📁 resources/
       ├── case-studies/
       └── examples/

## Next Steps

1. **Create Syllabus:** Run `/generate-syllabus` to build a complete, research-backed syllabus
2. **Generate Weekly Content:** After syllabus is complete, use `/generate-week [N]` for each week
3. **Track Progress:** Update course-info.md as you complete each component

## Quick Access

**Course folder:** `courses/{{COURSE_CODE}}-{{COURSE_NAME_SLUG}}/`
**Course info:** `courses/{{COURSE_CODE}}-{{COURSE_NAME_SLUG}}/course-info.md`

Ready to create your syllabus! Run `/generate-syllabus` when ready.
```

---

## Error Handling

**If course folder already exists:**
```
❌ Error: Course folder already exists at:
   courses/{{COURSE_CODE}}-{{COURSE_NAME_SLUG}}/

Options:
1. Choose a different course code
2. Delete existing folder and recreate
3. Work with existing structure

What would you like to do?
```

**If invalid inputs:**
- Course code empty: Prompt again
- Course name empty: Prompt again
- Number of weeks < 1 or > 20: Ask to confirm unusual length

---

## Customization Options

**Ask user (optional):**
"Would you like to customize the structure?"

**Options:**
- Add additional resource folders (videos/, readings/, etc.)
- Create custom assessment folders
- Add specific placeholders

**Default:** Use standard structure unless user requests customization

---

## Estimated Time

- Directory creation: < 1 minute
- File generation: 1-2 minutes
- **Total: 2-3 minutes** to have a complete course scaffold ready

Fast, organized setup lets you focus on content creation rather than file management.
