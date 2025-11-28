# Tutorial Activities Skill

## Prerequisites 🔐

**Required before generating tutorials:**
1. ✅ `syllabus.md` - Course structure and assessment overview
2. ✅ `assessment-handbook.md` - Scenarios, requirements, rubrics (MUST exist)
3. ✅ `lecture-content.md` - Week's frameworks for Quick Review

**Why Assessment Handbook must exist first:**
- Tutorials practice assessment scenarios (can't reference non-existent content)
- Success criteria come from rubric criteria (must be defined)
- Deliverables must match assessment formats (handbook specifies these)

---

## Core Structure (90 min) 🔐

| Phase | Time | Purpose |
|-------|------|---------|
| Quick Review | 5 min | Lecture recap + success criteria |
| Main Activity | 75 min | ONE task with deliverable + class feedback |
| Before Next Class | 10 min | 3 items only |

**Key rules:**
- NO inline timing in tutorial-content.md (timing goes in tutor-notes)
- NO separate "Assessment Connection" section (already in header)
- NO separate "Success Looks Like" section (merged into Quick Review)
- NO simplified rubric table (reference Assessment Handbook instead)

---

## Assessment Handbook Integration 🔐

Tutorials exist to prepare students for graded assessments. Every tutorial activity must directly practice a skill, format, or scenario from the Assessment Handbook.

### Mapping Weeks to Assessments

Before generating a tutorial, identify which assessment the week prepares for:

```
Week 1-2 → Email + Memo (Due Week 3)
Week 3-4 → Data Visualization Report (Due Week 5)
Week 5-6 → Persuasive Proposal (Due Week 7)
Week 7-8 → Critical Reflection (Due Week 9)
Week 9-10 → Executive Summary (Due Week 10)
Week 11-12 → Group Presentation (Due Week 12)
```

### Extracting From Assessment Handbook

For each tutorial, extract from the relevant assessment section:

| Extract | Location in Handbook | Use in Tutorial |
|---------|---------------------|-----------------|
| Scenario types | `#### Scenario (Choose ONE)` | Tutorial practices ONE scenario type |
| Deliverable format | Task Overview + Requirements | Tutorial deliverable matches format |
| Word counts/lengths | Requirements checklist | Tutorial uses scaled-down version |
| Rubric criteria | `#### Rubric Preview` table | Success Criteria in tutorial |
| Framework requirements | Scenario descriptions | Lecture concepts to apply |

### Tutorial Deliverable Scaling

Tutorials use **scaled-down versions** of assessment deliverables:

| Assessment Deliverable | Tutorial Practice |
|------------------------|-------------------|
| 350-word email + 500-word memo | 150-word email OR 200-word memo |
| 3-page data report | 1-page data analysis |
| 800-word proposal | 300-word proposal outline |
| 600-word reflection | 200-word reflection draft |
| 5-minute presentation | 2-minute mini-pitch |

### Success Criteria = Rubric Criteria

**DO NOT invent success criteria.** Pull directly from the Assessment Handbook rubric:

```markdown
## From Assessment Handbook:
| Criteria | Weight | Focus |
|----------|--------|-------|
| Content & Strategy | 25% | Message suits audience/purpose |
| Organization | 25% | BLUF/Pyramid structure applied |
| Clarity & Concision | 20% | Clear meaning; economical language |

## Tutorial Success Criteria (same criteria, tutorial scope):
**Success Criteria:**
- Message clearly addresses the specific audience and purpose
- BLUF structure evident in first paragraph
- No unnecessary words or phrases
```

---

## Quick Review (5 min)

ONE section combining lecture recap with success criteria.

```markdown
## Quick Review

**Key concepts from today's lecture:**
- [Concept 1 with brief explanation]
- [Concept 2 with brief explanation]
- [Concept 3 with brief explanation]

**What good work looks like:**
- [Success criterion 1 from rubric]
- [Success criterion 2 from rubric]

**Full rubric:** See Assessment Handbook, Section [X]
```

---

## Main Activity (75 min) 🔐

ONE consolidated task with clear deliverable. No fragmented phases.

**CRITICAL:** The activity must practice a SPECIFIC scenario type from the Assessment Handbook.

### Activity Selection Process

1. **Identify the target assessment** (use Week→Assessment mapping above)
2. **Read the assessment's scenario options** from Assessment Handbook
3. **Choose ONE scenario type** to practice (not exact scenario - a similar practice version)
4. **Scale down the deliverable** to tutorial length (see scaling table)
5. **Copy rubric criteria** as success criteria (do not invent new criteria)

### Activity-Assessment Alignment

| Assessment Type | Tutorial Activity | Handbook Source |
|-----------------|-------------------|-----------------|
| Email + Memo | Draft scaled email OR memo | Scenario Option A or B format |
| Data Visualization | Analyze single chart | Report requirements + rubric |
| Persuasive Proposal | Outline proposal structure | Proposal scenario format |
| Critical Reflection | Short reflection paragraph | Reflection requirements |
| Executive Summary | Summarize case study | Executive Summary requirements |
| Presentation | 2-minute mini-pitch | Presentation rubric criteria |

### Format

```markdown
## Main Activity: [Activity Name - reference assessment type]

**Assessment Connection:** [Assessment Name] (Due Week [N]) - this activity practices [specific skill/format]

**The Task:**
[Clear description of what students will produce - must match assessment format]

**Deliverable:**
[Specific output matching scaled assessment format - e.g., "150-word email using BLUF structure"]

**Success Criteria:** (from [Assessment Name] Rubric)
- [Criterion 1 - exact wording from rubric, scoped to tutorial]
- [Criterion 2 - exact wording from rubric, scoped to tutorial]
- [Criterion 3 - exact wording from rubric, scoped to tutorial]

**Resources:**
- [Scenario similar to Assessment Handbook Option A/B]
- [Framework reference from lecture]

**Class Feedback:**
At the end of the session, 4-6 students will share their work. Be prepared to:
- Show your deliverable
- Explain one decision you made
- Answer one question from peers

⚠️ **Participation:** You must produce a deliverable to share. Incomplete work will affect participation marks.
```

---

## Before Next Class (10 min)

Exactly three items. No vague tasks.

```markdown
## Before Next Class

1. **Complete Online Quiz** - Week N Quiz on Moodle (due [day/time])
2. **Pre-reading for Week N+1** - [Specific reading with page numbers]
3. **Save Your Work** - Keep [deliverable] for portfolio reference
```

**Do NOT include:**
- Observation tasks ("notice X around you")
- Reflection prompts ("start thinking about...")
- Revision reminders (they know)
- Assessment handbook reminders (they have it)

---

## Tutor Notes Must Include 🔐

### Timing Table (at top of tutor notes)

```markdown
## Session Timing

| Phase | Duration | Notes |
|-------|----------|-------|
| Quick Review | 5 min | Lecture recap + success criteria |
| Main Activity | 65 min | Students work on deliverable |
| Class Feedback | 10 min | 4-6 students share (2 min each) |
| Before Next Class | 10 min | Review 3 items |

**Selection for feedback:** Random or volunteer. All must be ready.
**If time short:** Reduce to 3 sharers, 90-second each.
```

### Other Required Sections

- 3-5 valid student approaches (not one "right" answer)
- Common misconceptions to address
- Facilitation tips for quiet groups
- Cultural considerations if relevant

---

## Example Activity (Persuasion Week)

```markdown
## Quick Review

**Key concepts from today's lecture:**
- **Cialdini's 6 Principles:** Reciprocity, commitment, social proof, authority, liking, scarcity
- **Ethos/Pathos/Logos:** Credibility, emotion, logic in persuasive appeals
- **Ethical persuasion:** Influence without manipulation

**What good work looks like:**
- Clear use of 2+ Cialdini principles
- Professional tone maintained
- Request specific and actionable

**Full rubric:** See Assessment Handbook, Section 6

---

## Main Activity: Persuasive Email Draft

**The Task:**
Draft a persuasive email requesting approval for a new software tool from your manager.

**Deliverable:**
150-word persuasive email using at least 2 of Cialdini's principles

**Success Criteria:**
- Principles clearly identifiable in the text
- Professional tone maintained throughout
- Specific request with clear next step

**Resources:**
- Scenario card (provided)
- Cialdini principles quick reference (Slide 12)

**Class Feedback:**
4-6 students will share. Be prepared to:
- Read your email aloud
- Identify which principles you used
- Explain why you chose them

⚠️ **Participation:** You must have a complete draft to share. Incomplete work will affect participation marks.

---

## Before Next Class

1. **Complete Online Quiz** - Week 6 Quiz on Moodle (due Sunday 11:59 PM)
2. **Pre-reading for Week 7** - Storytelling chapter (pp. 89-112)
3. **Save Your Work** - Keep persuasive email for portfolio reference
```

---

## Good vs Bad Examples 🔐

### BAD Tutorial (Generic, No Assessment Connection)

```markdown
## Main Activity: Communication Practice

**The Task:**
Work in groups to discuss communication challenges in the workplace.

**Deliverable:**
Group discussion notes

**Success Criteria:**
- Participated in discussion
- Shared at least one idea
- Listened to others

**Resources:**
- Discussion questions handout
```

**Problems:**
- ❌ No connection to any specific assessment
- ❌ Deliverable doesn't match any assessment format
- ❌ Success criteria are generic, not from rubric
- ❌ No portfolio value - nothing to keep
- ❌ Students can't practice assessment skills

---

### GOOD Tutorial (Direct Assessment Alignment)

**Context:** Week 2 prepares for Email + Memo (Due Week 3). Assessment Handbook shows:
- Scenario Option A: "Internal memo requesting budget approval for training program"
- Rubric criteria: Content & Strategy (25%), Organization (25%), Clarity (20%)
- Deliverable: 350-word email + 500-word memo

```markdown
## Main Activity: Business Memo Draft (Email + Memo Practice)

**Assessment Connection:** Email + Memo Portfolio (Due Week 3) - this activity practices memo structure and Pyramid Principle application

**The Task:**
Draft a 200-word internal memo requesting budget approval, using the Pyramid Principle to structure your argument.

**Deliverable:**
200-word memo with clear recommendation, 3 supporting points, and specific ask (scaled from 500-word assessment memo)

**Success Criteria:** (from Written Communication Rubric)
- Content & Strategy: Message clearly addresses the manager audience with appropriate supporting evidence
- Organization: Pyramid structure evident - main point first, supporting points follow logically
- Clarity & Concision: No unnecessary words; every sentence advances the argument

**Resources:**
- Scenario: Your department needs a $5,000 training budget. Write a memo to your supervisor requesting approval.
- Pyramid Principle template (Slide 8 from lecture)
- Sample memo structure (Assessment Handbook, Section 1)

**Class Feedback:**
4-6 students will share. Be prepared to:
- Read your opening paragraph (the "so what?")
- Explain how you applied Pyramid Principle
- Identify your strongest supporting point

⚠️ **Participation:** You must have a complete 200-word draft to share.
```

**Why this works:**
- ✅ Directly practices assessment format (memo)
- ✅ Uses scenario similar to Assessment Handbook Option A
- ✅ Deliverable scales assessment format (200 vs 500 words)
- ✅ Success criteria pulled from actual rubric
- ✅ Applies lecture framework (Pyramid Principle)
- ✅ Portfolio value - draft contributes to assessment preparation

---

### Tutorial Progression Example

Shows how tutorials build toward a single assessment across multiple weeks:

| Week | Assessment Target | Tutorial Activity | Skill Practiced |
|------|-------------------|-------------------|-----------------|
| Week 1 | Email + Memo (Week 3) | MKS Self-Assessment | Self-awareness, development planning |
| Week 2 | Email + Memo (Week 3) | Memo draft using Pyramid Principle | Memo structure, argument organization |
| Week 3 | Data Viz (Week 5) | Mini-chart analysis | Chart selection, audience focus |
| Week 4 | Data Viz (Week 5) | Data storytelling paragraph | Tufte principles, clarity |
| Week 5 | Proposal (Week 7) | Persuasive opening paragraph | Cialdini principles, BLUF |
| Week 6 | Proposal (Week 7) | Proposal outline structure | Full proposal organization |

---

## Validation Checklist

Before finalizing tutorial content, verify:

### Assessment Alignment
- [ ] Target assessment identified (Week→Assessment mapping)
- [ ] Activity practices specific skill from assessment
- [ ] Scenario similar to Assessment Handbook options
- [ ] Deliverable format matches assessment format (scaled)

### Success Criteria
- [ ] Criteria pulled from Assessment Handbook rubric
- [ ] NOT invented or generic
- [ ] Scoped appropriately for tutorial deliverable

### Portfolio Value
- [ ] Deliverable has tangible output student can keep
- [ ] Output contributes to assessment preparation
- [ ] "Save Your Work" in Before Next Class section

### Framework Application
- [ ] Activity requires applying lecture frameworks
- [ ] Resources reference lecture materials
