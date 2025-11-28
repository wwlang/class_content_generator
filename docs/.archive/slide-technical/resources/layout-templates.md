# Layout Templates: HTML Structures

This document provides complete HTML templates for slide layouts using the **Reference Design System**. Each template is designed for **1024x768px (4:3 aspect ratio)** slides.

**Design System:**
- **Fonts:** Cal Sans (headers) + Plus Jakarta Sans (body)
- **Colors:** Cream bg (#f4f3f1), Orange accent (#ed5e29), Dark gray text (#131313)
- **Letter-spacing:** -0.05em on Cal Sans headers
- See `design-guidelines.md` for complete design philosophy

---

## Layout 1: Title Slide

**Purpose:** Opening slide with main title and subtitle

**Structure:** Left-aligned content with large heading

```html
<div class="slide title-slide" data-slide="1">
  <div class="title-content">
    <h1>Presentation Title</h1>
    <p class="subtitle">Subtitle or Course Information</p>
    <p class="author">Instructor Name • Date</p>
  </div>
</div>
```

**CSS Requirements:**
- `.title-slide`: `display: flex; justify-content: flex-start; align-items: center; text-align: left; padding: 60px;`
- `h1`: Cal Sans 700, 70px, #ed5e29
- `.subtitle`: Plus Jakarta Sans 400, 24px, #475569, margin-top: 20px
- `.author`: Plus Jakarta Sans 400, 18px, #64748b, margin-top: 40px

**Variations:**
- **With background image:** Set slide to `position: relative; padding: 0;`, add full-bleed `<img>` with overlay, position text absolutely

---

## Layout 2: Section Break Slide

**Purpose:** Visual transition between major sections

**Structure:** Left-aligned heading on accent-colored background

```html
<div class="slide section-break-slide" data-slide="2">
  <h2 class="section-title">Section Name</h2>
</div>
```

**CSS Requirements:**
- `.section-break-slide`: `background: #ed5e29; display: flex; justify-content: flex-start; align-items: center; padding: 60px;`
- `.section-title`: Cal Sans 400, 50px, #ffffff, text-align: left

**Note:** No other content. The color change itself signals the transition.

---

## Layout 3: Standard Content (Title + Bullets)

**Purpose:** Main workhorse for delivering key points

**Structure:** Title at top, bulleted list below

```html
<div class="slide content-slide" data-slide="3">
  <h2 class="slide-title">Slide Title</h2>
  <div class="content-body">
    <ul>
      <li>First key point with brief explanation</li>
      <li>Second key point with brief explanation</li>
      <li>Third key point with brief explanation</li>
      <li>Fourth key point (optional)</li>
      <li>Fifth key point (optional - max 6 total)</li>
    </ul>
  </div>
</div>
```

**CSS Requirements:**
- `.content-slide`: `padding: 60px;`
- `.slide-title`: Cal Sans 400, 40px, #ed5e29, margin-bottom: 40px
- `ul`: List-style-position: outside, padding-left: 30px
- `li`: Plus Jakarta Sans 400, 18px, #475569, line-height: 1.5, margin-bottom: 16px

**Best Practices:**
- Keep bullets to short phrases (not full sentences)
- Maximum 6 bullets per slide
- Use sub-bullets sparingly (nested `<ul>`)

---

## Layout 4: Split Screen (50/50 Text & Image)

**Purpose:** Support text with visual evidence

**Structure:** Two equal columns using CSS Grid

```html
<div class="slide split-slide" data-slide="4">
  <h2 class="slide-title">Slide Title</h2>
  <div class="split-content">
    <div class="text-column">
      <p>Paragraph explaining the concept shown in the image.</p>
      <ul>
        <li>Supporting point one</li>
        <li>Supporting point two</li>
        <li>Supporting point three</li>
      </ul>
    </div>
    <div class="image-column">
      <img src="data:image/jpeg;base64,..." alt="Description" />
    </div>
  </div>
</div>
```

**CSS Requirements:**
- `.split-slide`: `padding: 60px;`
- `.slide-title`: Cal Sans 400, 40px, #ed5e29, margin-bottom: 30px
- `.split-content`: `display: grid; grid-template-columns: 1fr 1fr; gap: 40px; height: 550px;`
- `.text-column`: `display: flex; flex-direction: column; justify-content: center;`
- `.image-column img`: `width: 100%; height: 100%; object-fit: cover; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);`

**Variations:**
- **60/40 split:** `grid-template-columns: 3fr 2fr;`
- **Image left:** Swap column order in HTML or use `grid-template-columns: 1fr 1fr;` with order property

---

## Layout 5: Three-Column / Tiled Layout

**Purpose:** Present three related points, features, or concepts

**Structure:** Flexbox with three equal-width columns

```html
<div class="slide tiled-slide" data-slide="5">
  <h2 class="slide-title">Slide Title</h2>
  <div class="tiles-container">
    <div class="tile">
      <div class="icon-container">
        <!-- Lucide SVG icon here -->
        <svg class="lucide-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <!-- SVG paths -->
        </svg>
      </div>
      <h3>Feature One</h3>
      <p>Brief explanation of this feature or concept.</p>
    </div>

    <div class="tile">
      <div class="icon-container">
        <!-- Different icon -->
        <svg class="lucide-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <!-- SVG paths -->
        </svg>
      </div>
      <h3>Feature Two</h3>
      <p>Brief explanation of this feature or concept.</p>
    </div>

    <div class="tile">
      <div class="icon-container">
        <!-- Different icon -->
        <svg class="lucide-icon" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <!-- SVG paths -->
        </svg>
      </div>
      <h3>Feature Three</h3>
      <p>Brief explanation of this feature or concept.</p>
    </div>
  </div>
</div>
```

**CSS Requirements:**
- `.tiled-slide`: `padding: 60px;`
- `.slide-title`: Cal Sans 400, 40px, #ed5e29, margin-bottom: 40px
- `.tiles-container`: `display: flex; gap: 40px;`
- `.tile`: `flex: 1; display: flex; flex-direction: column; align-items: center; text-align: center;`
- `.icon-container`: `color: #ed5e29; margin-bottom: 20px;`
- `.tile h3`: Cal Sans 500, 22px, #ed5e29, margin-bottom: 12px
- `.tile p`: Plus Jakarta Sans 400, 16px, #475569, line-height: 1.5

**Note:** Icons should use accent color (#ed5e29) for visual pop

---

## Layout 6: The "Big Number" Slide

**Purpose:** Emphasize a single critical statistic

**Structure:** Centered huge number with explanation

```html
<div class="slide big-number-slide" data-slide="6">
  <div class="number-content">
    <h1 class="big-number">85%</h1>
    <p class="number-explanation">of users reported higher satisfaction after implementing these strategies</p>
    <p class="citation">¹ Source: Smith & Jones (2023)</p>
  </div>
</div>
```

**CSS Requirements:**
- `.big-number-slide`: `display: flex; justify-content: center; align-items: center; padding: 60px;`
- `.number-content`: `text-align: center;`
- `.big-number`: Cal Sans 700, 180px, #ed5e29 (accent color!)
- `.number-explanation`: Plus Jakarta Sans 400, 24px, #475569, margin-top: 30px, max-width: 700px
- `.citation`: Plus Jakarta Sans 400, 14px, #64748b, margin-top: 20px

**Variations:**
- Use accent color for maximum impact
- Can include small icon above number
- Keep explanation concise (1-2 lines max)

---

## Layout 7: Comparison (This vs. That) Slide

**Purpose:** Compare two opposing concepts, approaches, or states

**Structure:** Two side-by-side boxes with grid

```html
<div class="slide comparison-slide" data-slide="7">
  <h2 class="slide-title">Comparison Title</h2>
  <div class="comparison-container">
    <div class="comparison-box">
      <h3>Before / Option A</h3>
      <ul>
        <li>Characteristic one</li>
        <li>Characteristic two</li>
        <li>Characteristic three</li>
        <li>Characteristic four</li>
      </ul>
    </div>

    <div class="comparison-box">
      <h3>After / Option B</h3>
      <ul>
        <li>Characteristic one</li>
        <li>Characteristic two</li>
        <li>Characteristic three</li>
        <li>Characteristic four</li>
      </ul>
    </div>
  </div>
</div>
```

**CSS Requirements:**
- `.comparison-slide`: `padding: 60px;`
- `.slide-title`: Cal Sans 400, 40px, #ed5e29, margin-bottom: 40px
- `.comparison-container`: `display: grid; grid-template-columns: 1fr 1fr; gap: 40px;`
- `.comparison-box`: `background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 30px;`
- `.comparison-box h3`: Cal Sans 500, 24px, #ed5e29, margin-bottom: 20px, text-align: center
- `.comparison-box li`: Plus Jakarta Sans 400, 16px, #475569, margin-bottom: 12px

**Variations:**
- **Pros/Cons:** Use green/red accent borders
- **Timeline:** Add "Past" vs "Future" labels
- **Method comparison:** Two different approaches to same problem

---

## Layout 8: The Quote Slide

**Purpose:** Build authority or emotional connection

**Structure:** Centered or left-aligned blockquote with attribution

```html
<div class="slide quote-slide" data-slide="8">
  <div class="quote-content">
    <blockquote class="main-quote">
      "The most important single ingredient in the formula of success is knowing how to get along with people."
    </blockquote>
    <p class="quote-attribution">— Theodore Roosevelt</p>
    <p class="quote-context">26th President of the United States</p>
  </div>
</div>
```

**CSS Requirements:**
- `.quote-slide`: `display: flex; align-items: center; padding: 80px;`
- `.quote-content`: `max-width: 800px;`
- `.main-quote`: Plus Jakarta Sans 400 italic, 28px, #ed5e29, border-left: 4px solid #ed5e29, padding-left: 30px, margin: 0
- `.quote-attribution`: Plus Jakarta Sans 500, 20px, #475569, margin-top: 30px
- `.quote-context`: Plus Jakarta Sans 400, 16px, #64748b, margin-top: 8px

**Best Practices:**
- Keep quotes under 3 lines for readability
- Always attribute with full name and credentials
- Border-left in accent color for visual connection
- Generous padding and margins for impact

---

## Layout 9: Team / Profile Slide

**Purpose:** Introduce people, showcase team, or present profiles

**Structure:** Grid of profile cards with images

```html
<div class="slide team-slide" data-slide="9">
  <h2 class="slide-title">Our Team</h2>
  <div class="profiles-container">
    <div class="profile-card">
      <img src="data:image/jpeg;base64,..." alt="Person name" class="profile-image" />
      <h3>John Doe</h3>
      <p class="profile-role">Chief Executive Officer</p>
      <p class="profile-detail">15 years in industry leadership</p>
    </div>

    <div class="profile-card">
      <img src="data:image/jpeg;base64,..." alt="Person name" class="profile-image" />
      <h3>Jane Smith</h3>
      <p class="profile-role">Chief Technology Officer</p>
      <p class="profile-detail">Former Google engineer</p>
    </div>

    <div class="profile-card">
      <img src="data:image/jpeg;base64,..." alt="Person name" class="profile-image" />
      <h3>Alex Johnson</h3>
      <p class="profile-role">Head of Marketing</p>
      <p class="profile-detail">10+ successful campaigns</p>
    </div>
  </div>
</div>
```

**CSS Requirements:**
- `.team-slide`: `padding: 60px;`
- `.slide-title`: Cal Sans 400, 40px, #ed5e29, margin-bottom: 40px
- `.profiles-container`: `display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px;`
- `.profile-card`: `text-align: center;`
- `.profile-image`: `width: 120px; height: 120px; border-radius: 50%; object-fit: cover; margin: 0 auto 20px; border: 3px solid #e2e8f0;`
- `.profile-card h3`: Cal Sans 500, 20px, #ed5e29, margin-bottom: 8px
- `.profile-role`: Plus Jakarta Sans 500, 16px, #ed5e29 (accent color!)
- `.profile-detail`: Plus Jakarta Sans 400, 14px, #64748b, margin-top: 8px

**Variations:**
- **2 profiles:** `grid-template-columns: repeat(2, 1fr);` with larger images
- **4 profiles:** `grid-template-columns: repeat(4, 1fr);` with smaller text

---

## Layout 10: Final "Thank You" Slide

**Purpose:** Signal end and provide contact information

**Structure:** Centered thank you message with optional contact details

```html
<div class="slide thank-you-slide" data-slide="10">
  <div class="closing-content">
    <h2 class="thank-you-heading">Thank You</h2>
    <p class="closing-subtext">Questions?</p>

    <div class="contact-info">
      <p class="contact-item">Dr. Jane Smith</p>
      <p class="contact-item">jane.smith@university.edu</p>
      <p class="contact-item">Office Hours: Tuesdays 2-4 PM</p>
    </div>
  </div>
</div>
```

**CSS Requirements:**
- `.thank-you-slide`: `display: flex; justify-content: center; align-items: center; padding: 60px; background: #fafafa;`
- `.closing-content`: `text-align: center;`
- `.thank-you-heading`: Cal Sans 700, 60px, #ed5e29
- `.closing-subtext`: Plus Jakarta Sans 400, 24px, #475569, margin-top: 20px, margin-bottom: 60px
- `.contact-info`: `margin-top: 40px;`
- `.contact-item`: Plus Jakarta Sans 400, 18px, #475569, margin-bottom: 12px

**Variations:**
- **With QR code:** Add QR code image for contact/resources
- **With social media:** Include icon + handle links
- **Minimal:** Just "Thank You" and "Questions?" (no contact)

---

## Universal Slide Components

### Slide Footer (Citations)

Add to any slide that includes cited information:

```html
<div class="slide-footer">
  <p class="citation">¹ Author, A. (2023). Title of work. Journal, 15(3), 123-145.</p>
  <p class="citation">² Author, B. (2022). Title of work. Publisher.</p>
</div>
```

**CSS Requirements:**
- `.slide-footer`: `position: absolute; bottom: 20px; left: 60px; right: 60px;`
- `.citation`: Plus Jakarta Sans 400, 11px, #64748b, line-height: 1.4, margin-bottom: 4px

### Speaker Notes

Add to any slide for presenter guidance:

```html
<aside class="speaker-notes">
  <h4>Speaker Notes</h4>
  <p>This is a reminder for the presenter. These notes will appear in print view but are hidden during presentation.</p>
</aside>
```

**CSS Requirements:**
- `.speaker-notes`: `display: none; background: #f8fafc; padding: 20px; margin-top: 20px; border-left: 3px solid #ed5e29;`
- `.speaker-notes h4`: Cal Sans 500, 14px, #ed5e29, margin-bottom: 8px
- `.speaker-notes p`: Plus Jakarta Sans 400, 12px, #475569, line-height: 1.5
- `@media print { .speaker-notes { display: block; } }`

---

## Layout Selection Guidelines

**Use Layout 1 (Title)** when:
- First slide of presentation
- Opening a major standalone section

**Use Layout 2 (Section Break)** when:
- Transitioning between major topics
- Need clear visual signal of change

**Use Layout 3 (Standard Content)** when:
- Presenting list of key points
- Default for most informational content
- 3-6 related ideas to communicate

**Use Layout 4 (Split Screen)** when:
- Visual evidence supports text
- Diagram, chart, or image is essential
- 50/50 balance between text and visual

**Use Layout 5 (Tiled)** when:
- Presenting exactly 3 parallel concepts
- Features, options, or categories
- Icons enhance comprehension

**Use Layout 6 (Big Number)** when:
- Single statistic is most important message
- Data-driven impact needed
- Want dramatic emphasis

**Use Layout 7 (Comparison)** when:
- Contrasting two approaches, states, or options
- Before/after scenarios
- Pros/cons analysis

**Use Layout 8 (Quote)** when:
- Building authority through expert words
- Creating emotional connection
- Quote is from recognized source

**Use Layout 9 (Team/Profile)** when:
- Introducing people
- Showcasing credentials
- Building trust through faces

**Use Layout 10 (Thank You)** when:
- Final slide
- Ending presentation
- Providing contact information

---

## Technical Notes

**All layouts assume:**
- Base slide dimensions: `1024x768px` (4:3 ratio)
- Parent container: `.slide` class with `position: relative;`
- Slide visibility controlled by `.active` class
- Transitions handled by CSS (opacity fade)

**Responsive considerations:**
- These are fixed-dimension presentations (not responsive)
- Designed for projector display at native resolution
- Scaling handled by browser fullscreen mode
- Print view maintains aspect ratio

---

*Reference these templates when implementing automatic layout detection in the slide exporter skill.*

---

# PART 2: EDUCATIONAL-SPECIFIC LAYOUTS

## Tier 1 Layouts - Essential for Course Content

These layouts are specifically designed for educational contexts and align with the course content generator's pedagogical needs.

---

## Layout 11: Vocabulary Table (Bilingual)

**Purpose:** Support multilingual learners with key terminology

**Structure:** Three-column table with English, Vietnamese, and context

```html
<div class="slide vocab-table-slide" data-slide="N">
  <h2 class="slide-title">Key Vocabulary (Từ vựng quan trọng)</h2>
  <table class="vocab-table">
    <thead>
      <tr>
        <th>English Term</th>
        <th>Vietnamese Translation</th>
        <th>Context / Usage</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Personal mastery</strong></td>
        <td>Làm chủ bản thân</td>
        <td>The discipline of continually clarifying personal vision</td>
      </tr>
      <tr>
        <td><strong>Intrinsic motivation</strong></td>
        <td>Động lực nội tại</td>
        <td>Motivation from within; inherently satisfying</td>
      </tr>
      <tr>
        <td><strong>Autonomy</strong></td>
        <td>Quyền tự chủ</td>
        <td>The ability to direct your own life and work</td>
      </tr>
    </tbody>
  </table>
  <p class="vocab-note">Note: These terms appear throughout your professional development journey</p>
</div>
```

**CSS Requirements:**
- `.vocab-table-slide`: `padding: 60px;`
- `.vocab-table`: `width: 100%; border-collapse: collapse; margin: 30px 0;`
- `.vocab-table th`: `background: #ed5e29; color: white; padding: 16px; text-align: left; font-family: 'Cal Sans'; font-size: 24px;`
- `.vocab-table td`: `padding: 16px; border-bottom: 1px solid #e2e8f0; font-size: 22px; vertical-align: top;`
- `.vocab-table td:first-child`: `font-weight: 500; color: #ed5e29;` (English term highlighted)
- `.vocab-table tr:hover`: `background: #f8fafc;`
- `.vocab-note`: `font-size: 20px; color: #64748b; font-style: italic; margin-top: 20px;`

**Best Practices:**
- 4-6 terms per slide (not more - cognitive load)
- Vietnamese uses proper diacritics
- Context column explains WHEN to use the term
- Alternating row colors for readability

---

## Layout 12: Think-Pair-Share / Activity Instructions

**Purpose:** Structured collaborative activity with clear timing

**Structure:** Three phases with distinct visual treatment

```html
<div class="slide activity-slide" data-slide="N">
  <div class="activity-header">
    <h2 class="slide-title">Activity: Mapping Your Drive Elements</h2>
    <span class="activity-badge">Interactive</span>
  </div>
  
  <div class="activity-phases">
    <div class="phase phase-think">
      <div class="phase-header">
        <span class="phase-icon">🤔</span>
        <h3>THINK (Individual)</h3>
        <span class="phase-timing">5 minutes</span>
      </div>
      <p>On paper, draw three columns: AUTONOMY | MASTERY | PURPOSE</p>
      <ul>
        <li>Where do you have autonomy now?</li>
        <li>What are you working to master?</li>
        <li>What larger purpose drives you?</li>
      </ul>
    </div>

    <div class="phase phase-pair">
      <div class="phase-header">
        <span class="phase-icon">👥</span>
        <h3>PAIR (Dyads)</h3>
        <span class="phase-timing">3 minutes</span>
      </div>
      <p>Turn to a neighbor. Each person shares ONE insight from your reflection.</p>
    </div>

    <div class="phase phase-share">
      <div class="phase-header">
        <span class="phase-icon">💬</span>
        <h3>SHARE (Class)</h3>
        <span class="phase-timing">5 minutes</span>
      </div>
      <p>Volunteers share key discoveries with the whole class.</p>
    </div>
  </div>
  
  <div class="activity-footer">
    <p><strong>Total Time:</strong> 13 minutes | <strong>Use insights:</strong> Development Plan Section 4</p>
  </div>
</div>
```

**CSS Requirements:**
- `.activity-slide`: `padding: 50px; background: linear-gradient(to bottom, #fef3c7 0%, #ffffff 100%);` (subtle yellow gradient)
- `.activity-header`: `display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;`
- `.activity-badge`: `background: #ed5e29; color: white; padding: 8px 20px; border-radius: 20px; font-size: 18px;`
- `.activity-phases`: `display: flex; flex-direction: column; gap: 20px;`
- `.phase`: `background: white; border-left: 5px solid; padding: 20px; border-radius: 8px;`
- `.phase-think`: `border-color: #3b82f6;` (blue)
- `.phase-pair`: `border-color: #10b981;` (green)
- `.phase-share`: `border-color: #f59e0b;` (amber)
- `.phase-header`: `display: flex; align-items: center; gap: 15px; margin-bottom: 15px;`
- `.phase-icon`: `font-size: 32px;`
- `.phase h3`: `font-size: 28px; flex: 1;`
- `.phase-timing`: `background: #e2e8f0; padding: 6px 15px; border-radius: 15px; font-size: 20px; font-weight: 500;`
- `.phase ul`: `margin-left: 25px; margin-top: 10px;`
- `.phase li`: `font-size: 22px; margin-bottom: 8px;`
- `.activity-footer`: `margin-top: 25px; padding-top: 20px; border-top: 2px dashed #cbd5e1; font-size: 20px;`

**Why It Works:**
- Color-coded phases (blue→green→amber) show progression
- Large timing displays help instructor manage
- Visual hierarchy (icons, headers, content)
- Distinct from lecture slides (yellow tint)

---

## Layout 13: Rubric Preview

**Purpose:** Show students assessment criteria transparently

**Structure:** Simplified rubric table with key criteria

```html
<div class="slide rubric-slide" data-slide="N">
  <h2 class="slide-title">Assessment Connection: Development Plan Rubric</h2>
  
  <div class="rubric-intro">
    <p><strong>Due:</strong> Friday, November 28, 2025 | <strong>Weight:</strong> 40% of final grade</p>
    <p>Today's content helps you excel in these criteria:</p>
  </div>

  <table class="rubric-table">
    <thead>
      <tr>
        <th class="criterion-col">Criterion</th>
        <th class="excellent-col">Excellent (9-10)</th>
        <th class="good-col">Good (7-8)</th>
        <th class="needs-work-col">Needs Work (5-6)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="criterion-name"><strong>Integration</strong></td>
        <td>Clearly connects values, goals, and strategies; shows synthesis</td>
        <td>Links most elements with some connections</td>
        <td>Lists elements separately without integration</td>
      </tr>
      <tr>
        <td class="criterion-name"><strong>Self-Awareness</strong></td>
        <td>Deep reflection on strengths, growth areas, motivation patterns</td>
        <td>Basic reflection on key areas</td>
        <td>Surface-level or generic statements</td>
      </tr>
      <tr>
        <td class="criterion-name"><strong>Action Plan</strong></td>
        <td>Specific, measurable, realistic goals with clear timeline</td>
        <td>Goals stated but lacking some specificity</td>
        <td>Vague or unrealistic goals</td>
      </tr>
    </tbody>
  </table>

  <div class="rubric-footer">
    <p>📋 <strong>See complete rubric:</strong> Assessment Handbook Section 3 | <strong>Use today:</strong> Personal mastery framework helps integration criterion</p>
  </div>
</div>
```

**CSS Requirements:**
- `.rubric-slide`: `padding: 50px;`
- `.rubric-intro`: `background: #eff6ff; border-left: 4px solid #3b82f6; padding: 20px; margin-bottom: 30px; border-radius: 8px;`
- `.rubric-intro p`: `font-size: 22px; margin-bottom: 10px;`
- `.rubric-table`: `width: 100%; border-collapse: collapse; margin: 20px 0;`
- `.rubric-table th`: `padding: 14px; text-align: left; font-size: 20px; font-family: 'Cal Sans';`
- `.criterion-col`: `background: #ed5e29; color: white; width: 20%;`
- `.excellent-col`: `background: #10b981; color: white; width: 27%;`
- `.good-col`: `background: #f59e0b; color: white; width: 27%;`
- `.needs-work-col`: `background: #ef4444; color: white; width: 26%;`
- `.rubric-table td`: `padding: 14px; border: 1px solid #e2e8f0; font-size: 19px; vertical-align: top;`
- `.criterion-name`: `background: #f8fafc; font-weight: 500; color: #ed5e29;`
- `.rubric-footer`: `background: #fef3c7; padding: 18px; border-radius: 8px; margin-top: 20px; font-size: 20px;`

**Why It Works:**
- Color-coded performance levels (green=excellent, yellow=good, red=needs work)
- Students see EXACTLY what they're working toward
- Connects today's learning to assessment (integration criterion)
- Simplified version (3 criteria vs. full rubric's 8)
- Cross-references full rubric location

---

## Layout 14: Concept Map / Mind Map

**Purpose:** Show relationships between interconnected ideas

**Structure:** Central concept with branching connections

```html
<div class="slide concept-map-slide" data-slide="N">
  <h2 class="slide-title">Personal Mastery Framework - Interconnections</h2>
  
  <div class="concept-map">
    <!-- Central node -->
    <div class="concept-node concept-central">
      <h3>Personal Mastery</h3>
      <p>Lifelong discipline</p>
    </div>

    <!-- Connected nodes -->
    <div class="concept-node concept-top-left">
      <h4>Personal Vision</h4>
      <p>Who you want to become</p>
    </div>

    <div class="concept-node concept-top-right">
      <h4>Creative Tension</h4>
      <p>Gap as fuel for growth</p>
    </div>

    <div class="concept-node concept-bottom-left">
      <h4>Current Reality</h4>
      <p>Honest assessment</p>
    </div>

    <div class="concept-node concept-bottom-right">
      <h4>Continuous Learning</h4>
      <p>Never "finished"</p>
    </div>

    <!-- Connection lines (via CSS or SVG) -->
    <svg class="connection-lines" width="100%" height="100%">
      <line x1="50%" y1="50%" x2="25%" y2="30%" stroke="#ed5e29" stroke-width="3"/>
      <line x1="50%" y1="50%" x2="75%" y2="30%" stroke="#ed5e29" stroke-width="3"/>
      <line x1="50%" y1="50%" x2="25%" y2="70%" stroke="#ed5e29" stroke-width="3"/>
      <line x1="50%" y1="50%" x2="75%" y2="70%" stroke="#ed5e29" stroke-width="3"/>
    </svg>
  </div>

  <p class="concept-note">All elements work together - you can't have personal mastery without all four components</p>
</div>
```

**CSS Requirements:**
- `.concept-map-slide`: `padding: 60px;`
- `.concept-map`: `position: relative; height: 500px; margin: 30px 0;`
- `.concept-node`: `position: absolute; background: white; border: 3px solid #ed5e29; border-radius: 15px; padding: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);`
- `.concept-central`: `left: 50%; top: 50%; transform: translate(-50%, -50%); background: #ed5e29; color: white; width: 220px; z-index: 10;`
- `.concept-central h3`: `font-size: 28px; margin-bottom: 8px;`
- `.concept-central p`: `font-size: 20px; color: #e0e0e0;`
- `.concept-top-left`: `left: 10%; top: 15%; width: 180px;`
- `.concept-top-right`: `right: 10%; top: 15%; width: 180px;`
- `.concept-bottom-left`: `left: 10%; bottom: 15%; width: 180px;`
- `.concept-bottom-right`: `right: 10%; bottom: 15%; width: 180px;`
- `.concept-node h4`: `font-size: 24px; margin-bottom: 6px; color: #ed5e29;`
- `.concept-node p`: `font-size: 19px; color: #475569;`
- `.connection-lines`: `position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 1; pointer-events: none;`
- `.concept-note`: `font-size: 22px; color: #64748b; font-style: italic; text-align: center;`

**Why It Works:**
- Visual learners see structure at a glance
- Central concept emphasized (larger, colored)
- Lines show relationships explicitly
- Non-hierarchical (unlike flowcharts) - shows network
- Alternative: Use radial or tree structure based on content

---

## Layout 15: Worked Example

**Purpose:** Demonstrate problem-solving step-by-step

**Structure:** Problem → Solution steps → Answer

```html
<div class="slide worked-example-slide" data-slide="N">
  <h2 class="slide-title">Worked Example: Writing a SMART Goal</h2>
  
  <div class="problem-box">
    <h3>Problem:</h3>
    <p>Transform this vague goal into a SMART goal: "I want to get better at public speaking."</p>
  </div>

  <div class="solution-steps">
    <div class="step">
      <div class="step-number">1</div>
      <div class="step-content">
        <h4>Make it Specific</h4>
        <p>What exactly? → "Deliver confident presentations to groups of 20+ people"</p>
      </div>
    </div>

    <div class="step">
      <div class="step-number">2</div>
      <div class="step-content">
        <h4>Make it Measurable</h4>
        <p>How to track? → "Give 5 presentations and receive peer feedback scores of 4/5+"</p>
      </div>
    </div>

    <div class="step">
      <div class="step-number">3</div>
      <div class="step-content">
        <h4>Add Timeline</h4>
        <p>When? → "By end of semester (December 2025)"</p>
      </div>
    </div>
  </div>

  <div class="answer-box">
    <h3>✓ SMART Goal:</h3>
    <p>"By December 2025, I will deliver 5 confident presentations to audiences of 20+ people, achieving peer feedback scores of 4/5 or higher by practicing weekly and incorporating mentor feedback."</p>
  </div>
</div>
```

**CSS Requirements:**
- `.worked-example-slide`: `padding: 50px;`
- `.problem-box`: `background: #fef3c7; border-left: 5px solid #f59e0b; padding: 20px; margin-bottom: 25px; border-radius: 8px;`
- `.problem-box h3`: `font-size: 26px; color: #f59e0b; margin-bottom: 10px;`
- `.problem-box p`: `font-size: 23px; color: #78350f;`
- `.solution-steps`: `margin: 25px 0;`
- `.step`: `display: flex; gap: 20px; margin-bottom: 20px; align-items: flex-start;`
- `.step-number`: `background: #ed5e29; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 28px; font-weight: 700; flex-shrink: 0;`
- `.step-content h4`: `font-size: 24px; color: #ed5e29; margin-bottom: 8px;`
- `.step-content p`: `font-size: 21px; color: #475569;`
- `.answer-box`: `background: #dcfce7; border-left: 5px solid #10b981; padding: 20px; border-radius: 8px; margin-top: 25px;`
- `.answer-box h3`: `font-size: 26px; color: #10b981; margin-bottom: 10px;`
- `.answer-box p`: `font-size: 22px; color: #14532d; line-height: 1.5;`

**Why It Works:**
- Clear progression: Problem → Steps → Answer
- Numbered steps show sequence
- Color coding: Problem (yellow), Steps (purple), Answer (green)
- Students can replicate process for their own work
- Models metacognitive thinking ("here's HOW I solve this")

---

## Implementation in SKILL.md

Add these detection patterns to automatic layout detection:

```
IF (slide contains <table> with "English" and "Vietnamese" headers):
  → USE Layout 11: Vocabulary Table

IF (slide_title contains "Activity" OR "Think-Pair-Share" OR has .activity-phases):
  → USE Layout 12: Activity Instructions

IF (slide contains "rubric" OR "assessment criteria" OR rubric-table):
  → USE Layout 13: Rubric Preview

IF (slide has concept-map class OR central concept with branches):
  → USE Layout 14: Concept Map

IF (slide has problem-box AND solution-steps AND answer-box):
  → USE Layout 15: Worked Example
```

---

*These educational layouts integrate with the existing 10 general layouts to provide comprehensive coverage of pedagogical needs.*

---

## Tier 2 Educational Layouts (Intermediate Complexity)

These layouts build on Tier 1 foundations with more sophisticated pedagogical patterns for process visualization, case analysis, and structured discussion.

---

### Layout 16: Timeline / Process Flow

**Purpose:** Show chronological development, sequential processes, or historical progression

**When to use:**
- Historical development of theories/concepts
- Step-by-step project timelines
- Evolution of business practices
- Multi-stage processes with clear sequence

**Visual structure:** Horizontal timeline with nodes and connecting lines

**HTML Template:**

```html
<div class="slide timeline-slide" data-slide="N">
  <h2 class="slide-title">Evolution of Leadership Theory (1900-2025)</h2>
  
  <div class="timeline-container">
    <div class="timeline-line"></div>
    
    <div class="timeline-item">
      <div class="timeline-marker"></div>
      <div class="timeline-content">
        <h3 class="timeline-year">1900s</h3>
        <h4 class="timeline-title">Great Man Theory</h4>
        <p>Leaders are born, not made</p>
      </div>
    </div>
    
    <div class="timeline-item">
      <div class="timeline-marker"></div>
      <div class="timeline-content">
        <h3 class="timeline-year">1940s</h3>
        <h4 class="timeline-title">Trait Theory</h4>
        <p>Identifying key leader characteristics</p>
      </div>
    </div>
    
    <div class="timeline-item">
      <div class="timeline-marker"></div>
      <div class="timeline-content">
        <h3 class="timeline-year">1960s</h3>
        <h4 class="timeline-title">Behavioral Theory</h4>
        <p>Focus on leader actions</p>
      </div>
    </div>
    
    <div class="timeline-item">
      <div class="timeline-marker"></div>
      <div class="timeline-content">
        <h3 class="timeline-year">1970s</h3>
        <h4 class="timeline-title">Contingency Theory</h4>
        <p>Situational effectiveness</p>
      </div>
    </div>
    
    <div class="timeline-item">
      <div class="timeline-marker active"></div>
      <div class="timeline-content">
        <h3 class="timeline-year">2000s+</h3>
        <h4 class="timeline-title">Transformational</h4>
        <p>Inspiring change and vision</p>
      </div>
    </div>
  </div>
  
  <div class="slide-footer">
    <p class="citation">Adapted from Northouse (2021), <em>Leadership: Theory and Practice</em></p>
  </div>
</div>
```

**CSS Requirements:**

```css
.timeline-container {
  position: relative;
  padding: 60px 0;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 40px;
}

.timeline-line {
  position: absolute;
  top: 90px;
  left: 5%;
  right: 5%;
  height: 4px;
  background: linear-gradient(90deg, #c7d2fe 0%, #ed5e29 100%);
  z-index: 0;
}

.timeline-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  z-index: 1;
}

.timeline-marker {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: #ed5e29;
  border: 4px solid white;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  margin-bottom: 24px;
}

.timeline-marker.active {
  width: 32px;
  height: 32px;
  background: #ef4444;
  animation: pulse 2s ease-in-out infinite;
}

.timeline-content {
  text-align: center;
}

.timeline-year {
  font-family: 'Cal Sans';
  font-size: 30px;
  font-weight: 700;
  color: #ed5e29;
  margin-bottom: 12px;
}

.timeline-title {
  font-family: 'Cal Sans';
  font-size: 26px;
  font-weight: 400;
  color: #475569;
  margin-bottom: 8px;
}

.timeline-content p {
  font-size: 22px;
  color: #64748b;
  line-height: 1.4;
}
```

**Implementation Notes:**
- Maximum 5-6 timeline items for readability
- Use `.active` marker for current/most important point
- Vertical timeline variant for more items (see CSS variations)
- Consider adding icons to timeline markers for visual anchors

---

### Layout 17: Case Study Layout

**Purpose:** Present structured business/organizational cases for analysis and discussion

**When to use:**
- Real-world business examples
- Problem-based learning scenarios
- Application of theoretical concepts
- Critical thinking exercises

**Visual structure:** Structured sections with clear information hierarchy

**HTML Template:**

```html
<div class="slide case-study-slide" data-slide="N">
  <h2 class="slide-title">Case Study: Netflix's Cultural Transformation</h2>
  
  <div class="case-content">
    <div class="case-section background">
      <div class="case-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
          <line x1="3" y1="9" x2="21" y2="9"/>
        </svg>
      </div>
      <div class="case-text">
        <h3>Background</h3>
        <p>From DVD rental to streaming giant (1997-2024). Shifted to subscription model in 2007, now 230M+ subscribers globally.</p>
      </div>
    </div>
    
    <div class="case-section challenge">
      <div class="case-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"/>
          <line x1="12" y1="8" x2="12" y2="12"/>
          <line x1="12" y1="16" x2="12.01" y2="16"/>
        </svg>
      </div>
      <div class="case-text">
        <h3>Challenge</h3>
        <p>How to maintain innovation culture during rapid scaling? Risk of bureaucracy and slower decision-making as company grew.</p>
      </div>
    </div>
    
    <div class="case-section solution">
      <div class="case-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
        </svg>
      </div>
      <div class="case-text">
        <h3>Solution</h3>
        <p>Published "Netflix Culture Memo" (2009). Core principles: Freedom & Responsibility, Context not Control, Talent Density.</p>
      </div>
    </div>
    
    <div class="case-section result">
      <div class="case-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
        </svg>
      </div>
      <div class="case-text">
        <h3>Results</h3>
        <p>Industry-leading innovation rate. Employee satisfaction 85%+. Case study taught at HBS, Stanford GSB. "Culture deck" viewed 20M+ times.</p>
      </div>
    </div>
  </div>
  
  <div class="case-question">
    <strong>Discussion:</strong> How can your organization apply Netflix's culture principles?
  </div>
</div>
```

**CSS Requirements:**

```css
.case-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
  margin-bottom: 30px;
}

.case-section {
  display: flex;
  gap: 24px;
  align-items: flex-start;
  background: #f8fafc;
  padding: 24px;
  border-radius: 12px;
  border-left: 4px solid #ed5e29;
}

.case-section.challenge {
  border-left-color: #f59e0b;
}

.case-section.solution {
  border-left-color: #10b981;
}

.case-section.result {
  border-left-color: #ed5e29;
}

.case-icon {
  flex-shrink: 0;
  color: #ed5e29;
}

.case-section.challenge .case-icon {
  color: #f59e0b;
}

.case-section.solution .case-icon {
  color: #10b981;
}

.case-text h3 {
  font-family: 'Cal Sans';
  font-size: 30px;
  color: #475569;
  margin-bottom: 12px;
}

.case-text p {
  font-size: 24px;
  color: #475569;
  line-height: 1.5;
}

.case-question {
  background: #ed5e29;
  color: white;
  padding: 24px;
  border-radius: 12px;
  font-size: 26px;
  text-align: center;
}

.case-question strong {
  font-weight: 700;
}
```

**Implementation Notes:**
- Adapt 4-section structure: Background → Challenge → Solution → Results
- Use color coding for different sections (maintain accessibility)
- Always include discussion/analysis prompt at end
- Citations essential for real cases

---

### Layout 18: Learning Objectives Preview

**Purpose:** Set clear expectations for what students will learn in the session

**When to use:**
- Beginning of new topic/week
- Introducing complex multi-part concepts
- Setting assessment preparation context
- Aligning lecture to syllabus outcomes

**Visual structure:** Checklist-style objectives with Bloom's Taxonomy indicators

**HTML Template:**

```html
<div class="slide objectives-slide" data-slide="N">
  <h2 class="slide-title">Week 7 Learning Objectives</h2>
  
  <p class="objectives-intro">By the end of this session, you will be able to:</p>
  
  <div class="objectives-list">
    <div class="objective-item" data-level="understand">
      <div class="objective-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
          <circle cx="12" cy="12" r="3"/>
        </svg>
      </div>
      <div class="objective-content">
        <span class="bloom-level">Understand</span>
        <p><strong>Explain</strong> the three core principles of Cialdini's influence model</p>
      </div>
      <div class="objective-check">☐</div>
    </div>
    
    <div class="objective-item" data-level="apply">
      <div class="objective-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
        </svg>
      </div>
      <div class="objective-content">
        <span class="bloom-level">Apply</span>
        <p><strong>Apply</strong> persuasion techniques to draft business communication scenarios</p>
      </div>
      <div class="objective-check">☐</div>
    </div>
    
    <div class="objective-item" data-level="analyze">
      <div class="objective-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>
        </svg>
      </div>
      <div class="objective-content">
        <span class="bloom-level">Analyze</span>
        <p><strong>Analyze</strong> real-world examples to identify ethical vs. manipulative persuasion</p>
      </div>
      <div class="objective-check">☐</div>
    </div>
    
    <div class="objective-item" data-level="create">
      <div class="objective-icon">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 20h9"/>
          <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>
        </svg>
      </div>
      <div class="objective-content">
        <span class="bloom-level">Create</span>
        <p><strong>Design</strong> a persuasive pitch incorporating multiple influence principles</p>
      </div>
      <div class="objective-check">☐</div>
    </div>
  </div>
  
  <div class="assessment-link">
    <p>🎯 These objectives align with <strong>Assessment 2: Persuasive Presentation</strong> (Week 9)</p>
  </div>
</div>
```

**CSS Requirements:**

```css
.objectives-intro {
  font-size: 30px;
  color: #475569;
  margin-bottom: 30px;
  font-weight: 500;
}

.objectives-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

.objective-item {
  display: flex;
  gap: 20px;
  align-items: center;
  background: white;
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.objective-item:hover {
  border-color: #ed5e29;
  box-shadow: 0 4px 12px rgba(115, 115, 176, 0.15);
}

.objective-icon {
  flex-shrink: 0;
  color: #ed5e29;
}

.objective-item[data-level="understand"] .objective-icon { color: #3b82f6; }
.objective-item[data-level="apply"] .objective-icon { color: #10b981; }
.objective-item[data-level="analyze"] .objective-icon { color: #f59e0b; }
.objective-item[data-level="create"] .objective-icon { color: #8b5cf6; }

.objective-content {
  flex: 1;
}

.bloom-level {
  display: inline-block;
  font-size: 20px;
  font-weight: 700;
  color: #ed5e29;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 8px;
}

.objective-item[data-level="understand"] .bloom-level { color: #3b82f6; }
.objective-item[data-level="apply"] .bloom-level { color: #10b981; }
.objective-item[data-level="analyze"] .bloom-level { color: #f59e0b; }
.objective-item[data-level="create"] .bloom-level { color: #8b5cf6; }

.objective-content p {
  font-size: 24px;
  color: #475569;
  line-height: 1.5;
}

.objective-check {
  font-size: 48px;
  color: #cbd5e1;
  flex-shrink: 0;
}

.assessment-link {
  background: #ed5e29;
  color: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}

.assessment-link p {
  font-size: 26px;
  margin: 0;
}
```

**Implementation Notes:**
- Use Bloom's Taxonomy verbs (Understand, Apply, Analyze, Evaluate, Create)
- Color code by cognitive level for visual distinction
- Include assessment alignment explicitly
- 3-5 objectives maximum (more = overwhelming)
- Action verbs should be measurable/observable

---

### Layout 19: Discussion Prompt / Debate Setup

**Purpose:** Frame structured discussion or debate activities with clear guidelines

**When to use:**
- Controversial or multi-perspective topics
- Preparing for group discussions
- Critical thinking exercises
- Introducing case debate activities

**Visual structure:** Central question with supporting prompts and structure

**HTML Template:**

```html
<div class="slide discussion-slide" data-slide="N">
  <h2 class="slide-title">Discussion: Ethics of Workplace Surveillance</h2>
  
  <div class="central-question">
    <div class="question-icon">
      <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
      </svg>
    </div>
    <p class="main-question">Should companies use AI-powered tools to monitor employee productivity during remote work?</p>
  </div>
  
  <div class="debate-sides">
    <div class="side position-for">
      <h3>Arguments FOR</h3>
      <ul>
        <li>Maintains accountability</li>
        <li>Identifies productivity patterns</li>
        <li>Protects company resources</li>
        <li>Data-driven management</li>
      </ul>
    </div>
    
    <div class="side position-against">
      <h3>Arguments AGAINST</h3>
      <ul>
        <li>Violates employee privacy</li>
        <li>Reduces trust and morale</li>
        <li>Stressful surveillance culture</li>
        <li>Focuses on time, not outcomes</li>
      </ul>
    </div>
  </div>
  
  <div class="discussion-format">
    <h4>Format:</h4>
    <div class="format-steps">
      <span class="step">1. Think (2 min)</span>
      <span class="arrow">→</span>
      <span class="step">2. Pair discuss (5 min)</span>
      <span class="arrow">→</span>
      <span class="step">3. Class debate (10 min)</span>
    </div>
  </div>
</div>
```

**CSS Requirements:**

```css
.central-question {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  background: linear-gradient(135deg, #ed5e29 0%, #8b87c7 100%);
  color: white;
  padding: 40px;
  border-radius: 16px;
  margin-bottom: 30px;
  box-shadow: 0 8px 20px rgba(115, 115, 176, 0.25);
}

.question-icon {
  color: white;
  opacity: 0.9;
}

.main-question {
  font-family: 'Cal Sans';
  font-size: 34px;
  font-weight: 700;
  text-align: center;
  line-height: 1.4;
  margin: 0;
}

.debate-sides {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 30px;
}

.side {
  background: #f8fafc;
  padding: 24px;
  border-radius: 12px;
}

.side.position-for {
  border-left: 6px solid #10b981;
}

.side.position-against {
  border-left: 6px solid #ef4444;
}

.side h3 {
  font-family: 'Cal Sans';
  font-size: 28px;
  color: #475569;
  margin-bottom: 16px;
  text-align: center;
}

.side ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.side li {
  font-size: 24px;
  color: #475569;
  padding: 10px 0;
  padding-left: 32px;
  position: relative;
}

.side.position-for li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #10b981;
  font-weight: 700;
  font-size: 28px;
}

.side.position-against li::before {
  content: "✗";
  position: absolute;
  left: 0;
  color: #ef4444;
  font-weight: 700;
  font-size: 28px;
}

.discussion-format {
  background: #475569;
  color: white;
  padding: 24px;
  border-radius: 12px;
}

.discussion-format h4 {
  font-family: 'Cal Sans';
  font-size: 26px;
  margin-bottom: 16px;
  text-align: center;
}

.format-steps {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.step {
  background: rgba(255,255,255,0.1);
  padding: 12px 24px;
  border-radius: 8px;
  font-size: 22px;
  font-weight: 500;
}

.arrow {
  font-size: 32px;
  font-weight: 700;
}
```

**Implementation Notes:**
- Central question must be genuinely debatable (no clear "right" answer)
- Present balanced arguments for both sides
- Provide clear time structure for discussion
- Consider adding "Guiding Questions" section for deeper exploration
- Link to relevant theories/frameworks when applicable

---

### Layout 20: Resource List / Further Reading

**Purpose:** Provide curated additional learning resources for self-directed study

**When to use:**
- End of major topic sections
- Supporting advanced learners
- Providing research context
- Exam/assessment preparation guides

**Visual structure:** Categorized resource cards with access information

**HTML Template:**

```html
<div class="slide resources-slide" data-slide="N">
  <h2 class="slide-title">Further Resources: Organizational Culture</h2>
  
  <div class="resources-grid">
    <div class="resource-card essential">
      <div class="resource-header">
        <div class="resource-icon">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>
          </svg>
        </div>
        <span class="resource-badge">Essential</span>
      </div>
      <h3>Schein's Organizational Culture Model</h3>
      <p class="resource-description">Seminal framework for understanding culture's three levels: artifacts, values, and assumptions.</p>
      <div class="resource-meta">
        <span class="meta-type">📄 Article</span>
        <span class="meta-length">25 min read</span>
      </div>
      <a href="#" class="resource-link">Read on course portal →</a>
    </div>
    
    <div class="resource-card recommended">
      <div class="resource-header">
        <div class="resource-icon">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
        </div>
        <span class="resource-badge">Recommended</span>
      </div>
      <h3>Netflix Culture Deck</h3>
      <p class="resource-description">Real-world application of culture principles. One of most-viewed corporate culture documents (20M+ views).</p>
      <div class="resource-meta">
        <span class="meta-type">📊 Presentation</span>
        <span class="meta-length">127 slides</span>
      </div>
      <a href="#" class="resource-link">View on SlideShare →</a>
    </div>
    
    <div class="resource-card optional">
      <div class="resource-header">
        <div class="resource-icon">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <polygon points="10 8 16 12 10 16 10 8"/>
          </svg>
        </div>
        <span class="resource-badge">Optional</span>
      </div>
      <h3>TED Talk: Building Company Culture</h3>
      <p class="resource-description">Brian Chesky (Airbnb CEO) on intentional culture design during scaling. Engaging, accessible introduction.</p>
      <div class="resource-meta">
        <span class="meta-type">🎥 Video</span>
        <span class="meta-length">18 min</span>
      </div>
      <a href="#" class="resource-link">Watch on TED →</a>
    </div>
    
    <div class="resource-card practice">
      <div class="resource-header">
        <div class="resource-icon">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
            <polyline points="14 2 14 8 20 8"/>
            <line x1="16" y1="13" x2="8" y2="13"/>
            <line x1="16" y1="17" x2="8" y2="17"/>
            <polyline points="10 9 9 9 8 9"/>
          </svg>
        </div>
        <span class="resource-badge">Practice</span>
      </div>
      <h3>Culture Assessment Tool</h3>
      <p class="resource-description">Self-assessment quiz to analyze your organization's culture using Schein's framework. Prepares for Assessment 3.</p>
      <div class="resource-meta">
        <span class="meta-type">🔧 Interactive</span>
        <span class="meta-length">15 min activity</span>
      </div>
      <a href="#" class="resource-link">Start assessment →</a>
    </div>
  </div>
</div>
```

**CSS Requirements:**

```css
.resources-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.resource-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.resource-card:hover {
  border-color: #ed5e29;
  box-shadow: 0 8px 20px rgba(0,0,0,0.12);
  transform: translateY(-4px);
}

.resource-card.essential {
  border-color: #ed5e29;
  border-width: 3px;
}

.resource-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.resource-icon {
  color: #ed5e29;
}

.resource-badge {
  font-size: 18px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 6px 12px;
  border-radius: 6px;
  background: #f1f5f9;
  color: #475569;
}

.resource-card.essential .resource-badge {
  background: #ed5e29;
  color: white;
}

.resource-card.recommended .resource-badge {
  background: #10b981;
  color: white;
}

.resource-card.optional .resource-badge {
  background: #64748b;
  color: white;
}

.resource-card.practice .resource-badge {
  background: #f59e0b;
  color: white;
}

.resource-card h3 {
  font-family: 'Cal Sans';
  font-size: 26px;
  color: #475569;
  margin-bottom: 12px;
  line-height: 1.3;
}

.resource-description {
  font-size: 22px;
  color: #64748b;
  line-height: 1.5;
  margin-bottom: 16px;
  flex-grow: 1;
}

.resource-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.meta-type,
.meta-length {
  font-size: 20px;
  color: #94a3b8;
}

.resource-link {
  font-size: 22px;
  color: #ed5e29;
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s ease;
}

.resource-link:hover {
  color: #5a5a8f;
  text-decoration: underline;
}
```

**Implementation Notes:**
- Categorize: Essential (required), Recommended (strongly suggested), Optional (enrichment), Practice (skills development)
- Include time estimates (respect students' time)
- Specify format (article/video/interactive/etc.)
- Provide direct access links
- Maximum 6-8 resources (avoid overwhelming)
- Align with assessment preparation when relevant


---

## Tier 3 Educational Layouts (Advanced/Specialized)

These layouts address sophisticated pedagogical needs: research presentation, framework application, metacognition, collaborative learning, and assessment preparation.

---

### Layout 21: Research Findings / Study Results

**Purpose:** Present empirical research findings with proper methodology and statistical context

**When to use:**
- Introducing research studies that support theory
- Presenting original research or case study data
- Teaching research literacy
- Evidence-based decision making contexts

**Visual structure:** Structured research presentation with methodology, findings, and implications

**HTML Template:**

```html
<div class="slide research-slide" data-slide="N">
  <h2 class="slide-title">Research Study: Remote Work Productivity</h2>
  
  <div class="research-layout">
    <div class="research-metadata">
      <div class="meta-item">
        <strong>Researchers:</strong> Bloom et al. (2023)
      </div>
      <div class="meta-item">
        <strong>Journal:</strong> <em>Nature Human Behaviour</em>
      </div>
      <div class="meta-item">
        <strong>Sample:</strong> N=1,612 employees (tech industry)
      </div>
      <div class="meta-item">
        <strong>Method:</strong> Randomized controlled trial (9 months)
      </div>
    </div>
    
    <div class="research-findings">
      <h3>Key Findings</h3>
      
      <div class="finding-item primary">
        <div class="finding-stat">+5%</div>
        <div class="finding-desc">
          <p><strong>Productivity increase</strong> in hybrid work group vs. full-time office</p>
          <span class="stat-note">p < 0.01, statistically significant</span>
        </div>
      </div>
      
      <div class="finding-item secondary">
        <div class="finding-stat">+8%</div>
        <div class="finding-desc">
          <p><strong>Promotion rate</strong> for office workers vs. remote workers</p>
          <span class="stat-note">Suggests "proximity bias" in performance evaluation</span>
        </div>
      </div>
      
      <div class="finding-item secondary">
        <div class="finding-stat">-15%</div>
        <div class="finding-desc">
          <p><strong>Voluntary turnover</strong> in hybrid work group</p>
          <span class="stat-note">Employee satisfaction and retention improved</span>
        </div>
      </div>
    </div>
    
    <div class="research-implications">
      <h4>Implications for Practice</h4>
      <ul>
        <li>Hybrid models can improve both productivity and retention</li>
        <li>Organizations must address "proximity bias" in performance reviews</li>
        <li>Face-to-face time still matters for career advancement</li>
      </ul>
    </div>
  </div>
  
  <div class="slide-footer">
    <p class="citation">Bloom, N., Han, R., & Liang, J. (2023). How hybrid working from home works out. <em>Nature Human Behaviour</em>, 7, 1–11. https://doi.org/10.1038/s41562-023-01662-z</p>
  </div>
</div>
```

**CSS Requirements:**

```css
.research-layout {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.research-metadata {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  background: #f8fafc;
  padding: 20px;
  border-radius: 12px;
  border-left: 4px solid #ed5e29;
}

.meta-item {
  font-size: 22px;
  color: #475569;
}

.meta-item strong {
  color: #1e293b;
  font-weight: 600;
}

.research-findings h3 {
  font-family: 'Cal Sans';
  font-size: 32px;
  color: #ed5e29;
  margin-bottom: 20px;
}

.finding-item {
  display: flex;
  gap: 24px;
  align-items: center;
  background: white;
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  margin-bottom: 16px;
}

.finding-item.primary {
  border-color: #ed5e29;
  border-width: 3px;
}

.finding-stat {
  font-family: 'Cal Sans';
  font-size: 72px;
  font-weight: 700;
  color: #ed5e29;
  flex-shrink: 0;
  min-width: 160px;
  text-align: center;
}

.finding-item.secondary .finding-stat {
  font-size: 60px;
  color: #64748b;
}

.finding-desc {
  flex: 1;
}

.finding-desc p {
  font-size: 26px;
  color: #475569;
  margin-bottom: 8px;
  line-height: 1.4;
}

.stat-note {
  font-size: 20px;
  color: #64748b;
  font-style: italic;
}

.research-implications {
  background: #ed5e29;
  color: white;
  padding: 24px;
  border-radius: 12px;
}

.research-implications h4 {
  font-family: 'Cal Sans';
  font-size: 28px;
  margin-bottom: 16px;
}

.research-implications ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.research-implications li {
  font-size: 24px;
  padding: 8px 0;
  padding-left: 32px;
  position: relative;
  line-height: 1.5;
}

.research-implications li::before {
  content: "→";
  position: absolute;
  left: 0;
  font-weight: 700;
  font-size: 28px;
}
```

**Implementation Notes:**
- Always include complete citation (APA 7th format)
- Specify sample size and methodology (research literacy)
- Indicate statistical significance when relevant
- Distinguish primary findings from secondary observations
- Connect findings to practical implications
- Use proper notation (N=, p <, etc.)

---

### Layout 22: Framework Application Matrix

**Purpose:** Show how theoretical framework applies across multiple real-world scenarios/cases

**When to use:**
- After introducing theoretical framework
- Demonstrating framework versatility
- Comparing multiple cases using same analytical lens
- Preparing students for assessment application

**Visual structure:** Matrix/table with framework dimensions vs. case examples

**HTML Template:**

```html
<div class="slide framework-matrix-slide" data-slide="N">
  <h2 class="slide-title">Applying Kotter's 8-Step Change Model</h2>
  
  <p class="matrix-intro">How three organizations applied the same framework with different results:</p>
  
  <table class="framework-matrix">
    <thead>
      <tr>
        <th class="framework-column">Kotter's Step</th>
        <th class="case-column">Case A: Microsoft (2014)<br><span class="case-result success">✓ Success</span></th>
        <th class="case-column">Case B: Nokia (2011)<br><span class="case-result failure">✗ Failed</span></th>
        <th class="case-column">Case C: IBM (2002)<br><span class="case-result mixed">~ Mixed</span></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td class="framework-label">1. Create Urgency</td>
        <td class="case-cell">New CEO communicated "mobile-first" crisis clearly</td>
        <td class="case-cell">Leadership in denial about iPhone threat</td>
        <td class="case-cell">Clear urgency around mainframe decline</td>
      </tr>
      <tr>
        <td class="framework-label">2. Build Coalition</td>
        <td class="case-cell">Cross-functional "One Microsoft" team</td>
        <td class="case-cell">Siloed divisions competing, not collaborating</td>
        <td class="case-cell">Strong executive alignment, weak middle management buy-in</td>
      </tr>
      <tr>
        <td class="framework-label">3. Form Vision</td>
        <td class="case-cell">"Empower every person" - clear, aspirational</td>
        <td class="case-cell">Multiple conflicting visions (MeeGo, Windows Phone)</td>
        <td class="case-cell">"On Demand" services vision well-articulated</td>
      </tr>
      <tr>
        <td class="framework-label">4. Communicate</td>
        <td class="case-cell">Nadella's constant reinforcement (emails, town halls)</td>
        <td class="case-cell">Minimal communication, top-down only</td>
        <td class="case-cell">Extensive communication but skepticism remained</td>
      </tr>
      <tr>
        <td class="framework-label">8. Anchor Change</td>
        <td class="case-cell">New KPIs, compensation tied to collaboration</td>
        <td class="case-cell">Old culture persisted despite stated change</td>
        <td class="case-cell">Some cultural shift, but not fully embedded</td>
      </tr>
    </tbody>
  </table>
  
  <div class="matrix-insight">
    <strong>Key Insight:</strong> Success requires executing ALL steps. Nokia failed at Steps 1-4; IBM succeeded at most steps but struggled with anchoring change.
  </div>
</div>
```

**CSS Requirements:**

```css
.matrix-intro {
  font-size: 26px;
  color: #475569;
  margin-bottom: 24px;
  font-style: italic;
}

.framework-matrix {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  margin-bottom: 24px;
}

.framework-matrix thead {
  background: #ed5e29;
  color: white;
}

.framework-matrix th {
  padding: 20px 16px;
  text-align: left;
  font-family: 'Cal Sans';
  font-size: 24px;
  font-weight: 400;
}

.framework-column {
  width: 20%;
  background: #5a5a8f; /* Darker shade for first column */
}

.case-column {
  width: 26.67%;
  font-size: 22px;
  line-height: 1.4;
}

.case-result {
  display: block;
  font-size: 20px;
  font-weight: 700;
  margin-top: 8px;
  font-family: 'Plus Jakarta Sans';
}

.case-result.success { color: #d1fae5; }
.case-result.failure { color: #fee2e2; }
.case-result.mixed { color: #fef3c7; }

.framework-matrix tbody tr {
  border-bottom: 1px solid #e2e8f0;
}

.framework-matrix tbody tr:last-child {
  border-bottom: none;
}

.framework-matrix tbody tr:hover {
  background: #f8fafc;
}

.framework-label {
  font-family: 'Cal Sans';
  font-size: 24px;
  font-weight: 600;
  color: #ed5e29;
  padding: 16px;
  background: #f8fafc;
}

.case-cell {
  padding: 16px;
  font-size: 21px;
  color: #475569;
  line-height: 1.5;
  vertical-align: top;
}

.matrix-insight {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
  padding: 20px;
  border-radius: 8px;
  font-size: 24px;
  color: #78350f;
}

.matrix-insight strong {
  color: #92400e;
  font-weight: 700;
}
```

**Implementation Notes:**
- Maximum 4-5 framework dimensions (rows) for readability
- Maximum 3 cases (columns) to avoid clutter
- Use color coding for outcomes (green/red/yellow)
- Provide synthesis/insight after matrix
- Not all steps need to be shown (select most illustrative)
- Alternative: Horizontal layout (cases as rows, framework as columns)

---

### Layout 23: Reflection / Journal Prompt

**Purpose:** Facilitate metacognitive thinking and personal application of concepts

**When to use:**
- After introducing complex/challenging concepts
- Before major assessments (preparation reflection)
- End of major topic sections
- Promoting self-directed learning

**Visual structure:** Contemplative design with structured reflection questions

**HTML Template:**

```html
<div class="slide reflection-slide" data-slide="N">
  <div class="reflection-header">
    <svg class="reflection-icon" width="100" height="100" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
      <circle cx="12" cy="12" r="10" opacity="0.2"/>
    </svg>
    <h2 class="slide-title">Reflection: Your Leadership Style</h2>
  </div>
  
  <div class="reflection-prompt">
    <p class="prompt-intro">Take 5 minutes to reflect on these questions. Write honest responses in your learning journal:</p>
  </div>
  
  <div class="reflection-questions">
    <div class="reflection-question">
      <span class="question-number">1</span>
      <div class="question-content">
        <h3>Identify</h3>
        <p>Which leadership theory resonates most with your personal values? Why?</p>
      </div>
    </div>
    
    <div class="reflection-question">
      <span class="question-number">2</span>
      <div class="question-content">
        <h3>Analyze</h3>
        <p>Describe a situation where you demonstrated leadership (formal or informal). Which theory best explains your approach?</p>
      </div>
    </div>
    
    <div class="reflection-question">
      <span class="question-number">3</span>
      <div class="question-content">
        <h3>Apply</h3>
        <p>Based on today's learning, what is ONE concrete change you could make to your leadership practice?</p>
      </div>
    </div>
    
    <div class="reflection-question">
      <span class="question-number">4</span>
      <div class="question-content">
        <h3>Connect</h3>
        <p>How does this relate to your upcoming Assessment 2 (Leadership Reflection Essay)?</p>
      </div>
    </div>
  </div>
  
  <div class="reflection-footer">
    <p><strong>Reminder:</strong> Your learning journal is a private space for growth. No judgment, only honest exploration. 📓</p>
  </div>
</div>
```

**CSS Requirements:**

```css
.reflection-slide {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
  padding: 60px;
}

.reflection-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 30px;
}

.reflection-icon {
  color: #ed5e29;
  opacity: 0.6;
  margin-bottom: 20px;
}

.reflection-prompt {
  background: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
  border-left: 4px solid #ed5e29;
}

.prompt-intro {
  font-size: 26px;
  color: #475569;
  font-style: italic;
  margin: 0;
}

.reflection-questions {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.reflection-question {
  display: flex;
  gap: 20px;
  align-items: flex-start;
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: all 0.3s ease;
}

.reflection-question:hover {
  box-shadow: 0 6px 16px rgba(115, 115, 176, 0.2);
  transform: translateX(8px);
}

.question-number {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #ed5e29;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Cal Sans';
  font-size: 28px;
  font-weight: 700;
}

.question-content {
  flex: 1;
}

.question-content h3 {
  font-family: 'Cal Sans';
  font-size: 26px;
  color: #ed5e29;
  margin-bottom: 8px;
  font-weight: 600;
}

.question-content p {
  font-size: 24px;
  color: #475569;
  line-height: 1.5;
  margin: 0;
}

.reflection-footer {
  background: #ed5e29;
  color: white;
  padding: 20px;
  border-radius: 12px;
  text-align: center;
}

.reflection-footer p {
  font-size: 24px;
  margin: 0;
}
```

**Implementation Notes:**
- Use Bloom's Taxonomy verbs (Identify, Analyze, Apply, Connect, Evaluate)
- 3-5 questions maximum (more = overwhelming)
- Questions should build progressively (simple → complex)
- Always connect to upcoming assessments when relevant
- Provide adequate time (5-10 minutes typical)
- Emphasize non-judgmental, growth-oriented reflection
- Consider providing sentence starters for anxious students

---

### Layout 24: Group Assignment Brief

**Purpose:** Clearly communicate collaborative task requirements, roles, and deliverables

**When to use:**
- Introducing in-class group activities
- Explaining multi-week group projects
- Setting up case study group work
- Tutorial main activities

**Visual structure:** Task description, role assignments, timeline, success criteria

**HTML Template:**

```html
<div class="slide group-assignment-slide" data-slide="N">
  <h2 class="slide-title">Group Activity: Crisis Communication Plan</h2>
  
  <div class="assignment-overview">
    <div class="overview-section">
      <div class="icon-badge">⏱️</div>
      <div>
        <strong>Duration:</strong> 45 minutes
      </div>
    </div>
    <div class="overview-section">
      <div class="icon-badge">👥</div>
      <div>
        <strong>Groups:</strong> 4-5 students
      </div>
    </div>
    <div class="overview-section">
      <div class="icon-badge">📋</div>
      <div>
        <strong>Deliverable:</strong> 5-minute presentation + 1-page plan
      </div>
    </div>
  </div>
  
  <div class="assignment-content">
    <div class="scenario-box">
      <h3>Scenario</h3>
      <p>Your company's new product has caused allergic reactions in 15 customers. Social media backlash is growing. You have 45 minutes to develop a crisis communication plan.</p>
    </div>
    
    <div class="roles-timeline">
      <div class="roles-section">
        <h3>Team Roles</h3>
        <ul class="roles-list">
          <li><strong>Coordinator:</strong> Keeps team on track, manages time</li>
          <li><strong>Researcher:</strong> Finds crisis communication best practices</li>
          <li><strong>Writer:</strong> Documents the plan</li>
          <li><strong>Presenter:</strong> Prepares to share with class</li>
          <li><strong>Analyst:</strong> Identifies stakeholders and risks</li>
        </ul>
      </div>
      
      <div class="timeline-section">
        <h3>Timeline</h3>
        <div class="timeline-step">
          <span class="time-badge">0-10 min</span>
          <span class="step-desc">Assign roles, read scenario, brainstorm</span>
        </div>
        <div class="timeline-step">
          <span class="time-badge">10-30 min</span>
          <span class="step-desc">Draft communication plan (key messages, channels, timing)</span>
        </div>
        <div class="timeline-step">
          <span class="time-badge">30-45 min</span>
          <span class="step-desc">Finalize plan, prepare 5-min presentation</span>
        </div>
      </div>
    </div>
    
    <div class="success-criteria">
      <h3>Success Criteria (from Assessment Rubric)</h3>
      <ul>
        <li>✓ Clear identification of stakeholders</li>
        <li>✓ Appropriate communication channels selected</li>
        <li>✓ Key messages address crisis transparently</li>
        <li>✓ Timeline realistic and well-sequenced</li>
      </ul>
    </div>
  </div>
</div>
```

**CSS Requirements:**

```css
.assignment-overview {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  background: #f8fafc;
  padding: 24px;
  border-radius: 12px;
}

.overview-section {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 24px;
  color: #475569;
}

.icon-badge {
  font-size: 36px;
}

.scenario-box {
  background: linear-gradient(135deg, #ed5e29 0%, #8b87c7 100%);
  color: white;
  padding: 24px;
  border-radius: 12px;
  margin-bottom: 24px;
}

.scenario-box h3 {
  font-family: 'Cal Sans';
  font-size: 32px;
  margin-bottom: 12px;
}

.scenario-box p {
  font-size: 26px;
  line-height: 1.5;
  margin: 0;
}

.roles-timeline {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  margin-bottom: 24px;
}

.roles-section,
.timeline-section {
  background: white;
  padding: 24px;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
}

.roles-section h3,
.timeline-section h3 {
  font-family: 'Cal Sans';
  font-size: 28px;
  color: #ed5e29;
  margin-bottom: 16px;
}

.roles-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.roles-list li {
  font-size: 22px;
  color: #475569;
  padding: 8px 0;
  line-height: 1.4;
}

.roles-list strong {
  color: #ed5e29;
  font-weight: 600;
}

.timeline-step {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 12px;
}

.time-badge {
  flex-shrink: 0;
  background: #ed5e29;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 20px;
  font-weight: 700;
  font-family: 'Cal Sans';
  min-width: 100px;
  text-align: center;
}

.step-desc {
  font-size: 22px;
  color: #475569;
  line-height: 1.4;
}

.success-criteria {
  background: #d1fae5;
  border-left: 4px solid #10b981;
  padding: 24px;
  border-radius: 12px;
}

.success-criteria h3 {
  font-family: 'Cal Sans';
  font-size: 28px;
  color: #065f46;
  margin-bottom: 16px;
}

.success-criteria ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.success-criteria li {
  font-size: 22px;
  color: #065f46;
  font-weight: 500;
}
```

**Implementation Notes:**
- Clearly define roles to promote accountability
- Provide explicit time breakdown (prevents poor time management)
- Link to assessment rubric (shows how practice connects to grading)
- Include scenario details that require actual thinking (not generic)
- Consider providing templates/worksheets for complex tasks
- For Vietnamese students: Explicitly state that English/Vietnamese both acceptable
- Remind about respectful collaboration expectations

---

### Layout 25: Assessment Checklist / Success Criteria

**Purpose:** Demystify assessment requirements with clear, actionable checklist format

**When to use:**
- 2-3 weeks before major assessment due date
- Tutorial sessions focused on assessment preparation
- After explaining assessment task
- Review sessions before submission

**Visual structure:** Detailed checklist organized by rubric categories with examples

**HTML Template:**

```html
<div class="slide assessment-checklist-slide" data-slide="N">
  <h2 class="slide-title">Assessment 2 Success Checklist</h2>
  
  <div class="assessment-header">
    <div class="header-item">
      <strong>Due:</strong> Week 9 (April 15, 11:59 PM)
    </div>
    <div class="header-item">
      <strong>Weight:</strong> 40% of final grade
    </div>
    <div class="header-item">
      <strong>Format:</strong> 2000-word persuasive report + 10-min presentation
    </div>
  </div>
  
  <div class="checklist-sections">
    <div class="checklist-category">
      <div class="category-header excellent">
        <h3>Content & Analysis (40%)</h3>
        <span class="points">16-20 points = HD</span>
      </div>
      <ul class="checklist-items">
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>Research depth:</strong> Minimum 8 academic sources (peer-reviewed journals, textbooks)</span>
        </li>
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>Framework application:</strong> Clear use of at least 2 theories from weeks 5-8</span>
        </li>
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>Critical analysis:</strong> Evaluate strengths/weaknesses, don't just describe</span>
        </li>
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>Examples:</strong> Real Vietnamese business examples (2-3 detailed cases)</span>
        </li>
      </ul>
    </div>
    
    <div class="checklist-category">
      <div class="category-header good">
        <h3>Structure & Clarity (30%)</h3>
        <span class="points">12-15 points = HD</span>
      </div>
      <ul class="checklist-items">
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>Executive summary:</strong> 200 words, includes main argument & recommendations</span>
        </li>
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>Logical flow:</strong> Each paragraph = one idea, clear transitions</span>
        </li>
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>Headings:</strong> Descriptive headings (not generic "Introduction", "Body")</span>
        </li>
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>Professional formatting:</strong> 12pt font, 1.5 spacing, page numbers, cover page</span>
        </li>
      </ul>
    </div>
    
    <div class="checklist-category">
      <div class="category-header satisfactory">
        <h3>Presentation Skills (20%)</h3>
        <span class="points">8-10 points = HD</span>
      </div>
      <ul class="checklist-items">
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>Time management:</strong> 10 minutes ±1 minute (points deducted if significantly over/under)</span>
        </li>
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>Slide quality:</strong> Maximum 12 slides, minimal text, strong visuals</span>
        </li>
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>Engagement:</strong> Eye contact, vocal variety, address questions confidently</span>
        </li>
      </ul>
    </div>
    
    <div class="checklist-category">
      <div class="category-header basic">
        <h3>Referencing & Ethics (10%)</h3>
        <span class="points">4-5 points = HD</span>
      </div>
      <ul class="checklist-items">
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>APA 7th format:</strong> In-text citations + reference list (use Citation Machine tool)</span>
        </li>
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>Turnitin check:</strong> Similarity <20% (submit draft to check first)</span>
        </li>
        <li>
          <input type="checkbox" class="check-box">
          <span><strong>AI declaration:</strong> Complete AI use form if any AI tools used</span>
        </li>
      </ul>
    </div>
  </div>
  
  <div class="final-reminder">
    <strong>📌 Pro Tip:</strong> Use this checklist while drafting! Don't wait until the last day to check these items. See complete rubric in Assessment Handbook Section 4.2.
  </div>
</div>
```

**CSS Requirements:**

```css
.assessment-header {
  display: flex;
  gap: 30px;
  background: #ed5e29;
  color: white;
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 24px;
  justify-content: space-around;
}

.header-item {
  font-size: 24px;
}

.header-item strong {
  font-weight: 700;
}

.checklist-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 24px;
}

.checklist-category {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  color: white;
}

.category-header.excellent { background: #10b981; }
.category-header.good { background: #3b82f6; }
.category-header.satisfactory { background: #f59e0b; }
.category-header.basic { background: #64748b; }

.category-header h3 {
  font-family: 'Cal Sans';
  font-size: 28px;
  margin: 0;
}

.points {
  font-size: 22px;
  font-weight: 700;
  font-family: 'Plus Jakarta Sans';
}

.checklist-items {
  list-style: none;
  padding: 20px 24px;
  margin: 0;
}

.checklist-items li {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 12px 0;
  font-size: 23px;
  color: #475569;
  line-height: 1.5;
  border-bottom: 1px solid #f1f5f9;
}

.checklist-items li:last-child {
  border-bottom: none;
}

.check-box {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  margin-top: 4px;
  cursor: pointer;
  accent-color: #ed5e29;
}

.checklist-items strong {
  color: #1e293b;
  font-weight: 600;
}

.final-reminder {
  background: #fef3c7;
  border-left: 4px solid #f59e0b;
  padding: 20px;
  border-radius: 8px;
  font-size: 24px;
  color: #78350f;
}

.final-reminder strong {
  font-weight: 700;
  color: #92400e;
}
```

**Implementation Notes:**
- Organize by rubric categories with point allocations
- Use color coding to show relative importance (weights)
- Provide specific, actionable criteria (not vague "be creative")
- Include examples where helpful
- Reference full rubric location for complete details
- Consider adding "Common Mistakes to Avoid" section
- Update based on student questions from previous semesters
- Make checkboxes interactive in digital version (students can check off)

---

## Layout Detection Algorithm Update

When adding these layouts to SKILL.md, use these detection patterns:

**Tier 2 Detection Patterns:**
- **Layout 16 (Timeline):** Keywords: "evolution", "history", "development over time", "chronological", "timeline", years/dates in sequence
- **Layout 17 (Case Study):** Keywords: "case study", "background", "challenge", "solution", "results", company name + year
- **Layout 18 (Learning Objectives):** Keywords: "learning objectives", "by the end", "you will be able to", Bloom's verbs (explain, apply, analyze)
- **Layout 19 (Discussion):** Keywords: "discussion", "debate", "should we", question marks, "arguments for/against"
- **Layout 20 (Resources):** Keywords: "further reading", "resources", "recommended", "essential", multiple article/book titles

**Tier 3 Detection Patterns:**
- **Layout 21 (Research):** Keywords: "study", "research", "findings", "N=", "p <", "participants", "methodology"
- **Layout 22 (Framework Matrix):** Keywords: "applying", "framework", table structure with cases as columns
- **Layout 23 (Reflection):** Keywords: "reflection", "journal", "take time", "reflect on", numbered introspective questions
- **Layout 24 (Group Assignment):** Keywords: "group activity", "team roles", "deliverable", duration timing, "your task"
- **Layout 25 (Assessment Checklist):** Keywords: "assessment", "checklist", "success criteria", "rubric", percentage weights

