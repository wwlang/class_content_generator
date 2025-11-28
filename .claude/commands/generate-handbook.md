---
description: Generate assessment handbook from existing syllabus
---

# Generate Assessment Handbook

You are generating an assessment handbook from an existing syllabus.

This command creates a complete assessment handbook that:
- Consolidates all assessment information in one student-facing document
- Is parseable by `HandbookParser` for extraction into Assessment objects
- Provides detailed rubrics, scenarios, requirements, and submission formats

---

## Prerequisites Check

Before generating, verify these files exist:

```bash
courses/{COURSE_CODE}/syllabus.md
courses/{COURSE_CODE}/rubrics/*.md
```

If `assessment-schedule.md` exists, use it for detailed requirements. Otherwise, extract from syllabus.

**Load required skills:**
- `.claude/skills/assessment-design/handbook-generation.md`
- `.claude/skills/assessment-design/scenario-generation.md`

---

## Step 1: Extract Metadata

### From syllabus.md

Extract these elements:

**Course Metadata:**
- Course code (e.g., "BCI2AU")
- Course title (e.g., "Business Communication")
- Instructor name, email, phone
- Program (e.g., "BA in International Business")

**Assessment Overview Table:**
- Find section "## Assessment Overview"
- Extract table with columns: Assessment | Type | Weight | Due | Learning Objectives
- Parse each row:
  - Assessment name
  - Type (Portfolio, Presentation, Quiz, Project)
  - Weight (percentage)
  - Due week (number)
  - Learning objectives (comma-separated or ranges)

**Weekly Topics and Frameworks:**
- Find "## Course Calendar" table
- Extract columns: Week | Topic | Foundational Frameworks
- Create mapping: {week_number: [frameworks_taught]}
- Used to ensure scenarios only reference frameworks taught BEFORE assessment due week

Example:
```python
frameworks_by_week = {
    1: ["Shannon-Weaver Model", "Communication Style Assessment"],
    2: ["Pyramid Principle", "MECE", "SCQ Framework"],
    3: ["BLUF", "Clear Writing Principles", "Active Voice"],
    # ... etc
}
```

**All Learning Objectives:**
- Find section "## Learning Objectives"
- Extract complete list (usually 15-20 objectives)
- Number them 1-N
- Used for mapping assessments to objectives

### From rubrics/*.md

Load all rubric files:
```bash
courses/{COURSE_CODE}/rubrics/
├── written-work-rubric.md
├── presentation-rubric.md
├── project-rubric.md
└── ... (other rubrics)
```

For each rubric:
- Extract rubric name
- Extract "Used for:" line (if present)
- Extract full markdown table with 5 performance levels
- Store for later inclusion in Rubrics section

---

## Step 2: Generate Scenarios

For each non-quiz assessment:

### 2.1: Identify Applicable Frameworks

```python
assessment_due_week = 7  # example: Persuasive Proposal due Week 7
frameworks_available = []
for week in range(1, assessment_due_week):
    frameworks_available.extend(frameworks_by_week[week])

# Result: ["Shannon-Weaver", "Pyramid Principle", "BLUF", "Tufte", "Cialdini", ...]
```

### 2.2: Select Scenario Pattern

Based on assessment name/type, select pattern from `scenario-generation.md`:

| Assessment Name Contains | Pattern |
|-------------------------|---------|
| "Email" or "Memo" | Dual-Format Communication |
| "Data" or "Visualization" | Audience-Specific Analysis |
| "Proposal" or "Pitch" | Business Proposal Types |
| "Reflection" or "Development" | Reflection (may have no scenarios) |
| "Presentation" | Presentation Contexts |

### 2.3: Generate Options

Using selected pattern:

1. **Create 2-3 distinct options** labeled A, B, C (or D if appropriate)
2. **Apply framework constraints:** Only reference frameworks from `frameworks_available`
3. **Ensure genuine differentiation:** Options should be fundamentally different contexts
4. **Include specific details:**
   - WHO: Specific roles (Marketing VP, department head, investors)
   - WHAT: Specific deliverables (email + memo, one-page report)
   - WHY: Decision context (considering market entry, reviewing efficiency)
5. **Add "Create Your Own" option** as last option (usually)

Example for Week 3 Email + Memo:
```markdown
#### Scenario (Choose ONE)

**Option A: New Initiative Proposal**
- **Email:** Request a meeting with your department head to discuss a new initiative you want to propose
- **Memo:** Write to your team recommending they adopt a new tool, process, or approach

**Option B: Problem Resolution**
- **Email:** Request information or resources from an external vendor/partner to solve a workplace challenge
- **Memo:** Write to management recommending a solution to a recurring operational problem

**Option C: Create Your Own** (Instructor approval required)
- Propose your own scenario based on your work experience or career interests
```

**Frameworks used:** Pyramid Principle (Week 2), BLUF (Week 3), Audience analysis (Week 1)

### 2.4: Quality Check

Verify each scenario set:
- [ ] Frameworks referenced are taught before due week
- [ ] Options are genuinely different (not minor variations)
- [ ] Specific roles/audiences included
- [ ] Business contexts are realistic
- [ ] Complexity matches course stage (Week 3 = simpler, Week 10 = complex)

---

## Step 3: Assemble Handbook

Follow structure from `handbook-generation.md`:

### Header

```markdown
# {COURSE_CODE}: {Course Title}

## Assessment Handbook

## Table of Contents

1. [Assessment Overview](#assessment-overview)
2. [Portfolio Assessments ({total_portfolio_weight}%)](#portfolio-assessments-{weight})
   - [{Assessment 1}](#{slug-1})
   - [{Assessment 2}](#{slug-2})
   ...
3. [Presentation Assessments ({total_presentation_weight}%)](#presentation-assessments-{weight})
   - [{Assessment}](#{slug})
   ...
4. [Quizzes ({total_quiz_weight}%)](#quizzes-{weight})
5. [Rubrics](#rubrics)
6. [Tips for Success](#tips-for-success)

---
```

### Assessment Overview Table

```markdown
## Assessment Overview

| Assessment | Type | Weight | Due | Learning Objectives |
|------------|------|--------|-----|---------------------|
{for each assessment from syllabus:}
| {name} | {type} | {weight}% | Week {due_week} | {objectives} |
```

### Portfolio Assessments Section

```markdown
## Portfolio Assessments ({total_weight}%)

The portfolio demonstrates your growth in written business communication across multiple formats and purposes.

---

{for each portfolio assessment:}

### {number}. {Assessment Name} ({weight}%)

**Due:** End of Week {due_week}
**Weight:** {weight}%

#### Task Overview

{2-3 sentence description of what students will produce}

{scenarios from Step 2}

#### Requirements

{Generate specific, measurable requirements checklist}

**{Section Name}:**
- [ ] Requirement 1 (specific and measurable)
- [ ] Requirement 2
- [ ] Requirement 3

#### Submission Format

{Submission instructions}

**File naming:** StudentNumber_Name_{AssessmentSlug}_Week{N}.docx

#### Rubric Preview

| Criteria | Weight | Focus |
|----------|--------|-------|
{for each criterion from matching rubric:}
| {criterion_name} | {weight}% | {brief_focus} |

See [{Rubric Name}](#{rubric-slug}) for full details.

---
```

### Presentation Assessments Section

Same structure as Portfolio section, but with presentation-specific intro.

### Quizzes Section

Use boilerplate from `handbook-generation.md`:

```markdown
## Quizzes ({total_weight}%)

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
{for each quiz from syllabus:}
| Quiz {N} | Weeks {start}-{end} | Week {due} | {weight}% |

### Question Types

{Standard boilerplate - see handbook-generation.md}

### Study Resources

- Lecture slides and notes
- Required readings
- Tutorial practice questions
- Review sessions in class before each quiz
```

### Rubrics Section

```markdown
## Rubrics

{for each rubric from rubrics/*.md:}

### {Rubric Name}

{if "Used for" line exists in rubric file:}
Used for: {list of assessments}

{full rubric markdown table}

---
```

### Tips for Success Section

Use boilerplate from `handbook-generation.md`:

```markdown
## Tips for Success

### For Written Assessments

1. **Start with your conclusion** - Apply the Pyramid Principle to every document
2. **Know your audience** - Before writing, ask "What does my reader need?"
{... 3 more tips}

### For Presentations

1. **Practice out loud** - At least 5 full run-throughs before presenting
{... 4 more tips}

### For Quizzes

1. **Review weekly** - Don't cram; cumulative review beats last-minute studying
{... 4 more tips}

### General Success Strategies

1. **Attend every class** - Activities and discussions cannot be made up
{... 4 more tips}
```

### Footer

```markdown
---

## Questions?

- **Assessment clarifications:** Email instructor before due date
- **Rubric questions:** Raise in tutorial for whole-class discussion
- **Technical issues:** Contact instructor immediately; don't wait until deadline

---

*This handbook supplements the main syllabus. Both documents together provide complete course information.*
```

---

## Step 4: Validate with HandbookParser

Before saving, validate that the handbook is parseable:

```python
from pathlib import Path
from tools.assessment_domain.parsers.handbook_parser import HandbookParser

# Parse handbook
parser = HandbookParser()
handbook_path = Path(f"courses/{COURSE_CODE}/assessment-handbook.md")

# Save to temp location first
temp_path = Path(f"courses/{COURSE_CODE}/.temp-assessment-handbook.md")
temp_path.write_text(generated_handbook_content)

# Validate
try:
    assessments = parser.parse_file(temp_path)

    # Check all non-quiz assessments parsed
    expected_count = count_non_quiz_assessments_from_syllabus()
    if len(assessments) != expected_count:
        raise ValueError(f"Expected {expected_count} assessments, got {len(assessments)}")

    # Validate each assessment
    for aid, assessment in assessments.items():
        errors = assessment.validate()
        if errors:
            raise ValueError(f"Validation errors for {aid}: {errors}")

    print("✓ Parser validation PASSED")
    print(f"✓ {len(assessments)} assessments parsed successfully")

except Exception as e:
    print(f"✗ Parser validation FAILED: {e}")
    print("Review generated handbook and fix format issues")
    # Keep temp file for debugging
    return
```

If validation passes:
- Move temp file to final location
- Delete temp file

If validation fails:
- Show error details
- Keep temp file for user review
- Ask user if they want to proceed anyway or abort

---

## Step 5: Export to DOCX

After successful validation:

```bash
python3 tools/markdown_to_docx.py {COURSE_CODE} assessment-handbook
```

This creates:
```
courses/{COURSE_CODE}/assessment-handbook.docx
```

With proper formatting:
- Page headers with course code
- Page footers with instructor and page numbers
- Professional styling

---

## Output Report

After successful generation, report to user:

```
✓ Assessment Handbook Generated Successfully

Files created:
- courses/{COURSE_CODE}/assessment-handbook.md
- courses/{COURSE_CODE}/assessment-handbook.docx

Statistics:
- Assessments: {total_count} ({portfolio_count} portfolio, {presentation_count} presentation, {quiz_count} quiz)
- Scenarios generated: {scenario_count}
- Rubrics included: {rubric_count}
- Parser validation: PASSED

Next steps:
1. Review generated handbook for quality and accuracy
2. Test with: python3 tools/assessment_cli.py list-assessments {COURSE_CODE}
3. Generate PDF briefs: python3 tools/assessment_cli.py brief {COURSE_CODE} {assessment-id}

Handbook can be regenerated anytime with: /generate-handbook {COURSE_CODE}
```

---

## Error Handling

### Missing Prerequisites

If syllabus doesn't exist:
```
✗ Error: Syllabus not found at courses/{COURSE_CODE}/syllabus.md

Please generate syllabus first with: /generate-syllabus
```

If rubrics don't exist:
```
✗ Error: No rubrics found in courses/{COURSE_CODE}/rubrics/

Please create rubrics or run /generate-syllabus to generate them.
```

### Parser Validation Failure

If HandbookParser fails:
```
✗ Parser Validation Failed

Errors found:
- Cannot find Assessment Overview table
- Assessment "Email + Memo" missing scenarios section
- Rubric table has incorrect column count

Temp file saved to: courses/{COURSE_CODE}/.temp-assessment-handbook.md

Options:
1. Review temp file and identify issues
2. Check handbook-generation.md skill for format requirements
3. Regenerate with fixes

Continue anyway? (y/n)
```

### Insufficient Data

If syllabus is missing required information:
```
✗ Error: Syllabus missing required information

Missing:
- Assessment Overview table
- Course Calendar with frameworks
- Learning Objectives section

Please complete syllabus before generating handbook.
```

---

## Testing

After generation, test the handbook:

### Test 1: Parser Validation

```bash
python3 -c "
from pathlib import Path
from tools.assessment_domain.parsers.handbook_parser import HandbookParser

parser = HandbookParser()
assessments = parser.parse_file(Path('courses/{COURSE_CODE}/assessment-handbook.md'))

print(f'Assessments parsed: {len(assessments)}')
for aid, assessment in assessments.items():
    print(f'  - {aid}: {assessment.name} ({len(assessment.scenarios)} scenarios)')
"
```

### Test 2: List Assessments

```bash
python3 tools/assessment_cli.py list-assessments {COURSE_CODE}
```

Expected output:
```
=== Assessments (6) ===

email-memo:
  Name: Email + Memo
  Type: portfolio
  Weight: 10%
  Due: Week 3
  Rubric: Yes
  Scenarios: 3

...
```

### Test 3: Generate Brief

```bash
python3 tools/assessment_cli.py brief {COURSE_CODE} email-memo \
  --format html \
  -o test-brief.html
```

Open `test-brief.html` in browser to verify formatting.

---

## Notes

- This command can be run anytime to regenerate the handbook
- Existing `assessment-handbook.md` will be overwritten
- Backup recommended before regeneration: `cp assessment-handbook.md assessment-handbook.md.backup`
- Handbook generation takes ~15 minutes with AI scenario creation
- Manual review recommended after generation for quality and accuracy

---

## Integration

This command is called by:
- Manual invocation: `/generate-handbook [CODE]`
- Automatic invocation: `/generate-syllabus` Step 5.6

This command uses:
- `.claude/skills/assessment-design/handbook-generation.md`
- `.claude/skills/assessment-design/scenario-generation.md`
- `tools/assessment_domain/parsers/handbook_parser.py`
- `tools/markdown_to_docx.py`
