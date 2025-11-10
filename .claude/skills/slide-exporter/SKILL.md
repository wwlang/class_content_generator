---
name: slide-exporter
description: Converts lecture content markdown files to self-contained HTML presentations with PT Serif/Roboto fonts, 4:3 aspect ratio (1024x768px), 25 automatic layouts (10 base + 15 educational), image search, and SVG icons
version: 1.1.0
author: Custom
dependencies: none
---

# Slide Exporter Skill

## Overview

This skill converts lecture content from markdown files (`lecture-content.md`) into professional, self-contained HTML presentation files. The output follows a strict design philosophy with:

- **Fixed 4:3 aspect ratio** (1024x768px slides for projector compatibility)
- **Font pairing:** PT Serif (headers) + Roboto (body)
- **Color scheme:** White backgrounds, muted blue-purple titles (#7373b0), dark gray body (#475569)
- **25 comprehensive layouts:** 10 base + 15 educational layouts, automatically detected from content structure
- **Visual enhancements:** Unsplash image search, Lucide SVG icons, base64 embedding
- **Self-contained output:** Single HTML file with inline CSS, JavaScript, and embedded media

## When to Invoke This Skill

Auto-invoke when the user requests any of the following:

- "Convert week [N] to slides"
- "Export week [N] lecture to HTML"
- "Create presentation for week [N]"
- "Generate slides for week [N]"
- "/export-slides [N]" (explicit command)
- Any variant requesting lecture-to-presentation conversion

**Prerequisites:**
- File must exist: `courses/[COURSE-CODE]/weeks/week-[N]/lecture-content.md`
- If file doesn't exist, inform user and suggest running `/generate-week [N]` first

## Design Philosophy Integration

This skill implements the complete design philosophy documented in `resources/design-guidelines.md`. Key principles:

1. **Fixed "Stage" Layout:** Every slide is a 1024x768px container (4:3 ratio) centered on neutral background
2. **Generous White Space:** 60px padding on all sides (except bleed layouts)
3. **Typography Hierarchy:** PT Serif for all headers (h1-h3), Roboto for all body text
4. **Consistent Positioning:** Slide titles always in same position, creating visual stability
5. **Minimal Animation:** Simple fade transitions, no distracting effects
6. **High Contrast:** Accessibility-first color choices

**See `resources/design-guidelines.md` for complete philosophy.**
**See `resources/layout-templates.md` for all 25 layout HTML patterns (10 base + 15 educational).**
**See `resources/css-framework.md` for complete CSS system.**
**See `resources/visual-enhancements-guide.md` for strategies to make slides more attractive.**

---

## Conversion Process

### STEP 1: Read and Parse Lecture Content

**Input:** `courses/[COURSE-CODE]/weeks/week-[N]/lecture-content.md`

**Parse for:**
1. **Slide boundaries:** Identified by `---` dividers or markdown heading levels
2. **Content types:** Title slides, section breaks, content slides, images, quotes, data
3. **Speaker notes:** Usually in blockquotes or designated note sections
4. **Citations:** APA format inline citations (Author, Year) and reference lists
5. **Image references:** Markdown image syntax `![alt](path)` or image descriptions

**Example parsing patterns:**
```
# Title → Title Slide (Layout 1)
## Section Title → Section Break (Layout 2)
### Content with bullets → Standard Content (Layout 3)
Content + image reference → Split Screen (Layout 4)
3 parallel sections → Tiled Layout (Layout 5)
Large number/stat → Big Number Slide (Layout 6)
> Quote → Quote Slide (Layout 8)
```

---

### STEP 2: Automatic Layout Detection

Map parsed content to one of 10 layouts based on structure:

#### Layout Detection Algorithm

```
FOR EACH slide content block:

  IF (First slide of presentation):
    → USE Layout 1: Title Slide

  ELSE IF (Single h2 heading only, no body content):
    → USE Layout 2: Section Break Slide

  ELSE IF (Heading + bullet list with 2-6 items):
    → USE Layout 3: Standard Content (Title + Bullets)

  ELSE IF (Content has image reference OR description like "chart showing..."):
    → USE Layout 4: Split Screen (50/50 Text & Image)

  ELSE IF (Content has 3 parallel sections/features/points):
    → USE Layout 5: Tiled Layout (3 columns)

  ELSE IF (Content emphasizes single number/statistic):
    → USE Layout 6: Big Number Slide

  ELSE IF (Content shows 2 contrasting concepts like "Before/After", "Old/New"):
    → USE Layout 7: Comparison (This vs. That) Slide

  ELSE IF (Content is a blockquote or citation):
    → USE Layout 8: Quote Slide

  ELSE IF (Content introduces people/team members):
    → USE Layout 9: Team / Profile Slide

  ELSE IF (Last slide with "thank you" or "questions" or contact info):
    → USE Layout 10: Final "Thank You" Slide

  # Educational Layouts (Tier 1: 11-15)

  ELSE IF (Table with English/Vietnamese columns OR "vocabulary" in title):
    → USE Layout 11: Vocabulary Table (Bilingual)

  ELSE IF (Content describes activity with phases/timing OR "think-pair-share"):
    → USE Layout 12: Think-Pair-Share / Activity Instructions

  ELSE IF (Table showing criteria/performance levels OR "rubric" in title):
    → USE Layout 13: Rubric Preview

  ELSE IF (Central concept with multiple branches/connections OR "concept map"):
    → USE Layout 14: Concept Map / Mind Map

  ELSE IF (Content shows problem-solution-answer structure OR "worked example"):
    → USE Layout 15: Worked Example

  # Educational Layouts (Tier 2: 16-20)

  ELSE IF (Chronological years/dates OR keywords "evolution", "timeline", "history"):
    → USE Layout 16: Timeline / Process Flow

  ELSE IF (Contains "case study" OR sections: background/challenge/solution/results):
    → USE Layout 17: Case Study Layout

  ELSE IF ("learning objectives" OR "by the end" OR Bloom's taxonomy verbs):
    → USE Layout 18: Learning Objectives Preview

  ELSE IF (Question with "arguments for/against" OR "debate" OR "discussion"):
    → USE Layout 19: Discussion Prompt / Debate Setup

  ELSE IF ("further reading" OR "resources" OR "recommended" with article/book list):
    → USE Layout 20: Resource List / Further Reading

  # Educational Layouts (Tier 3: 21-25)

  ELSE IF (Contains "N=", "p <", "findings" OR research methodology details):
    → USE Layout 21: Research Findings / Study Results

  ELSE IF (Matrix/table applying framework to multiple cases):
    → USE Layout 22: Framework Application Matrix

  ELSE IF ("reflection" OR "journal" with introspective questions):
    → USE Layout 23: Reflection / Journal Prompt

  ELSE IF ("group activity" OR "team roles" OR assignment with deliverables/timing):
    → USE Layout 24: Group Assignment Brief

  ELSE IF ("assessment" + "checklist" OR success criteria with rubric percentages):
    → USE Layout 25: Assessment Checklist / Success Criteria

  ELSE:
    → DEFAULT to Layout 3: Standard Content
```

**Layout Reference:**
- All 25 layouts fully documented in `resources/layout-templates.md`
- Each includes complete HTML structure with semantic markup
- All follow 1024x768px (4:3) fixed dimensions with appropriate padding
- Educational layouts (11-25) optimized for interactive learning contexts

---

### STEP 3: Visual Enhancement - Image Handling

For each slide that requires an image (Layouts 4, 5, 9, or explicit image references):

#### Option A: Unsplash Image Search (Preferred)

**When to use:** User has UNSPLASH_ACCESS_KEY environment variable set, OR user approves API usage

**Process:**
1. **Extract keywords** from slide content (main concepts, topics)
2. **Search Unsplash API:**
   ```
   GET https://api.unsplash.com/search/photos?query=[keywords]&per_page=3
   Authorization: Client-ID [UNSPLASH_ACCESS_KEY]
   ```
3. **Select best match** from top 3 results (highest relevance score)
4. **Download image** from `urls.regular` (1080px width)
5. **Convert to base64:**
   - Fetch image binary data
   - Encode as base64 string
   - Format as data URI: `data:image/jpeg;base64,[base64string]`
6. **Embed in HTML:** Use data URI in `<img src="data:image/jpeg;base64,...">>`

**API Details:**
- Free tier: 50 requests/hour
- No attribution required for editorial use
- High-quality, royalty-free images

#### Option B: Reference Existing Images

**When to use:** Images already exist in course materials (e.g., `weeks/week-N/images/`)

**Process:**
1. **Check for image files** in `weeks/week-[N]/images/` directory
2. **If found:** Read file, convert to base64, embed as data URI
3. **If not found:** Fall back to Option C

#### Option C: Styled Placeholders (Fallback)

**When to use:** No API key, no existing images, or user prefers placeholders

**Process:**
Generate styled placeholder box:
```html
<div class="image-placeholder">
  <svg width="100%" height="100%" viewBox="0 0 640 360">
    <rect width="100%" height="100%" fill="#e2e8f0"/>
    <text x="50%" y="50%" text-anchor="middle" font-family="Lato" font-size="20" fill="#64748b">
      [Image: {description}]
    </text>
  </svg>
</div>
```

**Styling:**
- Background: Light gray (#e2e8f0)
- Border: 2px dashed #cbd5e1
- Border-radius: 12px
- Centered descriptive text in Lato

---

### STEP 4: Visual Enhancement - SVG Icons

For slides that benefit from icons (Layout 5: Tiled, Layout 9: Team, or conceptual slides):

#### Using Lucide Icons Library

**Icon Selection Process:**
1. **Extract concepts** from slide content (e.g., "communication", "leadership", "analysis")
2. **Map to Lucide icons** using keyword matching:
   ```
   Communication → MessageCircle, Phone, Mail
   Leadership → Users, Award, Target
   Analysis → BarChart, PieChart, TrendingUp
   Strategy → Compass, Map, Target
   Innovation → Lightbulb, Zap, Sparkles
   Teamwork → Users, UserPlus, Heart
   Time → Clock, Calendar, Timer
   Money → DollarSign, TrendingUp, Wallet
   Success → CheckCircle, Award, Star
   Growth → TrendingUp, ArrowUp, BarChart
   ```

3. **Retrieve SVG code** from Lucide library (3000+ available)
4. **Apply styling:**
   - Set `stroke="currentColor"` (allows CSS color control)
   - Add class: `class="lucide-icon"`
   - Size: `width="48" height="48"` for tiled layouts, `width="32" height="32"` for inline

5. **Color with accent:**
   ```html
   <div style="color: #4f46e5;">
     <svg class="lucide-icon" width="48" height="48" ...>
       <!-- Lucide SVG path here -->
     </svg>
   </div>
   ```

**Common Lucide Icons for Business/Academic Content:**
- MessageCircle, Users, Award, Target, Compass, TrendingUp
- Lightbulb, BarChart, CheckCircle, Calendar, FileText
- Search, Edit, Eye, Heart, Star, Shield, Zap

**No API Required:** Lucide is open-source, MIT licensed, can embed SVG directly.

---

### STEP 5: Speaker Notes Extraction

**Identify speaker notes in source markdown:**

Common patterns:
```markdown
**Speaker Notes:** [content here]
> Note to instructor: [content here]
[Content in italics at end of slide]
```

**Convert to HTML format:**
```html
<aside class="speaker-notes">
  <h4>Speaker Notes</h4>
  <p>[Extracted note content]</p>
</aside>
```

**Styling:**
- Hidden by default (`display: none;`)
- Displayed only in print view (`@media print`)
- Light gray background (#f8fafc)
- Smaller font (14px Lato)
- Appears below slide content when printed

---

### STEP 6: Citation Formatting

**Parse citations from lecture content:**

**Input formats:**
```
Inline: (Cialdini, 2021)
Inline: According to Smith and Jones (2020)...
Reference list: Smith, J., & Jones, M. (2020). Title. Journal, 15(3), 234-245. https://doi.org/...
```

**Convert to slide footnotes:**

**Option A: Per-slide footnotes (Recommended)**
```html
<div class="slide-footer">
  <p class="citation">¹ Cialdini, R. (2021). <em>Influence</em>. Harper Business.</p>
</div>
```

**Option B: Reference list on final slide**
```html
<!-- Last slide before Thank You -->
<div class="slide references-slide">
  <h2 class="slide-title">References</h2>
  <div class="references-list">
    <p class="citation">Cialdini, R. (2021)...</p>
    <p class="citation">Smith, J., & Jones, M. (2020)...</p>
  </div>
</div>
```

**Styling:**
- Font: Lato, 12px
- Color: #64748b (muted)
- Position: Bottom of slide with 20px padding
- Line height: 1.4 for readability

**Numbering:**
- Use superscript for in-text citations: `<sup>1</sup>`
- Match numbers to footer: `¹`, `²`, `³`, etc.

---

### STEP 7: Assemble HTML Structure

Generate complete self-contained HTML file:

#### HTML Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Course Code] Week [N] - [Lecture Title]</title>

  <!-- Google Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=PT+Serif:wght@400;700&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">

  <!-- Inline CSS -->
  <style>
    [COMPLETE CSS FROM resources/css-framework.md]
  </style>
</head>
<body>
  <!-- Presentation Container -->
  <div class="presentation-container">

    <!-- Navigation Controls -->
    <div class="nav-controls">
      <button id="prev-btn">‹</button>
      <span id="slide-counter">1 / [total]</span>
      <button id="next-btn">›</button>
    </div>

    <!-- Progress Bar -->
    <div class="progress-bar">
      <div class="progress-fill" id="progress-fill"></div>
    </div>

    <!-- Slides -->
    <div class="slide active" data-slide="1">
      [Slide 1 HTML from layout template]
    </div>

    <div class="slide" data-slide="2">
      [Slide 2 HTML from layout template]
    </div>

    <!-- ... more slides ... -->

  </div>

  <!-- JavaScript for Navigation -->
  <script>
    [COMPLETE NAVIGATION SCRIPT - see below]
  </script>
</body>
</html>
```

#### JavaScript Navigation (Inline)

```javascript
// Presentation Navigation Script
(function() {
  let currentSlide = 1;
  const slides = document.querySelectorAll('.slide');
  const totalSlides = slides.length;
  const prevBtn = document.getElementById('prev-btn');
  const nextBtn = document.getElementById('next-btn');
  const counter = document.getElementById('slide-counter');
  const progressFill = document.getElementById('progress-fill');

  function showSlide(n) {
    if (n < 1) n = 1;
    if (n > totalSlides) n = totalSlides;

    slides.forEach(slide => slide.classList.remove('active'));
    slides[n - 1].classList.add('active');

    currentSlide = n;
    counter.textContent = `${n} / ${totalSlides}`;
    progressFill.style.width = `${(n / totalSlides) * 100}%`;
  }

  function nextSlide() { showSlide(currentSlide + 1); }
  function prevSlide() { showSlide(currentSlide - 1); }

  // Button listeners
  prevBtn.addEventListener('click', prevSlide);
  nextBtn.addEventListener('click', nextSlide);

  // Keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
    if (e.key === 'ArrowLeft') prevSlide();
    if (e.key === 'Home') showSlide(1);
    if (e.key === 'End') showSlide(totalSlides);
  });

  // Initialize
  showSlide(1);
})();
```

---

### STEP 8: Generate Output File

**Save to:** `courses/[COURSE-CODE]/weeks/week-[N]/slides.html`

**Final checklist before saving:**
- [ ] All images converted to base64 data URIs (or styled placeholders)
- [ ] All icons embedded as inline SVG with correct styling
- [ ] All slides use correct layout from detection algorithm
- [ ] Speaker notes extracted and formatted (if present)
- [ ] Citations formatted as footnotes or reference slide
- [ ] Navigation JavaScript included and functional
- [ ] Google Fonts link included in `<head>`
- [ ] File is completely self-contained (can open without internet)

**Inform user:**
```
✓ Slides generated: courses/[COURSE-CODE]/weeks/week-[N]/slides.html

  Slides: [count]
  Layouts used: [list of layouts]
  Images: [count embedded / count placeholders]
  Icons: [count embedded]

  To view: Open slides.html in any modern browser
  To present: Press F11 for fullscreen, use arrow keys to navigate
  To print: Browser Print → Save as PDF for distribution
```

---

## Advanced Features

### Image Search Customization

If user wants different image sources, ask about:
- **Pexels API** (alternative to Unsplash, similar features)
- **Pixabay API** (larger library, mixed quality)
- **Local image directory** (use existing course materials)
- **AI generation** (DALL-E, Stable Diffusion - requires API keys)

### Layout Override

User can specify layout explicitly in markdown:
```markdown
<!-- layout: split-screen -->
# Slide Title
Content here...
```

Parse `<!-- layout: [name] -->` comments and override auto-detection.

### Theme Customization

User can modify color scheme by editing:
```css
:root {
  --color-primary: #1e293b;    /* Main text */
  --color-secondary: #475569;  /* Body text */
  --color-accent: #4f46e5;     /* Brand color */
  --color-background: #ffffff; /* Slide bg */
  --color-neutral: #e2e8f0;    /* Stage bg */
}
```

All colors reference these CSS variables for easy theming.

---

## Error Handling

### Common Issues

**1. Lecture content file not found**
```
Error: Could not find lecture-content.md for week [N]
Suggestion: Run /generate-week [N] first to create lecture content
```

**2. Unsplash API key missing**
```
Note: UNSPLASH_ACCESS_KEY not found in environment
Using styled placeholders for images
To enable image search: Set UNSPLASH_ACCESS_KEY env variable
```

**3. Malformed markdown**
```
Warning: Could not parse slide structure in section [X]
Defaulting to Layout 3 (Standard Content)
Review markdown formatting for best results
```

**4. Image download fails**
```
Warning: Failed to download image from Unsplash
Using styled placeholder instead
Reason: [API error message]
```

### Validation

Before finalizing output, validate:
- [ ] HTML is well-formed (no unclosed tags)
- [ ] All images either embedded or placeholder
- [ ] JavaScript navigation script included
- [ ] CSS includes all layout styles
- [ ] File size reasonable (<5MB for typical 20-30 slide deck)

---

## Quality Standards

Every generated presentation must meet these standards:

**Visual Quality:**
- ✓ 1024x768px (4:3) fixed slide dimensions
- ✓ PT Serif font for all headers (h1, h2, h3)
- ✓ Roboto font for all body text (p, li)
- ✓ Consistent 60px padding (except bleed layouts)
- ✓ High contrast text (WCAG AA minimum)
- ✓ Accent color (#7373b0 muted blue-purple) used sparingly and effectively

**Content Quality:**
- ✓ One main idea per slide (not cluttered)
- ✓ Images relevant and high-quality
- ✓ Icons enhance comprehension (not decorative only)
- ✓ Citations properly formatted
- ✓ Speaker notes preserved when present

**Technical Quality:**
- ✓ Self-contained (single HTML file, no dependencies)
- ✓ Works offline (all assets embedded)
- ✓ Keyboard navigation functional
- ✓ Print-friendly (speaker notes show in print view)
- ✓ Cross-browser compatible (Chrome, Firefox, Safari, Edge)

---

## Examples & References

**Complete working example:** See `resources/examples/sample-slide-output.html`

**Layout templates:** See `resources/layout-templates.md` for all 10 layouts

**CSS framework:** See `resources/css-framework.md` for complete styling system

**Design philosophy:** See `resources/design-guidelines.md` for full principles

---

## Version History

**v1.1.0** (January 2025)
- Added 15 educational-specific layouts (Layouts 11-25)
  - Tier 1: Vocabulary tables, activity instructions, rubric previews, concept maps, worked examples
  - Tier 2: Timelines, case studies, learning objectives, discussion prompts, resource lists
  - Tier 3: Research findings, framework matrices, reflection prompts, group assignments, assessment checklists
- Created comprehensive visual enhancements guide
- Enhanced layout detection algorithm with educational patterns
- Updated all documentation with new layouts

**v1.0.0** (January 2025)
- Initial release
- 10 base layout templates with auto-detection
- Unsplash image search integration
- Lucide icon library integration
- Base64 image embedding
- Speaker notes extraction
- Citation formatting
- Self-contained HTML output with navigation
- 4:3 aspect ratio (1024x768px) for projector compatibility
- PT Serif + Roboto font pairing
- Muted blue-purple accent color (#7373b0)
