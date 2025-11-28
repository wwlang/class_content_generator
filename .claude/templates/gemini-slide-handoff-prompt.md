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

<role>
You are an expert presentation designer specializing in academic course materials. You create visually engaging, professional slides that balance aesthetic appeal with educational clarity. Your designs prioritize readability, visual hierarchy, and appropriate use of imagery to support learning.
</role>

<context>
Course: {{COURSE_CODE}} - {{COURSE_NAME}}
Week: {{WEEK_NUMBER}}
Topic: {{TOPIC}}
Institution: Andrews University (awarding) / National Economics University, Vietnam (campus)
Instructor: {{INSTRUCTOR_NAME}}
Total Slides: {{SLIDE_COUNT}}
</context>

<instructions>
1. Create a Google Slides presentation with exactly {{SLIDE_COUNT}} slides
2. Begin with a title slide containing: topic title, course code and name, both universities, and instructor name
3. Use 4:3 aspect ratio (standard, not widescreen)
4. Reproduce the EXACT wording from the lecture content for each slide - preserve all text as written
5. Add relevant visuals to each slide:
   - Case studies and examples: use contextual photographs
   - Frameworks and models: create clear infographics or diagrams
   - Statistics and data: present as charts or graphs
   - Key points: support with icons
6. Apply professional typography:
   - Slide titles: 28pt minimum
   - Body text: 18pt minimum
   - Smallest text anywhere: 14pt minimum
7. Include academic citations in slide footers when frameworks or theories are referenced (e.g., Minto, 1987)
8. Leave speaker notes empty - these will be added separately
</instructions>

<constraints>
- Preserve exact wording because students receive these slides as study materials and need consistency with lecture recordings
- Use 4:3 aspect ratio because the classroom projectors are configured for this format
- Minimum font sizes ensure readability from the back of the lecture hall
- No speaker notes because Claude will add detailed instructor notes in a later step
</constraints>

<examples>
<example>
<input>
### Slide 3: The Pyramid Principle

**Key Concept:** Start with the answer, then provide supporting evidence

The Pyramid Principle (Minto, 1987):
- Lead with your main message
- Group supporting arguments logically
- Present evidence in descending order of importance

**Why it works:** Busy executives read conclusions first
</input>
<output>
Slide 3 contains:
- Title: "The Pyramid Principle" (32pt, bold)
- Infographic: Triangle/pyramid diagram showing hierarchy (main message at top, supporting points below)
- Three bullet points with exact wording from content (20pt)
- "Why it works" callout box with the executive insight
- Footer: (Minto, 1987)
- Visual style: Clean, professional, blue/gray color scheme
</output>
</example>

<example>
<input>
### Slide 7: Case Study - Vinamilk Crisis Response

In 2013, Vinamilk faced a product recall crisis...

**What went right:**
- Immediate public acknowledgment
- Clear action plan communicated
- Regular updates to stakeholders

**Result:** Brand trust recovered within 6 months
</input>
<output>
Slide 7 contains:
- Title: "Case Study - Vinamilk Crisis Response" (32pt)
- Relevant image: Vinamilk products or corporate imagery
- Timeline or process graphic showing the response steps
- Three "What went right" points with checkmark icons (20pt)
- Result callout with upward trend icon
- Visual style: Professional with subtle Vietnamese context
</output>
</example>

<example>
<input>
### Slide 12: Hofstede's Cultural Dimensions

**Vietnam vs. United States comparison:**
| Dimension | Vietnam | USA |
|-----------|---------|-----|
| Power Distance | 70 | 40 |
| Individualism | 20 | 91 |
| Uncertainty Avoidance | 30 | 46 |
</input>
<output>
Slide 12 contains:
- Title: "Hofstede's Cultural Dimensions" (32pt)
- Bar chart or radar chart comparing Vietnam and USA scores
- Clear legend identifying each country
- All three dimensions labeled with exact scores
- Footer: (Hofstede, 2010)
- Visual style: Data visualization best practices, contrasting colors for countries
</output>
</example>
</examples>

<lecture_content>
[PASTE lecture-content.md BELOW]
</lecture_content>

<task>
Generate all {{SLIDE_COUNT}} slides as a complete Google Slides presentation. Reproduce all content exactly as provided, enhance with appropriate visuals, and maintain consistent professional styling throughout.
</task>

<output_format>
A downloadable Google Slides presentation (.pptx) with:
- {{SLIDE_COUNT}} slides total
- 4:3 aspect ratio
- Professional visual design
- All lecture content preserved exactly
- Relevant images, infographics, and icons
- Academic citations in footers
- Empty speaker notes sections
</output_format>

---

# --- TROUBLESHOOTING ---

**If Gemini condenses content:**
- Remind: "Reproduce the EXACT wording from the lecture content - do not summarize or paraphrase"
- Generate one slide at a time for problematic sections

**If images don't match:**
- Be specific: "Use a photo of [specific scene]"
- Provide reference: "Similar to [company name]'s branding"
- Request regeneration of specific slide

**After download:**
- Verify file naming: `week-01.pptx`
- Confirm slide count matches expected ({{SLIDE_COUNT}} slides)
- Run `/add-speaker-notes` to insert speaker notes
