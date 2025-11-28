# Generate Gemini Slide Creation Prompt

Automatically generate the Gemini handoff prompt for a specific week's lecture content.

## Arguments
- `$ARGUMENTS` - Course code and week number (e.g., `BCI2AU 1` or `BCI2AU 1-5` for multiple weeks)

## Usage
```
/gemini-handoff BCI2AU 1           # Single week
/gemini-handoff BCI2AU 1-5         # Weeks 1-5 (creates prompts for each)
```

## Instructions

### Step 1: Parse Arguments

Extract:
- Course code (e.g., `BCI2AU`)
- Week number(s) (single or range)

### Step 2: Load Course Info

Read `courses/{CODE}-*/course-info.md` or `syllabus.md` for:
- Course name
- Instructor name
- Any other metadata

If course-info.md doesn't exist, extract from syllabus.md header.

### Step 3: For Each Week

Read `courses/{CODE}-*/weeks/week-{NN}/lecture-content.md`

Extract:
- Week topic (from first H1 heading or filename pattern)
- Full lecture content (WITHOUT speaker notes - these are added later)
- Slide count (count `### Slide` occurrences)

### Step 4: Generate Prompt

Fill the template from `.claude/templates/gemini-slide-handoff-prompt.md`:

Replace placeholders:
- `{{COURSE_CODE}}` → Course code
- `{{COURSE_NAME}}` → Course name from syllabus
- `{{WEEK_NUMBER}}` → Week number (zero-padded: 01, 02)
- `{{TOPIC}}` → Week topic from lecture content
- `{{INSTRUCTOR_NAME}}` → Instructor from syllabus
- `{{SLIDE_COUNT}}` → Total number of slides

**Important:** Strip speaker notes from lecture content before including. Speaker notes are added back by Claude after Gemini creates the visual slides.

### Step 5: Output

Create output file at:
```
courses/{CODE}-*/weeks/week-{NN}/gemini-prompt.md
```

Contents:
1. The complete prompt with all placeholders filled
2. The full lecture-content.md appended (without speaker notes)

### Step 6: Display Instructions

After generating, show:

```
## Gemini Handoff Ready: Week {N}

**Prompt saved to:** courses/{path}/weeks/week-{NN}/gemini-prompt.md

**Next steps:**
1. Open the prompt file
2. Copy everything from "Create a visually engaging..." to the end
3. Paste into Google Gemini
4. Wait for full slide deck to generate
5. Download as: week-{NN}.pptx
6. Run: /add-speaker-notes {CODE} {N}

**Total slides:** {count}
```

## Multi-Week Mode

For range like `BCI2AU 1-5`:
- Generate prompts for weeks 1, 2, 3, 4, 5
- Each week gets its own `gemini-prompt.md` in its folder
- Display summary of all weeks ready for handoff

## Error Handling

- If lecture-content.md missing: "Week {N} lecture content not found. Run /generate-week {N} first."
- If course not found: List available courses
