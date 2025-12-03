# Assessment Generation Standards

Document separation of concerns and quality standards for assessment documentation.

**Last Updated:** November 29, 2025

---

## Document Hierarchy

### 1. Syllabus (`syllabus.md`)

**Purpose:** Course policies and grading overview

**Contains:**
- Course calendar with frameworks
- Learning objectives
- Grading breakdown and weights
- Participation policies (attendance, active participation)
- Course policies (academic integrity, late work, etc.)
- Recommended resources

**Does NOT contain:**
- Detailed assessment instructions (in briefs)
- Rubrics (in briefs)
- Assessment scenarios (in briefs)

---

### 2. Assessment Handbook (`assessment-handbook.md`)

**Purpose:** Lightweight overview of all assessments

**Contains:**
- Assessment Overview table (all assessments at a glance)
- Portfolio assessments (brief descriptions + references to briefs)
- Presentation assessments (brief descriptions + references to briefs)
- Quiz section (format, question types, frameworks covered)
- Closing statement

**Does NOT contain:**
- Detailed scenarios (in individual briefs)
- Detailed requirements (in individual briefs)
- Rubrics (in individual briefs - eliminates redundancy)
- Tips for Success (removed - distracts from rubric focus)
- Questions section (removed - redundant with syllabus)
- Participation policies (in syllabus instead)

**Format:**
```markdown
## Portfolio Assessments (35%)

### 1. Business Memo: Audience Analysis (10%)

**Due:** End of Week 4
**Weight:** 10%

{2-3 sentence description}

**Detailed instructions:** See Business Memo Brief

**Rubric:** See individual assessment brief

---
```

---

### 3. Individual Assessment Briefs (`assessments/{assessment-id}.md` + `.docx`)

**Purpose:** Self-contained LMS-ready task instructions

**Contains:**
- Full task overview
- Complete scenario options (2-4 options)
- Detailed requirements checklist
- Submission format and file naming
- **Framework-informed rubric** (specific to this assessment)
- Professional DOCX formatting

**Key Requirement:** Briefs must be standalone - students can complete assessment using only the brief

**Format:**
```markdown
# Business Memo: Audience Analysis

**Course:** BCI2AU - Business Communication
**Due:** End of Week 4
**Weight:** 10%

---

## Task Overview

{2-3 paragraphs}

---

## Scenario (Choose ONE)

**Option A: New Initiative Proposal**
{Full scenario description}

**Option B: Problem Resolution**
{Full scenario description}

**Option C: Create Your Own** (Instructor approval required)

---

## Requirements

{Detailed checklist}

---

## Submission Format

{File naming, format, deadline}

---

## Rubric

{Framework-informed rubric - see below}

---
```

---

## Rubric Generation Standards

### Core Principle: Framework-Informed Rubrics

**NO GENERIC RUBRICS ALLOWED**

❌ **BAD (Generic):**
```markdown
| **Content & Strategy** | Sophisticated analysis | Strong analysis | Adequate analysis |
```

✅ **GOOD (Framework-Specific):**
```markdown
| **Audience Analysis (30%)** | Expertly applies Munter Framework and Stakeholder Mapping to identify all audience needs, concerns, and communication channels; demonstrates sophisticated understanding of communication competence theory | Effectively uses Munter Framework; identifies most audience needs; shows good competence theory understanding | Basic Munter Framework application; identifies primary audience needs |
```

### Rubric Generation Process

**Required Skill:** `.claude/skills/assessment-design/rubric-generation.md`

**Steps:**

1. **Extract frameworks from Course Calendar** (syllabus)
   ```
   Week 1: Shannon-Weaver Model, Communication Competence Theory
   Week 2: Munter Framework, Stakeholder Mapping
   Week 3: Pyramid Principle, SCQA Framework
   Week 4: Rhetorical Appeals, Problem-Solution-Benefit
   ```

2. **Filter to frameworks taught BEFORE assessment due week**
   ```python
   # For Week 4 assessment
   frameworks_available = frameworks_from_weeks[1, 2, 3]
   # Result: Shannon-Weaver, Competence Theory, Munter, Stakeholder Mapping, Pyramid, SCQA
   ```

3. **Select 3-5 most relevant frameworks for this assessment**
   ```
   Business Memo (Week 4):
   - Primary: Munter Framework (audience analysis)
   - Primary: Pyramid Principle (structure)
   - Secondary: SCQA (organization tool)
   - Secondary: Stakeholder Mapping (audience identification)
   ```

4. **Map frameworks to rubric criteria (4-5 criteria)**
   ```
   Criterion 1 (30%): Munter Framework + Stakeholder Mapping
   Criterion 2 (30%): Pyramid Principle + SCQA
   Criterion 3 (25%): Shannon-Weaver (message strategy)
   Criterion 4 (15%): Professional communication
   ```

5. **Write framework-specific descriptors**
   ```markdown
   | **Audience Analysis (30%)** |
   Excellent: Expertly applies Munter Framework and Stakeholder Mapping...
   Good: Effectively uses Munter Framework for audience analysis...
   Satisfactory: Basic Munter Framework application...
   Needs Work: Weak audience analysis; Munter Framework barely evident...
   Failing: No audience analysis; no framework application
   ```

6. **Validate alignment**
   - [ ] All frameworks referenced are taught before due week
   - [ ] Each criterion references specific frameworks by name
   - [ ] Performance descriptors are observable and measurable
   - [ ] No generic language without framework context
   - [ ] Criteria weights sum to 100%

### Rubric Quality Checklist

- [ ] Framework names are accurate (check spelling, attribution)
- [ ] Frameworks are taught BEFORE assessment due week
- [ ] Each performance level shows clear progression
- [ ] Students can self-assess using these criteria
- [ ] Instructor can grade objectively using descriptors
- [ ] NO generic terms like "good analysis" without framework context

### Examples by Week

**Week 4 Business Memo** (Frameworks: Weeks 1-3)
```markdown
| **Audience Analysis (30%)** | Expertly applies Munter Framework and Stakeholder Mapping to identify all audience needs, concerns, and preferred communication channels | Effectively uses Munter Framework; identifies most audience needs | Basic Munter application |
| **Organization (30%)** | Perfect Pyramid Principle structure; flawless SCQA flow (Situation-Complication-Question-Answer) | Strong Pyramid structure; clear SCQA with minor gaps | Adequate top-down structure |
```

**Week 7 Persuasive Proposal** (Frameworks: Weeks 1-6)
```markdown
| **Persuasive Strategy (35%)** | Masterfully employs 4+ Cialdini principles; perfect ethos-pathos-logos balance using rhetorical appeals; compelling Problem-Solution-Benefit structure | Effectively uses 3+ Cialdini principles; strong appeals balance | Applies 2 Cialdini principles adequately |
| **Framework Integration (25%)** | Seamlessly integrates Pyramid Principle, SCQA, Munter Framework into cohesive argument | Integrates 2-3 frameworks effectively | Uses 1-2 frameworks |
```

---

## Skills Required

### For Handbook Generation
- `.claude/skills/assessment-design/handbook-generation.md`
- `.claude/skills/assessment-design/scenario-generation.md`

### For Brief Generation
- `.claude/skills/assessment-design/brief-generation.md`
- `.claude/skills/assessment-design/rubric-generation.md`

---

## Commands

### Generate All Assessment Documentation
```bash
/generate-assessments [COURSE_CODE]
```

**Generates:**
1. Assessment handbook (overview)
2. Individual briefs with framework-informed rubrics
3. DOCX versions of all documents

**Prerequisites:**
- Syllabus must exist with Course Calendar (frameworks by week)
- Learning objectives must be defined

---

## Separation of Concerns Summary

| Content | Syllabus | Handbook | Brief |
|---------|----------|----------|-------|
| Course policies | ✅ | ❌ | ❌ |
| Participation rules | ✅ | ❌ | ❌ |
| Assessment overview table | ✅ | ✅ | ❌ |
| Brief descriptions | ❌ | ✅ | ❌ |
| Detailed scenarios | ❌ | ❌ | ✅ |
| Detailed requirements | ❌ | ❌ | ✅ |
| Rubrics | ❌ | ❌ | ✅ |
| Submission format | ❌ | ❌ | ✅ |

**Rationale:**
- **No redundancy** - each element appears in exactly one place
- **Clear ownership** - syllabus = policies, handbook = overview, briefs = detailed instructions
- **Easier maintenance** - change once, not multiple times
- **Student clarity** - one authoritative source per information type

---

## Quality Standards

### Handbook Quality
- [ ] Overview table includes all assessments
- [ ] Each assessment has 2-3 sentence description
- [ ] References to individual briefs are clear
- [ ] NO detailed scenarios (reference briefs instead)
- [ ] NO rubrics (reference briefs instead)
- [ ] NO participation policies (in syllabus)
- [ ] NO tips/questions sections (removed)

### Brief Quality
- [ ] Self-contained (student can complete with only this document)
- [ ] 2-4 scenario options provided
- [ ] Scenarios reference only frameworks taught before due week
- [ ] Requirements are specific and measurable
- [ ] Rubric is framework-informed (no generic language)
- [ ] All framework names accurate and spelled correctly
- [ ] Professional DOCX formatting applied

### Rubric Quality
- [ ] References specific course frameworks by name
- [ ] Only frameworks taught BEFORE assessment due week
- [ ] Each criterion maps to 1-2 specific frameworks
- [ ] Performance descriptors are observable and measurable
- [ ] NO generic terms without framework context
- [ ] Criteria weights sum to 100%
- [ ] 4-5 criteria total (not too many, not too few)

---

## Backward Design Alignment

**Test:** If students read only the rubric on Day 1, would they know what to learn?

**Answer should be: YES**

Example:
```markdown
Rubric says: "Applies Munter Framework and Stakeholder Mapping"
→ Student learns: "I need to learn Munter Framework and Stakeholder Mapping"
→ Instructor teaches: Munter Framework and Stakeholder Mapping
→ Assessment measures: Application of Munter Framework and Stakeholder Mapping
```

**Perfect alignment:** Research → Teaching → Assessment → Rubric

---

## Validation Checklist

Before finalizing assessment documentation:

### Handbook
- [ ] Parsed successfully by HandbookParser
- [ ] All non-quiz assessments included
- [ ] No rubrics section
- [ ] No tips/questions sections
- [ ] No participation section

### Briefs
- [ ] One brief per non-quiz assessment
- [ ] Each brief is self-contained
- [ ] Framework-informed rubric included
- [ ] All frameworks validated (taught before due week)
- [ ] DOCX conversion successful

### Rubrics
- [ ] No generic language
- [ ] Specific framework references
- [ ] Framework timeline validated
- [ ] Performance descriptors measurable
- [ ] Criteria weights = 100%

---

## Common Mistakes to Avoid

### ❌ Generic Rubrics
```markdown
| **Content** | Excellent analysis | Good analysis | Adequate analysis |
```
**Fix:** Reference specific frameworks by name

### ❌ Frameworks Not Yet Taught
Week 4 assessment referencing Week 7 frameworks
**Fix:** Filter frameworks to only those taught before due week

### ❌ Too Many Documents
Rubrics duplicated in handbook AND briefs
**Fix:** Rubrics only in briefs

### ❌ Missing Framework Names
```markdown
| **Strategy** | Uses persuasion principles effectively |
```
**Fix:** Specify which principles: "Uses Cialdini's 6 principles (reciprocity, authority, social proof...)"

### ❌ Vague Descriptors
```markdown
| **Organization** | Well organized | Organized | Somewhat organized |
```
**Fix:** "Perfect Pyramid Principle structure: conclusion first, then 3-4 supporting arguments in logical order"

---

## Regeneration

To regenerate assessment documentation for an existing course:

```bash
/generate-assessments [COURSE_CODE]
```

**Note:** This will:
- Overwrite existing `assessment-handbook.md`
- Regenerate all individual briefs in `assessments/` folder
- Apply all current quality standards
- Generate framework-informed rubrics

**Recommendation:** Backup existing files before regeneration:
```bash
cp courses/[CODE]/assessment-handbook.md courses/[CODE]/assessment-handbook.md.backup
cp -r courses/[CODE]/assessments courses/[CODE]/assessments.backup
```

---

## Integration with Course Generation Workflow

**Correct Order:**

1. `/generate-syllabus` - Creates course structure with frameworks
2. **`/generate-assessments`** - Creates handbook + briefs with framework-informed rubrics
3. `/generate-course` or `/generate-week` - Weekly content references assessments
4. `/export-docx` - Convert all to professional DOCX

**Why this order:**
- Syllabus defines frameworks timeline
- Assessment rubrics use frameworks timeline → backward design
- Weekly content teaches frameworks that appear in rubrics
- Perfect alignment: Research → Syllabus → Rubrics → Teaching → Assessment

---

## References

- Handbook Generation Skill: `.claude/skills/assessment-design/handbook-generation.md`
- Brief Generation Skill: `.claude/skills/assessment-design/brief-generation.md`
- Rubric Generation Skill: `.claude/skills/assessment-design/rubric-generation.md`
- Scenario Generation Skill: `.claude/skills/assessment-design/scenario-generation.md`
- Generate Assessments Command: `.claude/commands/generate-assessments.md`
