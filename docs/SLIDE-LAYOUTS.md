# Slide Layouts Reference

**Complete guide to all slide layouts for the HTML to PPTX converter**

**Version:** 2.0 (Consolidated)
**Last Updated:** January 10, 2025
**Total Layouts:** 18

---

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Layout System Overview](#layout-system-overview)
3. [Core Slide Types (14)](#core-slide-types)
4. [Content Patterns (3)](#content-patterns)
5. [Modifier Classes](#modifier-classes)
6. [Prescriptive Layout Hints](#prescriptive-layout-hints)
7. [Usage Guidelines](#usage-guidelines)
8. [Troubleshooting](#troubleshooting)

---

## Quick Reference

| # | Layout Name | CSS Class | Priority | Use For | Hint Available |
|---|-------------|-----------|----------|---------|----------------|
| 1 | Title Slide | `title-slide` | 10 | Opening slide | No |
| 2 | Section Break | `section-break-slide` | 15 | Major transitions | No |
| 3 | Big Number | `big-number-slide` | 20 | Key statistics | No |
| 4 | Quote | `quote-slide` | 25 | Impactful quotes | `<!-- LAYOUT: quote -->` |
| 5 | Reflection | `reflection-slide` | 25 | Thinking prompts | `<!-- LAYOUT: reflection -->` |
| 6 | Framework/Diagram | `framework-slide` | 30 | Visual models | `<!-- LAYOUT: framework -->` |
| 7 | Comparison Table | `comparison-table-slide` | 35 | Side-by-side | `<!-- LAYOUT: comparison-table -->` |
| 8 | References | `references-slide` | 40 | Citations | `<!-- LAYOUT: references -->` |
| 9 | Stats Banner | `stats-banner-slide` | 45 | Multiple stats | No |
| 10 | Vocabulary Table | `vocab-table-slide` | 50 | Term definitions | No |
| 11 | Learning Objectives | `objectives-slide` | 55 | Learning goals | No |
| 12 | Activity | `activity-slide` | 60 | Exercises | No |
| 13 | Checklist | `checklist-slide` | 65 | Task lists | No |
| 14 | Card Layout | `cards-slide` | 70 | Info cards | No |
| 15 | Standard Content | `content-slide` | 100 | General content | No |
| - | **Content Patterns** | | | | |
| 16 | Grid Layout | `grid-2-col`, `grid-3-col` | Auto | Multi-column | No |
| 17 | Bullet Lists | Auto-detected | Auto | Lists | No |
| 18 | Image + Text | Auto-detected | Auto | Images with text | No |
| - | **Modifier** | | | | |
| M1 | Dark Background | `dark-slide` | Modifier | High contrast | No |

**Priority Notes:**
- Lower number = higher priority (checked first)
- Content slide (100) is fallback for unmatched patterns
- Auto-detected patterns work within content slides

### Alternate CSS Class Names

Some layouts accept **multiple CSS class names** (aliases) for flexibility:

| Layout | Primary Class | Alternate Classes | Notes |
|--------|---------------|-------------------|-------|
| Big Number | `big-number-slide` | `stat-slide` | Both work identically |
| Stats Banner | `stats-banner-slide` | `stats-slide` | Both work identically |
| Dark Background | `dark-slide` | `dark-background` | Modifier class |
| References | `references-slide` | `citations-slide` | Both work identically |
| Framework | `framework-slide` | `diagram-slide`, `model-slide` | All three work identically |
| Reflection | `reflection-slide` | `thinking-prompt` | Both work identically |
| Comparison | `comparison-table-slide` | `comparison-slide` | Both work identically |

**Recommendation:** Use **primary class names** for consistency. Alternates provided for backward compatibility and flexibility.

### Naming Convention: "standard" vs "content-slide"

**Clarification:** The **Standard Content** layout (Layout #15) has two names:

- **Internal/Config name:** `standard` (used in `layout_config.py`)
- **CSS class name:** `content-slide` (used in HTML)

These refer to **the same layout**. Use `class="slide content-slide"` in your HTML.

---

## Layout System Overview

### How Layout Detection Works

The converter uses a **priority-based handler system** to match HTML slides to PowerPoint layouts:

1. **Handler checks slides in priority order** (lowest number first)
2. **First matching handler processes the slide** (no further checking)
3. **Each handler looks for specific CSS classes or content patterns**
4. **Content slide is the fallback** (priority 100, catches everything else)

### Two Ways to Specify Layouts

#### 1. CSS Classes (Automatic Detection)

Add class to slide `<div>`:

```html
<div class="slide quote-slide">
  <!-- Quote content -->
</div>
```

**Pros:** Clean, semantic HTML
**Cons:** May not detect correctly with complex content

#### 2. Layout Hints (Prescriptive Control)

Add HTML comment before slide content:

```markdown
<!-- LAYOUT: quote -->
"Your quote text here"
— Attribution
```

**Pros:** Guaranteed correct layout, overrides auto-detection
**Cons:** Requires explicit hint in source markdown

**Recommendation:** Use hints for:
- Quotes, references, frameworks, reflections, comparison tables
- Any slide where visual formatting is critical
- Content that might be ambiguous (e.g., list that should be comparison table)

---

## Core Slide Types

### 1. Title Slide

**CSS Class:** `title-slide`
**Priority:** 10 (highest)
**Purpose:** Opening slide of presentation

#### Visual Characteristics

- **Background:** White (#ffffff)
- **Title:** Cal Sans, 52-72pt, bold, dark gray (#131313)
- **Subtitle:** Plus Jakarta Sans, 18pt, orange (#ed5e29)
- **Decorative Shapes:** Bottom-left corner (tan circles)
- **Layout:** Left-aligned with generous white space

#### When to Use

- First slide of every lecture
- Course title and code
- Presenter name and credentials
- Date/semester information

#### HTML Structure

```html
<div class="slide title-slide">
  <div class="title-content">
    <h1>Week 3: Communication Strategies</h1>
    <p class="subtitle">Effective Messaging in Business</p>
    <p class="author">BUS101 | Dr. Smith | Fall 2025</p>
  </div>
  <div class="decorative-shapes">
    <div class="circle"></div>
    <div class="circle"></div>
    <div class="circle"></div>
  </div>
</div>
```

#### Markdown Format

```markdown
---

# Week 3: Communication Strategies
*Effective Messaging in Business*
BUS101 | Dr. Smith | Fall 2025

---
```

#### PPTX Output

- Title at y=2.5", large and bold
- Subtitle at y=4.1", medium size with orange color
- Author info at y=4.5", small gray text
- Three decorative circles at bottom-left
- White background (not cream)

---

### 2. Section Break Slide

**CSS Class:** `section-break-slide`
**Priority:** 15
**Purpose:** Divide presentation into major sections

#### Visual Characteristics

- **Background:** Orange (#ed5e29) - full slide
- **Text:** White, Cal Sans, 36-54pt, bold
- **Layout:** Left-aligned, vertically centered
- **Letter-spacing:** Condensed (-0.05em)

#### When to Use

- Between major sections (use 2-3 times per lecture max)
- After introducing all concepts before moving to application
- Before major transitions in content
- To create dramatic visual breaks

#### HTML Structure

```html
<div class="slide section-break-slide">
  <h2 class="section-title">Part 1: Understanding Persuasion</h2>
</div>
```

#### Markdown Format

```markdown
---

## Part 1: Understanding Persuasion

---
```

*(Note: Requires `section-break-slide` class to be added during HTML generation)*

#### PPTX Output

- Orange background covering entire slide
- White text centered vertically at y=3.0"
- No footer (clean, impactful design)
- Multi-line support with `<br>` tags

**Pro Tip:** Keep section titles to 1-2 lines maximum for visual impact.

---

### 3. Big Number Slide

**CSS Class:** `big-number-slide`
**Priority:** 20
**Purpose:** Highlight single impactful statistic

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Number:** Cal Sans, 135pt (PPTX) / 180px (HTML), bold, orange
- **Explanation:** Plus Jakarta Sans, 18-28pt, dark gray
- **Layout:** Vertically and horizontally centered

#### When to Use

- Highlight ONE key statistic dramatically
- Research findings that need emphasis
- Memorable data points
- Before/after comparisons (use two slides)

#### HTML Structure

```html
<div class="slide big-number-slide">
  <h2 class="slide-title">Student Success</h2>
  <div class="number-content">
    <div class="big-number">73%</div>
    <p class="number-label">improvement in student engagement with interactive content</p>
  </div>
</div>
```

#### Markdown Format

```markdown
---

**SLIDE: Student Success**

# 73%

improvement in student engagement with interactive content

---
```

#### PPTX Output

- Cream background
- Title at y=0.62" (optional)
- Number centered at y=2.5", height=1.5"
- Explanation below number with 0.3" gap
- Footer at standard position

**Pro Tip:** Keep explanation to 1-2 lines. Use source citation in smaller text if needed.

---

### 4. Quote Slide

**CSS Class:** `quote-slide`
**Priority:** 25
**Prescriptive Hint:** `<!-- LAYOUT: quote -->`
**Purpose:** Display impactful quotes with visual prominence

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Quotation Mark:** Cal Sans, 120pt, light gray (#e2e8f0) - decorative
- **Quote Text:** Plus Jakarta Sans, 36pt, dark gray, left-aligned
- **Attribution:** 18pt, muted gray (#64748b), right-aligned with em dash
- **Line Spacing:** 1.0 (single spacing for quote)

#### When to Use

- Opening a new topic with thought-provoking question
- Emphasizing expert opinions or thought leadership
- Key philosophical statements that guide the lesson
- Memorable takeaways at end of sections
- Reflection prompts formulated as questions

#### HTML Structure

```html
<div class="slide quote-slide">
  <blockquote>
    <p>Who do you want to become in the next chapter of your life?</p>
    <cite>Robert Fritz, The Path of Least Resistance (1989)</cite>
  </blockquote>
</div>
```

#### Markdown Format with Layout Hint

```markdown
---

<!-- LAYOUT: quote -->

"Who do you want to become in the next chapter of your life?"

— Robert Fritz, The Path of Least Resistance (1989)

---
```

#### PPTX Output

- Large decorative " at y=1.8"
- Quote text at y=2.2" (top-aligned, not centered)
- Attribution at y=4.8", right-aligned
- Cream background
- Clean, uncluttered with generous white space

**Pro Tip:** Keep quotes to 2-3 lines maximum. For longer quotes, use standard content slide.

---

### 5. Reflection Slide

**CSS Class:** `reflection-slide`
**Priority:** 25
**Prescriptive Hint:** `<!-- LAYOUT: reflection -->`
**Purpose:** Prompt students to think/reflect

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Icon:** 💭 Thought bubble emoji, 72pt
- **Question:** Plus Jakarta Sans, 32pt, centered, dark gray
- **Instruction:** 16pt, italic, light gray (#94a3b8)
- **Line Spacing:** 1.0 (single)

#### When to Use

- Pause for student reflection during lecture
- Self-assessment prompts
- Connect theory to personal experience
- Before group discussions
- End of major sections

#### HTML Structure

```html
<div class="slide reflection-slide">
  <div class="reflection-icon">💭</div>
  <div class="reflection-question">
    What is one area of your life where you feel stuck between
    your current reality and your desired future?
  </div>
  <div class="reflection-instruction">
    Take a moment to reflect...
  </div>
</div>
```

#### Markdown Format with Layout Hint

```markdown
---

<!-- LAYOUT: reflection -->

What is one area of your life where you feel stuck between your current reality and your desired future?

*Take a moment to reflect...*

---
```

#### PPTX Output

- Thought bubble emoji at y=1.8"
- Question at y=2.8" (top-aligned, centered)
- Instruction at y=5.0", italic, muted
- Cream background

**Pro Tip:** Keep questions focused and specific. Allow 1-2 minutes of silence for reflection.

---

### 6. Framework/Diagram Slide

**CSS Class:** `framework-slide`
**Priority:** 30
**Prescriptive Hint:** `<!-- LAYOUT: framework -->`
**Purpose:** Visualize conceptual models with component boxes

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Framework Title:** Cal Sans, 28pt, centered
- **Component Boxes:** Light gray background (#f1f5f9), rounded borders
- **Component Title:** Plus Jakarta Sans, 16pt, bold
- **Component Description:** 12pt, muted gray (#64748b)
- **Grid Layout:** Responsive (1-3: row, 4: 2×2, 5-6: 3×2)

#### When to Use

- Process models with 3-6 steps
- Conceptual frameworks with interconnected parts
- Systems with multiple components (e.g., business model canvas)
- Strategic planning models
- Decision-making frameworks

#### HTML Structure

```html
<div class="slide framework-slide">
  <h2 class="framework-title">Creative Tension Framework</h2>
  <div class="framework-components" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
    <div class="component">
      <h3>Current Reality</h3>
      <p>Where you are now</p>
    </div>
    <div class="component">
      <h3>Creative Tension</h3>
      <p>Drive for change</p>
    </div>
    <div class="component">
      <h3>Desired Future</h3>
      <p>Your vision</p>
    </div>
  </div>
</div>
```

#### Markdown Format with Layout Hint

```markdown
---

<!-- LAYOUT: framework -->

## Creative Tension Framework

**Current Reality**: Where you are now

**Creative Tension**: Drive for change

**Desired Future**: Your vision

---
```

#### PPTX Output

- Framework title centered at y=1.0"
- Component boxes in responsive grid
- Each box: 0.25" padding, light background, centered text
- Automatic grid arrangement based on number of components:
  - 1-3 components: Horizontal row
  - 4 components: 2×2 grid
  - 5-6 components: 3×2 grid

**Pro Tip:** Keep component descriptions to 1-2 lines. Use 3-6 components for best visual balance.

---

### 7. Comparison Table Slide

**CSS Class:** `comparison-table-slide` or `comparison-slide`
**Priority:** 35
**Prescriptive Hint:** `<!-- LAYOUT: comparison-table -->`
**Purpose:** Side-by-side 2-column comparisons

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Title:** Cal Sans, 36pt, centered
- **Table:** 2 columns, equal width
- **Column Headers:** Plus Jakarta Sans, 18pt, bold, orange background
- **Rows:** Alternating white/light gray background
- **Text:** 14pt, dark gray

#### When to Use

- Before/after comparisons
- Pros/cons analysis
- Feature comparisons
- Two approaches/theories side-by-side
- Traditional vs modern methods

#### HTML Structure

```html
<div class="slide comparison-table-slide">
  <h2 class="slide-title">Fixed vs Growth Mindset</h2>
  <table class="comparison-table">
    <thead>
      <tr>
        <th>Fixed Mindset</th>
        <th>Growth Mindset</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Intelligence is static</td>
        <td>Intelligence can be developed</td>
      </tr>
      <tr>
        <td>Avoids challenges</td>
        <td>Embraces challenges</td>
      </tr>
      <tr>
        <td>Gives up easily</td>
        <td>Persists through obstacles</td>
      </tr>
    </tbody>
  </table>
</div>
```

#### Markdown Format with Layout Hint

```markdown
---

<!-- LAYOUT: comparison-table -->

## Fixed vs Growth Mindset

| Fixed Mindset | Growth Mindset |
|---------------|----------------|
| Intelligence is static | Intelligence can be developed |
| Avoids challenges | Embraces challenges |
| Gives up easily | Persists through obstacles |

---
```

#### PPTX Output

- Title at y=0.62"
- Table starting at y=1.5"
- Column headers with orange background (#ed5e29), white text
- Rows with alternating backgrounds
- Equal column widths (50% each)
- Proper cell padding and borders

**Pro Tip:** Keep to 4-6 rows for readability. Use concise phrases, not full sentences.

---

### 8. References Slide

**CSS Class:** `references-slide`
**Priority:** 40
**Prescriptive Hint:** `<!-- LAYOUT: references -->`
**Purpose:** Display academic citations with APA formatting

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Title:** "References", Cal Sans, 36pt
- **Citations:** Plus Jakarta Sans, 14pt, dark gray
- **Hanging Indent:** 0.5" (APA style)
- **Line Spacing:** 1.3 within citation, 12pt between citations
- **No Bullet Points:** Clean citation list

#### When to Use

- End of lecture to show all sources
- Required reading lists
- Bibliography for research-based content
- Compliance with academic citation requirements
- Recommended resources

#### HTML Structure

```html
<div class="slide references-slide">
  <h2>References</h2>
  <ul class="references">
    <li>Fritz, R. (1989). *The Path of Least Resistance: Learning to Become the Creative Force in Your Own Life*. Ballantine Books.</li>
    <li>Senge, P. M. (2006). *The Fifth Discipline: The Art & Practice of The Learning Organization*. Doubleday.</li>
    <li>Dweck, C. S. (2008). *Mindset: The New Psychology of Success*. Ballantine Books.</li>
  </ul>
</div>
```

#### Markdown Format with Layout Hint

```markdown
---

<!-- LAYOUT: references -->

## References

- Fritz, R. (1989). *The Path of Least Resistance*. Ballantine Books.
- Senge, P. M. (2006). *The Fifth Discipline*. Doubleday.
- Dweck, C. S. (2008). *Mindset*. Ballantine Books.

---
```

#### PPTX Output

- "References" title at y=0.62"
- Citations starting at y=1.5"
- Each citation with hanging indent (first line outdented by 0.5")
- Consistent spacing between citations
- Professional academic formatting
- No decorative elements

**Pro Tip:** Use full APA 7th edition format. Italicize book titles with `*asterisks*` in markdown.

---

### 9. Stats Banner Slide

**CSS Class:** `stats-banner-slide`
**Priority:** 45
**Purpose:** Display multiple statistics in row layout

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Title:** Cal Sans, 36pt (optional)
- **Stats Row:** 2-4 statistics in equal-width columns
- **Each Stat:**
  - Number: Cal Sans, 60pt, bold, orange
  - Label: Plus Jakarta Sans, 14pt, dark gray
  - Centered in column

#### When to Use

- Show 2-4 related statistics
- Key metrics for a topic
- Comparison of multiple data points
- Dashboard-style data presentation

#### HTML Structure

```html
<div class="slide stats-banner-slide">
  <h2 class="slide-title">Impact of Visual Design</h2>
  <div class="stats-container" style="display: grid; grid-template-columns: repeat(3, 1fr);">
    <div class="stat">
      <div class="stat-number">73%</div>
      <div class="stat-label">Improved engagement</div>
    </div>
    <div class="stat">
      <div class="stat-number">2.5x</div>
      <div class="stat-label">Faster comprehension</div>
    </div>
    <div class="stat">
      <div class="stat-number">91%</div>
      <div class="stat-label">Student satisfaction</div>
    </div>
  </div>
</div>
```

#### Markdown Format

```markdown
---

**SLIDE: Impact of Visual Design**

**73%** - Improved engagement
**2.5x** - Faster comprehension
**91%** - Student satisfaction

---
```

#### PPTX Output

- Title at y=0.62" (optional)
- Stats row at y=2.5"
- Equal-width columns (33.3% each for 3 stats)
- Numbers large and centered
- Labels below numbers

**Pro Tip:** Use 2-4 stats maximum. Too many stats reduce visual impact.

---

### 10. Vocabulary Table Slide

**CSS Class:** `vocab-table-slide`
**Priority:** 50
**Purpose:** Display term definitions in structured table

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Title:** Cal Sans, 36pt
- **Table:** 2 columns (Term | Definition), full width
- **Header Row:** Orange background, white text, bold
- **Content Rows:** Alternating white/light gray
- **Text:** 14pt, left-aligned

#### When to Use

- Key terminology for the topic
- Glossary of technical terms
- Concept definitions
- Acronym explanations

#### HTML Structure

```html
<div class="slide vocab-table-slide">
  <h2 class="slide-title">Key Communication Terms</h2>
  <table class="vocab-table">
    <thead>
      <tr>
        <th>Term</th>
        <th>Definition</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Ethos</td>
        <td>Credibility and character of the speaker</td>
      </tr>
      <tr>
        <td>Pathos</td>
        <td>Emotional appeal to the audience</td>
      </tr>
      <tr>
        <td>Logos</td>
        <td>Logical reasoning and evidence</td>
      </tr>
    </tbody>
  </table>
</div>
```

#### PPTX Output

- Title at y=0.62"
- Table starting at y=1.5"
- Term column: 30% width
- Definition column: 70% width
- Orange header row
- Alternating row colors

**Pro Tip:** Keep definitions to 1-2 lines. Use 4-6 terms per slide.

---

### 11. Learning Objectives Slide

**CSS Class:** `objectives-slide`
**Priority:** 55
**Purpose:** Display numbered learning objectives

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Title:** "Learning Objectives", Cal Sans, 36pt
- **Objectives:** Numbered list, Plus Jakarta Sans, 18pt
- **Numbering:** Bold, orange
- **Line Spacing:** 1.5
- **Bullets:** None (numbered list)

#### When to Use

- Opening slides of lectures (after title)
- Module/section introductions
- Assessment alignment (show what students will learn)

#### HTML Structure

```html
<div class="slide objectives-slide">
  <h2 class="slide-title">Learning Objectives</h2>
  <ol class="objectives-list">
    <li>Analyze the principles of persuasive communication</li>
    <li>Evaluate message effectiveness using Cialdini's framework</li>
    <li>Apply ethical persuasion techniques to business scenarios</li>
    <li>Create persuasive messages for different audiences</li>
  </ol>
</div>
```

#### Markdown Format

```markdown
---

## Learning Objectives

1. Analyze the principles of persuasive communication
2. Evaluate message effectiveness using Cialdini's framework
3. Apply ethical persuasion techniques to business scenarios
4. Create persuasive messages for different audiences

---
```

#### PPTX Output

- "Learning Objectives" title at y=0.62"
- Numbered list starting at y=1.9"
- Each objective with 0.3" spacing
- Orange numbers, dark gray text
- Left-aligned with proper indentation

**Pro Tip:** Use Bloom's Taxonomy verbs (Analyze, Evaluate, Apply, Create). Keep to 3-5 objectives.

---

### 12. Activity Slide

**CSS Class:** `activity-slide`
**Priority:** 60
**Purpose:** Interactive exercises with instructions

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Activity Icon:** 📝 or 🤝 emoji, 60pt
- **Title:** Cal Sans, 32pt, bold
- **Instructions:** Numbered list, Plus Jakarta Sans, 16pt
- **Timing:** Displayed prominently
- **Border:** Optional colored border for emphasis

#### When to Use

- In-class activities during lecture
- Think-pair-share exercises
- Case study analysis
- Group discussions
- Problem-solving tasks

#### HTML Structure

```html
<div class="slide activity-slide">
  <div class="activity-icon">📝</div>
  <h2 class="activity-title">Activity: Analyze a Persuasive Message</h2>
  <div class="activity-time">Time: 5 minutes</div>
  <ol class="activity-instructions">
    <li>Find a recent advertisement (print or video)</li>
    <li>Identify which of Cialdini's 6 principles it uses</li>
    <li>Explain why the principle is effective for this audience</li>
    <li>Share your findings with a partner</li>
  </ol>
</div>
```

#### PPTX Output

- Icon at y=1.0"
- Title at y=1.6"
- Time indicator at y=2.2"
- Instructions starting at y=2.8"
- Large, readable font for quick scanning

**Pro Tip:** Keep instructions to 3-5 steps. Display slide throughout activity.

---

### 13. Checklist Slide

**CSS Class:** `checklist-slide`
**Priority:** 65
**Purpose:** Task lists and procedural steps

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Title:** Cal Sans, 36pt
- **Checklist Items:** Plus Jakarta Sans, 18pt
- **Checkboxes:** ☐ before each item (16pt)
- **Checked Items:** ☑ with strikethrough (optional)
- **Line Spacing:** 1.8

#### When to Use

- Pre-assessment checklists
- Assignment requirements
- Process verification steps
- Study guides
- Self-assessment criteria

#### HTML Structure

```html
<div class="slide checklist-slide">
  <h2 class="slide-title">Portfolio Submission Checklist</h2>
  <ul class="checklist">
    <li>☑ <s>Draft completed and revised</s></li>
    <li>☐ Peer feedback incorporated</li>
    <li>☐ Citations in APA format</li>
    <li>☐ Rubric self-assessment completed</li>
    <li>☐ Submitted to course portal</li>
  </ul>
</div>
```

#### PPTX Output

- Title at y=0.62"
- Checklist starting at y=1.9"
- Large checkboxes (☐) for each item
- Generous spacing between items
- Optional: Completed items shown with ☑

**Pro Tip:** Use for procedural tasks. Students can mentally "check off" items during review.

---

### 14. Card Layout Slide

**CSS Class:** `cards-slide`
**Priority:** 70
**Purpose:** Display information in grid of cards

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Title:** Cal Sans, 36pt
- **Cards:** White background, subtle shadow, rounded corners
- **Card Icon:** Emoji or icon, 48pt, centered
- **Card Title:** Plus Jakarta Sans, 18pt, bold
- **Card Content:** 14pt, 2-3 lines
- **Grid:** 2×2 or 3×2 layout

#### When to Use

- Multiple related concepts (3-6 items)
- Feature highlights
- Process steps with icons
- Comparison of approaches
- Key points with visual cues

#### HTML Structure

```html
<div class="slide cards-slide">
  <h2 class="slide-title">Cialdini's 6 Principles of Persuasion</h2>
  <div class="cards-container" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
    <div class="card">
      <div class="card-icon">🤝</div>
      <h3 class="card-title">Reciprocity</h3>
      <p class="card-content">People feel obligated to return favors</p>
    </div>
    <div class="card">
      <div class="card-icon">💎</div>
      <h3 class="card-title">Scarcity</h3>
      <p class="card-content">Limited availability increases value</p>
    </div>
    <!-- More cards... -->
  </div>
</div>
```

#### PPTX Output

- Title at y=0.62"
- Cards in grid layout starting at y=1.5"
- Each card: White background, border, shadow
- Icon, title, and content vertically centered in card
- Equal-size cards with padding

**Pro Tip:** Use 3-6 cards. More than 6 becomes cluttered. Keep content to 2-3 lines per card.

---

### 15. Standard Content Slide

**CSS Class:** `content-slide`
**Priority:** 100 (fallback)
**Purpose:** General content with title and body

#### Visual Characteristics

- **Background:** Cream (#f4f3f1)
- **Title:** Cal Sans, 36pt, bold, left-aligned
- **Body:** Plus Jakarta Sans, 14-18pt, dark gray
- **Supports:** Paragraphs, bullet lists, emphasis, images
- **Padding:** 0.625" all sides

#### When to Use

- General content slides (60-70% of lectures)
- Bullet point lists
- Paragraphs with explanations
- Mixed content (text + images)
- Default for most content

#### HTML Structure

```html
<div class="slide content-slide">
  <h2 class="slide-title">Communication Principles</h2>
  <p>Effective communication requires understanding of fundamental principles that govern human interaction.</p>
  <ul>
    <li><strong>Clarity:</strong> Messages should be easy to understand</li>
    <li><strong>Relevance:</strong> Content must matter to the audience</li>
    <li><strong>Timing:</strong> Deliver messages when ready to receive</li>
  </ul>
  <p>These principles apply across all communication channels and contexts.</p>
</div>
```

#### Markdown Format

```markdown
---

## Communication Principles

Effective communication requires understanding of fundamental principles that govern human interaction.

- **Clarity:** Messages should be easy to understand
- **Relevance:** Content must matter to the audience
- **Timing:** Deliver messages when ready to receive

These principles apply across all communication channels and contexts.

---
```

#### PPTX Output

- Title at y=0.62"
- Content starting at y=1.9"
- Auto-detects and formats:
  - Bullet lists (with proper indentation)
  - Paragraphs (with spacing)
  - Bold and italic text
  - Images (if present)
- Footer at standard position

**Pro Tip:** This is the most flexible layout. Use for most content. Can be enhanced with grid layout or other content patterns.

---

## Content Patterns

Content patterns work **within content slides** and are **auto-detected** based on HTML structure.

### 16. Grid Layout Pattern

**CSS Classes:** `grid-2-col`, `grid-3-col`
**Detection:** Automatic based on `grid-template-columns` CSS

#### Visual Characteristics

- **Columns:** 2 or 3 equal-width columns
- **Gap:** 0.2" between columns
- **Content:** Text, lists, images, or mixed
- **Alignment:** Top-aligned

#### When to Use

- Side-by-side comparisons
- Multiple lists
- Text + image combinations
- Parallel concepts

#### HTML Structure

```html
<div class="slide content-slide">
  <h2 class="slide-title">Two Approaches to Change</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
    <div>
      <h3>Top-Down Change</h3>
      <ul>
        <li>Leadership-driven</li>
        <li>Clear directives</li>
        <li>Fast implementation</li>
      </ul>
    </div>
    <div>
      <h3>Bottom-Up Change</h3>
      <ul>
        <li>Employee-initiated</li>
        <li>Organic growth</li>
        <li>Higher buy-in</li>
      </ul>
    </div>
  </div>
</div>
```

#### PPTX Output

- Detects `grid-template-columns` CSS
- Creates equal-width columns
- Distributes content across columns
- Maintains vertical alignment

**Pro Tip:** Works automatically with CSS grid. No special class needed if CSS is present.

---

### 17. Bullet Lists Pattern

**Detection:** Automatic for `<ul>` and `<ol>` elements

#### Visual Characteristics

- **Bullet Style:** Orange circles (•)
- **Font:** Plus Jakarta Sans, 14-18pt
- **Line Spacing:** 1.5
- **Indentation:** 0.25" per level
- **Sub-bullets:** Smaller orange circles

#### When to Use

- Key points (3-7 items)
- Lists of concepts
- Steps in a process
- Features or benefits

#### HTML Structure

```html
<div class="slide content-slide">
  <h2>Communication Principles</h2>
  <ul>
    <li>Clarity in messaging</li>
    <li>Audience awareness
      <ul>
        <li>Demographics</li>
        <li>Prior knowledge</li>
      </ul>
    </li>
    <li>Timing of delivery</li>
  </ul>
</div>
```

#### PPTX Output

- Auto-formatted bullet lists
- Supports nested bullets (up to 3 levels)
- Orange bullet color (brand accent)
- Proper indentation

**Pro Tip:** Keep to 5-7 main bullets. Use sub-bullets sparingly.

---

### 18. Image + Text Pattern

**Detection:** Automatic when `<img>` present in content

#### Visual Characteristics

- **Image:** Left or right side, 40-50% width
- **Text:** Wraps around image
- **Spacing:** 0.2" gap between image and text
- **Alignment:** Top-aligned

#### When to Use

- Diagrams with explanations
- Photos with context
- Icons with descriptions
- Visual + textual information

#### HTML Structure

```html
<div class="slide content-slide">
  <h2>Visual Communication</h2>
  <img src="diagram.png" alt="Communication model" style="float: left; width: 40%;">
  <p>The Shannon-Weaver model illustrates the core components of communication...</p>
  <ul>
    <li>Sender encodes message</li>
    <li>Message transmitted through channel</li>
    <li>Receiver decodes message</li>
  </ul>
</div>
```

#### PPTX Output

- Downloads and embeds image
- Positions image (left or right based on CSS)
- Flows text around image
- Maintains aspect ratio

**Pro Tip:** Use images for complex concepts. Keep text concise when image is present.

---

## Modifier Classes

### Dark Slide Modifier

**CSS Class:** `dark-slide`
**Type:** Modifier (works with any layout)
**Purpose:** High-contrast slides for emphasis

#### Visual Characteristics

- **Background:** Dark gray (#131313)
- **Text:** White or cream
- **Accent:** Orange remains orange
- **High Contrast:** Maximum readability

#### When to Use

- Emphasize critical information
- Create visual variety (every 8-10 slides)
- Highlight warnings or important notes
- Before major transitions

#### Usage

Add `dark-slide` class to any slide type:

```html
<div class="slide content-slide dark-slide">
  <!-- Content -->
</div>
```

#### PPTX Output

- Dark background instead of cream/white
- Text colors inverted (white on dark)
- Orange accents remain visible
- All layouts supported

**Pro Tip:** Use dark slides strategically, not randomly. See [DARK_SLIDE_USAGE_GUIDE.md](DARK_SLIDE_USAGE_GUIDE.md) for detailed guidance.

---

## Prescriptive Layout Hints

### What Are Layout Hints?

Layout hints are **HTML comments** that explicitly tell the converter which layout to use, **overriding automatic detection**.

### When to Use Layout Hints

#### ✅ **USE hints when:**

1. **Visual formatting is critical**
   - Quotes need large typography
   - References need hanging indents
   - Frameworks need component boxes

2. **Content might be ambiguous**
   - List that should be comparison table
   - Questions that should be reflection prompts
   - Citations that should be references slide

3. **Guaranteed results needed**
   - Student-facing materials
   - Professional presentations
   - Assessment materials

#### ⚠️ **OPTIONAL when:**

- Auto-detection works correctly (most cases)
- Using standard bullet points or paragraphs
- Content slide with simple layout

### Supported Layout Hints

| Hint | Layout | Use Case |
|------|--------|----------|
| `<!-- LAYOUT: quote -->` | Quote Slide | Impactful quotes |
| `<!-- LAYOUT: references -->` | References Slide | Academic citations |
| `<!-- LAYOUT: framework -->` | Framework Slide | Visual models |
| `<!-- LAYOUT: reflection -->` | Reflection Slide | Thinking prompts |
| `<!-- LAYOUT: comparison-table -->` | Comparison Table | Side-by-side |

### How to Use Layout Hints

#### In Markdown

Place hint **before slide content** (after `---` separator):

```markdown
---

<!-- LAYOUT: quote -->

"Your quote text here"
— Attribution

---
```

#### In HTML

Place hint **inside slide div**, before content:

```html
<div class="slide content-slide">
  <!-- LAYOUT: quote -->
  <blockquote>
    <p>Your quote text here</p>
    <cite>Attribution</cite>
  </blockquote>
</div>
```

### Hint Processing

1. **Converter scans for layout hint** in slide HTML
2. **If hint found**: Uses specified layout (ignores class-based detection)
3. **If no hint**: Falls back to class-based detection
4. **If no hint and no class match**: Uses content slide (fallback)

**Priority:** Layout Hint > CSS Class > Auto-detection > Content Slide (fallback)

### Benefits of Hints

- ✅ **Guaranteed formatting** - Override auto-detection
- ✅ **Explicit intent** - Clear what layout is expected
- ✅ **Reliable output** - No surprises in PPTX
- ✅ **Self-documenting** - Source shows intended layout

### Hint Best Practices

1. **Use for specialized layouts** (quote, references, framework, reflection, comparison-table)
2. **Skip for standard content** (auto-detection works fine)
3. **Be consistent** - If using hints, use them for all instances of that layout
4. **Document in workflow** - Tell content generators when to use hints

---

## Usage Guidelines

### Lecture Structure Recommendations

**Typical 90-minute lecture (22-30 slides):**

1. **Title Slide** (1 slide)
   - Course and lecture title

2. **Learning Objectives** (1 slide)
   - 3-5 objectives

3. **Section Break** (optional, 1 slide)
   - "Part 1: Understanding X"

4. **Content Slides** (12-18 slides)
   - Mix of standard content, quotes, frameworks
   - Dark slide every 8-10 slides for variety

5. **Activity** (1-2 slides)
   - In-class exercises

6. **Section Break** (optional, 1 slide)
   - "Part 2: Applying X"

7. **More Content** (6-10 slides)
   - Applications, examples, case studies

8. **Reflection** (optional, 1 slide)
   - Self-assessment or thinking prompt

9. **References** (1 slide)
   - All sources cited

**Total:** 22-30 slides

### Layout Distribution

**Recommended mix for lectures:**

- **Content Slides:** 60-70%
- **Specialized Layouts:** 20-30%
  - Quote: 2-3 slides
  - Framework: 1-2 slides
  - Comparison Table: 1-2 slides
  - Big Number: 1-2 slides
- **Structural:** 10-15%
  - Title: 1 slide
  - Section Breaks: 2-3 slides
  - References: 1 slide

### Visual Variety

**Every 8-10 slides, use:**
- Section break slide
- Dark slide modifier
- Big number slide
- Quote slide
- Activity slide

**Goal:** Maintain visual interest and prevent monotony.

### Common Mistakes

#### ❌ **DON'T:**

1. **Too many section breaks** (>3 per lecture)
   - Solution: Use for major transitions only

2. **Big number slide with multiple stats**
   - Solution: Use stats banner slide instead

3. **Quote slide with long quotes** (>3 lines)
   - Solution: Use standard content slide with blockquote

4. **Vocabulary table with 10+ terms**
   - Solution: Split across 2 slides or use standard content

5. **Framework with 8+ components**
   - Solution: Split into 2 frameworks or simplify

6. **Dark slides randomly placed**
   - Solution: Use strategically for emphasis

#### ✅ **DO:**

1. **Match layout to content purpose**
2. **Use prescriptive hints for critical slides**
3. **Maintain visual rhythm** (variety every 8-10 slides)
4. **Keep specialized layouts concise**
5. **Test output** before finalizing

### Accessibility Considerations

1. **Contrast:** Dark text on light background (or white on dark)
2. **Font Size:** Minimum 14pt for body text
3. **Alt Text:** Provide for all images
4. **Color:** Don't rely solely on color to convey meaning
5. **Reading Order:** Logical top-to-bottom, left-to-right

---

## Troubleshooting

### Layout Not Detected

**Problem:** Slide uses wrong layout

**Solutions:**
1. Check CSS class is correct: `class="slide quote-slide"`
2. Use prescriptive layout hint: `<!-- LAYOUT: quote -->`
3. Verify HTML structure matches expected pattern
4. Check handler priority (higher priority checked first)

### Quote Slide Not Formatting

**Problem:** Quote appears as standard content

**Solutions:**
1. Add layout hint: `<!-- LAYOUT: quote -->`
2. Use `<blockquote>` tag for quote
3. Verify attribution in `<cite>` tag
4. Check for conflicting CSS classes

### References Hanging Indent Missing

**Problem:** Citations don't have hanging indent

**Solutions:**
1. Add layout hint: `<!-- LAYOUT: references -->`
2. Use `<ul class="references">` for list
3. Verify slide has `references-slide` class
4. Check converter version (feature added v1.1)

### Framework Components Not Grid

**Problem:** Components stack vertically instead of grid

**Solutions:**
1. Add layout hint: `<!-- LAYOUT: framework -->`
2. Check CSS: `display: grid; grid-template-columns: repeat(3, 1fr);`
3. Use 3-6 components (optimal for grid)
4. Verify framework-slide class present

### Dark Slide Not Dark

**Problem:** Dark modifier not applying

**Solutions:**
1. Add both classes: `class="slide content-slide dark-slide"`
2. Verify `dark-slide` is in class attribute
3. Check converter supports dark modifier
4. Use with any base layout type

### Content Slide Too Cluttered

**Problem:** Too much content, hard to read

**Solutions:**
1. Split into 2 slides
2. Use grid layout for multi-column
3. Use cards layout for multiple concepts
4. Simplify bullet points (max 5-7)

### Image Not Displaying

**Problem:** Image missing in PPTX

**Solutions:**
1. Verify image URL is accessible
2. Check internet connection (downloads images)
3. Use relative paths for local images
4. Check image format (PNG, JPG, SVG supported)

### Layout Detection Conflicts

**Problem:** Slide matches multiple patterns

**Solutions:**
1. Use prescriptive hint to force specific layout
2. Check handler priority (lower number = higher priority)
3. Review CSS classes (remove conflicting classes)
4. Simplify HTML structure

### Custom CSS Not Working

**Problem:** Custom styles not applied in PPTX

**Solutions:**
1. Check which CSS properties are supported
2. Use config constants when possible
3. Test with sample HTML first
4. Some CSS may not convert to PPTX

---

## Additional Resources

### Related Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical deep-dive into converter system
- **[DARK_SLIDE_USAGE_GUIDE.md](DARK_SLIDE_USAGE_GUIDE.md)** - When and how to use dark slides
- **[reference-design-style-guide.md](reference-design-style-guide.md)** - Design system reference
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - How to add new layouts

### Examples

- **Sample HTML:** `.claude/skills/slide-exporter/resources/examples/`
- **Generated PPTX:** `samples/`

### Getting Help

- **Workflow Issues:** See `.claude/CLAUDE.md`
- **Technical Issues:** See `ARCHITECTURE.md`
- **Layout Issues:** This document + test with sample HTML

---

## Version History

### Version 2.0 (January 10, 2025) - Consolidated

- **Merged 4 layout documentation files into one**
- Added comprehensive quick reference table
- Enhanced usage guidelines and best practices
- Consolidated prescriptive layout hints documentation
- Improved troubleshooting section
- Added lecture structure recommendations

**Previous versions:**
- layout-catalog.md (deprecated)
- SLIDE-LAYOUT-TYPES.md (deprecated)
- NEW-LAYOUTS-GUIDE.md (deprecated)
- layout-usage-example.md (deprecated)

### Version 1.1 (January 2025)

- Added 5 new academic layouts
- Introduced prescriptive layout hints
- Enhanced comparison table layout

### Version 1.0 (December 2024)

- Initial 12 core layouts
- Basic handler system

---

**This is the single authoritative reference for all slide layouts. For technical implementation details, see ARCHITECTURE.md.**
