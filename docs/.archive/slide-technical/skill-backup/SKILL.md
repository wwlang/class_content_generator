---
name: slide-exporter
description: Convert lecture markdown to HTML presentations (FALLBACK - prefer Gemini hybrid workflow)
version: 2.0.0
---

# Slide Exporter Skill (Fallback)

> **Preferred workflow:** Use `/finalize-slides` with Gemini batches for superior visuals.
> This skill is for HTML export when Gemini is unavailable.

Convert `lecture-content.md` to self-contained HTML presentations.

## When to Invoke

- User explicitly requests HTML export
- `/export-slides [N]` command (when Gemini unavailable)
- Fallback when Gemini workflow not possible

## Quick Process

1. **Read** `courses/[CODE]/weeks/week-[N]/lecture-content.md`
2. **Detect** layout type for each slide (see Layout Detection below)
3. **Enhance** with images (Unsplash) and icons (Lucide SVG)
4. **Extract** speaker notes from `## Speaker Notes` sections
5. **Output** `slides.html` - self-contained, works offline

## Layout Detection (Priority Order)

| Pattern | Layout |
|---------|--------|
| First slide | Title |
| Single h2, no body | Section Break |
| `<!-- LAYOUT: quote -->` or blockquote | Quote |
| Table with English/Vietnamese | Vocabulary |
| "objectives", "outcomes" + Bloom's verbs | Learning Objectives |
| Large number + `.big-number` | Big Number |
| 2-4 `.card` elements | Card Layout |
| `.grid-2-col` or `.grid-3-col` | Grid Layout |
| "framework", "model", "process" in title | Framework |
| Question + "reflection", "think" | Reflection |
| `.dark-slide` class | Dark Background (modifier) |
| Default | Standard Content |

## Design System (Reference)

- **Dimensions:** 1024x768px (4:3)
- **Fonts:** Cal Sans (headers) + Plus Jakarta Sans (body)
- **Colors:** Cream bg (#f4f3f1), orange accent (#ed5e29), dark text (#131313)
- **Padding:** 60px standard

**Full specs:** See `resources/design-guidelines.md`
**All layouts:** See `resources/layout-templates.md`
**CSS framework:** See `resources/css-framework.md`

## Layout Variety Check

Before converting, verify content has variety:
- Section breaks: 3-6 (every 4-8 slides)
- Visual slides (quote/framework/dark): 8-12
- Standard content: ~60% max

**If >70% standard:** Warn user to regenerate with `/generate-week`.
