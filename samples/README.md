# Sample Files

This directory contains example files demonstrating the Class Content Generator system.

## Course Content Examples

### `BUSINESS COMMUNICATION Syllabus Fall 2025.md`
Complete course syllabus example showing:
- Full 10-week course structure
- Assessment schedule (portfolio + presentation + quiz)
- Learning objectives (4 categories following Bloom's Taxonomy)
- Weekly topics with validated required readings
- Professional formatting and organization

**Use for:** Understanding syllabus structure, seeing research-backed article selection, reference for creating new courses.

## Slide Layout Examples

### `comprehensive-layout-showcase.html` ⭐ **RECOMMENDED**
**Complete demonstration of all 18 slide layouts (25 slides)**

Organized in 5 sections:
1. **Introduction** - Title, objectives, section break
2. **Core Layouts Part 1** - Content, big number, stats, quote, reflection, framework, comparison
3. **Academic Layouts** - Vocabulary table, activity, checklist, card layout, references
4. **Content Patterns** - 2-col grid, 3-col grid, image+text, bullet lists
5. **Modifiers** - Dark slide variations

**Features:**
- Full coverage of all 18 layout types
- Prescriptive layout hints demonstrated
- Navigation with arrow keys or buttons
- Progress bar and slide counter
- CSS variables for reference design

**Purpose:** Complete reference for all layouts. Use this to:
- Test converter functionality
- Demonstrate capabilities to instructors
- Learn layout syntax and structure
- Verify new features work across all types

**Convert to PPTX:**
```bash
python3 html_to_pptx_converter.py samples/comprehensive-layout-showcase.html samples/output.pptx
```

### `comprehensive-layout-showcase.pptx`
Pre-converted PowerPoint version of the comprehensive showcase. Open directly in PowerPoint to see how HTML layouts translate to slides.

### `showcase-enhancements.html`
Earlier example focusing on visual enhancements (12 slides). Demonstrates:
- Footer system with course name and slide numbers
- Decorative shapes on title slides
- Icons above statistics
- Dark background variants
- Card layouts with white backgrounds

**Purpose:** Shows visual design evolution. Use comprehensive showcase instead for complete layout coverage.

## Quick Start

### View HTML Examples in Browser
```bash
# Open in default browser
open samples/comprehensive-layout-showcase.html

# Or serve locally
python3 -m http.server 8000
# Then open: http://localhost:8000/samples/comprehensive-layout-showcase.html
```

### Convert to PowerPoint
```bash
# From project root
python3 html_to_pptx_converter.py \
  samples/comprehensive-layout-showcase.html \
  samples/my-output.pptx

# With validation
python3 html_to_pptx_converter.py \
  samples/comprehensive-layout-showcase.html \
  samples/my-output.pptx
# Validation runs automatically
```

### Create Your Own Slides

1. **Use lecture content generator:**
   ```bash
   # Generate week content (creates lecture-content.md)
   /generate-week 1

   # Send gemini-handoff.md to Gemini for PPTX creation
   # Then insert speaker notes:
   /add-speaker-notes [CODE] 1
   ```

2. **Or use HTML converter (fallback):**
   - Copy structure from comprehensive showcase
   - Use layout classes or prescriptive hints
   - Follow reference design system (colors, fonts, spacing)
   - Convert with html_to_pptx_converter.py

## Layout Quick Reference

| Layout | CSS Class | Use When | Prescriptive Hint |
|--------|-----------|----------|-------------------|
| Title | `title-slide` | Opening slide | No |
| Section Break | `section-break-slide` | Major transitions | No |
| Big Number | `big-number-slide` | Single statistic | No |
| Stats Banner | `stats-banner-slide` | Multiple stats | No |
| Quote | `quote-slide` | Impactful quotes | `<!-- LAYOUT: quote -->` |
| Reflection | `reflection-slide` | Thinking prompts | `<!-- LAYOUT: reflection -->` |
| Framework | `framework-slide` | Visual models | `<!-- LAYOUT: framework -->` |
| Comparison | `comparison-table-slide` | Side-by-side | `<!-- LAYOUT: comparison-table -->` |
| References | `references-slide` | Citations | `<!-- LAYOUT: references -->` |
| Vocabulary | `vocab-table-slide` | Term definitions | No |
| Objectives | `objectives-slide` | Learning goals | No |
| Activity | `activity-slide` | Exercises | No |
| Checklist | `checklist-slide` | Task lists | No |
| Cards | `cards-slide` | Info cards | No |
| Content | `content-slide` | General content | No |

**Modifiers:**
- `dark-slide` - Dark background for high contrast (works with any layout)

**Content Patterns:**
- Grid Layout: Use CSS `grid-template-columns`
- Bullet Lists: Use `<ul>` or `<ol>` (auto-detected)
- Image + Text: Include `<img>` in content (auto-detected)

## Color Palette

```css
--color-primary: #131313    /* Dark gray - main text */
--color-accent: #ed5e29     /* Orange - emphasis */
--color-cream: #f4f3f1      /* Cream - backgrounds */
--color-tan: #cac3b7        /* Tan - decorative */
--color-white: #ffffff      /* White - cards */
--color-muted: #64748b      /* Muted gray - secondary */
```

## Typography

- **Headers:** Cal Sans (bold, condensed letter-spacing)
- **Body:** Plus Jakarta Sans (clean, readable)
- **Title Size:** 48pt (slides) / 60px (HTML)
- **Body Size:** 14-18pt (slides) / 18px (HTML)

## Documentation

- **Layout Vocabulary:** `docs/LAYOUT-VOCABULARY.md`
- **Converter Architecture:** `docs/ARCHITECTURE.md`
- **Validation Guide:** `docs/VALIDATION-GUIDE.md`
- **Workflows:** `.claude/CLAUDE.md`
- **Content Instructions:** `lecture_content_instructions.md`

## Need Help?

1. **Layout not working?** See `docs/LAYOUT-VOCABULARY.md` and `docs/TROUBLESHOOTING.md`
2. **Validation errors?** See `docs/VALIDATION-GUIDE.md`
3. **Want to add new layout?** See `docs/ARCHITECTURE.md`
4. **Course development?** See `.claude/CLAUDE.md`
