# Generate Gemini Slide Creation Prompt

Automatically generate Gemini handoff prompts for lecture content using the Python generation script.

## Arguments
- `$ARGUMENTS` - Course code and optional week number/range (e.g., `BCI2AU`, `BCI2AU 1`, or `BCI2AU 1-5`)

## Usage
```
/gemini-handoff BCI2AU              # All weeks (1-12)
/gemini-handoff BCI2AU 1            # Single week
/gemini-handoff BCI2AU 1-5          # Weeks 1-5
```

## Instructions

### Step 1: Parse Arguments

Extract from `$ARGUMENTS`:
- Course code (required, e.g., `BCI2AU`)
- Week specification (optional):
  - If omitted: generate all weeks (1-12)
  - Single number: generate that week only
  - Range: generate all weeks in range (e.g., `1-5`)

### Step 2: Run Python Script

Execute the generation script:

```bash
python3 tools/generate_gemini_prompts.py {COURSE_CODE} [week_range]
```

**Examples:**
- `python3 tools/generate_gemini_prompts.py BCI2AU` - All weeks
- `python3 tools/generate_gemini_prompts.py BCI2AU 5` - Week 5 only
- `python3 tools/generate_gemini_prompts.py BCI2AU 1-10` - Weeks 1-10

The script automatically:
- Locates the course directory
- Extracts course name, instructor, university from syllabus
- For each week:
  - Reads lecture-content.md
  - Extracts topic from H1 heading
  - Counts slides (handles both explicit "## Slide N" and section-based formats)
  - Strips speaker notes from content
  - Fills template from `.claude/templates/gemini-slide-handoff-prompt.md`
  - Writes `gemini-prompt.md` to week folder

### Step 3: Display Results

The script outputs a summary showing:
- Course information
- Which weeks were processed
- Slide counts for each week
- Next steps for the user

## What Gets Generated

Each `courses/{CODE}-*/weeks/week-{NN}/gemini-prompt.md` contains:

1. **Header section** with:
   - Week number and topic
   - Course code and name
   - Expected slide count
   - Download and next-step instructions

2. **Complete Gemini prompt** with:
   - Role (expert presentation designer)
   - Context (course, week, topic, institution, instructor, slide count)
   - Instructions (6 key points)
   - Constraints (preserve wording, Modern Bright Pastel Corporate style)
   - Examples (4 scenarios showing content structure)
   - Full lecture content (speaker notes stripped)
   - Task and output format

## Error Handling

The script handles:
- Course not found → Error message
- Week folder missing → "MISSING" status in summary
- lecture-content.md missing → Skips that week
- Multiple slide formats → Fallback counting logic

## Technical Details

**Template:** `.claude/templates/gemini-slide-handoff-prompt.md`
**Script:** `tools/generate_gemini_prompts.py`

**Key features:**
- Strips speaker notes (`<speaker-notes>` XML tags)
- Counts slides from XML structure
- Extracts topic and removes "Week N:" prefix
- Generic university placeholder support
- Zero-padded week numbers (01, 02, etc.)

## Next Steps After Generation

1. Navigate to each week folder
2. Open `gemini-prompt.md`
3. Copy everything below the instructions section
4. Paste into Google Gemini
5. Download generated PPTX as `week-{NN}.pptx`
6. Run `/add-speaker-notes {CODE} {N}` to insert speaker notes
