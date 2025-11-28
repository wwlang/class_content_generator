# Presentation Design Philosophy: Reference Design System

When building HTML presentations, the goal is to make them look like professional, static slide decks (like Google Slides or PowerPoint), not like standard, scrolling webpages. The two most important decisions to achieve this are **1) a fixed-aspect-ratio layout** and **2) a clean, hierarchical font system**.

**This document describes the Reference Design System** - the current design standard using Cal Sans + Plus Jakarta Sans fonts and an orange (#ed5e29) accent color.

---

## 1. The Layout: "A Stage, Not a Page"

The single most important trick is to stop thinking like a webpage (which scrolls) and start thinking like a slide (which is a fixed-size canvas).

### Fixed Aspect Ratio

Create a main div for each slide and lock its dimensions to a 4:3 aspect ratio (standard for projectors). **Standard dimensions:**

- **Width:** 1024px
- **Height:** 768px

### Slide Centering

Place this 1024x768 "slide" onto a neutral background (like a light gray, e.g., `#e5e5e5`). Center the slide on the page. This creates the "stage" effect, just like in Google Slides' "Present" mode.

### Internal Padding

All content inside the slide is pulled away from the edges with generous, consistent padding.

**Standard Padding:** `60px` on all sides (`padding: 60px;`).

**Bleed Layouts:** For layouts with an image that "bleeds" to the edge (like full-bleed backgrounds), set the slide's `padding` to `0` and apply padding only to the content areas.

### Core Layouts (The Workhorses)

Rely on **CSS Flexbox** and **CSS Grid** to organize the content within the 1024x768 container.

**Title_Slide:** Uses `display: flex;`, `justify-content: flex-start;`, and `align-items: center;` to left-align the title and subtitle.

**Grid Layouts:** Uses `display: grid;` with `grid-template-columns` to create equal columns. Supports 2-column (`1fr 1fr`) and 3-column (`1fr 1fr 1fr`) patterns with automatic orange header styling.

**Card Layout:** Uses `display: grid;` with `gap: 24px;` to create visual cards with consistent spacing.

---

## 2. The Font Styles: "Clarity and Contrast"

The typography strategy is built on **font pairing**. Use two different fonts: one for headers (to grab attention) and one for body text (for maximum readability).

### Header Font: Cal Sans

**Why:** A modern, bold display font perfect for headlines. Creates strong visual hierarchy and immediate impact. The condensed letter-spacing (-0.05em) adds sophistication while maintaining readability.

**Where used:** `h1`, `h2` (the slide-title), `h3` (section headers, grid headers).

**Font Loading:**
- **HTML:** Embedded as base64 in CSS (no external file needed)
- **PPTX:** Embedded using `tools/embed_fonts_in_pptx.py`

#### Common Styles

**h1 (Title Slide):**
- Font: Cal Sans
- Weight: 700 (Bold)
- Size: 60px
- Color: #131313 (Dark gray)
- Letter-spacing: -0.05em (condensed)

**slide-title (The h2 on most slides):**
- Font: Cal Sans
- Weight: 700 (Bold)
- Size: 28px
- Color: #131313 (Dark gray)
- Letter-spacing: -0.05em (condensed)
- Margin: `margin-bottom: 24px;` (to create space)

**h3 (Grid headers, section headers):**
- Font: Cal Sans
- Weight: 700 (Bold)
- Size: 20px
- Color: #ed5e29 (Orange - accent color)
- Letter-spacing: -0.05em (condensed)

**Framework Components (Special Sizing):**
Framework layouts use larger fonts for readability:
- **Framework title:** 48px (Cal Sans, same as slide titles)
- **Component heading:** 27px (Cal Sans, bold)
- **Component description:** 17px (Plus Jakarta Sans, 20% smaller for cleaner cards)
- **Commentary text:** 24px (Plus Jakarta Sans)
- **Commentary citation:** 21px (Plus Jakarta Sans, italic, muted)

### Body Font: Plus Jakarta Sans

**Why:** A modern, geometric sans-serif with excellent readability. Clean lines and balanced proportions work perfectly for presentations. Variable font weights provide flexibility. Excellent multilingual support including Vietnamese diacritics.

**Where used:** `p`, `li`, captions, labels, speaker notes.

**Font Loading:**
- **HTML:** Google Fonts (variable font, weights 400-700)
- **PPTX:** Embedded using `tools/embed_fonts_in_pptx.py`

#### Common Styles

**p, li (body text):**
- Font: Plus Jakarta Sans
- Weight: 400 (Regular)
- Size: 18px
- Line Height: 1.6 (Essential for readability)
- Color: #131313 (Dark gray)

**small text (captions, citations):**
- Font: Plus Jakarta Sans
- Weight: 400 (Regular)
- Size: 12px
- Color: #64748b (Muted gray)

### Accent Colors (Reference Design System)

Use a simple **60-30-10 rule:**

- **60% (Dominant):** `#f4f3f1` (Cream) - The slide background. Creates warmth and reduces eye strain compared to pure white.
- **30% (Secondary):** `#131313` (Dark gray) - Main text color. High contrast for readability.
- **10% (Accent):** `#ed5e29` (Orange) - Used for emphasis, icons, chart bars, and interactive elements. Creates energy and draws attention.

**Supporting Colors:**
- `#cac3b7` (Tan) - Decorative elements, borders
- `#ffffff` (White) - Cards, high-contrast backgrounds
- `#64748b` (Muted gray) - Secondary text, captions

**Background Policy (STRICT):**
All slides default to cream background (`#f4f3f1`). ONLY these slide types can override:
1. **Title slide** - Cream with decorative shapes
2. **Section break slide** - Orange (`#ed5e29`) or dark gray (`#131313`)
3. **Dark slides** (`.dark-bg` class) - Dark gray (`#131313`)

All other slide types (content, framework, comparison table, quote, reflection, etc.) MUST use the default cream background.

---

## 3. Integrating Visuals & Complex Layouts

### Integrating Images

The choice depends on how much focus the image should have.

#### Split Screen Layout (Image + Text)

**How:** Use `display: grid;` with `grid-template-columns: 1fr 1fr;` on the slide.

**Why:** This is more robust than Flexbox. It guarantees a perfect 50/50 split, even if the text in one column is much shorter than the image height in the other.

**Image Sizing:** The `<img>` tag is set to `width: 100%; height: 100%;` and `object-fit: cover;`. This ensures the image fills its (50%) column perfectly without being stretched or distorted.

#### Full Bleed Layout

For a powerful, modern look (often for a Title or Section Break).

**How:** The slide div has `padding: 0;`. An `<img>` is placed inside with `width: 100%; height: 100%; object-fit: cover;`.

**Text:** A new div containing the text (h1, p) is placed on top of the image. This is done by setting the slide to `position: relative;` and the text div to `position: absolute; top: 0; left: 0; width: 100%; height: 100%;`.

**Readability:** To ensure the text is readable, the text div gets a semi-transparent dark overlay (e.g., `background-color: rgba(19, 19, 19, 0.7);`) and the text itself is set to cream or white.

#### Simple Image

For just showing a diagram or photo.

**How:** Inside the standard slide with `padding: 60px;`, add an `<img>` tag.

**Styling:** Give it a `max-width: 100%;` (so it doesn't break the layout) and often a `border-radius: 16px;` and a subtle `box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);` to lift it off the page.

### Integrating Icons

Icons are for quickly communicating a concept. **Use inline SVG from Lucide Icons library.**

**How:** Copy the SVG code from Lucide and paste it directly into the HTML.

**Why:**
- **No Files:** Keeps everything in one HTML file.
- **Scalable:** They are "vector" and look sharp at any size.
- **Stylable:** Can style them with CSS using `currentColor`.

**Styling:** Set the icon's color to the accent color (`#ed5e29`) to make it pop. Do this by setting the SVG's `stroke` attribute to `currentColor` and then setting the text color of its container (`color: #ed5e29;`).

#### Card Layout with Icons

This layout uses `display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px;`.

- Each card is a white box with rounded corners and subtle shadow
- Each card can include an orange icon at the top
- Cal Sans headers in each card
- Plus Jakarta Sans body text

### Grid Layouts (2-Column and 3-Column)

**Auto-Styling Feature:** Grid layouts automatically apply orange color to h3 headers without inline styles needed.

**2-Column Grid:**
```html
<div class="grid-2-col">
  <div>
    <h3>Concept A</h3>
    <ul>
      <li>Point one</li>
      <li>Point two</li>
    </ul>
  </div>
  <div>
    <h3>Concept B</h3>
    <ul>
      <li>Point one</li>
      <li>Point two</li>
    </ul>
  </div>
</div>
```

**Result:** Headers automatically styled orange (#ed5e29) with Cal Sans font, bullets automatically styled orange.

### Framework Layouts (Component Grids)

**Purpose:** Display structured frameworks with multiple components (e.g., theories, models, development plans).

**Structure:**
- **Framework title** (48px, centered)
- **Component grid** (responsive: 1-3 columns auto-fit, 4 components = 2×2, 5-6 = 3×2)
- **Optional commentary section** (below grid for general statements and citations)

**Component Anatomy:**
Each component has:
- White background (`#ffffff`) - stands out against cream slide
- Rounded corners (8px)
- Light border (`#cbd5e1`)
- **Heading:** 27px, dark gray, bold
- **Description:** 17px, muted gray (20% smaller for cleaner cards)

**Commentary Section:**
- Center-aligned, 80% max-width
- **Text:** 24px
- **Bold statements:** Orange color (`#ed5e29`)
- **Citations:** 21px, italic, muted gray
- Appears below component grid, not inside cards

**Usage:** Automatically parsed from markdown with `**Component:**` format for components and standalone bold/italic text for commentary.

### Table Layouts (Comparison & Vocabulary)

**Consistent Table Styling:**
All tables use minimal vertical padding for space efficiency:
- **Cell padding:** `8px` (vertical) × `12px` (horizontal)
- **Line height:** `1.5` (reduced from 1.7 for tighter spacing)
- **Table margins:** Reduced top/bottom for optimal fit

**Comparison Tables:**
- Orange headers (`#ed5e29`)
- White cell backgrounds
- Clean borders (`#e2e8f0`)
- Hover effect for rows

**Vocabulary Tables:**
- Purple/blue headers for language context
- Same padding as comparison tables
- Supports bilingual content

### Other Common Layouts

#### Quote Slide

**How:** Usually a centered layout (flex-col, justify-center). Use a `<blockquote>` element.

**Styling:** Give the blockquote a `border-left: 4px solid #ed5e29;` (using the accent color) and set the text to a larger size (e.g., 32-40px) in Cal Sans. The citation/author is a smaller `<p>` tag below it in Plus Jakarta Sans.

#### Big Number Slide

**How:** Centered layout using flexbox.

**Typography:**
- A massive number (100-135px) in Cal Sans, colored orange (#ed5e29)
- A descriptive paragraph (18px) in Plus Jakarta Sans underneath

**Purpose:** Create visual drama with a single key statistic.

---

## 4. Guiding Principles (The "Why")

### Simplicity: One Idea Per Slide

Layouts are intentionally simple. The goal is to support the speaker, not replace them. Avoid slide layouts that encourage lots of text. **A slide should have one key takeaway.** If you have two key takeaways, you should probably have two slides.

### The Power of White Space

"White space" (or negative space) is the empty area around your content. The 60px padding rule is a good example. This "breathing room" is the most important part of the design. It reduces cognitive load, directs the audience's eye to what's important, and makes the slide feel calm and confident instead of cluttered and anxious.

### Consistency is King

This is why there's a strict "recipe" for fonts and colors. But it's also about position. **The slide title (.slide-title) should be in the exact same position on every single slide where it appears.** This consistency creates a stable visual "anchor" for the audience, so they don't have to re-learn the layout of every slide.

### Subtle Animation

When building interactive HTML presentations, the animation is minimal.

**Slide Transitions:** A simple, fast fade (`opacity: 0` to `opacity: 1`) is all you need. It's clean, professional, and not distracting. Avoid "fly," "swivel," or "checkerboard" animations, as they can feel unprofessional.

**Content Animation:** Avoid having every single bullet point fly in. If the content isn't a "reveal," it's best to have it appear all at once with the slide. This respects the audience's time and is less distracting.

### Accessibility as Good Design

Design choices are also accessibility choices.

- The Cal Sans / Plus Jakarta Sans pairing provides very clear, readable text with strong hierarchy.
- The font sizes (60px, 28px, 18px) are large enough to be read from a distance.
- The color-contrast (e.g., `#131313` text on `#f4f3f1` background) exceeds WCAG AA standards, making it easy to read for everyone.
- The cream background reduces eye strain compared to pure white.

---

## 5. Common Slide Layouts

Here are **key slide layouts** that build upon all the principles above.

### 1. The Title Slide

**Purpose:** To make a strong first impression and state the presentation's topic.

**How-To:** Use `display: flex;`, `justify-content: flex-start;`, `align-items: center;` with `text-align: left;`.

**Typography:** The h1 (Cal Sans, 700 weight, 60px) and a subtitle p (Plus Jakarta Sans, 400 weight, 20px, orange accent).

**Visual Elements:** Decorative geometric shapes in tan/orange at bottom-left corner.

### 2. The Section Break Slide

**Purpose:** To signal a transition to a new topic, giving the audience a "chapter break."

**How-To:** Full-slide colored background.

**Typography:** Place a single, centered h2 title (Cal Sans, 700 weight, 40px) in cream color.

**Background:** Can use dark gray (#131313) or accent orange (#ed5e29) for impact.

**Why:** The sudden change clearly breaks the visual flow and re-engages the audience.

### 3. Standard Content (Title + Bullets)

**Purpose:** The "workhorse" of the presentation. Used to deliver core information.

**How-To:** A simple vertical stack. Use the standard 60px padding.

**Typography:** The `.slide-title` (Cal Sans, 28px) at the top. Below it, a `<ul>` with `<li>` elements (Plus Jakarta Sans, 18px).

**Key:** Don't put more than 5-6 bullets on a slide. Keep them as short phrases, not long sentences.

### 4. Grid Layouts (2 or 3 Columns)

**Purpose:** To compare concepts or present parallel information.

**How-To:** Use `grid-2-col` or `grid-3-col` CSS classes. Headers automatically styled orange.

**Typography:** Cal Sans headers (20px, orange) + Plus Jakarta Sans bullets (18px).

**Key Feature:** Auto-styling eliminates need for inline styles.

### 5. Card Layout

**Purpose:** To present 2-4 related concepts as distinct visual cards.

**How-To:** Use `display: grid` with cards having white backgrounds and rounded corners.

**Styling:** Each card has subtle shadow, optional orange left border, Cal Sans headers, Plus Jakarta Sans body.

### 6. The "Big Number" Slide

**Purpose:** To emphasize a single, critical statistic or number in a dramatic way.

**How-To:** Use `display: flex;`, `flex-direction: column;`, `justify-content: center;`, `align-items: center;`.

**Typography:**
- A massive `<span class="big-number">` (Cal Sans, 700 weight, 100-135px) in orange (#ed5e29)
- A small `<p>` (Plus Jakarta Sans, 18px) underneath explaining the number

**Why:** Pure visual drama. The lack of other content forces focus on that single data point.

### 7. Comparison Table

**Purpose:** To compare two concepts in detail with multiple dimensions.

**How-To:** Use 2-column table with contrasting column colors.

**Styling:** Orange headers, alternating row backgrounds for readability.

### 8. The Quote Slide

**Purpose:** To build authority or emotional connection using someone else's words.

**How-To:** Use a `<blockquote>` with a `border-left` in orange.

**Typography:** The quote text should be large (32-40px, Cal Sans). The citation below (`<p>`) should be smaller (16px, Plus Jakarta Sans, muted gray).

**Layout:** Centered with plenty of white space.

### 9. Dark Slide (Modifier)

**Purpose:** To create emphasis through high contrast. Can be combined with other layouts.

**How-To:** Add `dark-slide` class to any slide type.

**Styling:** Dark gray background (#131313), cream text (#f4f3f1), orange accents remain bright.

**Use Cases:** Case studies, examples, Vietnamese context slides, dramatic quotes.

### 10. References Slide

**Purpose:** To present academic citations in proper format.

**Typography:** Small text (11-12px Plus Jakarta Sans), hanging indents, multi-column if needed.

**Styling:** Minimal, clean, professional. Focus on readability of citations.

---

## Summary: Core Design Rules (Reference Design System)

✓ **Fixed dimensions:** 1024x768px per slide (4:3 aspect ratio for projectors)
✓ **Centered on stage:** Light gray background (#e5e5e5)
✓ **Generous padding:** 60px standard (0px for bleed layouts)
✓ **Font pairing:** Cal Sans (headers, -0.05em letter-spacing) + Plus Jakarta Sans (body)
✓ **Font sizes:** 60px (h1), 28px (h2), 18px (body), 20px (h3 grid headers)
✓ **Color scheme:** Cream bg (#f4f3f1), orange accent (#ed5e29), dark gray text (#131313)
✓ **High contrast:** Exceeds WCAG AA standards
✓ **CSS Grid/Flexbox:** For reliable, responsive layouts
✓ **Inline SVG icons:** Stylable, scalable, no external files (Lucide library)
✓ **Minimal animation:** Simple fades only
✓ **One idea per slide:** Support speaker, don't replace them
✓ **White space is king:** Breathing room reduces cognitive load
✓ **Consistency:** Same positioning across all slides
✓ **Auto-styling:** Grid headers automatically orange, no manual styling needed

---

## Font Embedding

**HTML Presentations:**
- Plus Jakarta Sans: Loaded from Google Fonts
- Cal Sans: Embedded as base64 in CSS (see `resources/css-framework.md`)

**PPTX Conversion:**
- Both fonts embedded using `tools/embed_fonts_in_pptx.py`
- Adds ~800KB to file size
- Ensures fonts display correctly on any system

---

*This Reference Design System ensures professional, accessible, and effective presentations that look like polished slide decks, not webpages.*
