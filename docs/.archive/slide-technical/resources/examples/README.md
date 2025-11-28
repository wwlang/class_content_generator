# Slide Exporter Example Files

This directory contains HTML examples demonstrating the slide-exporter skill capabilities.

## Files

### `comprehensive-layout-showcase.html`
**Complete demonstration of all 18 slide layouts and converter capabilities**

**Slides:** 25 total slides organized in 5 sections
- **Section 1:** Introduction (3 slides)
  - Title slide with decorative shapes
  - Learning objectives layout
  - Section break

- **Section 2:** Core Layouts Part 1 (8 slides)
  - Standard content slide with bullets
  - Big number slide (single statistic)
  - Stats banner (multiple statistics)
  - Quote slide with decorative quotation mark
  - Reflection slide with thinking prompt
  - Framework slide with component boxes
  - Comparison table (side-by-side)
  - Section break

- **Section 3:** Academic Layouts (6 slides)
  - Vocabulary table with term definitions
  - Activity slide with instructions
  - Checklist slide with checkboxes
  - Card layout with 6 cards (Cialdini's principles)
  - References slide with hanging indents
  - Section break

- **Section 4:** Content Patterns (4 slides)
  - 2-column grid layout
  - 3-column grid layout
  - Image + text pattern (with mock image)
  - Bullet list pattern
  - Section break

- **Section 5:** Modifiers (3 slides)
  - Dark slide modifier on content
  - Dark slide modifier on big number
  - Final title slide

**Purpose:** Complete reference for all available layouts. Use this to test converter features, demonstrate capabilities to users, and verify new features work across all layout types.

**Navigation:** Use arrow keys (← →) or click buttons to navigate. Press Home/End for first/last slide.

### `enhanced-sample-slides.html`
**Focus on visual enhancements and design system**

**Slides:** 17 slides demonstrating the reference design
- Design enhancements (footers, decorative shapes, icons)
- Statistics with visual hierarchy
- Color palette and typography showcase
- Implementation metrics
- Academic layouts (quote, framework, reflection, comparison, references)

**Purpose:** Demonstrates the visual design system with focus on aesthetics. Better for showing design principles rather than comprehensive layout coverage.

## Usage

### For Testing
Use `comprehensive-layout-showcase.html` to test converter features:
```bash
python3 html_to_pptx_converter.py .claude/skills/slide-exporter/resources/examples/comprehensive-layout-showcase.html output.pptx
```

### For Demonstrations
Use either file depending on audience:
- **Comprehensive:** When showcasing all layout types and technical capabilities
- **Enhanced:** When focusing on visual design and aesthetics

### For Development
When adding new layouts or features:
1. Add example to `comprehensive-layout-showcase.html`
2. Test conversion to PPTX
3. Verify layout appears correctly
4. Update SLIDE-LAYOUTS.md documentation

## Converting to PPTX

From project root:
```bash
# Comprehensive showcase
python3 html_to_pptx_converter.py \
  .claude/skills/slide-exporter/resources/examples/comprehensive-layout-showcase.html \
  output/showcase.pptx

# Enhanced design showcase
python3 html_to_pptx_converter.py \
  .claude/skills/slide-exporter/resources/examples/enhanced-sample-slides.html \
  output/enhanced.pptx
```

## Validation

All examples should pass validation with minimal warnings:
```bash
python3 html_to_pptx_converter.py input.html output.pptx
# Validation runs automatically after conversion
```

Expected warnings:
- Section break slides use orange background (by design)
- Title slides use white background (by design)
- Some content may extend beyond boundaries (usually fine)

## Layout Coverage

| Layout Type | Comprehensive | Enhanced |
|------------|--------------|----------|
| Title Slide | ✓ | ✓ |
| Section Break | ✓ (4×) | ✓ (3×) |
| Big Number | ✓ | ✓ |
| Stats Banner | ✓ | ✓ (2×) |
| Quote | ✓ | ✓ |
| Reflection | ✓ | ✓ |
| Framework | ✓ | ✓ |
| Comparison Table | ✓ | ✓ |
| References | ✓ | ✓ |
| Vocabulary Table | ✓ | ✗ |
| Learning Objectives | ✓ | ✗ |
| Activity | ✓ | ✗ |
| Checklist | ✓ | ✗ |
| Card Layout | ✓ | ✗ |
| Standard Content | ✓ | ✓ |
| Grid 2-col | ✓ | ✗ |
| Grid 3-col | ✓ | ✓ |
| Image + Text | ✓ | ✗ |
| Dark Slide Modifier | ✓ | ✓ |

**Total Layouts:** 18 (14 core + 3 patterns + 1 modifier)
**Comprehensive Coverage:** 18/18 ✓
**Enhanced Coverage:** 11/18

## References

- **Layout Documentation:** `docs/SLIDE-LAYOUTS.md`
- **Architecture:** `docs/ARCHITECTURE.md`
- **Validation Guide:** `docs/VALIDATION-GUIDE.md`
- **Main README:** `README.md`
