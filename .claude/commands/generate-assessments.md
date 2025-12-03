---
description: Generate assessment handbook and individual briefs from syllabus
---

# Generate Assessments

You are generating assessment documentation from an existing syllabus.

This command creates TWO types of documents with distinct purposes:

## 1. Assessment Handbook (`assessment-handbook.md`)

**Purpose:** Lightweight overview reference document for students
**Use Case:** Students understand the full assessment landscape

**Contents:**
- Assessment Overview table (all assessments at a glance)
- Portfolio/Presentation/Quiz sections with brief descriptions
- References to individual briefs for detailed instructions

**What it does NOT include:**
- Detailed scenarios (in individual briefs instead)
- Detailed requirements checklists (in individual briefs instead)
- Rubrics (in individual briefs instead - no duplication)
- Tips for Success (distracts from rubric focus)
- Questions section (redundant with syllabus)
- Participation policies (belongs in syllabus)

## 2. Individual Assessment Briefs (`assessments/{assessment-id}.md` + `.docx`)

**Purpose:** Standalone task instructions for LMS upload
**Use Case:** Students working on a specific assessment

**Contents:**
- Full task overview for THIS assessment
- Complete scenario options
- Detailed requirements checklist
- Submission format and file naming
- Framework-informed rubric for THIS assessment (see rubric-generation.md skill)
- Professional DOCX formatting (consistent with all course docs)

**Key Difference:** Briefs are self-contained and can be attached to individual LMS assignments

**Rubric Requirements:**
- Must reference specific course frameworks taught BEFORE assessment due week
- NO generic rubrics (e.g., "good analysis" → "applies Munter Framework")
- Load `rubric-generation.md` skill for framework-specific rubric generation

**Format:** Generated as markdown, then converted to DOCX using same workflow as syllabus/lectures

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
- `.claude/skills/assessment-design/brief-generation.md`
- `.claude/skills/assessment-design/rubric-generation.md` (for framework-informed rubrics)

---

## Step 1: Extract Metadata

### From syllabus.md

Extract these elements:

**Course Metadata:**
- Course code (e.g., "BCI2AU")
- Course title (e.g., "Business Communication")
- Semester/year (e.g., "Fall 2025")
- University and campus (e.g., "Andrews University - National Economics University Campus")

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

**Option C: Create Your Own**
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

**{Semester/Year} - {University} - {Campus}**

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

{2-3 sentence description of what students will produce}

**Detailed instructions:** See {Assessment Name} Brief

**Rubric:** See individual assessment brief

---
```

### Presentation Assessments Section

Same structure as Portfolio section, but with presentation-specific intro.

### Quiz Section

Use boilerplate from `handbook-generation.md`:

```markdown
## Quiz ({total_weight}%)

### In-Class Quiz

**When:** Week {due_week} tutorial session
**Duration:** 30 minutes
**Weight:** {weight}%
**Format:** Closed book, no notes, no devices

#### Quiz Format

The comprehensive quiz assesses understanding of all frameworks and concepts from Weeks 1-{coverage_end}:

- **25-30 questions** total
- **Multiple choice** and **scenario application**
- **Time:** 30 minutes (approximately 1 minute per question)

#### Question Types

**Remembering (40%):** Key concepts, definitions, framework components
> *Example: What do the letters stand for in [Framework acronym]?*

**Understanding (40%):** Explaining why, distinguishing concepts, interpreting
> *Example: What is the key difference between X and Y in [Framework]?*

**Brief Application (20%):** Identifying appropriate frameworks for scenarios
> *Example: A manager's message was delivered but behavior didn't change. Which communication level problem?*

#### Frameworks Covered

{Table mapping weeks to frameworks - extract from Course Calendar}

#### Study Resources

- Weekly lecture slides and notes
- Tutorial quiz questions (same format)
- Required readings
- Week {review_week} review session in class
```

### Footer

```markdown
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

## Step 5: Generate Individual Assessment Briefs

Load required skills:
- `.claude/skills/assessment-design/brief-generation.md`
- `.claude/skills/assessment-design/rubric-generation.md`

Create the `assessments/` directory if it doesn't exist:
```bash
mkdir -p courses/{COURSE_CODE}/assessments
```

For each non-quiz assessment:

**Step 5.1:** Extract frameworks taught before assessment due week

```python
# From Course Calendar in syllabus
frameworks_by_week = extract_frameworks_from_course_calendar(syllabus)

# For assessment due Week N, filter to Weeks 1 to N-1
assessment_due_week = 7
frameworks_available = []
for week in range(1, assessment_due_week):
    frameworks_available.extend(frameworks_by_week.get(week, []))
```

**Step 5.2:** Generate framework-informed rubric

Using `rubric-generation.md` skill:

1. Select 3-5 most relevant frameworks for this assessment type
2. Map frameworks to rubric criteria (4-5 criteria)
3. Write framework-specific performance descriptors
4. Validate all frameworks are taught before due week

**NO GENERIC RUBRICS** - Must reference specific frameworks by name

**Portfolio Assessment Reflection Components:**

For portfolio assessments (Business Memo, Persuasive Proposal, Executive Summary), include reflection requirements:

```markdown
**Reflection Requirements:**

- [ ] Identify which frameworks you applied (specific to this assessment)
- [ ] Explain HOW you applied each framework to specific communication decisions
- [ ] Discuss what you learned about [topic] through framework application
- [ ] Reflect on challenges encountered and how frameworks helped address them
- [ ] Demonstrate metacognitive awareness per Reflective Practice Model
```

Word count splits for portfolio assessments:
- Business Memo: 400-500 words + 200-250 words reflection
- Persuasive Proposal: 800-1100 words + 300-400 words reflection
- Executive Summary: 250-350 words + 150-200 words reflection

**Step 5.3:** Generate complete markdown brief

```python
from tools.assessment_domain import HandbookParser

# Parse handbook
parser = HandbookParser()
assessments = parser.parse_file("courses/{COURSE_CODE}/assessment-handbook.md")

# For each assessment, generate brief markdown
for aid, assessment in assessments.items():
    # Generate brief with:
    # - Task overview
    # - Scenarios (from handbook)
    # - Requirements
    # - Submission format
    # - Framework-informed rubric (from Step 5.2)
    # Save to courses/{COURSE_CODE}/assessments/{aid}.md
```

**Step 5.4:** Convert all briefs to DOCX

```bash
python3 tools/markdown_to_docx.py {COURSE_CODE} assessments
```

This automatically:
- Finds all .md files in `courses/{COURSE_CODE}/assessments/`
- Skips `assessment-schedule.md` if present
- Converts each brief to professional DOCX format
- Applies course branding (headers/footers)

This creates standalone DOCX briefs for each assessment with:
- Full task overview
- Complete scenarios
- Detailed requirements
- Submission format
- Full rubric
- Professional DOCX styling

---

## Step 6: Convert Handbook to DOCX

After all briefs are converted, export the handbook:

```bash
python3 tools/markdown_to_docx.py {COURSE_CODE} handbook
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
✓ Assessment Documentation Generated Successfully

Handbook:
- courses/{COURSE_CODE}/assessment-handbook.md
- courses/{COURSE_CODE}/assessment-handbook.docx

Individual Briefs (for LMS upload):
- courses/{COURSE_CODE}/assessments/business-memo.md
- courses/{COURSE_CODE}/assessments/business-memo.docx
- courses/{COURSE_CODE}/assessments/persuasive-proposal.md
- courses/{COURSE_CODE}/assessments/persuasive-proposal.docx
- courses/{COURSE_CODE}/assessments/executive-summary.md
- courses/{COURSE_CODE}/assessments/executive-summary.docx
  [... etc]

Statistics:
- Assessments: {total_count} ({portfolio_count} portfolio, {presentation_count} presentation, {quiz_count} quiz)
- Scenarios generated: {scenario_count}
- Rubrics included: {rubric_count}
- Parser validation: PASSED

Next steps:
1. Review handbook and briefs for quality and accuracy
2. Upload individual PDFs to LMS assignments
3. Distribute handbook.docx to students as reference guide

Regenerate anytime with: /generate-assessments {COURSE_CODE}
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
