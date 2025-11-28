# Export DOCX

Convert markdown files to professional DOCX format with course-branded footers.

## Arguments

- `$ARGUMENTS` - Course code and week number OR "syllabus"
  - Week: `BCI2AU 1`
  - Syllabus: `BCI2AU syllabus`

## Usage

```
/export-docx BCI2AU 1
/export-docx BCI2AU syllabus
```

## Week Conversion

Converts to `output/` subfolder:
- `tutorial-content.md` → `output/tutorial-content.docx`
- `tutorial-tutor-notes.md` → `output/tutorial-tutor-notes.docx`

**Excludes:** `lecture-content.md` (already becomes slides)

## Syllabus Conversion

Converts:
- `syllabus.md` → `syllabus.docx` (in course folder)

## Footer Format

All DOCX files include a professional footer:

```
BCI2AU | Andrews University | NEU Vietnam | William Lang | Page X of Y
```

Footer info extracted from `course-info.md` or `syllabus.md`.

## Markdown Features Supported

| Markdown | DOCX Output |
|----------|-------------|
| `# H1` | Heading 1 |
| `## H2` | Heading 2 |
| `**bold**` | Bold text |
| `*italic*` | Italic text |
| `- item` | Bullet list |
| `1. item` | Numbered list |
| `\| table \|` | Formatted table |
| ``` code ``` | Monospace block |
| `> quote` | Indented italic |

## Example Output

```
Converting markdown files for BCI2AU Week 1
----------------------------------------

Converting to output/ folder...
   tutorial-content.md -> output/tutorial-content.docx
   tutorial-tutor-notes.md -> output/tutorial-tutor-notes.docx

Status: SUCCESS
Files converted: 2
```

## Prerequisites

- Markdown source files exist
- python-docx installed (`pip install python-docx`)

## Notes

- Week deliverables are created in `output/` subfolder
- Course info is extracted from `course-info.md` or syllabus header
- Page numbers are dynamic (Page X of Y format)

---

Run the DOCX export:

```bash
source venv/bin/activate && python3 tools/markdown_to_docx.py $ARGUMENTS
```
