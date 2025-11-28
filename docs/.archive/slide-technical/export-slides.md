# /export-slides [week-number]

Convert lecture content to HTML slides (fallback for Gemini hybrid workflow).

> **Preferred:** Use Gemini single-batch workflow, then `/add-speaker-notes` for speaker notes.

## Prerequisites

- `lecture-content.md` exists and reviewed
- Content follows rules: 150-200 words/slide, ≤7 bullets, speaker notes

## Process

### Step 1: Locate Content

Find `courses/[CODE]/weeks/week-[N]/lecture-content.md`

### Step 2: Convert to HTML 🔐

**Load skill:** `slide-exporter/SKILL.md`

- Parse markdown
- Apply 18 layout templates
- Embed fonts (Cal Sans, Plus Jakarta Sans)
- Generate self-contained HTML

### Step 3: Convert to PPTX

```bash
python3 html_to_pptx_converter.py slides.html slides.pptx
```

### Step 4: Auto-Validation 🔒

| Tier | Checks | Action |
|------|--------|--------|
| Critical | Slide count, empty slides, speaker notes | Must fix |
| Warning | Word count >200, bullets >7, layout variety | Review |
| Info | Colors, font sizes | No action |

## Outputs

- `slides.html` - Self-contained HTML
- `slides.pptx` - PowerPoint with embedded fonts

## Time

3-5 minutes per week

## Example

```
/export-slides 5

✓ Converting lecture-content.md...
✓ 28 slides generated
✓ Converting to PPTX...
✓ Validation: 5 passed, 0 issues

Saved: courses/BCI2AU/weeks/week-05/slides.pptx
```

## If Things Go Wrong

- **Missing lecture-content.md:** Run `/generate-week` first
- **Layout hints not applied:** Check syntax `<!-- LAYOUT: quote -->`
- **Validation errors:** Fix in lecture-content.md, re-export
- **Fonts wrong:** Check font files in converter resources

## When to Use

- Gemini unavailable
- Quick preview needed
- HTML output preferred

**For production slides:** Use Gemini single-batch workflow + `/add-speaker-notes`
