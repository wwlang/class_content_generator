# Slide Exporter Skill

**Version:** 1.0.0
**Author:** Custom
**Type:** Claude Code Skill (Auto-invocation)

---

## Overview

The **Slide Exporter** skill automatically converts lecture content markdown files into professional, self-contained HTML presentations. It implements a complete design system with:

- **Fixed 4:3 aspect ratio** (1024x768px) for projector compatibility
- **Professional typography** using PT Serif (headers) and Roboto (body text)
- **10 layout templates** with automatic content-based detection
- **Visual enhancements** including Unsplash image search and Lucide SVG icons
- **Self-contained output** with inline CSS, JavaScript, and embedded media
- **Keyboard navigation** and progress tracking

## Quick Start

### Basic Usage

The skill auto-invokes when you request slide conversion in natural language:

```
"Convert week 3 to slides"
"Export week 5 lecture to HTML"
"Create presentation for week 2"
```

Or explicitly:
```
/export-slides 3
```

### Prerequisites

- **Required:** Lecture content must exist at `courses/[COURSE-CODE]/weeks/week-[N]/lecture-content.md`
- **Optional:** Set `UNSPLASH_ACCESS_KEY` environment variable for image search

### Output

Generated file: `courses/[COURSE-CODE]/weeks/week-[N]/slides.html`

Open in any modern browser. Press F11 for fullscreen presentation mode.

---

## Features

### 1. Automatic Layout Detection

The skill intelligently maps your lecture content to one of 10 professional layouts:

| Layout | When Used | Key Features |
|--------|-----------|--------------|
| Title Slide | First slide | Large heading, subtitle, author info |
| Section Break | Topic transitions | Full accent-color background |
| Standard Content | Key points (bullets) | Title + 3-6 bullet points |
| Split Screen | Text + visual support | 50/50 text and image columns |
| Tiled (3-column) | Three parallel concepts | Icons + titles + descriptions |
| Big Number | Emphasize statistic | Huge number in accent color |
| Comparison | This vs. That | Two side-by-side boxes |
| Quote | Build authority | Large quote with attribution |
| Team/Profile | Introduce people | Profile cards with images |
| Thank You | Final slide | Closing message + contact info |

### 2. Visual Enhancement System

#### Image Integration
- **Unsplash API Search:** Automatically finds relevant, high-quality images based on slide content
- **Base64 Embedding:** Images converted to data URIs for self-contained files
- **Styled Placeholders:** Elegant placeholders when images unavailable

#### Icon Library
- **3000+ Lucide Icons:** Searchable by keyword (communication, leadership, analysis, etc.)
- **Inline SVG:** No external dependencies, fully stylable
- **Auto-colored:** Icons automatically use accent color (#4f46e5)

### 3. Academic Features

- **Citation Management:** Inline citations converted to slide footnotes with proper formatting
- **Speaker Notes:** Extracted and formatted for print view
- **Reference Lists:** Automatic bibliography slides when needed

### 4. Navigation & Interactivity

- **Keyboard Controls:**
  - `→` or `Space` = Next slide
  - `←` = Previous slide
  - `Home` = First slide
  - `End` = Last slide
- **Visual Navigation:** On-screen previous/next buttons
- **Progress Bar:** Top-of-screen indicator showing presentation progress
- **Slide Counter:** Shows current slide number / total slides

### 5. Presentation-Ready Output

- **Fullscreen Mode:** Press F11 for immersive presentation
- **Print-Friendly:** Browser print → PDF with speaker notes included
- **Cross-Browser:** Works in Chrome, Firefox, Safari, Edge
- **Offline Capable:** No internet required after generation

---

## Configuration

### Unsplash Image Search (Optional)

To enable automatic image search:

1. **Get API Key:**
   - Visit https://unsplash.com/developers
   - Create account and register application (free)
   - Copy Access Key

2. **Set Environment Variable:**
   ```bash
   export UNSPLASH_ACCESS_KEY="your_access_key_here"
   ```

3. **Verify:**
   Next time you generate slides, images will be automatically searched and embedded.

**Free Tier Limits:**
- 50 requests per hour
- High-quality, royalty-free images
- No attribution required

**Without API Key:**
The skill works perfectly fine without Unsplash. It will generate styled placeholders with descriptive text that you can replace manually if desired.

---

## Examples

### Example 1: Standard Lecture Conversion

**Input:** `courses/BUS201/weeks/week-03/lecture-content.md`

**Command:**
```
Convert week 3 to slides
```

**Result:**
- Parses 25-30 slides from lecture content
- Detects layouts: 1 title, 2 section breaks, 18 content, 4 split-screen, 1 quote, 1 thank you
- Searches Unsplash for 4 images (embedded as base64)
- Adds 3 Lucide icons to tiled layouts
- Formats 12 inline citations as footnotes
- Generates `slides.html` (self-contained, ~2.5MB)

**Usage:**
```bash
open courses/BUS201/weeks/week-03/slides.html
# Press F11 for fullscreen
# Use arrow keys to navigate
```

### Example 2: Custom Content

You can also create slides from any markdown file:

```markdown
# Business Communication Strategies
Week 5: Persuasive Techniques

---

## Key Persuasion Principles

- Reciprocity: Give before asking
- Social Proof: Leverage testimonials
- Authority: Establish credibility
- Scarcity: Create urgency

---

> "The key to successful leadership today is influence, not authority."
> — Kenneth Blanchard
```

The skill will automatically:
- Detect `#` heading → Title Slide layout
- Detect `##` + bullets → Standard Content layout
- Detect `>` blockquote → Quote Slide layout

---

## File Structure

```
.claude/skills/slide-exporter/
├── SKILL.md                          # Main skill instructions (auto-invocation logic)
├── resources/
│   ├── design-guidelines.md          # Complete design philosophy
│   ├── layout-templates.md           # 10 HTML layout patterns
│   ├── css-framework.md              # Complete CSS system
│   └── examples/
│       └── sample-slide-output.html  # Working example with all 10 layouts
└── README.md                         # This file
```

### Key Documentation

- **SKILL.md**: Complete instructions for Claude on how to use this skill
- **design-guidelines.md**: Full design philosophy (fonts, colors, spacing, layouts)
- **layout-templates.md**: HTML structure for all 10 slide layouts
- **css-framework.md**: Complete CSS that gets inlined into generated HTML
- **sample-slide-output.html**: Working demo you can open in browser

---

## Customization

### Changing Colors

Edit CSS variables in generated HTML:

```css
:root {
  --color-accent: #10b981;     /* Change to green */
  --color-primary: #0f172a;    /* Darker text */
}
```

All slides automatically update to use new colors.

### Changing Fonts

Replace Google Fonts link in `<head>`:

```html
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Open+Sans:wght@400;700&display=swap" rel="stylesheet">
```

Update CSS variables:
```css
:root {
  --font-header: 'Roboto', sans-serif;
  --font-body: 'Open Sans', sans-serif;
}
```

### Modifying Layouts

See `resources/layout-templates.md` for HTML structure of each layout. Copy and modify as needed.

---

## Troubleshooting

### Issue: "Lecture content file not found"

**Cause:** `lecture-content.md` doesn't exist for specified week

**Solution:**
```
Run /generate-week [N] first to create lecture content
```

### Issue: Images not loading / showing placeholders

**Cause:** Either no `UNSPLASH_ACCESS_KEY` set, or API limit reached

**Solutions:**
1. Set environment variable (see Configuration section)
2. Accept placeholders and add images manually later
3. Use local images (place in `weeks/week-N/images/` folder)

### Issue: Slides not displaying correctly

**Cause:** Browser compatibility or zoom level

**Solutions:**
1. Use modern browser (Chrome, Firefox, Safari, Edge)
2. Reset browser zoom to 100% (Cmd/Ctrl + 0)
3. Try different browser
4. Clear browser cache

### Issue: Navigation not working

**Cause:** JavaScript blocked or error

**Solutions:**
1. Check browser console for errors (F12)
2. Ensure JavaScript enabled in browser
3. Try opening file with different browser
4. Check file permissions

### Issue: Print view doesn't show speaker notes

**Cause:** Print CSS not loading correctly

**Solution:**
1. Use "Print Preview" in browser first
2. Select "Print backgrounds" option
3. Try "Save as PDF" instead
4. Verify `@media print` styles in CSS

---

## Best Practices

### Content Preparation

✓ **Keep bullets concise** - Short phrases, not full sentences
✓ **One idea per slide** - Don't overload slides with information
✓ **Use visuals strategically** - Images should enhance, not decorate
✓ **Include citations** - Give credit for research and statistics
✓ **Add speaker notes** - Remind yourself of key points to discuss

### Presentation Delivery

✓ **Test beforehand** - Open slides.html and navigate through once
✓ **Fullscreen mode** - Press F11 for immersive presentation
✓ **Practice transitions** - Know when to pause, ask questions, engage
✓ **Have backup** - Save PDF version in case of technical issues
✓ **Print handouts** - Browser print → PDF for distributing to students

### File Management

✓ **Keep source markdown** - Always maintain original `lecture-content.md`
✓ **Version control** - Use git for tracking changes
✓ **Backup API keys** - Store `UNSPLASH_ACCESS_KEY` securely
✓ **Archive old versions** - Keep previous slide versions for reference

---

## Technical Specifications

### Output Specifications

- **Format:** Single HTML file
- **Dimensions:** 1024x768px (4:3 aspect ratio)
- **File Size:** 2-5MB typical (depends on embedded images)
- **Dependencies:** None (self-contained)
- **Fonts:** Google Fonts CDN (Poppins, Lato)

### Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✓ Fully supported |
| Firefox | 88+ | ✓ Fully supported |
| Safari | 14+ | ✓ Fully supported |
| Edge | 90+ | ✓ Fully supported |
| IE 11 | - | ✗ Not supported |

### API Integrations

- **Unsplash API v1** (optional)
  - Endpoint: `https://api.unsplash.com/search/photos`
  - Authentication: Access Key in header
  - Rate Limit: 50 requests/hour (free tier)

- **Lucide Icons** (built-in)
  - Version: Latest
  - Format: Inline SVG
  - Count: 3000+ icons available

---

## Support & Resources

### Documentation

- **Design Philosophy:** See `resources/design-guidelines.md`
- **Layout Reference:** See `resources/layout-templates.md`
- **CSS System:** See `resources/css-framework.md`
- **Live Example:** Open `resources/examples/sample-slide-output.html`

### External Resources

- **Unsplash:** https://unsplash.com/developers
- **Lucide Icons:** https://lucide.dev
- **Google Fonts:** https://fonts.google.com
- **Poppins Font:** https://fonts.google.com/specimen/Poppins
- **Lato Font:** https://fonts.google.com/specimen/Lato

### Getting Help

1. **Check documentation** in `resources/` folder
2. **View example** in `resources/examples/sample-slide-output.html`
3. **Review SKILL.md** for complete conversion logic
4. **Test with sample content** before using real lecture content

---

## Version History

### v1.0.0 (January 2025)
- Initial release
- 10 layout templates with automatic detection
- Unsplash image search integration
- Lucide icon library (3000+ icons)
- Base64 image embedding
- Speaker notes extraction
- Citation formatting
- Self-contained HTML output
- Keyboard navigation
- Progress tracking
- Print-friendly output

---

## License

This skill is part of the Class Content Generator system and follows the same license.

---

*For questions or improvements, update relevant files in the skill directory.*
