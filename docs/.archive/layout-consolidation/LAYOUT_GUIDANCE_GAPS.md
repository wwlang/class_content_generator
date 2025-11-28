# Layout Guidance Gaps Analysis

**Date:** January 11, 2025
**Purpose:** Identify layouts in SLIDE-LAYOUTS.md that need better guidance in generate-week.md

---

## Summary

**SLIDE-LAYOUTS.md has:** 18 layouts (14 core + 3 patterns + 1 modifier)
**generate-week.md detailed guidance:** 4 layouts (dark, framework, reflection, checklist)
**Gap:** 10+ layouts mentioned but lacking detailed usage guidance

---

## Layouts Needing Detailed Guidance

### 1. **Quote Slide** ⭐ HIGH PRIORITY

**Currently in generate-week:** Listed under "EMPHASIS & VISUAL IMPACT" - 1 line
**In SLIDE-LAYOUTS.md:** Full documentation with examples, prescriptive hint

**Why add detailed guidance:**
- Used frequently in lectures (2-3 per lecture recommended)
- Requires prescriptive hint: `<!-- LAYOUT: quote -->`
- Specific content structure (2-3 line quotes, attribution format)
- Opening slides, expert opinions, reflection prompts

**Recommended content types that should use quote-slide:**
- Opening provocative questions at start of topics
- Expert thought leadership statements
- Key philosophical statements that guide lesson
- Memorable takeaways at end of sections
- Reflection prompts formulated as questions

**Example from Week 12:**
- Could use for Senge quote on Slide 26
- Could use for opening questions about motivation

---

### 2. **Card Layout** ⭐ HIGH PRIORITY

**Currently in generate-week:** Listed under "GROUPED CONTENT" - 1 line
**In SLIDE-LAYOUTS.md:** Full documentation, when to use, structure

**Why add detailed guidance:**
- Perfect for multiple related concepts (3-6 items)
- Grid arrangement with icons
- Better than bullet lists for conceptual frameworks

**Recommended content types that should use cards-slide:**
- Framework elements (e.g., "Cialdini's 6 Principles" as 6 cards)
- Multiple related concepts with icons/emojis
- Process steps with visual cues
- Feature highlights or benefits
- Key dimensions of a model

**Example from Week 12:**
- Slide 10: Drive Theory's 3 elements (Autonomy, Mastery, Purpose) - currently bullets, could be 3 cards
- Any slide presenting 3-6 parallel concepts

---

### 3. **Big Number Slide** ⭐ MEDIUM PRIORITY

**Currently in generate-week:** Listed under "EMPHASIS & VISUAL IMPACT" - 1 line
**In SLIDE-LAYOUTS.md:** Full documentation, when to use

**Why add detailed guidance:**
- ONE impactful statistic with dramatic emphasis
- 135pt number on cream background
- Different from stats-banner (which shows 2-4 stats)

**Recommended content types that should use big-number-slide:**
- Single key research finding that needs emphasis
- Memorable data point
- Before/after single metric (use 2 big-number slides)
- "The one number you need to remember" moments

**Example from Week 12:**
- Could use for "90% of online courses incomplete" as standalone dramatic stat
- Could use for "2.7x more likely to stay" (purpose retention)

---

### 4. **Stats Banner Slide** ⭐ MEDIUM PRIORITY

**Currently in generate-week:** Listed under "EMPHASIS & VISUAL IMPACT" - 1 line
**In SLIDE-LAYOUTS.md:** Full documentation

**Why add detailed guidance:**
- 2-4 related statistics in horizontal row
- Dashboard-style presentation
- Different from big-number (which shows only ONE stat)

**Recommended content types that should use stats-banner-slide:**
- Multiple related statistics (2-4 data points)
- Key metrics overview for a topic
- Comparison of multiple data points
- Assessment deadlines or course statistics

**Example from Week 12:**
- Slide 4: Assessment percentages (40% + 30% + 20%) could be stats banner
- Multiple PwC statistics (92% willing to adapt, 73% overwhelmed)

---

### 5. **Section Break Slide** ⭐ MEDIUM PRIORITY

**Currently in generate-week:** Listed under "FOUNDATIONAL LAYOUTS" - 1 line
**In SLIDE-LAYOUTS.md:** Full documentation

**Why add detailed guidance:**
- Orange background, white text, dramatic transition
- Use 2-3 times per lecture MAX
- Specific formatting (1-2 lines, bold statement)

**Recommended content types that should use section-break-slide:**
- Between major sections ("Part 1: Understanding X")
- After introducing concepts before moving to application
- Before major transitions in content
- Create visual break and refocus attention

**Example from Week 12:**
- Could add section breaks for "Segment 1: Personal Mastery", "Segment 2: Drive Theory", etc.

---

### 6. **Grid Layout Pattern** ⭐ LOW PRIORITY

**Currently in generate-week:** NOT MENTIONED
**In SLIDE-LAYOUTS.md:** Content pattern (grid-2-col, grid-3-col)

**Why add guidance:**
- Auto-detected pattern WITHIN content slides
- 2 or 3 column side-by-side layout
- Different from comparison-table (which is formal table)

**Recommended content types that should use grid layout:**
- Side-by-side comparisons (informal, not tabular)
- Text + image combinations
- Multiple lists in parallel
- Theory (left) + Application (right)

**How it works:**
- Uses CSS `display: grid; grid-template-columns: 1fr 1fr;`
- Auto-detected, no special class needed
- Works within standard content-slide

---

## Critical Missing Information

### 1. **Prescriptive Layout Hints** ⚠️ IMPORTANT

**What they are:**
HTML comments that FORCE a specific layout, overriding auto-detection

**Which layouts require hints:**
- `<!-- LAYOUT: quote -->` - Quote slide
- `<!-- LAYOUT: references -->` - References slide
- `<!-- LAYOUT: framework -->` - Framework slide
- `<!-- LAYOUT: reflection -->` - Reflection slide
- `<!-- LAYOUT: comparison-table -->` - Comparison table

**Why important:**
From SLIDE-LAYOUTS.md: "Use hints for: Quotes, references, frameworks, reflections, comparison tables - any slide where visual formatting is critical"

**Not mentioned in generate-week.md!** This is a gap.

---

### 2. **CSS Class Aliases** ℹ️ INFORMATIONAL

Some layouts accept multiple CSS class names:

| Primary Class | Alternate Classes |
|---------------|-------------------|
| `big-number-slide` | `stat-slide` |
| `stats-banner-slide` | `stats-slide` |
| `dark-slide` | `dark-background` |
| `references-slide` | `citations-slide` |
| `framework-slide` | `diagram-slide`, `model-slide` |
| `reflection-slide` | `thinking-prompt` |
| `comparison-table-slide` | `comparison-slide` |

**Recommendation:** Mention these exist, recommend primary class for consistency

---

### 3. **Layout Priority System** ℹ️ INFORMATIONAL

From SLIDE-LAYOUTS.md, layouts are checked in priority order:

**High Priority (checked first):**
- Section Break (15)
- Big Number (20)
- Quote (25)
- Reflection (25)
- Framework (30)
- Comparison Table (35)

**Low Priority:**
- Content Slide (100) - fallback for everything else

**Why it matters:** If content could match multiple layouts, higher priority wins.

---

## Recommendations for generate-week.md

### Priority 1: Add Concise Guidance for High-Use Layouts

Add to the "DETAILED LAYOUT GUIDANCE" section:

**QUOTE SLIDES (quote-slide):**
Use for: Expert quotes, opening questions, philosophical statements, thought leadership
Target: 2-3 per lecture, at topic openings or section closings
Title patterns: Direct quote text or question
Examples: "Who do you want to become?", Senge quote on learning organizations
Structure: 2-3 line quotes max, attribution with em dash, use `<!-- LAYOUT: quote -->` hint
**Note:** Requires prescriptive hint for proper formatting

**CARD LAYOUT (cards-slide):**
Use for: 3-6 related concepts, framework elements, parallel ideas with icons
Target: 1-2 per lecture when presenting frameworks with multiple components
Title patterns: Framework name or concept category
Examples: "Cialdini's 6 Principles", "Drive Theory Elements", "Key Components"
Structure: 3-6 cards with icon/emoji, title, 2-3 line description per card

**BIG NUMBER SLIDE (big-number-slide):**
Use for: ONE impactful statistic, dramatic emphasis, memorable data point
Target: 1-2 per lecture for key research findings
Title patterns: Context for the number
Examples: "Impact of Purpose", "Online Learning Reality"
Structure: One large number (135pt), brief explanation (1-2 lines), source citation

**STATS BANNER (stats-banner-slide):**
Use for: 2-4 related statistics, dashboard presentation, multiple metrics
Target: 1-2 per lecture when showing multiple related data points
Title patterns: Context for the metrics
Examples: "Assessment Breakdown", "Course Impact Metrics"
Structure: 2-4 stats in row, each with large number and short label

**SECTION BREAK (section-break-slide):**
Use for: Major topic transitions, part divisions, visual dramatic breaks
Target: 2-3 per lecture MAX (overuse reduces impact)
Title patterns: "Part 1:", "Segment:", short bold statement (1-2 lines)
Examples: "Part 1: Understanding Persuasion", "Application Phase"
Structure: Single bold statement, orange background, white text, 2-6 words ideal

---

### Priority 2: Add Prescriptive Layout Hints Section

Add new section after detailed guidance:

```markdown
**PRESCRIPTIVE LAYOUT HINTS:**

For certain layouts, add HTML comment to FORCE specific layout (overrides auto-detection):

- Quote slides: `<!-- LAYOUT: quote -->`
- References: `<!-- LAYOUT: references -->`
- Framework diagrams: `<!-- LAYOUT: framework -->`
- Reflection prompts: `<!-- LAYOUT: reflection -->`
- Comparison tables: `<!-- LAYOUT: comparison-table -->`

**When to use hints:**
- Visual formatting is critical (quotes, references, frameworks)
- Content might be ambiguous (questions that should be reflections)
- Guaranteed results needed (student-facing materials)

**Place hint before slide content in markdown:**
```markdown
---

<!-- LAYOUT: quote -->

"Your quote text here"
— Attribution

---
```
```

---

### Priority 3: Update Quality Checklist

Current checklist mentions:
- [ ] 2-4 dark slides included

Add:
- [ ] Quote slides used for expert statements and opening questions (2-3 per lecture)
- [ ] Card layout used for frameworks with 3-6 parallel concepts
- [ ] Section breaks used sparingly (2-3 max) for major transitions
- [ ] Prescriptive hints added for quotes, references, frameworks, reflections
- [ ] Big number vs stats banner used appropriately (1 stat = big-number, 2-4 = stats-banner)

---

## Example: Better Layout Choices for Common Content

### Instead of content-slide with bullets...

**❌ Current approach:**
```markdown
## Drive Theory - Three Elements

- Autonomy: Control over your work
- Mastery: Getting better at things
- Purpose: Contribution to something meaningful
```

**✅ Better with card-layout:**
```markdown
## Drive Theory - Three Elements
[LAYOUT: cards-slide]

**🎯 Autonomy**: Control over your work
**📈 Mastery**: Getting better at things
**🎯 Purpose**: Contribution to something meaningful
```

---

### Instead of content-slide with statistic...

**❌ Current approach:**
```markdown
## Online Learning Reality

Research shows:
- 90% of online courses are never completed
- Lack of accountability is primary reason
```

**✅ Better with big-number-slide:**
```markdown
<!-- LAYOUT: big-number -->

# 90%

of online courses are never completed without accountability systems

*Jordan (2014)*
```

---

### Instead of paragraph at topic opening...

**❌ Current approach:**
```markdown
## Personal Mastery

Peter Senge defines personal mastery as "the discipline of continually clarifying and deepening our personal vision..."
```

**✅ Better with quote-slide:**
```markdown
<!-- LAYOUT: quote -->

"Personal mastery is the discipline of continually clarifying and deepening our personal vision, of focusing our energies, of developing patience, and of seeing reality objectively."

— Peter Senge, The Fifth Discipline (2006)
```

---

## Conclusion

**Current state:**
- 18 layouts available in converter
- 4 layouts have detailed guidance in generate-week
- 10+ layouts mentioned but not explained

**Recommended additions:**
1. **Detailed guidance for:** quote, card-layout, big-number, stats-banner, section-break
2. **New section:** Prescriptive layout hints
3. **Updated checklist:** Include quote, card, section-break usage
4. **Examples:** Show better layout choices for common content

**Result:** Content generators will use more diverse, appropriate layouts instead of defaulting to content-slide for everything.
