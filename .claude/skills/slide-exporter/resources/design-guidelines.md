# Presentation Design Philosophy: Layouts & Fonts

When building HTML presentations, the goal is to make them look like professional, static slide decks (like Google Slides or PowerPoint), not like standard, scrolling webpages. The two most important decisions to achieve this are **1) a fixed-aspect-ratio layout** and **2) a clean, hierarchical font system**.

---

## 1. The Layout: "A Stage, Not a Page"

The single most important trick is to stop thinking like a webpage (which scrolls) and start thinking like a slide (which is a fixed-size canvas).

### Fixed Aspect Ratio

Create a main div for each slide and lock its dimensions to a 4:3 aspect ratio (standard for projectors). **Standard dimensions:**

- **Width:** 1024px
- **Height:** 768px

### Slide Centering

Place this 1024x768 "slide" onto a neutral background (like a light gray, e.g., `#e2e8f0`). Center the slide on the page. This creates the "stage" effect, just like in Google Slides' "Present" mode.

### Internal Padding

All content inside the slide is pulled away from the edges with generous, consistent padding.

**Standard Padding:** `60px` on all sides (`padding: 60px;`).

**Bleed Layouts:** For layouts with an image that "bleeds" to the edge (like Bleed_Image_Right), set the slide's `padding` to `0` and apply padding only to the text column.

### Core Layouts (The Workhorses)

Rely on **CSS Flexbox** and **CSS Grid** to organize the content within the 1024x768 container.

**Title_Slide:** Uses `display: flex;`, `justify-content: flex-start;`, and `align-items: center;` to left-align the title and subtitle.

**Image_Right_Text_Left:** Uses `display: grid;` with `grid-template-columns: 1fr 1fr;` to create two perfectly equal columns. The left column holds the text, and the right column holds the image container.

**Tiled_Text_With_Icons:** Uses `display: flex;` with `gap: 40px;`. Each "tile" inside is set to `flex: 1;` so they automatically share the space equally and have the same height.

---

## 2. The Font Styles: "Clarity and Contrast"

The typography strategy is built on **font pairing**. Almost always use two different fonts: one for headers (to grab attention) and one for body text (for maximum readability). Pull these from **Google Fonts**.

### Header Font: PT Serif

**Why:** It's an elegant, highly readable serif typeface designed for both headlines and body text. It conveys authority and academic credibility while remaining modern and clean. Excellent support for both Latin and Cyrillic scripts, including Vietnamese diacritics.

**Where used:** `h1`, `h2` (the slide-title), `h3` (tile headers).

#### Common Styles

**h1 (Title Slide):**
- Font: PT Serif
- Weight: 700 (Bold)
- Size: 70px (It should be big!)
- Color: #7373b0 (Muted blue-purple)

**slide-title (The h2 on most slides):**
- Font: PT Serif
- Weight: 400 (Regular)
- Size: 40px
- Color: #7373b0 (Muted blue-purple)
- Margin: `margin-bottom: 40px;` (to create space)

### Body Font: Roboto

**Why:** It's Google's flagship sans-serif, designed for optimal readability on screens. The mechanical skeleton with geometric forms creates a natural reading rhythm. Widely tested across devices and proven excellent for presentations. Has extensive language support including Vietnamese.

**Where used:** `p`, `li`, captions, chart labels.

#### Common Styles

**p, li:**
- Font: Roboto
- Weight: 400 (Regular)
- Size: 27px (Increased for better readability from distance)
- Line Height: 1.5 (Essential for readability in blocks of text)
- Color: #475569 (A softer dark gray/blue)

### Accent Colors

Use a simple **60-30-10 rule:**

- **60% (Dominant):** `#FFFFFF` (White) - The slide background.
- **30% (Secondary):** `#7373b0` & `#475569` - The title and text colors.
- **10% (Accent):** `#7373b0` (Muted blue-purple) - Used for titles, icons, chart bars, and quote borders. This sophisticated color creates visual cohesion without overwhelming.

---

## 3. Integrating Visuals & Complex Layouts

### Integrating Images

The choice depends on how much focus the image should have.

#### Split Screen Layout (Image_Right_Text_Left)

**How:** Use `display: grid;` with `grid-template-columns: 1fr 1fr;` on the slide.

**Why:** This is more robust than Flexbox. It guarantees a perfect 50/50 split, even if the text in one column is much shorter than the image height in the other.

**Image Sizing:** The `<img>` tag is set to `width: 100%; height: 100%;` and `object-fit: cover;`. This ensures the image fills its (50%) column perfectly without being stretched or distorted.

#### Full Bleed Layout

For a powerful, modern look (often for a Title or Section Break).

**How:** The slide div has `padding: 0;`. An `<img>` is placed inside with `width: 100%; height: 100%; object-fit: cover;`.

**Text:** A new div containing the text (h1, p) is placed on top of the image. This is done by setting the slide to `position: relative;` and the text div to `position: absolute; top: 0; left: 0; width: 100%; height: 100%;`.

**Readability:** To ensure the text is readable, the text div gets a semi-transparent dark overlay (e.g., `background-color: rgba(0, 0, 0, 0.5);`) and the text itself is set to white.

#### Simple Image

For just showing a diagram or photo.

**How:** This is the easiest. Inside the standard slide with `padding: 60px;`, add an `<img>` tag.

**Styling:** Give it a `max-width: 100%;` (so it doesn't break the layout) and often a `border-radius: 12px;` and a subtle `box-shadow` to lift it off the page.

### Integrating Icons

Icons are for quickly communicating a concept. **Never use image files for them; use inline SVGs.**

**How:** Copy the SVG code (e.g., from a library like Heroicons or Lucide) and paste it directly into the HTML.

**Why:**
- **No Files:** Keeps everything in one HTML file.
- **Scalable:** They are "vector" and look sharp at any size.
- **Stylable:** This is the most important part. Can style them with CSS.

**Styling:** Set the icon's color to the accent color (`#7373b0`) to make it pop. Often do this by setting the SVG's `stroke` or `fill` attribute to `currentColor` and then setting the text color of its container (`color: #7373b0;`).

#### Layout (Tiled_Text_With_Icons)

This layout (e.g., "3 Features") uses `display: flex; gap: 40px;`.

- Each of the three "feature" divs inside is set to `flex: 1;` (so they share space equally).
- Each div is also a flex container: `display: flex; flex-direction: column; align-items: center; text-align: center;`.
- This centers the (accent-colored) Icon on top, with the h3 (Poppins) and p (Lato) text centered below it.

### Other Common Layouts

#### Quote Slide

**How:** Usually a centered layout (flex-col, justify-center). Use a `<blockquote>` element.

**Styling:** Give the blockquote a `border-left: 4px solid #7373b0;` (using the accent color) and set the text to a larger size (e.g., 24px) and italic. The citation/author is a smaller `<p>` tag below it.

#### Data/Chart Slide

**How:** "Fake" a bar chart using simple divs.

**Layout:** Use `display: flex; align-items: flex-end; height: 300px; gap: 20px;`.

**Bars:** Each "bar" is a div with a `flex: 1;` (so they all have the same width) and the accent color (`background-color: #7373b0;`).

**Data:** The height of each bar is set with an inline style (e.g., `style="height: 60%;"`). This creates a simple, clean, and effective bar chart without any complex libraries.

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

- The Poppins/Lato pairing provides very clear, readable text.
- The font sizes (70px, 40px, 18px) are large enough to be read from a distance.
- The color-contrast (e.g., `#1e293b` text on a `#FFFFFF` background) is very high, making it easy to read for everyone.

---

## 5. A Comprehensive Guide to Common Slide Layouts

Here are **10 common and effective slide layouts** that build upon all the principles above.

### 1. The Title Slide

**Purpose:** To make a strong first impression and state the presentation's topic.

**How-To:** Use `display: flex;`, `justify-content: flex-start;`, `align-items: center;` with `text-align: left;`.

**Typography:** The h1 (Poppins, 700 weight, 70px) and a subtitle p (Lato, 400 weight, 20px).

**Pro-Tip:** This is a great place to use the Full Bleed Layout with a high-quality, relevant image and white text to create a powerful opening.

### 2. The Section Break Slide

**Purpose:** To signal a transition to a new topic, giving the audience a "chapter break."

**How-To:** Extremely simple. Use a full-slide background of the accent color (`#7373b0`).

**Typography:** Place a single, left-aligned h2 title (PT Serif, 400 weight, 50px) in white.

**Why:** The sudden flash of color clearly breaks the visual flow and re-engages the audience, telling them, "Pay attention, we're moving on."

### 3. Standard Content (Title + Bullets)

**Purpose:** The "workhorse" of the presentation. Used to deliver core information.

**How-To:** A simple vertical stack. Use the standard 60px padding.

**Typography:** The `.slide-title` (Poppins, 40px) at the top. Below it, a `<ul>` with `<li>` elements (Lato, 18px).

**Key:** Don't put more than 5-6 bullets on a slide. Keep them as short phrases, not long sentences.

### 4. Split Screen (50/50 Text & Image)

**Purpose:** To visually support a text-based idea with a powerful image, chart, or diagram.

**How-To:** Use `display: grid; grid-template-columns: 1fr 1fr;`. One column gets text, the other gets the image.

**Image:** Use `object-fit: cover;` to ensure the image fills its half without distortion.

**Variation:** Can also do a 60/40 or 40/60 split by changing the grid columns (e.g., `grid-template-columns: 2fr 3fr;`).

### 5. Three-Column / Tiled Layout

**Purpose:** To present three related but distinct points, features, or options.

**How-To:** Use `display: flex; gap: 40px;` on the content container. Each of the three child divs will have `flex: 1;`.

**Best Practice:** This is perfect for the Icon + Title + Text pattern. The icon (in the accent color) provides a quick visual cue for each point.

### 6. The "Big Number" Slide

**Purpose:** To emphasize a single, critical statistic or number in a dramatic way.

**How-To:** Use `display: flex;`, `flex-direction: column;`, `justify-content: center;`, `align-items: center;`.

**Typography:**
- A massive `<h1>` (Poppins, 700 weight, 150px - 200px) showing just the number (e.g., "85%"). Use the accent color.
- A small `<p>` (Lato, 18px) underneath it that explains what the number means (e.g., "of users reported higher satisfaction...").

**Why:** It's pure visual drama. The lack of other content forces the audience to focus on that single data point.

### 7. Comparison (This vs. That) Slide

**Purpose:** To compare two opposing ideas, products, or states (e.g., "Before" vs. "After").

**How-To:** Use `display: grid; grid-template-columns: 1fr 1fr; gap: 40px;` after the slide title.

**Styling:** Create two divs. It's effective to give each a subtle border (`border: 1px solid #e2e8f0;`) and light background (`background: #f8fafc;`) to visually separate them.

**Content:** Inside each div, use a h3 for the item name and a `<ul>` for its properties.

### 8. The Quote Slide

**Purpose:** To build authority or emotional connection using someone else's words.

**How-To:** Use a `<blockquote>` with a `border-left` in the accent color.

**Typography:** The quote text itself should be large and italic (e.g., 24px). The citation below (`<p>`) should be smaller and regular (e.g., 16px).

**Layout:** This can be centered or aligned left, but make sure it has plenty of white space.

### 9. Team / Profile Slide

**Purpose:** To introduce the people behind a project.

**How-To:** Use CSS Grid. After the slide title, create a div with `display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px;`. (Adjust column count as needed).

**Content:** Each grid item is a div containing:
- An `<img>` for the headshot (use `border-radius: 50%;` to make it a circle).
- An h3 (Poppins, 20px) for the name.
- A `<p>` (Lato, 16px) for the title or role.

### 10. The Final "Thank You" Slide

**Purpose:** To signal the end of the presentation and provide contact information.

**How-To:** Keep it simple. A centered layout is best.

**Content:**
- A large h2 (Poppins, 50px): "Thank You."
- A `<p>` (Lato, 20px): "Questions?"
- (Optional) Key contact info:
  - p (Lato, 18px): Your Name
  - p (Lato, 18px): your.email@example.com
  - p (Lato, 18px): @YourSocialHandle

---

## Summary: Core Design Rules

✓ **Fixed dimensions:** 1024x768px per slide (4:3 aspect ratio for projectors)
✓ **Centered on stage:** Light gray background (#e2e8f0)
✓ **Generous padding:** 60px standard (0px for bleed layouts)
✓ **Font pairing:** PT Serif (headers) + Roboto (body)
✓ **Font sizes:** 70px (h1), 40px (h2), 27px (body - increased 50% for readability)
✓ **Color scheme:** White bg, muted blue-purple titles (#7373b0), dark gray body (#475569)
✓ **High contrast:** WCAG AA minimum
✓ **CSS Grid/Flexbox:** For reliable, responsive layouts
✓ **Inline SVG icons:** Stylable, scalable, no external files
✓ **Minimal animation:** Simple fades only
✓ **One idea per slide:** Support speaker, don't replace them
✓ **White space is king:** Breathing room reduces cognitive load
✓ **Consistency:** Same positioning across all slides

---

*This design philosophy ensures professional, accessible, and effective presentations that look like polished slide decks, not webpages.*
