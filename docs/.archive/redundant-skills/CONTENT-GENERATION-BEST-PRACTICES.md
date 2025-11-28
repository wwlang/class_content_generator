# Content Generation Best Practices

**Purpose:** Single source of truth for ALL content generation rules - read BEFORE generating any lecture or tutorial content.

**Version:** 2.0 (Consolidated)
**Last Updated:** January 19, 2025

---

## Quick Reference - Critical Constraints

| Element | Limit | Action if Exceeded |
|---------|-------|-------------------|
| **Slide Content** | 150-200 words | Split into 2 slides |
| **Bullets per slide** | 5-7 max | Split into 2 slides |
| **Quote length** | 2-3 lines | Use content slide instead |
| **Vocab terms** | 4-6 max | Split across 2 slides |
| **Framework components** | 3-6 optimal | Split into 2 frameworks |
| **Comparison rows** | 4-6 max | Simplify or split |
| **Speaker notes** | 3-8 lines | Be more concise |
| **Total slides** | 22-30 | Adjust content density |

---

## Table of Contents

1. [Slide Content Requirements](#slide-content-requirements)
2. [Splitting Rules - When to Split Slides](#splitting-rules---when-to-split-slides)
3. [Speaker Notes Rules](#speaker-notes-rules)
4. [Layout Usage & Hints](#layout-usage--hints)
5. [Tutorial Content Requirements](#tutorial-content-requirements)
6. [Pre-Generation Checklist](#pre-generation-checklist)
7. [During Generation Checklist](#during-generation-checklist)

---

## Slide Content Requirements

### Content Must Stand Alone

**Slides need sufficient detail to be self-contained** - not just sparse bullets.

✅ **DO include ON the slide:**
- Core concepts with enough detail to understand without speaker
- Examples, data, frameworks directly on slide (not just in notes)
- Inline citations for all sourced material (Author, Year)
- Full APA reference at bottom if source heavily referenced

❌ **DON'T:**
- Create sparse bullet-only slides requiring speaker explanation
- Put critical content only in speaker notes
- Omit citations, examples, or context from slide

### Word Count Limits

**Target: 150-200 words per slide maximum**

- Count all text on slide (title, bullets, body text, citations)
- If exceeds 200 words → **SPLIT into 2 slides**
- Better two focused slides than one overwhelming slide

### Lecture Structure

**90-minute lecture = 22-30 slides total**

- **Opening (4-6 slides):** Title, vocab, objectives, assessment connection
- **Core content (14-20 slides):** 3-4 major segments with section breaks
- **Wrap-up (4-6 slides):** Synthesis, checklist, references, closing

---

## Splitting Rules - When to Split Slides

### Bullet Points
- **Max 5-7 bullets per slide**
- Each bullet max 1-2 lines (20 words)
- More than 7 bullets? → **SPLIT into 2 slides**
- Don't number bullets 1-8 on one slide

### Quote Slides
- **Max 2-3 lines** for quote slide layout
- Longer quote? → **Use standard content slide** with blockquote
- Attribution should be 1 line

### Vocabulary/Definition Tables
- **Max 4-6 terms** per slide (with Vietnamese translations)
- 10+ terms? → **SPLIT across 2-3 slides**
- Keep definitions to 1-2 lines each

### Framework Slides
- **Optimal: 3-6 components**
- 8+ components? → **SPLIT into 2 frameworks** or simplify
- Keep component descriptions to 1-2 lines each

### Comparison Tables
- **Max 4-6 rows** for readability
- Use concise phrases, not full sentences
- Balance content length in both columns

### General Cluttered Content
- **If slide feels cluttered → SPLIT**
- Use 2-column grid layout for moderate content
- Use cards layout for 3-6 related concepts
- Trust your judgment: overwhelming = split

### Example: Splitting a Verbose Slide

**BEFORE (Verbose - 250 words, 8 bullets):**
```markdown
**SLIDE 11: Autonomy in Vietnamese Workplace Context**

**Pink's first element: Autonomy**
- Definition of autonomy
- Four types of autonomy
- Research findings
- Vietnamese cultural context
- Examples from Vingroup, VNG
- Balance with hierarchy
- How to find autonomy pockets
- Interview questions to ask

[TOO LONG - exceeds limits]
```

**AFTER (Split into 2 slides - each ~90 words, 4 bullets):**
```markdown
**SLIDE 11: Autonomy - The First Element of Drive**

**Pink's first element: Autonomy (Pink, 2009)**

The desire to direct your own work - choosing:
- **What** you work on (task autonomy)
- **When** you work (time autonomy)
- **How** you do it (technique autonomy)
- **Who** you work with (team autonomy)

**Research finding:** Autonomy increases motivation, creativity, and job satisfaction by 40% (Deci & Ryan, 2000).

---

**SLIDE 12: Autonomy in Vietnamese Workplace Culture**

**Cultural adaptation of autonomy:**

Vietnamese workplace values hierarchy. How does autonomy fit?

**Modern Vietnamese companies finding balance:**
- **Vingroup, VNG**: Project-based autonomy within reporting structure
- **Agile teams**: Choose HOW, not WHETHER
- **Example**: Devs decide tech approach; managers set goals

**Key insight:** Autonomy within structure, not instead of it.

*Source: Vietnam Tech Talent Report 2024*
```

---

## Speaker Notes Rules

### Length Requirement
**3-8 lines per slide** - ruthlessly concise

### Core Principles

✅ **DO include:**
- Deeper context students can't get from reading slide
- Common misconceptions or confusion points to address
- Timing guidance (how long to pause, when to move on)
- Key questions to ask (not exact scripted wording)
- Cultural considerations for Vietnamese students
- Concrete examples NOT already on slide
- Connections to prior concepts or upcoming assessments
- What successful responses look like

❌ **DON'T include:**
- Restating definitions/frameworks already visible on slide
- Generic transitions ("Now let's move to...")
- Over-explaining self-evident content
- Dramatic language ("Stop them!", "Watch for...")
- Scripting exact words for instructor to say
- **Prescriptive physical actions:** "walk around," "circulate," "make eye contact," "point to slide"

### Voice and Tone

- **Professional and succinct** - not formal academic, not casual
- **Complete sentences** that flow naturally when read aloud
- **Direct to instructor:** "Point out that..." not "Students will see..."
- **Neutral:** Avoid drama, trust instructor judgment

### Match Slide Type

Different slides need different support:

**Quote slide:**
```markdown
## Speaker Notes

Students typically interpret "mastery" as perfection. Clarify that Senge means discipline - daily practice, not a destination.

After reading, pause briefly. Ask which of the four verbs resonates most with where they are now. Take 2-3 responses.
```

**Framework slide:**
```markdown
## Speaker Notes

Students have already practiced all four components this semester. This is synthesis, not new material.

Common mistake: setting time-based goals without clear outcomes or feedback. This creates directionless effort.

Have students identify which component is weakest in their plan. Give them 30 seconds.
```

**Reflection slide:**
```markdown
## Speaker Notes

Give them 2 minutes. Remind them to write answers rather than just think - writing surfaces insights thinking alone misses.

Maintain silence during reflection. This needs genuine thinking time.

When time's up, ask if anyone discovered something surprising. Take one volunteer if offered.
```

---

## Layout Usage & Hints

### The 18 Available Layouts

**Use layouts that best present your content - visual variety should emerge naturally from diverse content.**

**Foundational (3):**
1. **title-slide** - Course opening (slide 1)
2. **section-break** - Major topic transitions or framework introductions
3. **content-slide** - Standard explanations and applications

**Structured Content (4):**
4. **vocab-table-slide** - Key terms (4-6 terms)
5. **objectives-slide** - Learning objectives (3-5)
6. **checklist-slide** - Assessment requirements
7. **references-slide** - Citations (end of lecture)

**Visual Impact (3):**
8. **big-number-slide** - ONE statistic (dramatic)
9. **stats-banner** - 2-4 metrics dashboard
10. **quote-slide** - Expert quotes (2-3 lines)

**Comparisons (3):**
11. **comparison-slide** - Side-by-side boxes
12. **comparison-table-slide** - Detailed 2-column table
13. **framework-slide** - Process/model diagrams

**Interaction (2):**
14. **activity-slide** - In-class exercises
15. **reflection-slide** - Contemplation prompts

**Grouped Content (1):**
16. **card-layout** - 3-6 visual cards with icons

**Modifiers (2):**
17. **dark-slide** - Dark background for Vietnamese examples and case studies
18. **grid patterns** - 2-col or 3-col layouts

### Layout Distribution Example (Content-Driven)

**Example 26-slide lecture with natural layout variety:**

```
Opening (4): title, vocab, objectives, assessment
Section Break 1: Understanding Communication Models
Core Segment 1 (4): framework, content, comparison-table, dark-slide
Section Break 2: Strategic Message Design
Core Segment 2 (5): big-number, content, card-layout, activity, content
Section Break 3: Building Credibility
Core Segment 3 (5): quote, content, reflection, content x2
Wrap-up (5): synthesis, stats-banner, tutorial preview, checklist, references
```

**Principles for natural variety:**
- **Section breaks** align with major frameworks and topic shifts (not arbitrary counts)
- **Visual layouts** (big-number, quote, framework, cards) used when content merits emphasis
- **Dark slides** used for Vietnamese examples and case studies that benefit from emphasis
- **Content slides** used for explanations and applications - no percentage target

### Prescriptive Layout Hints

**Use HTML comments to guarantee correct layout:**

```markdown
<!-- LAYOUT: quote -->
"Quote text here"
— Attribution (Author, Year)

<!-- LAYOUT: framework -->
**Component 1:** Description
**Component 2:** Description

<!-- LAYOUT: reflection -->
What question prompts thinking?

<!-- LAYOUT: comparison-table -->
| Column A | Column B |

<!-- LAYOUT: references -->
- Citation in APA format
```

**When to use hints:**
- ✅ Quotes, frameworks, reflections, comparison tables, references
- ⚠️ Optional for standard content, bullet lists

---

## Tutorial Content Requirements

### Two Separate Files

**1. tutorial-content.md** (Student-facing):
- Activity instructions, datasets, quiz questions (NO answers)
- High-level section timings
- Rubric checklist, peer review sentence starters
- **NO** "Tutor:" notes, "Expected:" answers, facilitation guidance

**2. tutorial-tutor-notes.md** (Instructor-facing):
- Complete quiz answer keys with explanations (why correct, why each distractor wrong)
- 3-5 valid student approaches to main activity
- Facilitation tips, quality indicators, timing flexibility
- Professional conversational tone

### Tutorial Structure (90 minutes)

**Opening (10 min):**
- Quick review (3 key concepts from lecture)
- Assessment preview with simplified rubric (3-4 criteria)
- Reference full details: "See Assessment Handbook Section X" or "See syllabus"

**Main Activity (55-60 min):**
- ONE substantial activity that mirrors actual assessment
- Task-based writing (clear deliverable, not micro-steps)
- Peer review using rubric criteria
- Multiple valid approaches explicitly acknowledged

**Quiz Prep (15-20 min):**
- 6-10 multiple-choice questions
- Direct questions, NOT scenarios
- Test Remembering + Understanding (Bloom's) only
- Based on slide content ONLY (NOT speaker notes)

**Wrap-up (5-10 min):**
- Self-assessment checklist against rubric
- Next steps for assessment preparation

### Quiz Question Rules (CRITICAL)

**Content Source:**
- ✅ Test ONLY slide content (consistent across all instructors)
- ❌ NEVER test speaker notes (varies by instructor - unfair)
- ✅ Test section break topics + major framework creators
- ❌ Skip vocabulary slides, reference lists, minor examples

**Format:**
- Direct questions, NOT scenarios (scenarios = tutorial activities)
- ONE clearly correct answer based on slide content
- 3-4 plausible distractors based on common misconceptions
- Test ONE concept per question
- No "All of the above" or "None of the above"
- Parallel structure (same grammar, similar length)

**Example:**
```markdown
According to Hofstede's framework, which dimension measures the extent to which less powerful members accept unequal power distribution?

A) Uncertainty Avoidance
B) Power Distance ← CORRECT (from Slide 8)
C) Individualism vs. Collectivism
D) Long-term Orientation
```

---

## Pre-Generation Checklist

**Before generating ANY content:**

- [ ] Read course syllabus - week topic, assessments due, required articles
- [ ] Read lecture_content_instructions.md - slide format, speaker notes, tutorial structure
- [ ] Review this document (CONTENT-GENERATION-BEST-PRACTICES.md) - all constraints
- [ ] Understand assessment schedule for tutorial alignment
- [ ] Identify 2-3 major topic segments (for section breaks)
- [ ] Note opportunities for quotes, frameworks, Vietnamese examples

---

## During Generation Checklist

### For Each Slide

While writing, check:
- [ ] Content substantial (150-200 words, stands alone)?
- [ ] Examples/data/frameworks ON the slide?
- [ ] Inline citations (Author, Year)?
- [ ] Speaker notes 3-8 lines (not repeating slide)?
- [ ] Bullet count ≤7 (split if more)?
- [ ] Quote ≤3 lines (use content slide if longer)?
- [ ] Framework ≤6 components (split if 8+)?
- [ ] Cluttered? (split into 2 slides)
- [ ] Layout hint used for quotes/frameworks/comparisons/reflections/references?

### Layout Diversity Check

Before finalizing lecture, verify you've included:
- [ ] 1 title slide
- [ ] 2-3 section breaks (major transitions)
- [ ] 1 vocab table (4-6 terms)
- [ ] 1 objectives slide (3-5 objectives)
- [ ] 2-3 quote slides WITH `<!-- LAYOUT: quote -->`
- [ ] 1-2 framework slides WITH `<!-- LAYOUT: framework -->`
- [ ] 1 comparison (table or boxes)
- [ ] 1-2 big numbers OR 1 stats banner
- [ ] 1-2 card layouts (frameworks with 3-6 elements)
- [ ] 1-2 reflection slides WITH `<!-- LAYOUT: reflection -->`
- [ ] 0-1 activity slides
- [ ] 1 checklist (assessment requirements)
- [ ] 1 references slide WITH `<!-- LAYOUT: references -->`
- [ ] 2-4 dark slides (Vietnamese examples)
- [ ] Remaining: content slides (40-50%)

### Tutorial Quality Check

- [ ] Main activity mirrors actual assessment?
- [ ] Simplified rubric (3-4 criteria) from real rubric?
- [ ] Quiz questions test slide content ONLY (not speaker notes)?
- [ ] 6-10 questions covering section break topics?
- [ ] Student file has NO answers or tutor guidance?
- [ ] Tutor notes file has complete answer keys with explanations?
- [ ] Reference to full assessment details ("See Assessment Handbook Section X")?

### Final Check Before Presenting

- [ ] Lecture: 22-30 slides total?
- [ ] No slides exceed word/bullet/component limits?
- [ ] 3-5 verified sources with DOI/URLs?
- [ ] Speaker notes on ALL slides (3-8 lines each)?
- [ ] Layout hints present for quotes/frameworks/comparisons/reflections/references?
- [ ] Tutorial: Two separate files (student + tutor)?
- [ ] Tutorial aligns with upcoming assessment?

---

## Common Mistakes to Avoid

1. ❌ **Sparse slide content** - Everything in speaker notes instead of on slide
2. ❌ **Speaker notes repeat slide** - Instead of adding context/timing/misconceptions
3. ❌ **Too many bullets** (>7) - Instead of splitting into 2 slides
4. ❌ **Long quotes** (>3 lines) - On quote slide layout instead of content slide
5. ❌ **No section breaks** - 26 slides with no structure or visual breaks
6. ❌ **Only content-slide** - Missing visual layouts (quotes, frameworks, cards)
7. ❌ **Quiz tests speaker notes** - Instead of slide content only
8. ❌ **Combined student/tutor file** - Instead of two separate files
9. ❌ **Forgetting layout hints** - Auto-detection fails for quotes/frameworks
10. ❌ **No Vietnamese examples** - Missing cultural context (use dark slides)
11. ❌ **Verbose slides** (>200 words) - Instead of splitting
12. ❌ **Tutorial without rubric** - Missing assessment alignment

---

## Good Example: Restructured Lecture

```
Slide 1: Title
Slide 2: Vocabulary table (6 terms)
Slide 3: Learning objectives (4)
Slide 4: Assessment connection

--- SECTION BREAK: Part 1 - Understanding ---
Slide 5: Section break title

Slide 6: Framework - Model/process <!-- LAYOUT: framework -->
Slide 7: Big Number - Key statistic
Slide 8: Comparison Table - Two concepts <!-- LAYOUT: comparison-table -->
Slide 9: Dark Slide - Vietnamese example

--- SECTION BREAK: Part 2 - Application ---
Slide 10: Section break title

Slide 11: Quote - Expert statement <!-- LAYOUT: quote -->
Slide 12: Card Layout - Framework elements (3-6 cards)
Slide 13: Content - Theory explanation
Slide 14: Dark Slide - ASEAN context
Slide 15: Activity - Practice exercise

--- SECTION BREAK: Part 3 - Integration ---
Slide 16: Section break title

Slide 17: Framework - Integration model <!-- LAYOUT: framework -->
Slide 18: Reflection - Self-assessment <!-- LAYOUT: reflection -->
Slide 19: Stats Banner - 3 metrics
Slide 20: Dark Slide - Vietnamese case study
Slide 21: Content - Synthesis

Wrap-up:
Slide 22: Quote - Closing inspiration <!-- LAYOUT: quote -->
Slide 23: Tutorial preview
Slide 24: Checklist - Assessment requirements
Slide 25: References <!-- LAYOUT: references -->
Slide 26: Final questions

STRENGTHS:
✓ 3 section breaks (structure)
✓ All slides <200 words
✓ 10 special layouts (varied, engaging)
✓ 4 dark slides (cultural context)
✓ Layout hints used (6 times)
✓ Visual rhythm maintained
```

---

## Additional Resources

- **Full slide format guide:** [lecture_content_instructions.md](../lecture_content_instructions.md)
- **All 18 layout details:** [SLIDE-LAYOUTS.md](SLIDE-LAYOUTS.md)
- **Tutorial design:** [TUTORIAL-DESIGN-GUIDELINES.md](TUTORIAL-DESIGN-GUIDELINES.md)
- **Quiz questions:** [QUIZ-QUESTION-GUIDELINES.md](QUIZ-QUESTION-GUIDELINES.md)
- **Workflow commands:** [.claude/CLAUDE.md](../.claude/CLAUDE.md)

---

## Version History

**v2.0** (January 19, 2025) - Consolidated
- Added speaker notes rules (3-8 lines, don't repeat slide)
- Added splitting rules with specific limits
- Added tutorial content requirements (two files)
- Added quiz question rules (test slide content only)
- Added pre-generation and during-generation checklists
- Reorganized for workflow clarity

**v1.0** (January 11, 2025) - Layout Optimization
- Initial documentation based on Week 12 analysis
- Layout distribution strategy
- Word count limits and splitting examples
- Layout diversity checklist

---

**This is the single source of truth for content generation. Read this BEFORE generating any lecture or tutorial content.**
