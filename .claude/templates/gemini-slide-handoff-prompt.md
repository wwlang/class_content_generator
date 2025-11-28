# Gemini Slide Creation Handoff Prompt

Hand off lecture content to Google Gemini for professional slide creation.

---

## Hybrid Workflow Overview

This is part of a **Gemini + Claude hybrid workflow**:

1. **Gemini creates visual slides** (better images, infographics, design)
2. **You download batches** to the week folder
3. **Claude merges batches + inserts speaker notes** (via `/finalize-slides`)

**Gemini handles:** Visual design, images, infographics, layout
**Claude handles:** Speaker notes, merging, quality validation

---

## Instructions

1. Copy everything below `--- PROMPT START ---`
2. Replace `{{PLACEHOLDERS}}` with actual values
3. Paste the full `lecture-content.md` at the end
4. Send to Google Gemini
5. **Download each batch** with naming: `week-{{WEEK_NUMBER}}-batch-1.pptx`
6. Repeat for batches 2, 3, etc.
7. Run `/finalize-slides {{COURSE_CODE}} {{WEEK_NUMBER}}` to merge and add speaker notes

---

## Batch File Naming Convention

Save downloaded files to: `courses/{{COURSE_CODE}}/weeks/week-{{WEEK_NUMBER}}/`

**Preferred naming:**
```
week-01-batch-1.pptx  (slides 1-10)
week-01-batch-2.pptx  (slides 11-20)
week-01-batch-3.pptx  (slides 21-30 + References)
```

**Alternative:** Gemini may use descriptive names like `Topic Name - Batch 2.pptx`.
This is fine — `/finalize-slides` handles multiple naming patterns.

---

# --- PROMPT START ---

Create a visually engaging Google Slides presentation from the lecture content below.

## Course Details

- **Course:** {{COURSE_CODE}} {{COURSE_NAME}}
- **Week:** {{WEEK_NUMBER}} - {{TOPIC}}
- **Awarding University:** Andrews University
- **Campus:** National Economics University (NEU), Vietnam
- **Instructor:** {{INSTRUCTOR_NAME}}

## Important: Batch Processing

This lecture has 25-30 slides. To avoid content condensation due to output limits, process in batches:

- **Batch 1:** Slides 1-10
- **Batch 2:** Slides 11-20
- **Batch 3:** Slides 21-30 (or remaining)

**For this request, generate Slides 1-10 only.** Follow the content exactly for each slide. Do not summarize or condense. I will request the next batch in a follow-up prompt.

---

## Requirements

1. **Visual Style:** Professional, clean, and modern. Choose an appropriate visual style that fits academic/business content. Prioritize readability and visual clarity.

2. **Format:** Use 4:3 aspect ratio (not widescreen).

3. **Title Slide (Slide 1):** Every batch 1 must begin with a title slide containing:
   - **Title:** {{TOPIC}} (the week's topic from syllabus)
   - **Course:** {{COURSE_CODE}} - {{COURSE_NAME}}
   - **Awarding University:** Andrews University
   - **Campus:** National Economics University (NEU), Vietnam
   - **Instructor:** {{INSTRUCTOR_NAME}}

4. **Content Fidelity:** Use the EXACT wording from the lecture content. Do not summarize, paraphrase, or condense. Each slide should contain the content as written.

5. **Visuals:** Make it visually rich:
   - Use relevant images for case studies and examples
   - Create infographics for frameworks and models
   - Use charts/graphs for data and statistics
   - Add icons to support key points
   - Let visuals do the heavy lifting, not text walls

6. **Typography:** Ensure all text is readable at a distance:
   - Slide titles: 28pt minimum
   - Body text: 18pt minimum
   - No text smaller than 14pt anywhere

7. **Citations:** When referencing a framework or theory, include the citation in the slide footer, e.g., (Minto, 1987), (Cialdini, 1984).

8. **Speaker notes:** Not required - these will be added separately by Claude.

## Lecture Content

[PASTE lecture-content.md BELOW]

---

# --- TROUBLESHOOTING ---

**If Gemini condenses content:**
- Remind: "Use EXACT wording, do not summarize"
- Process smaller batches (7-8 slides instead of 10)
- Generate one slide at a time for problematic sections

**If images don't match:**
- Be specific: "Use a photo of [specific scene]"
- Provide reference: "Similar to [company name]'s branding"
- Request regeneration of specific slide

**If batch order gets confused:**
- Always specify: "This is batch X of Y, slides N-M"
- Reference previous batch: "Continuing from slide 10..."

**After download:**
- Verify file naming: `week-01-batch-1.pptx`
- Confirm slide count matches expected
- Run `/finalize-slides` to merge and add speaker notes

