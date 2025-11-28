# Gemini Slide Creation Handoff Prompt

Hand off lecture content to Google Gemini for professional slide creation.

---

## Hybrid Workflow Overview

This is part of a **Gemini + Claude hybrid workflow**:

1. **Gemini creates visual slides** (better images, infographics, design)
2. **You download** the complete deck to the week folder
3. **Claude inserts speaker notes** (via `/add-speaker-notes`)

**Gemini handles:** Visual design, images, infographics, layout
**Claude handles:** Speaker notes, quality validation

---

## Instructions

1. Copy everything below `--- PROMPT START ---`
2. The `/gemini-handoff` command fills all placeholders automatically
3. Paste into Google Gemini
4. Wait for full slide deck to generate
5. Download as: `week-{{WEEK_NUMBER}}.pptx`
6. Run `/add-speaker-notes {{COURSE_CODE}} {{WEEK_NUMBER}}` to insert speaker notes

---

## File Naming Convention

Save downloaded file to: `courses/{{COURSE_CODE}}-*/weeks/week-{{WEEK_NUMBER}}/`

**Naming:** `week-01.pptx`, `week-02.pptx`, etc.

---

# --- PROMPT START ---

Create a visually engaging Google Slides presentation from the lecture content below.

## Course Details

- **Course:** {{COURSE_CODE}} {{COURSE_NAME}}
- **Week:** {{WEEK_NUMBER}} - {{TOPIC}}
- **Awarding University:** Andrews University
- **Campus:** National Economics University (NEU), Vietnam
- **Instructor:** {{INSTRUCTOR_NAME}}

## Slide Count

This lecture has **{{SLIDE_COUNT}} slides**. Generate all slides in a single response.

---

## Requirements

1. **Visual Style:** Professional, clean, and modern. Choose an appropriate visual style that fits academic/business content. Prioritize readability and visual clarity.

2. **Format:** Use 4:3 aspect ratio (not widescreen).

3. **Title Slide (Slide 1):** Must begin with a title slide containing:
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
- Generate one slide at a time for problematic sections

**If images don't match:**
- Be specific: "Use a photo of [specific scene]"
- Provide reference: "Similar to [company name]'s branding"
- Request regeneration of specific slide

**After download:**
- Verify file naming: `week-01.pptx`
- Confirm slide count matches expected ({{SLIDE_COUNT}} slides)
- Run `/add-speaker-notes` to insert speaker notes

