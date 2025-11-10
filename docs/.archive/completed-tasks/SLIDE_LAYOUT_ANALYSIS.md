# Slide Layout Analysis & Content Generator Alignment

**Date:** January 11, 2025
**Purpose:** Align content generation with slide converter layouts

---

## Current Slide Layouts in Converter

### 1. **Title Slide**
- **Detection:** CSS class `title-slide`
- **Use:** Course title, opening slide
- **Content:** Title, subtitle, author
- **Limit:** 1 per presentation

### 2. **Section Break Slide**
- **Detection:** CSS class `section-break`
- **Use:** Divide presentation into major segments
- **Content:** Section title, dark background
- **Visual:** Large centered text, minimalist

### 3. **Big Number Slide**
- **Detection:** CSS class `big-number-slide`
- **Use:** Display key statistics or metrics
- **Content:** Large number (135pt) + explanation text
- **Visual:** Number dominates, supporting text below

### 4. **Content Slide** (Default/Fallback)
- **Detection:** CSS class `content-slide` or `objectives-slide`
- **Use:** Standard slides with title + body
- **Supports multiple sub-layouts:**
  - Bullet lists (single column)
  - Card layouts (grid of cards)
  - Stats banners (horizontal stats)
  - Grid layouts (CSS grid)
  - Objectives (learning objectives format)

---

## Missing Layouts (Opportunity for Enhancement)

### 5. **Two-Column Layout** ⭐ HIGH PRIORITY
**Why needed:** Very common pattern in teaching
**Use cases:**
- Theory (left) + Example (right)
- Concept (left) + Application (right)
- Before (left) + After (right)
- Problem (left) + Solution (right)

**Week 12 examples that need this:**
- Slide 7: Vision vs. Goals comparison
- Slide 20: Wrong vs. Right approach

**Detection:** CSS class `two-column-slide` or `split-slide`

---

### 6. **Comparison Table Layout** ⭐ HIGH PRIORITY
**Why needed:** Show structured comparisons
**Use cases:**
- Feature comparisons
- Good vs. Bad practices
- Different approaches

**Current workaround:** Tables in content slides (may not render optimally)

**Detection:** CSS class `comparison-slide`

---

### 7. **Process/Timeline Layout** ⭐ MEDIUM PRIORITY
**Why needed:** Show sequential steps
**Use cases:**
- Step-by-step processes
- Timelines (4-stage research process)
- Workflows

**Week 12 examples:**
- Could visualize 70-20-10 model as process
- Integration steps (Slide 20)

**Detection:** CSS class `process-slide` or `timeline-slide`

---

### 8. **Activity/Exercise Layout** ⭐ MEDIUM PRIORITY
**Why needed:** Visually distinguish interactive moments
**Use cases:**
- Reflection activities
- Pair/group exercises
- Think-pair-share

**Week 12 examples:**
- Slide 14: Drive mapping activity
- Slide 27: Reflection questions

**Detection:** CSS class `activity-slide`

**Visual:**
- Distinct color/background
- Clear instructions format
- Timer/duration visible
- Icon or graphic indicating "hands-on"

---

### 9. **Quote Slide** ⭐ LOW PRIORITY
**Why needed:** Highlight important quotes
**Use cases:**
- Expert quotes
- Research findings
- Inspirational messages

**Week 12 examples:**
- Senge quotes throughout
- Could use for Vietnamese proverbs

**Detection:** CSS class `quote-slide`

---

### 10. **Image + Text Layout** ⭐ LOW PRIORITY
**Why needed:** Visual + explanation
**Use cases:**
- Case studies with images
- Diagrams with explanations
- Visual examples

**Detection:** CSS class `image-text-slide`

---

## Week 12 Redundancy Analysis

### Issues Found:

#### 1. **Overly Verbose Slides**
**Slide 17: Five Sources of Continuous Learning**
- **Problem:** 200+ words, tries to cover 5 sources + model + example
- **Solution:** Split into 2 slides:
  - 17a: The 70-20-10 Model (overview + visual)
  - 17b: Applying the Model (strategy + Vietnamese example)

**Slide 11: Autonomy in Vietnamese Context**
- **Problem:** Long explanation of cultural paradox + 4 strategies + example
- **Solution:** Could use two-column layout (Cultural challenge | Strategies)

**Slide 12: Mastery - Learning Organization**
- **Problem:** 4 characteristics + statistics + examples
- **Solution:** Split or use two-column (Characteristics | Evidence)

#### 2. **Repetitive Content**

**Slides 6-9: Personal Mastery Sequence**
- Slide 6: Introduces personal mastery
- Slide 7: Vision vs. goals
- Slide 8: Values-career alignment
- Slide 9: Creative tension

**Assessment:** Good progression, not redundant. Keep as is.

**Slides 10-13: Drive Theory Sequence**
- Slide 10: Overview of 3 elements
- Slide 11: Autonomy detail
- Slide 12: Mastery detail
- Slide 13: Purpose detail

**Assessment:** Good structure, but could condense 11-12-13 using two-column layouts instead of separate slides.

**Slides 23 & 26: Synthesis slides**
- Slide 23: Key Concepts Synthesis (4 main frameworks)
- Slide 26: The Beginning, Not the End (what changes vs. stays same)

**Assessment:** Different purposes. Slide 23 = content summary, Slide 26 = inspirational closing. Not redundant.

#### 3. **Slides That Should Be Split**

**Slide 4: Assessment Connection**
- Covers 3 different assessments with dates and percentages
- Could split into:
  - 4a: Development Plan (40%) - THIS WEEK
  - 4b: Final Oral Exam (30%) + Mentorship (20%)

**Slide 17: Five Sources** (already mentioned)

**Slide 25: Assessment Bridge**
- Checklist of 4 different tasks with time estimates
- Could split into:
  - 25a: Development Plan & Presentation tasks
  - 25b: Mentorship & Reflective Essay tasks

---

## Content Generation Rules (To Implement)

### **Rule 1: Word Limits**
```
SLIDE CONTENT:
- Maximum 150 words per slide
- Maximum 6-8 bullet points
- Maximum 20 words per bullet
- One main concept per slide

IF exceeded → Auto-split into Part 1 & Part 2
```

### **Rule 2: Speaker Notes Format**
```
SPEAKER NOTES:
- Key points, NOT word-for-word scripts
- Bullet format, not paragraphs
- Structure:
  1. Opening hook/transition (1-2 bullets)
  2. Teaching points (3-5 bullets)
  3. Common misconceptions (if applicable)
  4. Examples or stories (1-2 bullets)
  5. Check for understanding (1 bullet)
  6. Transition to next slide (1 bullet)

- Maximum 150-200 words total
```

### **Rule 3: Layout Selection**
```
Content generator should specify layout type:

IF comparing two approaches → two-column-slide
IF showing stats/metrics → big-number-slide
IF hands-on activity → activity-slide
IF defining 5+ items → split into multiple slides
IF showing process/steps → process-slide (future)
```

---

## Recommendations for Implementation

### **Phase 1: Immediate Fixes** (Today)
1. ✅ Update `/generate-week` with word limits
2. ✅ Fix speaker notes format (bullets not paragraphs)
3. ✅ Add auto-split logic for verbose slides
4. ✅ Document layout types for content creators

### **Phase 2: Week 12 Refactoring** (Today)
1. Split Slide 17 into 17a & 17b
2. Refactor Slide 11 speaker notes (too verbose)
3. Consider splitting Slide 4 or condensing
4. Shorten Slide 12 content

### **Phase 3: New Layout Types** (Future)
1. Add two-column layout handler
2. Add activity slide handler
3. Add process/timeline handler
4. Add comparison table handler

---

## Updated Slide Type Specifications

### **Content Slide Limits**
- **Title:** 60 characters max
- **Body text:** 150 words max
- **Bullet points:** 6-8 max
- **Bullet text:** 20 words max each
- **If table:** 5 rows x 4 columns max

### **Two-Column Slide** (To implement)
- **Left column:** 75 words max
- **Right column:** 75 words max
- **Total:** 150 words combined
- **Use for:** Comparisons, theory+example

### **Activity Slide** (To implement)
- **Title:** Activity name
- **Instructions:** 3-5 numbered steps
- **Duration:** Clearly stated
- **Setup:** 30-40 words
- **Activity:** 60-80 words
- **Debrief:** 20-30 words

---

## Week 12 Specific Recommendations

### **Slides to Split:**
1. **Slide 17** → 17a (Model) + 17b (Application)
2. **Slide 4** → 4a (Dev Plan) + 4b (Other assessments) [Optional]

### **Slides to Condense:**
1. **Slide 11:** Move 4 strategies detail to speaker notes, keep 4 headlines on slide
2. **Slide 12:** Move statistics detail to speaker notes, keep headlines only

### **Slides Needing Speaker Notes Fix:**
- ALL slides need speaker notes converted from paragraphs to bullets
- Focus on key points, not full scripts

### **Slides That Are Good:**
- Slides 1-3: Good length
- Slides 6-9: Good progression
- Slide 14: Activity well-structured
- Slides 23-27: Appropriate for closing

---

**Next Steps:**
1. Update `/generate-week` command with new rules
2. Create speaker notes template (bullet format)
3. Refactor Week 12 Slides 17, 11, 12
4. Document layout selection guidance
