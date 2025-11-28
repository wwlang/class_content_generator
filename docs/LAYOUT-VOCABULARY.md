# Slide Layouts Vocabulary

Layout names and hints for lecture content generation. **Gemini handles visual design; this doc provides consistent vocabulary.**

---

## Quick Reference

| Layout | Purpose | Markdown Hint |
|--------|---------|---------------|
| **Title** | Opening slide | First slide with `# Title` |
| **Section Break** | Major transitions | `## Section Name` (2-3 per lecture) |
| **Big Number** | Single impactful statistic | `# 73%` + explanation |
| **Quote** | Impactful 2-3 line quotes | `<!-- LAYOUT: quote -->` |
| **Reflection** | Thinking prompts | `<!-- LAYOUT: reflection -->` |
| **Framework** | Visual models (3-6 components) | `<!-- LAYOUT: framework -->` |
| **Comparison** | Side-by-side tables | `<!-- LAYOUT: comparison-table -->` |
| **References** | Academic citations | `<!-- LAYOUT: references -->` |
| **Stats Banner** | Multiple stats (2-4) | Bold numbers with labels |
| **Vocabulary** | Term definitions | Table with Term/Definition |
| **Objectives** | Learning goals | Numbered list |
| **Activity** | In-class exercises | Instructions with timing |
| **Checklist** | Task lists | Checkbox items |
| **Cards** | Grid of related concepts | 3-6 items with titles |
| **Content** | General (default, 60-70%) | Standard bullets/paragraphs |
| **Dark** | High contrast emphasis | Add `dark-slide` modifier |

---

## Prescriptive Layout Hints

Use HTML comments in markdown to guarantee specific layouts:

```markdown
---

<!-- LAYOUT: quote -->

"Your quote text here"
— Attribution

---
```

**Supported hints:**
- `<!-- LAYOUT: quote -->` - Impactful quotes
- `<!-- LAYOUT: reflection -->` - Thinking prompts
- `<!-- LAYOUT: framework -->` - Visual models
- `<!-- LAYOUT: comparison-table -->` - Side-by-side
- `<!-- LAYOUT: references -->` - Academic citations

**When to use hints:** Quotes, references, frameworks, reflections, comparison tables - any slide where visual formatting is critical.

---

## Layout Distribution (22-30 slides)

| Category | Percentage | Examples |
|----------|------------|----------|
| Content slides | 60-70% | Standard bullets, paragraphs |
| Specialized | 20-30% | Quote (2-3), Framework (1-2), Comparison (1-2), Big Number (1-2) |
| Structural | 10-15% | Title (1), Section Breaks (2-3), References (1) |

**Visual rhythm:** Every 8-10 slides, use a section break, dark slide, quote, or big number to maintain interest.

---

## Common Layouts by Purpose

### Opening Section
1. Title slide
2. Learning objectives (numbered list, 3-5 items)
3. Section break (optional)

### Core Content
- **Concepts:** Content slides with bullets (max 5-7)
- **Statistics:** Big number (1 stat) or stats banner (2-4 stats)
- **Models:** Framework slide (3-6 components)
- **Contrasts:** Comparison table (4-6 rows)
- **Expert opinions:** Quote slide (2-3 lines max)

### Engagement
- **Reflection:** Thinking prompts
- **Activity:** In-class exercises with timing

### Closing
- Section break (optional)
- Key takeaways (content slide)
- References slide (always required)

---

## Framework Markdown Example

```markdown
<!-- LAYOUT: framework -->

## Creative Tension Framework

**Current Reality:** Where you are now

**Creative Tension:** Drive for change

**Desired Future:** Your vision

*Based on Senge's Fifth Discipline (2006)*
```

## Quote Markdown Example

```markdown
<!-- LAYOUT: quote -->

"Who do you want to become in the next chapter of your life?"

— Robert Fritz, The Path of Least Resistance (1989)
```

## Comparison Table Markdown Example

```markdown
<!-- LAYOUT: comparison-table -->

## Fixed vs Growth Mindset

| Fixed Mindset | Growth Mindset |
|---------------|----------------|
| Intelligence is static | Intelligence can develop |
| Avoids challenges | Embraces challenges |
| Gives up easily | Persists through obstacles |
```

---

## Best Practices

- **Match layout to content purpose** - Don't use quote layout for long text
- **Keep specialized layouts concise** - Quotes 2-3 lines, frameworks 3-6 components
- **Use hints for critical formatting** - Ensures consistent output
- **Maintain visual variety** - Mix layouts every 8-10 slides

---

**For HTML/PPTX converter technical details:** See `docs/.archive/slide-technical/` (fallback workflow only)
