# Add Speaker Notes

Insert speaker notes from `lecture-content.md` into an existing PPTX file, saving to `output/slides.pptx`.

## Arguments

- `$ARGUMENTS` - Course code and week number (e.g., "BCI2AU 1")

## Usage

```
/add-speaker-notes BCI2AU 1
```

## Process

1. **Find PPTX file** in week folder or output/ subfolder
   - Looks for `*.pptx` files (excludes `slides.pptx` and batch files)
   - Prefers files with "Lecture" in the name

2. **Parse speaker notes** from `lecture-content.md`
   - Extracts `<speaker-notes>` sections from each slide (XML format only)

3. **Insert notes** into each slide
   - Maps by slide number (Slide 1 notes → slide 1, etc.)
   - Preserves existing slide content

4. **Save to output/slides.pptx** (original source PPTX preserved)

## Output

Reports:
- Total slides in PPTX
- Notes inserted count
- Slides without notes (skipped)
- Coverage percentage

## Example Output

```
Adding speaker notes for BCI2AU Week 1
----------------------------------------

1. Finding PPTX file in: .../weeks/week-01
   Found: BCI2AU Business Communication Lecture 1.pptx

2. Parsing speaker notes from: lecture-content.md
   Parsed 25 speaker notes sections
   PPTX has 28 slides

3. Inserting speaker notes...
   Inserted: 25, Skipped: 3

4. Saved to: output/slides.pptx

Status: SUCCESS
Coverage: 89%
```

## Prerequisites

- PPTX file exists in week folder (from Gemini)
- `lecture-content.md` exists with speaker notes sections
- python-pptx installed (`pip install python-pptx`)

## Notes

- This command replaces the old `/finalize-slides` command
- Does NOT merge batches (use single-batch Gemini workflow instead)
- Title slide and References slide typically don't have speaker notes (expected to be skipped)
- Source PPTX is preserved; final deliverable is in output/ folder

---

Run the speaker notes insertion:

```bash
source venv/bin/activate && python tools/add_speaker_notes.py $ARGUMENTS
```
