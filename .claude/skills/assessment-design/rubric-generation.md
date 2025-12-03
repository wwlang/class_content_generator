# Framework-Informed Rubric Generation

Generate assessment rubrics that reference specific course frameworks and concepts.

---

## Purpose

Create rubrics that are:
1. **Framework-specific** - Reference actual frameworks taught in the course (e.g., "Applies Cialdini's 6 principles")
2. **Course-aligned** - Use terminology and concepts from course research
3. **Criterion-referenced** - Students know exactly what knowledge/skills are being assessed
4. **Backward-designed** - Assessment criteria drive what needs to be taught

## Core Principle: No Generic Rubrics

**BAD (Generic):**
```
| **Content & Strategy** | Sophisticated analysis | Strong analysis | Adequate analysis |
```

**GOOD (Framework-Specific):**
```
| **Framework Application (30%)** | Expertly applies Munter Framework and Stakeholder Mapping to analyze all audience needs; demonstrates sophisticated strategic thinking with Pyramid Principle structure | Applies Munter Framework and audience analysis effectively; uses Pyramid Principle with minor gaps | Attempts to apply frameworks; basic audience analysis; weak Pyramid structure |
```

---

## Input Requirements

### From Syllabus Course Calendar

Extract frameworks taught each week:

**Example from Business Communication:**
```
Week 1: Shannon-Weaver Model, Communication Competence Theory (Spitzberg & Cupach)
Week 2: Munter Strategic Communication Framework, Stakeholder Mapping Matrix
Week 3: Pyramid Principle (Minto), SCQA Framework
Week 4: Rhetorical Appeals (Aristotle), Problem-Solution-Benefit Structure
Week 7: Cialdini's 6 Principles of Persuasion, Storytelling Arc Framework
```

### From Assessment Due Week

**Rule:** Only reference frameworks taught BEFORE the assessment due week.

**Example:**
- Week 4 assessment can reference: Week 1-3 frameworks only
- Week 7 assessment can reference: Week 1-6 frameworks only
- Week 10 assessment can reference: Week 1-9 frameworks only

---

## Rubric Structure

### Standard Format

```markdown
## Rubric

| Criteria | Excellent (94-100%) | Good (84-93%) | Satisfactory (74-83%) | Needs Work (60-73%) | Failing (<60%) |
|----------|---------------------|---------------|----------------------|---------------------|----------------|
| **[Criterion]** | [Description] | [Description] | [Description] | [Description] | [Description] |
```

### Criteria Weighting

**Total must equal 100%**

Standard distributions:
- **Written work:** 4-5 criteria (20-35% each)
- **Presentations:** 4-6 criteria (15-30% each)
- **Executive communication:** 3-4 criteria (20-35% each)

---

## Framework Integration Patterns

### Pattern 1: Explicit Framework Reference

**When to use:** Core criterion directly assesses framework application

**Example:**
```markdown
| **Framework Application (30%)** | Masterfully applies Munter Strategic Communication Framework to analyze audience; uses Pyramid Principle throughout with flawless SCQA structure | Effectively applies Munter Framework; strong Pyramid Principle structure with minor gaps | Attempts Munter analysis; basic Pyramid structure; weak SCQA application | Limited framework use; Pyramid Principle not evident | No framework application |
```

### Pattern 2: Framework-Informed Expectations

**When to use:** Criterion assesses skills taught through specific frameworks

**Example (Organization):**
```markdown
| **Organization (25%)** | Perfect Pyramid Principle structure; conclusion first, then supporting arguments in logical order; flawless SCQA flow (Situation-Complication-Question-Answer) | Strong Pyramid structure; mostly logical flow; SCQA evident with minor gaps | Adequate structure; attempts top-down approach; some logical flow | Weak structure; bottom-up reasoning; difficult to follow | No discernible structure; disorganized |
```

### Pattern 3: Concept-Specific Criteria

**When to use:** Assessment focuses on specific course concepts

**Example (Persuasion):**
```markdown
| **Persuasive Strategy (30%)** | Expertly employs 3+ Cialdini principles (reciprocity, authority, social proof, etc.); strong ethos, pathos, logos balance; compelling evidence throughout | Uses 2-3 Cialdini principles effectively; good rhetorical appeals balance; solid evidence | Applies 1-2 persuasion principles; basic rhetorical appeals; adequate evidence | Limited persuasion strategy; weak appeals; insufficient evidence | No persuasion principles; no rhetorical strategy |
```

### Pattern 4: Progressive Skill Building

**When to use:** Later assessments build on earlier frameworks

**Example (Week 10 assessment building on Weeks 1-9):**
```markdown
| **Synthesis & Integration (35%)** | Seamlessly integrates multiple frameworks (Munter, Pyramid Principle, Cialdini, Cultural Dimensions); demonstrates sophisticated strategic thinking; connects all course concepts | Integrates 2-3 frameworks effectively; good strategic approach; clear connections | Uses 1-2 frameworks; basic integration; some connections | Limited framework integration; weak synthesis | No framework integration; isolated thinking |
```

---

## Rubric Types by Assessment

### Written Communication Rubric

**Used for:** Memos, proposals, reports, executive summaries

**Standard Criteria (adapt to specific frameworks):**
1. **Framework Application (25-30%)** - Which frameworks are students applying?
2. **Organization & Structure (20-25%)** - Pyramid Principle? SCQA? Other structural frameworks?
3. **Clarity & Concision (15-20%)** - Direct writing principles taught?
4. **Evidence & Analysis (15-20%)** - Analytical frameworks? Research integration?
5. **Professional Communication (15-20%)** - Tone, mechanics, formatting

### Presentation Rubric

**Used for:** Oral presentations, pitches, Q&A assessments

**Standard Criteria:**
1. **Content & Framework Application (25-30%)** - Which frameworks for content?
2. **Delivery & Presence (20-25%)** - Executive presence models? Communication apprehension theory?
3. **Visual Communication (15-20%)** - Duarte? Tufte principles? Visual hierarchy?
4. **Persuasion & Storytelling (15-20%)** - Cialdini? Storytelling arc? Rhetorical appeals?
5. **Q&A / Audience Engagement (10-15%)** - How do they handle questions?

### Executive Communication Rubric

**Used for:** Executive summaries, board briefs, C-suite communications

**Standard Criteria:**
1. **Executive Communication (30-35%)** - Pyramid Principle? BLUF? Recommendation clarity?
2. **Synthesis & Analysis (25-30%)** - Analytical frameworks applied?
3. **Strategic Thinking (20-25%)** - Strategic frameworks? Audience analysis?
4. **Concision & Clarity (15-20%)** - Maximum information density principles?

---

## Examples by Course Week

### Week 4 Assessment (Frameworks: Weeks 1-3)

**Available Frameworks:**
- Shannon-Weaver Model (Week 1)
- Communication Competence Theory (Week 1)
- Munter Framework (Week 2)
- Stakeholder Mapping (Week 2)
- Pyramid Principle (Week 3)
- SCQA Framework (Week 3)

**Rubric Example:**
```markdown
| Criteria | Excellent (94-100%) | Good (84-93%) | Satisfactory (74-83%) | Needs Work (60-73%) | Failing (<60%) |
|----------|---------------------|---------------|----------------------|---------------------|----------------|
| **Audience Analysis (30%)** | Expertly applies Munter Framework and Stakeholder Mapping to identify all audience needs, concerns, and preferred communication channels; demonstrates deep understanding of communication competence theory | Effectively uses Munter Framework and stakeholder analysis; identifies most audience needs; shows good understanding of competence theory | Basic Munter Framework application; identifies primary audience needs; limited stakeholder analysis | Weak audience analysis; Munter Framework barely evident; missing key stakeholder considerations | No audience analysis; no framework application |
| **Organization & Structure (30%)** | Perfect Pyramid Principle structure with conclusion first; flawless SCQA flow clearly establishing situation, complication, question, and answer | Strong Pyramid structure; clear SCQA framework with minor gaps in flow | Adequate top-down structure; attempts SCQA but incomplete or unclear | Weak structure; minimal Pyramid Principle application; confused SCQA | No clear structure; bottom-up organization |
| **Message Strategy (25%)** | Sophisticated message strategy directly addressing Shannon-Weaver communication challenges (technical, semantic, effectiveness levels); perfect channel selection for audience | Good message strategy; addresses most communication challenges; appropriate channel selection | Basic message strategy; addresses some challenges; acceptable channel choice | Weak strategy; doesn't address key challenges; poor channel fit | No strategic thinking; ignores communication barriers |
| **Professional Communication (15%)** | Flawless grammar, tone, and formatting; perfectly adapted to business context | Strong professional communication; minor errors | Adequate professionalism; some errors or tone inconsistencies | Weak professionalism; frequent errors | Unprofessional; pervasive errors |
```

### Week 7 Assessment (Frameworks: Weeks 1-6)

**Additional Frameworks Available:**
- Rhetorical Appeals (Week 4)
- Problem-Solution-Benefit Structure (Week 4)
- Communication Apprehension Theory (Week 5)
- Duarte Resonate (Week 6)
- Visual Communication Theory (Week 6)

**Rubric Example:**
```markdown
| Criteria | Excellent (94-100%) | Good (84-93%) | Satisfactory (74-83%) | Needs Work (60-73%) | Failing (<60%) |
|----------|---------------------|---------------|----------------------|---------------------|----------------|
| **Persuasive Strategy (35%)** | Masterfully employs 4+ Cialdini principles with specific examples; perfect ethos-pathos-logos balance using rhetorical appeals; compelling Problem-Solution-Benefit structure | Effectively uses 3+ Cialdini principles; strong rhetorical appeals balance; clear Problem-Solution-Benefit flow | Applies 2 Cialdini principles adequately; basic rhetorical appeals; attempts Problem-Solution-Benefit structure | Weak persuasion; 1 Cialdini principle evident; unbalanced appeals; unclear problem-solution link | No persuasive strategy; no Cialdini principles; no rhetorical structure |
| **Framework Integration (25%)** | Seamlessly integrates Pyramid Principle, SCQA, Munter Framework, and stakeholder analysis into cohesive argument; sophisticated strategic thinking | Integrates 2-3 frameworks effectively; good strategic coherence | Uses 1-2 frameworks; basic integration | Minimal framework integration; weak connections | No framework application |
| **Evidence & Credibility (20%)** | Exceptional evidence selection demonstrating authority (ethos); compelling emotional connection (pathos); flawless logic (logos) | Strong evidence across all appeals; good credibility building | Adequate evidence; addresses most appeals | Weak evidence; limited appeal to credibility | No credible evidence |
| **Clarity & Organization (20%)** | Perfect Pyramid structure throughout; every paragraph follows SCQA; effortless comprehension | Strong Pyramid organization; clear SCQA in most sections | Basic top-down structure; some SCQA application | Weak organization; little Pyramid Principle use | Disorganized; no clear structure |
```

---

## Generation Workflow

### Step 1: Extract Framework Timeline

```
1. Read syllabus Course Calendar table
2. Extract frameworks by week
3. Determine assessment due week
4. Filter to frameworks taught BEFORE due week
```

### Step 2: Select Relevant Frameworks

**For each assessment, identify 3-5 most relevant frameworks:**

**Example (Business Memo - Week 4):**
- Primary: Munter Framework (audience analysis focus)
- Primary: Pyramid Principle (structure focus)
- Secondary: SCQA (organization tool)
- Secondary: Stakeholder Mapping (audience identification)
- Tertiary: Communication Competence Theory (foundation)

### Step 3: Map Frameworks to Criteria

**Create 4-5 criteria, each referencing 1-2 specific frameworks:**

```
Criterion 1 (30%): Munter Framework + Stakeholder Mapping
Criterion 2 (30%): Pyramid Principle + SCQA
Criterion 3 (25%): Shannon-Weaver (message strategy)
Criterion 4 (15%): Professional standards
```

### Step 4: Write Framework-Specific Descriptors

**For each performance level:**
1. **Excellent:** "Masterfully applies [Framework]..." / "Expertly employs [Concept]..."
2. **Good:** "Effectively uses [Framework]..." / "Strong application of [Concept]..."
3. **Satisfactory:** "Adequately applies [Framework]..." / "Basic [Concept] use..."
4. **Needs Work:** "Weak [Framework] application..." / "Limited [Concept] understanding..."
5. **Failing:** "No [Framework] evident..." / "Missing [Concept]..."

### Step 5: Validate Alignment

**Checklist:**
- [ ] All frameworks referenced are taught before due week
- [ ] Each criterion references specific course content
- [ ] Performance descriptors are measurable
- [ ] Framework names are accurate (check spelling, attribution)
- [ ] Criteria weights sum to 100%
- [ ] No generic language like "good analysis" without framework reference

---

## Anti-Patterns to Avoid

### ❌ Generic Language

**Bad:**
```
| **Content** | Excellent analysis | Good analysis | Adequate analysis |
```

**Why bad:** Students don't know WHAT constitutes "excellent analysis"

**Good:**
```
| **Stakeholder Analysis (30%)** | Comprehensive Munter Framework analysis identifying all audience needs, KSIs, and communication barriers | Munter Framework applied to most stakeholders; identifies key needs | Basic Munter analysis; missing some stakeholder considerations |
```

### ❌ Frameworks Not Yet Taught

**Bad (Week 4 assessment):**
```
| **Persuasion** | Expertly applies Cialdini's 6 principles... |
```

**Why bad:** Cialdini taught in Week 7; students haven't learned it yet

**Good:**
```
| **Argument Structure** | Strong Problem-Solution-Benefit organization (Week 4 framework)... |
```

### ❌ Vague Performance Descriptors

**Bad:**
```
| **Organization** | Well organized | Organized | Somewhat organized |
```

**Why bad:** No clear standard; subjective judgment

**Good:**
```
| **Organization** | Perfect Pyramid Principle: conclusion first, then 3-4 supporting arguments in logical order; each paragraph follows SCQA | Pyramid structure evident; mostly top-down with minor bottom-up moments | Attempts Pyramid structure but inconsistent; some bottom-up reasoning |
```

### ❌ Too Many Frameworks Per Criterion

**Bad:**
```
| **Analysis** | Applies Munter, Pyramid, SCQA, Cialdini, Duarte, and Cultural Dimensions frameworks to... |
```

**Why bad:** Unrealistic to assess 6 frameworks in one criterion

**Good:**
```
| **Audience Strategy (30%)** | Expert Munter Framework and Stakeholder Mapping application... |
| **Organization (25%)** | Perfect Pyramid Principle and SCQA structure... |
| **Persuasion (25%)** | Masterful use of Cialdini's principles and rhetorical appeals... |
```

---

## Testing & Validation

After generating rubric, validate:

### Framework Accuracy
```python
# Check all framework references are spelled correctly
frameworks_mentioned = extract_frameworks_from_rubric(rubric)
for framework in frameworks_mentioned:
    assert framework in course_frameworks_list
    assert framework.taught_week < assessment.due_week
```

### Criterion Coverage
```
- [ ] Each criterion has specific framework reference
- [ ] Performance levels show clear progression
- [ ] Students can self-assess using these criteria
- [ ] Instructor can grade objectively using descriptors
```

### Backward Design Check
```
Question: "If students read only this rubric on Day 1, would they know what to learn?"

Answer should be: YES
- Rubric lists specific frameworks by name
- Students can identify what concepts are most important
- Clear connection between course content and assessment
```

---

## Integration with Brief Generation

When generating assessment briefs:

1. **Load this skill** (`rubric-generation.md`)
2. **Extract frameworks** from syllabus for assessment week
3. **Generate framework-specific rubric** using patterns above
4. **Include in brief** under ## Rubric section
5. **Validate** framework references before finalizing

---

## Summary

**Key Principles:**
1. Always reference specific frameworks taught in course
2. Only use frameworks taught BEFORE assessment due week
3. Make performance descriptors measurable and framework-specific
4. Students should know exactly what knowledge/skills are being assessed
5. Rubrics should drive instruction (backward design)

**Impact:**
- Students know what to learn (rubric clarity)
- Instruction is focused (teach what rubrics assess)
- Assessments are fair (students assessed on taught content)
- Course coherence (research → teaching → assessment alignment)
