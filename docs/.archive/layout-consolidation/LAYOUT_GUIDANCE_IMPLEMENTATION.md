# Layout Guidance Implementation Summary

**Date:** January 11, 2025
**Purpose:** Document implementation of layout guidance improvements to `/generate-week` command

---

## What Was Implemented

Based on the comprehensive analysis in `LAYOUT_GUIDANCE_GAPS.md`, the following improvements were added to `.claude/commands/generate-week.md`:

---

## 1. Enhanced Quick Reference Descriptions

**Before:** Generic one-line mentions
**After:** Specific, actionable descriptions

### Changes Made:

**Big Number Slide:**
- Before: "Single key statistic → big-number-slide (one large number with context)"
- After: "Single key statistic → big-number-slide (ONE dramatic number, 135pt, cream background)"

**Stats Banner:**
- Before: "Multiple related stats → stats-banner (2-4 metrics side-by-side)"
- After: "Multiple related stats → stats-banner (2-4 metrics side-by-side, dashboard style)"

**Quote Slide:**
- Before: "Important quote → quote-slide (quotation marks, attribution)"
- After: "Important quote → quote-slide (2-3 lines, attribution, requires prescriptive hint)"

**Section Break:**
- Before: "Major section transition → section-break (single bold statement, 2-6 words)"
- After: "Major section transition → section-break (orange background, white text, bold statement, 2-6 words, use 2-3 max per lecture)"

**Card Layout:**
- Before: "2-4 related concepts → card-layout (visual cards with borders)"
- After: "3-6 related concepts → card-layout (visual cards with icons/emojis, better than bullets for frameworks)"

---

## 2. Added Detailed 5-Line Guidance for High-Priority Layouts

Added comprehensive guidance following consistent 5-line format:
- Use for:
- Target:
- Title patterns:
- Examples:
- Structure:

### New Detailed Guidance Sections:

**QUOTE SLIDES (quote-slide):**
```
Use for: Expert quotes, opening questions, philosophical statements, thought leadership, reflection prompts as questions
Target: 2-3 per lecture at topic openings or section closings
Title patterns: Direct quote text or provocative question
Examples: "Who do you want to become?", Expert quotes from Senge, Pink, or thought leaders
Structure: 2-3 line quotes max, attribution with em dash, REQUIRES prescriptive hint <!-- LAYOUT: quote -->
```

**CARD LAYOUT (cards-slide):**
```
Use for: 3-6 related concepts, framework elements (Cialdini's 6 Principles), parallel ideas with icons, multiple dimensions of model
Target: 1-2 per lecture when presenting frameworks with multiple components
Title patterns: Framework name or concept category
Examples: "Drive Theory Elements", "Cialdini's 6 Principles", "Key Components"
Structure: 3-6 cards with icon/emoji, title (bold), 2-3 line description per card
```

**BIG NUMBER SLIDE (big-number-slide):**
```
Use for: ONE impactful statistic needing dramatic emphasis, memorable data point, "the one number to remember" moments
Target: 1-2 per lecture for key research findings
Title patterns: Context for the number
Examples: "Impact of Purpose", "Online Learning Reality", dramatic single statistics
Structure: One large number (135pt), brief explanation (1-2 lines), source citation
```

**STATS BANNER SLIDE (stats-banner-slide):**
```
Use for: 2-4 related statistics presented together, dashboard-style metrics, multiple data points comparison
Target: 1-2 per lecture when showing multiple related data points
Title patterns: Context for the metrics
Examples: "Assessment Breakdown", "Course Impact Metrics", multiple related statistics
Structure: 2-4 stats in horizontal row, each with large number and short label
```

**SECTION BREAK SLIDE (section-break-slide):**
```
Use for: Major topic transitions, part divisions between content sections, visual dramatic breaks for attention reset
Target: 2-3 per lecture MAX (overuse reduces impact)
Title patterns: "Part 1:", "Segment:", short bold statement (1-2 lines)
Examples: "Part 1: Understanding Persuasion", "Application Phase", major section markers
Structure: Single bold statement, orange background, white text, 2-6 words ideal
```

---

## 3. Added Prescriptive Layout Hints Section

**Location:** New section after detailed layout guidance (lines 250-311)

**Critical Missing Information Now Documented:**

### What Was Added:

**Prescriptive Layout Hints Explained:**
- What they are (HTML comments that force specific layouts)
- Which layouts require them (quote, references, framework, reflection, comparison-table)
- When to use them (critical formatting, ambiguous content, guaranteed results)
- How to place them in markdown (before slide content, after separator)

**Two Complete Examples Provided:**

1. **Quote slide example:**
```markdown
---

<!-- LAYOUT: quote -->

"Personal mastery is the discipline of continually clarifying and deepening our personal vision, of focusing our energies, of developing patience, and of seeing reality objectively."

— Peter Senge, The Fifth Discipline (2006)

---
```

2. **Framework slide example:**
```markdown
---

<!-- LAYOUT: framework -->

## The Creative Tension Model

**Current Reality** ← [GAP: Creative Tension] → **Vision**

The gap between where you are and where you want to be creates natural energy for change.

*Senge, P. M. (2006). The fifth discipline. Currency/Doubleday.*

---
```

---

## 4. Updated Quality Checklist

**Location:** Lines 416-429

### New Checklist Items Added:

**Content & Structure section:**
- ✅ Quote slides used for expert statements and opening questions (2-3 per lecture)
- ✅ Card layout used for frameworks with 3-6 parallel concepts (better than bullets)
- ✅ Big number vs stats banner used appropriately (1 stat = big-number, 2-4 = stats-banner)
- ✅ Section breaks used sparingly (2-3 max) for major transitions
- ✅ Prescriptive hints added for quotes, references, frameworks, reflections (<!-- LAYOUT: type -->)

**Result:** Quality checklist now covers all 18 layout types with specific usage criteria.

---

## Impact on Content Generation

### Before Implementation:

**Problem:** Content generators defaulted to `content-slide` for almost everything
- Only 4 layouts had detailed guidance (dark, framework, reflection, checklist)
- 10+ layouts mentioned but not explained
- Prescriptive hints completely undocumented
- No guidance on when to use quote vs dark slide for quotes
- No guidance on cards vs bullets for frameworks
- No distinction between big-number and stats-banner

### After Implementation:

**Solution:** Generators now have clear guidance for all layouts
- All 18 layouts documented with usage criteria
- 9 layouts have detailed 5-line guidance (quote, card, big-number, stats-banner, section-break, dark, framework, reflection, checklist)
- Prescriptive hints fully documented with examples
- Clear use cases: quote slide for quotes, card layout for frameworks
- Quality checklist enforces appropriate layout usage

---

## Expected Improvements in Generated Content

**More Layout Diversity:**
- Lectures will use 8-10 different layout types instead of 2-3
- Quote slides for expert statements (2-3 per lecture)
- Card layouts for frameworks (1-2 per lecture)
- Section breaks for transitions (2-3 max)

**Better Visual Impact:**
- Big number slides for dramatic statistics (1-2 per lecture)
- Stats banner for multiple metrics (1-2 per lecture)
- Dark slides for stories and case studies (2-4 per lecture)

**Proper Technical Implementation:**
- Prescriptive hints used where required (quotes, frameworks, reflections)
- Guaranteed correct rendering in HTML to PPTX converter
- No ambiguity in layout detection

**Enhanced Pedagogical Quality:**
- Visual variety maintains student attention
- Appropriate layouts match content type
- Professional presentation design standards

---

## Files Modified

**Primary file:**
- `.claude/commands/generate-week.md` (lines 163-429 updated/added)

**Documentation created:**
- `docs/LAYOUT_GUIDANCE_IMPLEMENTATION.md` (this file)

**Reference documents:**
- `docs/LAYOUT_GUIDANCE_GAPS.md` (gap analysis that drove this work)
- `docs/LAYOUT_COMPATIBILITY_CHECK.md` (compatibility verification)
- `docs/SLIDE-LAYOUTS.md` (comprehensive layout reference)

---

## Alignment with Converter

**Status:** ✅ Fully compatible with `html_to_pptx/layout_config.py`

All guidance aligns with:
- 17 layout types in converter
- Priority-based handler system
- CSS class detection patterns
- Prescriptive hint override system

---

## Next Steps

**For Future Weekly Content Generation:**
1. Run `/generate-week [N]` with updated command
2. Verify quality checklist compliance
3. Check for appropriate layout variety
4. Confirm prescriptive hints used where required

**For Existing Content (Optional):**
1. Review Week 12 lecture content
2. Identify opportunities for better layouts:
   - Drive Theory → card layout (currently bullets)
   - Senge quotes → quote slides with hints (currently dark or content)
   - Single statistics → big-number slides (currently in paragraphs)
3. Refactor as needed for visual improvement

---

## Validation

**Quality Checks Passed:**
- ✅ All 18 layouts from SLIDE-LAYOUTS.md covered
- ✅ Consistent 5-line format for detailed guidance
- ✅ Prescriptive hints fully documented
- ✅ Quality checklist comprehensive
- ✅ Examples provided for complex layouts
- ✅ Compatible with converter architecture

**No Breaking Changes:**
- Existing content still valid
- Backward compatible with previous guidance
- Additive improvements only

---

## Conclusion

**Gap closed:** From 4 detailed layouts to 9 detailed layouts
**Critical documentation added:** Prescriptive layout hints section
**Quality checklist enhanced:** 5 new layout-specific items

**Result:** Content generators now have comprehensive, balanced guidance for all 18 slide layouts, ensuring appropriate variety and professional visual design in all generated lectures.
