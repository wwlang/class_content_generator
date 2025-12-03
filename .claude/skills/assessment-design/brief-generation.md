# Assessment Brief Generation

Generate standalone markdown assessment briefs and convert to DOCX for LMS upload.

---

## Purpose

Create individual assessment briefs that are:
1. **Self-contained** - All instructions in one document
2. **LMS-ready** - Professional DOCX for attaching to assignments
3. **Student-focused** - Clear task instructions without handbook cruft
4. **Printable** - Professional formatting for physical distribution
5. **Consistent** - Uses same MD→DOCX workflow as all other course documents

## Key Principle: One Brief = One Assessment Task

Each brief is a complete, standalone markdown document that students can use without needing the full handbook.

**Workflow:** Generate markdown → Convert to DOCX (same as syllabus, lectures, tutorials)

---

## Brief Structure

### Required Sections (in order)

```markdown
# [Assessment Name]

**Course:** [COURSE_CODE] - [Course Name]
**Due:** End of Week [N]
**Weight:** [weight]%

---

## Task Overview

[2-3 paragraphs describing:
- What students will produce
- Why this assessment matters
- How it connects to learning objectives]

---

## Scenario (Choose ONE)

**Option A: [Scenario Title]**
[Full scenario description with context and deliverables]
- Specific requirement 1
- Specific requirement 2

**Option B: [Scenario Title]**
[Full scenario description with context and deliverables]
- Specific requirement 1
- Specific requirement 2

**Option C: Create Your Own**
[Description of what students must include if creating their own scenario]

---

## Requirements

**[Section Name]:**
- [ ] Requirement 1 (specific and measurable)
- [ ] Requirement 2
- [ ] Requirement 3

**[Section Name]:**
- [ ] Requirement 4
- [ ] Requirement 5

---

## Submission Format

**File naming:** StudentNumber_Name_[AssessmentSlug]_Week[N].docx

**Submit via:** Moodle by Sunday 11:59 PM, Week [N]

**Format:** Microsoft Word (.docx) or PDF

---

## Rubric

**IMPORTANT:** Load `rubric-generation.md` skill to create framework-informed rubrics.

### [Rubric Name]

| Criteria | Excellent (94-100%) | Good (84-93%) | Satisfactory (74-83%) | Needs Work (60-73%) | Failing (<60%) |
|----------|---------------------|---------------|----------------------|---------------------|----------------|
| **[Framework-Specific Criterion]** | [Framework application description] | [Framework application description] | [Framework application description] | [Framework application description] | [Framework application description] |

**Rubric Requirements:**
- Reference specific frameworks taught BEFORE this assessment's due week
- Use framework names in criterion descriptors (e.g., "Applies Munter Framework...")
- Make performance levels measurable and observable
- NO generic language like "good analysis" without framework context
```

---

## Content Sources

All content comes from the Assessment Handbook via `HandbookParser`:

1. **Task Overview** - Extract from handbook or generate based on assessment name/type
2. **Scenarios** - From `assessment.scenarios` (2-4 options)
3. **Requirements** - From `assessment.requirements` (grouped by section)
4. **Submission Format** - From handbook submission section
5. **Rubric** - From `assessment.rubric` (full 5-level table)

---

## Generation Process

### Step 1: Parse Assessment from Handbook

```python
from tools.assessment_domain import HandbookParser

# Parse handbook
parser = HandbookParser()
handbook_path = Path(f"courses/{COURSE_CODE}/assessment-handbook.md")
assessments = parser.parse_file(handbook_path)

# Get specific assessment
assessment = assessments[assessment_id]
```

### Step 2: Generate Brief Markdown

Create markdown file with all sections populated from `assessment` object:

```python
brief_content = f"""# {assessment.name}

**Course:** {COURSE_CODE} - {course_name}
**Due:** End of Week {assessment.due_week}
**Weight:** {assessment.weight * 100}%

---

## Task Overview

{assessment.task_overview}

---

## Scenario (Choose ONE)

{format_scenarios(assessment.scenarios)}

---

## Requirements

{format_requirements(assessment.requirements)}

---

## Submission Format

{assessment.submission_format}

---

## Rubric

{format_rubric(assessment.rubric)}

---
"""

# Save markdown
brief_path = Path(f"courses/{COURSE_CODE}/assessments/{assessment_id}.md")
brief_path.write_text(brief_content)
```

### Step 3: Convert to DOCX

Use the same `markdown_to_docx.py` tool as all other course documents:

```bash
python3 tools/markdown_to_docx.py {COURSE_CODE} assessments/{assessment_id}
```

This generates professional DOCX with:
- Professional styling
- Page headers with course code
- Page footers with instructor and page numbers
- Consistent formatting with syllabus/lectures/tutorials

---

## DOCX Styling

The `markdown_to_docx.py` tool handles all styling consistently:

- **Typography:** Professional fonts, appropriate sizes
- **Spacing:** Consistent line height and margins
- **Tables:** Clean borders, professional formatting
- **Headers/Footers:** Course code, instructor, page numbers
- **Page breaks:** Appropriate section breaks

Students receive professional, printable documents matching all other course materials.

---

## Validation

Before generating briefs, ensure:

- [ ] Handbook has been generated and parsed successfully
- [ ] All assessments have scenarios (except quizzes)
- [ ] All assessments have requirements
- [ ] All assessments have rubrics
- [ ] Scenarios reference only frameworks taught before due week

Use `HandbookParser` validation to catch issues early.

---

## Common Patterns

### Portfolio Assessments (with Framework Reflection)

**ALL portfolio assessments require framework reflection** to demonstrate thought processes.

Typical structure:
- 2-3 scenario options
- 8-12 requirements (grouped by Content, Format, Mechanics, Reflection)
- Written communication rubric (5 criteria including Framework Reflection 10-20%)

**Word Count Split:**
- Business Memo (Week 4): 400-500 words memo + 200-250 words reflection
- Persuasive Proposal (Week 7): 800-1100 words proposal + 300-400 words reflection
- Executive Summary (Week 10): 250-350 words summary + 150-200 words reflection

**Reflection Requirements Template:**

```markdown
**Reflection Requirements:**

- [ ] Identify which frameworks you applied (specific to assessment)
- [ ] Explain HOW you applied each framework to specific decisions
- [ ] Discuss what you learned through framework application
- [ ] Reflect on challenges encountered and how frameworks helped
- [ ] Demonstrate metacognitive awareness per Reflective Practice Model
```

**Rubric Adjustment:**
- Add "Framework Reflection" criterion (10-20% weight)
- Reduce other criteria weights proportionally
- Prefix existing criteria with "Memo:", "Proposal:", or "Summary:" to clarify scope

### Presentation Assessments

Typical structure:
- 2-3 context options (audience, topic, purpose)
- 10-15 requirements (Content, Delivery, Visual Aids, Q&A)
- Presentation rubric (6-7 criteria)

### Project Assessments

Typical structure:
- 1-2 open-ended scenarios
- 15-20 requirements (multiple phases/deliverables)
- Project rubric (7-8 criteria)

---

## Integration

This skill is used by:
- `/generate-assessments` command (Step 5 - batch brief generation)
- Manual brief regeneration after handbook updates

This skill requires:
- `handbook-generation.md` (generates source data)
- `scenario-generation.md` (scenario patterns for validation)
- `tools/assessment_domain/parsers/handbook_parser.py` (content parsing)
- `tools/markdown_to_docx.py` (DOCX conversion)

---

## Notes

- Briefs are self-contained; students don't need the handbook to complete the assessment
- Briefs can be regenerated anytime from the handbook source
- Uses same MD→DOCX workflow as syllabus, lectures, and tutorials for consistency
- Briefs should be uploaded to LMS assignment attachments, not distributed separately
- Both .md and .docx versions are kept in `assessments/` directory
