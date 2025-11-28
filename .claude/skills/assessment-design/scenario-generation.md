# Scenario Generation for Assessment Handbooks

Guidance for AI-based generation of assessment scenarios using existing patterns from BCI2AU handbook.

---

## Purpose

Generate contextual, framework-aligned assessment scenarios that:
1. Match the course's teaching progression (only use frameworks taught before assessment)
2. Provide genuinely different options for students to choose from
3. Include specific, measurable deliverables
4. Reflect realistic business contexts

---

## Core Patterns (From BCI2AU Analysis)

### Pattern 1: Dual-Format Communication

**Use for:** Assessments requiring two related documents (e.g., Email + Memo)

**Structure:**
```markdown
**Option A: New Initiative Proposal**
- **[Format 1]:** [Action 1 - e.g., Request meeting with stakeholder]
- **[Format 2]:** [Action 2 - e.g., Recommend adoption to team]

**Option B: Problem Resolution**
- **[Format 1]:** [Action 1 - e.g., Request information from external party]
- **[Format 2]:** [Action 2 - e.g., Recommend solution to management]

**Option C: Create Your Own** (Instructor approval required)
- Propose your own scenario based on work experience or career interests
```

**Example (Email + Memo):**
```markdown
**Option A: New Initiative Proposal**
- **Email:** Request a meeting with your department head to discuss a new initiative you want to propose
- **Memo:** Write to your team recommending they adopt a new tool, process, or approach

**Option B: Problem Resolution**
- **Email:** Request information or resources from an external vendor/partner to solve a workplace challenge
- **Memo:** Write to management recommending a solution to a recurring operational problem

**Option C: Create Your Own** (Instructor approval required)
- Propose your own scenario based on your work experience or career interests
```

**Key Rules:**
- Options A/B address fundamentally different business situations
- Both require using the same two formats
- Frameworks taught before due week guide the approach
- Specific word counts included in requirements section, not scenarios

---

### Pattern 2: Audience-Specific Analysis

**Use for:** Assessments requiring data analysis with presentation to decision-makers

**Structure:**
```markdown
**Option A: [Analysis Type 1]**
- Dataset provided: [Data categories]
- Audience: [Specific role + decision context]

**Option B: [Analysis Type 2]**
- Dataset provided: [Data categories]
- Audience: [Specific role + decision context]

**Option C: [Analysis Type 3]** (if applicable)
- Dataset provided: [Data categories]
- Audience: [Specific role + decision context]
```

**Example (Data Visualization Report):**
```markdown
**Option A: Market Analysis**
- Dataset provided: Market share, growth rates, competitor positioning
- Audience: Marketing VP considering market entry strategy

**Option B: Performance Dashboard**
- Dataset provided: Department KPIs, quarterly trends, benchmark comparisons
- Audience: COO reviewing operational efficiency

**Option C: Financial Summary**
- Dataset provided: Revenue breakdown, cost analysis, profitability metrics
- Audience: CFO preparing for board presentation

*Datasets will be provided on Moodle by Week 4*
```

**Key Rules:**
- Audience is specific (title + decision context)
- Dataset types clearly stated
- May omit "Create Your Own" if datasets are provided
- Note when/where datasets will be available

---

### Pattern 3: Business Proposal Types

**Use for:** Persuasive proposals, recommendations, pitches

**Structure:**
```markdown
**Option A: [Proposal Type 1]**
[Brief description of proposal context]
Must include: [Key requirements specific to this type]

**Option B: [Proposal Type 2]**
[Brief description of proposal context]
Must include: [Key requirements specific to this type]

**Option C: [Proposal Type 3]**
[Brief description of proposal context]
Must include: [Key requirements specific to this type]

**Option D: Create Your Own** (Instructor approval required)
```

**Example (Persuasive Proposal):**
```markdown
**Option A: Innovation Proposal**
Propose a new product, service, or business initiative to senior leadership. Must include market opportunity, resource requirements, and expected ROI.

**Option B: Change Management Proposal**
Propose a significant change to how your organization operates (new technology adoption, process redesign, organizational restructuring). Must address stakeholder concerns and implementation plan.

**Option C: Investment Pitch**
Propose that investors fund your business idea. Must include problem statement, solution, market size, competitive advantage, and ask.

**Option D: Create Your Own** (Instructor approval required)
```

**Key Rules:**
- 3-4 options (including "Create Your Own")
- Each option has distinct business context
- "Must include" requirements are high-level (details in requirements section)
- All options require same core frameworks but apply them differently

---

### Pattern 4: Reflection and Development

**Use for:** Personal reflection, development planning, self-assessment

**Structure:**
```markdown
[Instructions for reflection scope, no scenario options needed]

OR

**Focus Option A: [Development Area 1]**
[Guidance for this focus]

**Focus Option B: [Development Area 2]**
[Guidance for this focus]
```

**Example (Reflection + Development Plan):**
```markdown
Complete a personal communication audit and create a 12-month development plan. This assessment demonstrates your ability to self-diagnose communication strengths and create actionable growth strategies.

[No scenario options - single reflective task]
```

**Key Rules:**
- May not have scenario options if single reflective task
- If options provided, they're focus areas not scenarios
- Emphasis on self-directed content
- Requirements provide structure, not scenarios

---

### Pattern 5: Presentation Contexts

**Use for:** Pitch presentations, formal presentations, briefings

**Structure:**
```markdown
**Option A: [Presentation Context 1]**
[Description of audience, purpose, setting]

**Option B: [Presentation Context 2]**
[Description of audience, purpose, setting]

**Option C: [Presentation Context 3]**
[Description of audience, purpose, setting]

**Option D: Create Your Own** (Instructor approval required)
```

**Example (Final Presentation):**
```markdown
**Option A: Business Recommendation**
Present a strategic recommendation to a board or leadership team. Include problem analysis, options evaluation, recommendation, and implementation plan.

**Option B: Thought Leadership**
Present an original perspective on a business communication topic. Teach something valuable to your peers with evidence and practical applications.

**Option C: Case Analysis**
Analyze a real communication success or failure (corporate crisis, viral campaign, leadership speech). What happened, why, and what can we learn?

**Option D: Personal Brand Presentation**
Present your professional story, unique value proposition, and career vision. Integrate course frameworks into a compelling personal narrative.
```

**Key Rules:**
- 3-4 options covering different presentation purposes
- Each has distinct audience/context
- All use same presentation frameworks
- Complexity appropriate to course stage

---

## AI Generation Rules

### Rule 1: Framework Alignment

**Extract frameworks from syllabus:**
1. Identify assessment due week (e.g., Week 7)
2. Extract "Foundational Frameworks" column from syllabus for weeks 1 to (due_week - 1)
3. Only reference frameworks taught in those weeks

**Example:**
- Assessment: Persuasive Proposal (Week 7)
- Available frameworks: Weeks 1-6
  - Week 2: Pyramid Principle, MECE
  - Week 3: BLUF, Clear writing principles
  - Week 4: Tufte principles, Data visualization
  - Week 5: Presentation structure, Delivery mechanics
  - Week 6: Cialdini's principles, Aristotle's appeals
- Scenarios should reference persuasion frameworks from Week 6, structure from Week 2-3

**DO NOT:**
- Reference frameworks not yet taught
- Use week numbers in scenarios (just framework names)
- Assume frameworks without checking syllabus

---

### Rule 2: Structural Consistency

**Always provide:**
- 2-3 options minimum (usually 2-4)
- Last option often "Create Your Own (Instructor approval required)"
- Bold option headers: `**Option A: Title**`
- Consistent labeling: A, B, C, D (not 1, 2, 3)

**Ensure genuine differentiation:**
- Options should be fundamentally different situations
- NOT: "Propose marketing tool" vs "Propose sales tool" (too similar)
- YES: "Propose new initiative" vs "Resolve existing problem" (different contexts)

**Pattern selection:**
- Email + Memo → Dual-Format Communication
- Data analysis → Audience-Specific Analysis
- Proposals/pitches → Business Proposal Types
- Reflection → Single task or Focus Areas
- Presentations → Presentation Contexts

---

### Rule 3: Specificity Requirements

**Include in scenarios:**
- WHO: Specific roles (Marketing VP, department head, investors)
- WHAT: Specific deliverables (email + memo, one-page report, pitch deck)
- WHY: Decision context (considering market entry, reviewing efficiency)
- CONSTRAINTS: Implied by context (formal/informal, internal/external)

**Measurable details go in Requirements section, not scenarios:**
- Word counts: "250-350 words" → Requirements section
- Format specs: "PDF with embedded charts" → Submission Format
- Specific frameworks: "Use Cialdini's principles" → Requirements section

**Example - Good Specificity:**
```markdown
**Option A: Market Analysis**
- Dataset provided: Market share, growth rates, competitor positioning
- Audience: Marketing VP considering market entry strategy
```

**Example - Poor Specificity:**
```markdown
**Option A: Analysis**
- Data provided
- Present to leadership
```

---

### Rule 4: Business Realism

**Use realistic business contexts:**
- Actual job roles (not "manager X" or "person Y")
- Real business decisions (market entry, cost reduction, product launch)
- Authentic communication challenges (persuading skeptical stakeholders, delivering bad news)

**Avoid:**
- Academic framing ("For this assignment...")
- Hypothetical abstraction ("Imagine a company...")
- Generic roles ("Business leader", "Organization member")

**Good Examples:**
- "Marketing VP considering market entry strategy"
- "Request meeting with department head to discuss new initiative"
- "Recommend solution to recurring operational problem"

**Poor Examples:**
- "Leader making a decision"
- "Write about a business situation"
- "Communicate something important"

---

### Rule 5: Complexity Matching

**Week 3-4 (Early):**
- Simpler scenarios
- Individual documents
- Single framework application
- Familiar contexts

Example: "Write email requesting meeting + memo recommending tool adoption"

**Week 5-7 (Mid):**
- Moderate complexity
- Multi-part deliverables
- Multiple framework integration
- Professional contexts

Example: "Analyze market data + create one-page exec summary with visualization"

**Week 8-10 (Late):**
- High complexity
- Comprehensive deliverables
- Integrated framework application
- Strategic contexts

Example: "Present strategic recommendation with problem analysis, options evaluation, and implementation plan"

---

## Quality Checklist

Before finalizing scenarios, verify:

**Framework Alignment:**
- [ ] Frameworks referenced are taught before assessment due week
- [ ] Scenarios allow application of 2-3 specific frameworks
- [ ] No mention of frameworks not yet covered

**Structural Consistency:**
- [ ] 2-4 options provided with consistent labeling (A, B, C, D)
- [ ] Last option is usually "Create Your Own"
- [ ] Options are genuinely different (not minor variations)
- [ ] Pattern matches assessment type

**Specificity:**
- [ ] WHO specified (roles, audiences)
- [ ] WHAT specified (deliverables, contexts)
- [ ] WHY specified (decision contexts)
- [ ] Measurable details moved to Requirements section

**Business Realism:**
- [ ] Realistic roles and titles
- [ ] Authentic business decisions
- [ ] Professional communication challenges
- [ ] No academic framing

**Complexity Matching:**
- [ ] Scenario complexity appropriate to week
- [ ] Deliverable scope matches course stage
- [ ] Framework integration level matches student readiness

---

## Example High-Quality Scenarios

### Week 3: Email + Memo (Dual-Format Communication)

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

**Why this works:**
- Uses Dual-Format pattern (appropriate for email + memo)
- Options A/B are genuinely different (new initiative vs problem solving)
- Specific roles (department head, team, vendor, management)
- Frameworks Week 1-2: Pyramid Principle, BLUF, Audience analysis (can be applied)
- Complexity appropriate for Week 3 (straightforward documents)

---

### Week 5: Data Visualization Report (Audience-Specific Analysis)

```markdown
#### Scenario

You are a business analyst presenting findings to senior leadership. Choose ONE dataset:

**Option A: Market Analysis**
- Dataset provided: Market share, growth rates, competitor positioning
- Audience: Marketing VP considering market entry strategy

**Option B: Performance Dashboard**
- Dataset provided: Department KPIs, quarterly trends, benchmark comparisons
- Audience: COO reviewing operational efficiency

**Option C: Financial Summary**
- Dataset provided: Revenue breakdown, cost analysis, profitability metrics
- Audience: CFO preparing for board presentation

*Datasets will be provided on Moodle by Week 4*
```

**Why this works:**
- Uses Audience-Specific pattern
- Three distinct analysis types (market, performance, financial)
- Specific roles with decision contexts
- Frameworks Week 1-4: Tufte principles, Executive summaries, Visual design
- Note about dataset availability (practical detail)
- Complexity appropriate for Week 5 (data + visualization + summary)

---

### Week 7: Persuasive Proposal (Business Proposal Types)

```markdown
#### Scenario (Choose ONE)

**Option A: Innovation Proposal**
Propose a new product, service, or business initiative to senior leadership. Must include market opportunity, resource requirements, and expected ROI.

**Option B: Change Management Proposal**
Propose a significant change to how your organization operates (new technology adoption, process redesign, organizational restructuring). Must address stakeholder concerns and implementation plan.

**Option C: Investment Pitch**
Propose that investors fund your business idea. Must include problem statement, solution, market size, competitive advantage, and ask.

**Option D: Create Your Own** (Instructor approval required)
```

**Why this works:**
- Uses Business Proposal pattern
- Four distinct proposal contexts (innovation, change, investment, custom)
- Each has different stakeholder and requirements
- Frameworks Week 1-6: Pyramid Principle, SCQ, Cialdini's persuasion, Storytelling
- "Must include" gives high-level structure (details in Requirements section)
- Complexity appropriate for Week 7 (comprehensive proposals)

---

## Common Mistakes to Avoid

### Mistake 1: Framework Misalignment

**Wrong:**
```markdown
Week 3 Email + Memo assessment references:
"Apply storytelling techniques from Week 7"
```

**Reason:** Week 7 hasn't been taught yet when assessment is due Week 3.

**Right:**
```markdown
Week 3 Email + Memo assessment references:
"Use Pyramid Principle (Week 2) and BLUF structure (Week 3)"
```

---

### Mistake 2: Minor Variations Instead of Genuine Options

**Wrong:**
```markdown
**Option A: Marketing Tool Proposal**
**Option B: Sales Tool Proposal**
**Option C: HR Tool Proposal**
```

**Reason:** All three are nearly identical (just different departments).

**Right:**
```markdown
**Option A: New Initiative Proposal** (proactive)
**Option B: Problem Resolution** (reactive)
**Option C: Create Your Own**
```

---

### Mistake 3: Vague Deliverables

**Wrong:**
```markdown
**Option A: Business Analysis**
Analyze something and present your findings.
```

**Reason:** Too vague (analyze what? present to whom? what format?).

**Right:**
```markdown
**Option A: Market Analysis**
- Dataset provided: Market share, growth rates, competitor positioning
- Audience: Marketing VP considering market entry strategy
```

---

### Mistake 4: Academic Framing

**Wrong:**
```markdown
**Option A: Assignment Scenario**
For this assignment, imagine you work at a company and need to write a proposal.
```

**Reason:** Breaks immersion, feels like a school exercise.

**Right:**
```markdown
**Option A: Innovation Proposal**
Propose a new product, service, or business initiative to senior leadership.
```

---

### Mistake 5: Measurable Details in Scenarios

**Wrong:**
```markdown
**Option A: Email + Memo**
- **Email:** 250-350 words requesting meeting using BLUF structure
- **Memo:** 400-500 words with Pyramid Principle and 3 arguments minimum
```

**Reason:** Too much detail in scenario (should be in Requirements section).

**Right:**
```markdown
**Option A: New Initiative Proposal**
- **Email:** Request a meeting with your department head
- **Memo:** Recommend your team adopt a new tool/process

[Word counts and structure requirements go in Requirements section]
```

---

## Integration with handbook-generation.md

This skill is referenced by `handbook-generation.md` for:
1. Pattern selection based on assessment type
2. AI generation rules for contextual scenarios
3. Quality standards for scenario content
4. Examples of high-quality scenarios

When generating scenarios:
1. Identify assessment type from syllabus
2. Select appropriate pattern from this guide
3. Apply AI generation rules (framework alignment, specificity, etc.)
4. Validate against quality checklist
5. Integrate into handbook structure from handbook-generation.md
