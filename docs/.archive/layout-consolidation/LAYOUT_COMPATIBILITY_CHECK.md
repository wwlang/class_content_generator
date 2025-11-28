# Layout Compatibility Check

**Date:** January 11, 2025
**Purpose:** Verify `/generate-week` command is compatible with all layout types in `layout_config.py`

---

## Layout Types in layout_config.py

Total: **17 layout types**

| # | Layout ID | CSS Classes | In generate-week? |
|---|-----------|-------------|-------------------|
| 1 | `title` | `title-slide` | ✅ Yes |
| 2 | `section-break` | `section-break` | ✅ Yes |
| 3 | `vocab-table` | `vocab-table-slide` | ✅ Yes |
| 4 | `objectives` | `objectives-slide` | ✅ Yes |
| 5 | `big-number` | `big-number-slide`, `stat-slide` | ✅ Yes |
| 6 | `activity` | `activity-slide` | ✅ Yes |
| 7 | `comparison` | `comparison-slide` | ✅ Yes |
| 8 | `card` | `card-layout` | ✅ Yes |
| 9 | `stats-banner` | `stats-banner`, `stats-slide` | ✅ Yes |
| 10 | `checklist` | `checklist-slide` | ✅ Yes |
| 11 | `dark` | `dark-slide`, `dark-background` | ✅ Yes |
| 12 | `quote` | `quote-slide` | ✅ Yes |
| 13 | `references` | `references-slide`, `citations-slide` | ✅ Yes |
| 14 | `framework` | `framework-slide`, `diagram-slide`, `model-slide` | ✅ Yes |
| 15 | `reflection` | `reflection-slide`, `thinking-prompt` | ✅ Yes |
| 16 | `comparison-table` | `comparison-table-slide` | ✅ Yes |
| 17 | `standard` | `content-slide` | ✅ Yes (as default) |

---

## Compatibility Status: ✅ COMPATIBLE

All 17 layout types from `layout_config.py` are represented in the `/generate-week` command.

---

## Issues Found

### 1. **Alternate CSS Class Names Not Mentioned** ⚠️

Some layouts have alternate CSS class names that aren't documented in generate-week:

| Layout | Primary Class (mentioned) | Alternate Classes (not mentioned) |
|--------|--------------------------|-----------------------------------|
| big-number | `big-number-slide` | `stat-slide` |
| stats-banner | `stats-banner` | `stats-slide` |
| dark | `dark-slide` | `dark-background` |
| references | `references-slide` | `citations-slide` |
| framework | `framework-slide` | `diagram-slide`, `model-slide` |
| reflection | `reflection-slide` | `thinking-prompt` |

**Impact:** Low - primary classes are correct, alternates are optional
**Action:** Document alternates for completeness

---

### 2. **Missing Guidance Detail for Some Layouts** ⚠️

Some layouts lack detailed guidance compared to others:

**Well-documented:**
- dark-slide (comprehensive guidance, 60+ lines)
- activity-slide (clear use cases)
- comparison-table-slide (specific examples)

**Under-documented:**
- framework-slide (mentioned but no detailed guidance)
- reflection-slide (mentioned but no examples)
- checklist-slide (mentioned but no structure guidance)

**Impact:** Medium - generators may not know when to use these effectively
**Action:** Add detailed guidance for framework, reflection, and checklist slides

---

### 3. **Layout Priority Not Mentioned** ℹ️

The `layout_config.py` has priority levels for layout detection, but this isn't reflected in generate-week:

**High Priority (checked first):**
- quote-slide (Priority 8)
- comparison-table-slide (Priority 8)
- vocab-table-slide (Priority 9)
- objectives-slide (Priority 8)

**Why it matters:** Converter checks high-priority layouts first. If content could match multiple layouts, the higher priority wins.

**Impact:** Low - mostly informational
**Action:** Add note about priority for edge cases

---

### 4. **Content-slide vs Standard Confusion** ⚠️

In `layout_config.py`:
- Layout ID: `standard`
- CSS class: `content-slide`

In generate-week:
- Referenced as "content-slide (default)"

**Potential confusion:** Is it `standard` or `content-slide`?

**Clarification needed:** The CSS class is `content-slide`, layout ID is `standard`. For markdown, use `[LAYOUT: content-slide]`

**Impact:** Low - works correctly but could be clearer
**Action:** Add note clarifying relationship

---

## Recommendations

### Priority 1: Add Missing Guidance (RECOMMENDED)

Add detailed sections for:

1. **Framework/Diagram Slides** (`framework-slide`, `diagram-slide`, `model-slide`)
   - When to use: Visual models, processes, theoretical diagrams
   - Examples: Gibbs' Cycle, Creative Tension diagram, 70-20-10 model visual
   - Structure: Labeled components, arrows, relationships

2. **Reflection Slides** (`reflection-slide`, `thinking-prompt`)
   - When to use: Contemplative questions, self-assessment prompts
   - Examples: "Reflect: What drives your motivation?", journaling prompts
   - Structure: Open-ended questions, thinking time indicator

3. **Checklist Slides** (`checklist-slide`)
   - When to use: Assessment criteria, requirements, success indicators
   - Examples: Development Plan checklist, rubric preview
   - Structure: Categorized items with checkboxes, 3-5 categories

### Priority 2: Document Alternate CSS Classes (OPTIONAL)

Add note in generate-week:

```markdown
**Note on CSS classes:** Some layouts accept alternate class names:
- big-number-slide OR stat-slide
- stats-banner OR stats-slide
- dark-slide OR dark-background
- references-slide OR citations-slide
- framework-slide OR diagram-slide OR model-slide
- reflection-slide OR thinking-prompt

Use primary class names (first in list) for consistency.
```

### Priority 3: Clarify Standard/Content Naming (OPTIONAL)

Add note:
```markdown
**Note:** The "standard" layout uses CSS class `content-slide`.
In markdown, specify [LAYOUT: content-slide] for the default layout.
```

---

## CSS Class Reference Table

For quick reference when generating content:

| When you want... | Use this class |
|-----------------|----------------|
| Default slide with bullets/paragraphs | `content-slide` |
| First slide of deck | `title-slide` |
| Major topic transition | `section-break` |
| English-Vietnamese vocabulary | `vocab-table-slide` |
| Learning objectives list | `objectives-slide` |
| One big statistic | `big-number-slide` |
| Multiple stats side-by-side | `stats-banner` |
| Expert quote | `quote-slide` |
| Case study/Vietnamese example | `dark-slide` |
| Two-item comparison | `comparison-slide` |
| Detailed comparison table | `comparison-table-slide` |
| Process/framework diagram | `framework-slide` |
| Hands-on activity | `activity-slide` |
| Reflection questions | `reflection-slide` |
| 2-4 concept cards | `card-layout` |
| Assessment criteria | `checklist-slide` |
| End-of-deck citations | `references-slide` |

---

## Conclusion

**Status:** ✅ **COMPATIBLE**

All layout types from `layout_config.py` are supported in `/generate-week` command.

**Recommended improvements:**
1. Add detailed guidance for framework-slide, reflection-slide, checklist-slide
2. Document alternate CSS class names
3. Clarify standard/content-slide relationship

**Action required:** No breaking changes needed, only enhancements for clarity and completeness.
