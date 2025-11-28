# Assessment Handbook Generation

Generate complete assessment handbooks from syllabus data that are parseable by `HandbookParser`.

---

## Purpose

Create a comprehensive assessment handbook that:
1. Consolidates all assessment information in one student-facing document
2. Can be parsed by `HandbookParser` to extract Assessment objects
3. Provides detailed rubrics, scenarios, requirements, and submission formats
4. References existing rubric files without duplication

---

## Input Requirements

### From syllabus.md

Extract these elements:

**Course Metadata:**
- Course code (e.g., "BCI2AU")
- Course title (e.g., "Business Communication")
- Instructor name, email, phone
- Program (e.g., "BA in International Business")

**Assessment Overview Table:**
- Assessment name
- Type (Portfolio, Presentation, Quiz, Project)
- Weight (percentage of final grade)
- Due week
- Learning objectives addressed

**Weekly Topics and Frameworks:**
- Extract from "Course Calendar" table
- Map what frameworks are taught in each week
- Used to ensure scenarios only reference frameworks taught BEFORE assessment due week

**All Learning Objectives:**
- Complete list (usually 15-20)
- Used to map assessments to objectives

### From assessment-schedule.md (if exists)

- Detailed requirements per assessment
- Submission format instructions
- File naming conventions

### From rubrics/*.md

- All rubric markdown tables
- Rubric names and descriptions
- Performance level descriptors

---

## Output Structure

### Required Document Sections (in order)

```markdown
# [COURSE-CODE]: [Course Name]

## Assessment Handbook

## Table of Contents

[Auto-generated list of sections]

---

## Assessment Overview

[Table from syllabus with columns: Assessment | Type | Weight | Due | Learning Objectives]

---

## Portfolio Assessments ([total weight]%)

[Description of portfolio approach]

### 1. [Assessment Name] ([weight]%)

**Due:** End of Week [N]
**Weight:** [weight]%

#### Task Overview

[2-3 sentence description of what students will produce]

#### Scenario (Choose ONE)

[2-4 scenario options - see Scenario Generation section]

#### Requirements

[Checklist of requirements with [ ] checkboxes]

#### Submission Format

[Instructions for file format, naming, submission method]

#### Rubric Preview

[Table showing criteria and weights - link to full rubric below]

---

[Repeat for each portfolio assessment]

---

## Presentation Assessments ([total weight]%)

[Description of presentation approach]

### [N]. [Assessment Name] ([weight]%)

[Same structure as portfolio assessments above]

---

## Quizzes ([total weight]%)

[Standard boilerplate - see Boilerplate Sections below]

---

## Rubrics

### [Rubric Name]

Used for: [List of assessments using this rubric]

[Full rubric table with 5 performance levels]

---

[Repeat for each rubric]

---

## Tips for Success

### For Written Assessments

[5 practical tips]

### For Presentations

[5 practical tips]

### For Quizzes

[5 practical tips]

### General Success Strategies

[5 general tips]

---

## Questions?

[Contact information and support resources]

---

*This handbook supplements the main syllabus. Both documents together provide complete course information.*
```

---

## Scenario Generation

Load `scenario-generation.md` skill for detailed patterns and rules.

### Core Principles

1. **Framework Alignment:**
   - Extract frameworks taught in weeks 1 to (due_week - 1)
   - Each scenario must apply 2-3 specific frameworks
   - Example: Week 3 assessment uses Pyramid Principle (Week 2), BLUF (Week 3)

2. **Structural Consistency:**
   - Always provide 2-3 options labeled A, B, C (or D if appropriate)
   - Option C (or last option) is usually "Create Your Own (Instructor approval required)"
   - Options A/B must be genuinely different (not minor variations)

3. **Business Context:**
   - Use realistic business scenarios (not academic exercises)
   - Include specific deliverables (word counts, formats)
   - Specify audience when relevant (VP, COO, investors)

4. **Specificity:**
   - Include: who, what, why, constraints
   - Example: "Marketing VP considering market entry" (not just "senior leader")
   - Deliverables are measurable: "150-word email" (not "persuasive email")

5. **Complexity Matching:**
   - Week 3 scenarios: simpler, individual documents
   - Week 7 scenarios: complex, multi-part deliverables
   - Week 10 scenarios: comprehensive, integrated applications

### Scenario Format

```markdown
#### Scenario (Choose ONE)

**Option A: [Scenario Title]**
[Brief description of context and task]
- [Specific requirement 1]
- [Specific requirement 2]

**Option B: [Scenario Title]**
[Brief description of context and task]
- [Specific requirement 1]
- [Specific requirement 2]

**Option C: Create Your Own** (Instructor approval required)
- [Brief description of flexibility and approval process]
```

---

## Requirements Checklists

Generate specific, measurable requirements for each assessment.

### Format

Use checkbox format (parser expects this):

```markdown
#### Requirements

**[Section Name]:**
- [ ] Requirement 1 (specific and measurable)
- [ ] Requirement 2 (specific and measurable)
- [ ] Requirement 3 (specific and measurable)

**[Section Name]:**
- [ ] Requirement 1
- [ ] Requirement 2
```

### Guidelines

- **Specific:** "Clear subject line" not "Good subject line"
- **Measurable:** "250-350 words" not "Appropriate length"
- **Actionable:** "Include 3 supporting arguments" not "Support your point"
- **Format-focused:** "Professional greeting" not "Be professional"

### Examples

**Email + Memo Requirements:**
```markdown
**Email Requirements:**
- [ ] Clear, specific subject line
- [ ] Professional greeting appropriate to relationship
- [ ] BLUF (Bottom Line Up Front) structure
- [ ] Specific ask with clear next steps
- [ ] Professional closing and signature
- [ ] 250-350 words

**Memo Requirements:**
- [ ] Proper memo header (To, From, Date, Subject)
- [ ] Executive summary in first paragraph
- [ ] Pyramid structure (conclusion first, then supporting points)
- [ ] At least 3 supporting arguments with evidence
- [ ] Clear recommendation and call to action
- [ ] 400-500 words
```

---

## Boilerplate Sections

### Quizzes Section

```markdown
## Quizzes ([total weight]%)

Three quizzes assess your understanding of key concepts, frameworks, and their application.

### Quiz Format

Each quiz consists of:
- **25-30 questions**
- **Duration:** 30 minutes
- **Format:** Multiple choice, scenario application, short answer
- **Open book:** No (closed book, no notes, no devices)

### Quiz Schedule

| Quiz | Coverage | Due | Weight |
|------|----------|-----|--------|
| Quiz 1 | Weeks 1-3 | Week 4 | [weight]% |
| Quiz 2 | Weeks 4-6 | Week 7 | [weight]% |
| Quiz 3 | Weeks 7-9 | Week 10 | [weight]% |

### Question Types

**Recall (30%):** Key concepts, definitions, framework components
> *Example: According to Barbara Minto's Pyramid Principle, where should the main conclusion appear in a business document?*

**Application (40%):** Applying frameworks to scenarios
> *Example: A manager needs to communicate a significant organizational change to employees. Using the BLUF technique, how should they structure the first paragraph of their memo?*

**Analysis (30%):** Evaluating communication examples
> *Example: Review this email response to an angry customer. Which of Cialdini's principles could improve its effectiveness?*

### Study Resources

- Lecture slides and notes
- Required readings
- Tutorial practice questions
- Review sessions in class before each quiz
```

### Tips for Success

```markdown
## Tips for Success

### For Written Assessments

1. **Start with your conclusion** - Apply the Pyramid Principle to every document
2. **Know your audience** - Before writing, ask "What does my reader need?"
3. **Revise ruthlessly** - Cut 20% of your first draft; every word should earn its place
4. **Read aloud** - Catches awkward phrasing and unclear sentences
5. **Get feedback early** - Use tutorial peer reviews to improve before submission

### For Presentations

1. **Practice out loud** - At least 5 full run-throughs before presenting
2. **Time yourself** - Being 2 minutes over is unprofessional
3. **Prepare for Q&A** - Anticipate 5 likely questions and prepare answers
4. **Video yourself** - Watch for distracting habits you don't notice
5. **Arrive early** - Technical issues happen; give yourself buffer time

### For Quizzes

1. **Review weekly** - Don't cram; cumulative review beats last-minute studying
2. **Practice application** - Most questions are scenarios, not definitions
3. **Know the frameworks** - Pyramid Principle, Cialdini, Tufte principles, etc.
4. **Use tutorial quizzes** - Same format as actual quizzes
5. **Connect concepts** - Understand how frameworks relate to each other

### General Success Strategies

1. **Attend every class** - Activities and discussions cannot be made up
2. **Participate in tutorials** - Peer feedback is invaluable
3. **Start assessments early** - Leave time for revision and improvement
4. **Visit office hours** - Get feedback before submission, not after
5. **Apply concepts immediately** - Use course frameworks in your other classes and work
```

### Questions Section

```markdown
## Questions?

- **Assessment clarifications:** Email instructor before due date
- **Rubric questions:** Raise in tutorial for whole-class discussion
- **Technical issues:** Contact instructor immediately; don't wait until deadline

---

*This handbook supplements the main syllabus. Both documents together provide complete course information.*
```

---

## Rubric Preview Tables

Each assessment section should include a **Rubric Preview** that shows criteria and weights, then links to the full rubric.

### Format

```markdown
#### Rubric Preview

| Criteria | Weight | Focus |
|----------|--------|-------|
| [Criterion 1] | [weight]% | [Brief focus description] |
| [Criterion 2] | [weight]% | [Brief focus description] |
| [Criterion 3] | [weight]% | [Brief focus description] |

See [Rubric Name](#rubric-name) for full details.
```

### Example

```markdown
#### Rubric Preview

| Criteria | Weight | Focus |
|----------|--------|-------|
| Content & Strategy | 25% | Message suits audience/purpose; strategic approach |
| Organization | 25% | Clear structure; BLUF/Pyramid principle applied |
| Clarity & Concision | 20% | Clear meaning; economical language |
| Tone & Professionalism | 15% | Professional register; audience-appropriate |
| Mechanics | 15% | Grammar, spelling, formatting |

See [Written Communication Rubric](#written-communication-rubric) for full details.
```

---

## Parser Compatibility Rules

**CRITICAL:** The handbook must be parseable by `HandbookParser`. Follow these rules exactly:

### 1. Assessment Overview Table

**Required format:**
```markdown
## Assessment Overview

| Assessment | Type | Weight | Due | Learning Objectives |
|------------|------|--------|-----|---------------------|
| Email + Memo | Portfolio | 10% | Week 3 | 1, 2, 9, 12 |
```

**Parser expects:**
- Section header: `## Assessment Overview`
- Table with 5 columns (Assessment, Type, Weight, Due, Learning Objectives)
- Type values: Portfolio, Presentation, Quiz, Project
- Weight: number followed by %
- Due: "Week N" format
- Learning Objectives: comma-separated numbers or ranges (e.g., "1-8" or "1, 2, 9, 12")

### 2. Assessment Sections

**Required format:**
```markdown
### 1. Email + Memo (10%)

**Due:** Week 3
**Weight:** 10%

#### Task Overview
[Description]

#### Scenario (Choose ONE)
[Options A, B, C]

#### Requirements
[Checklist]

#### Submission Format
[Instructions]

**File naming:** StudentNumber_Name_EmailMemo_Week3.docx

#### Rubric Preview
[Table]
```

**Parser expects:**
- Section header: `### N. [Name] ([weight]%)`
- Subsections with `####` headers
- Scenario section with "Choose ONE" in header
- Requirements as bulleted list (may have checkboxes)

### 3. Scenario Options

**Required format:**
```markdown
#### Scenario (Choose ONE)

**Option A: [Title]**
[Description]

**Option B: [Title]**
[Description]

**Option C: Create Your Own** (Instructor approval required)
```

**Parser expects:**
- Options labeled A, B, C (or D)
- Bold option headers: `**Option A: Title**`
- Last option often "Create Your Own"

### 4. Requirements

**Parser-friendly format:**
```markdown
#### Requirements

**Section Name:**
- [ ] Requirement 1
- [ ] Requirement 2

**Section Name:**
- [ ] Requirement 3
```

**Parser expects:**
- Bulleted list with optional `[ ]` checkboxes
- Parser strips checkboxes when extracting

### 5. Rubrics Section

**Required format:**
```markdown
## Rubrics

### Written Communication Rubric

Used for: Email + Memo, Data Visualization Report, Persuasive Proposal

| Criteria | Excellent (94-100%) | Good (84-93%) | Satisfactory (74-83%) | Poor (60-73%) | Failing (<60%) |
|----------|---------------------|---------------|----------------------|---------------|----------------|
| **Content & Strategy** | [Description] | [Description] | [Description] | [Description] | [Description] |
```

**Parser expects:**
- Section header: `## Rubrics`
- Subsections: `### [Rubric Name] Rubric`
- Optional "Used for:" line
- Table with 6 columns (Criteria + 5 performance levels)
- Bold criterion names: `**Criterion Name**`

---

## Validation Checklist

Before saving the handbook, validate:

### Structure
- [ ] All required sections present and in correct order
- [ ] Section headers use correct markdown levels (##, ###, ####)
- [ ] Table of Contents generated and links work
- [ ] Assessment Overview table has all assessments

### Content
- [ ] All non-quiz assessments have scenarios (2-4 options each)
- [ ] All non-quiz assessments have requirements checklist
- [ ] All non-quiz assessments have submission format
- [ ] All non-quiz assessments have rubric preview
- [ ] Quizzes section uses standard boilerplate
- [ ] All rubrics included in Rubrics section

### Parser Compatibility
- [ ] Assessment Overview table has correct format
- [ ] Assessment sections use `### N. Name (weight%)`
- [ ] Scenario sections have "Choose ONE" in header
- [ ] Options labeled A, B, C with bold headers
- [ ] Rubric tables have 6 columns
- [ ] Criterion names in bold

### Quality
- [ ] Scenarios reference appropriate frameworks
- [ ] Scenarios use only frameworks taught before due week
- [ ] Requirements are specific and measurable
- [ ] Language is professional and clear
- [ ] Rubric criteria align with assessment types

---

## Example Generation Workflow

```
1. Extract metadata from syllabus:
   - Course info: BCI2AU, Business Communication, Instructor: William Lang
   - Assessments: 6 non-quiz (Email+Memo, Data Viz, Proposal, Reflection, Mini-Pitch, Final)
   - Frameworks by week: Week 2 = Pyramid Principle, Week 3 = BLUF, etc.

2. Load scenario-generation.md for patterns

3. Generate scenarios for each assessment:
   - Email + Memo (Week 3): Use Dual-Format pattern, frameworks Week 1-2 only
   - Data Viz (Week 5): Use Audience-Specific pattern, frameworks Week 1-4
   - Proposal (Week 7): Use Business Proposal pattern, frameworks Week 1-6

4. Assemble handbook:
   - Header + TOC
   - Assessment Overview table
   - Portfolio section (4 assessments)
   - Presentation section (2 assessments)
   - Quizzes section (boilerplate)
   - Rubrics section (from rubrics/*.md)
   - Tips section (boilerplate)
   - Questions section (boilerplate)

5. Validate with HandbookParser:
   ```python
   from tools.assessment_domain import HandbookParser
   parser = HandbookParser()
   assessments = parser.parse_file("assessment-handbook.md")
   assert len(assessments) == 6  # All non-quiz assessments
   ```

6. Export to DOCX:
   ```bash
   python3 tools/markdown_to_docx.py [COURSE_CODE] assessment-handbook
   ```
```

---

## Common Mistakes to Avoid

1. **Including frameworks not yet taught:** Week 3 assessment references Week 5 framework
2. **Generic scenarios:** "Write a business proposal" instead of specific context
3. **Missing requirements:** No word count, no format specification
4. **Duplicating rubrics:** Full rubric in assessment section AND rubrics section
5. **Wrong markdown levels:** Using `##` for assessment names instead of `###`
6. **Missing "Choose ONE":** Scenarios section doesn't indicate selection requirement
7. **Vague deliverables:** "Persuasive email" instead of "150-word persuasive email"
8. **Inconsistent option labels:** Using "1, 2, 3" instead of "A, B, C"

---

## Integration Points

This skill is used by:
- `/generate-handbook` command (standalone handbook generation)
- `/generate-syllabus` command (Step 5.6 - automatic handbook generation)

This skill references:
- `scenario-generation.md` (for scenario patterns and rules)
- `tools/assessment_domain/parsers/handbook_parser.py` (defines format expectations)
- `tools/assessment_domain/models/assessment.py` (Assessment object structure)

---

## Testing

After generation, test with:

```python
from pathlib import Path
from tools.assessment_domain.parsers.handbook_parser import HandbookParser

# Parse handbook
parser = HandbookParser()
handbook_path = Path("courses/[CODE]/assessment-handbook.md")
assessments = parser.parse_file(handbook_path)

# Validate
print(f"Assessments parsed: {len(assessments)}")
for aid, assessment in assessments.items():
    errors = assessment.validate()
    if errors:
        print(f"Validation errors for {aid}:")
        for error in errors:
            print(f"  - {error}")
    else:
        print(f"✓ {aid}: {assessment.name} ({len(assessment.scenarios)} scenarios)")
```

Expected output: All assessments parse successfully with 0 validation errors.
