---
description: Package all course deliverables into a ZIP archive
---

You are packaging course materials for delivery.

# Task

Automatically convert all markdown files to DOCX (if needed), then create a ZIP archive containing all deliverable files (.docx, .pptx, .gift) from a course, preserving the relative folder structure.

## Auto-Conversions

Before packaging, automatically converts these files (always regenerates DOCX):
- `syllabus.md` → `output/syllabus.docx`
- `assessment-handbook.md` → `output/assessment-handbook.docx`
- `tutor-guide.md` → `tutor-guide.docx`
- `package/course-package-guide.md` → `package/README.docx`
- `assessments/*.md` → `assessments/output/*.docx` (briefs, revision guide, etc.)

This ensures all DOCX files have:
- Consistent formatting and footers
- Latest markdown content
- Correct course information

# Arguments

- `$COURSE_CODE` - Course code (e.g., BCI2AU)

# Usage

```
/package-course BCI2AU
```

# What Gets Packaged

The ZIP archive includes:

## Root Files
From `output/` folder:
- `syllabus.docx`
- `assessment-handbook.docx`

## Assessment Files
From `assessments/output/` folder:
- All `.docx` files (assessment briefs, final-exam-revision guide)
- All `.gift` files (consolidated quizzes)

## Weekly Materials
From each `weeks/week-*/output/` folder:
- `tutorial-content.docx`
- `tutorial-tutor-notes.docx`
- `week-*-research.docx`
- `slides.pptx`
- `week-*-quiz.gift`
- `readings/` folder (PDFs + reading list)

# ZIP Structure

The archive preserves folder structure:

```
BCI2AU-deliverables.zip
├── syllabus.docx                    (from output/)
├── assessment-handbook.docx         (from output/)
├── assessments/
│   ├── business-memo.docx
│   ├── executive-summary.docx
│   ├── final-exam-revision.docx
│   ├── quiz-1.gift
│   └── quiz-2.gift
└── weeks/
    ├── week-01/
    │   ├── tutorial-content.docx
    │   ├── tutorial-tutor-notes.docx
    │   ├── week-01-research.docx
    │   ├── slides.pptx
    │   ├── week-01-quiz.gift
    │   └── readings/
    │       ├── READING-LIST.md
    │       └── *.pdf
    └── week-02/
        └── ...
```

# Output Location

ZIP file created at:
```
courses/[CODE]/package/[CODE]-deliverables.zip
```

# Process

1. **Get Course Code**
   - Ask user for course code if not provided

2. **Validate Course Exists**
   - Check that `courses/[CODE]/` directory exists
   - Report error if not found

3. **Run Packaging Script**
   - Collect all deliverable files
   - Create ZIP with preserved structure
   - Report results

4. **Display Report**
   - Show packaged file count by category
   - Display ZIP file location
   - List any warnings (missing expected files)

# Example Output

```
============================================================
COURSE PACKAGING REPORT
============================================================
✓ Packaging successful

Package created:
  courses/BCI2AU-business-communication/package/BCI2AU-deliverables.zip

Files packaged: 47

Breakdown by category:
  - Root files:       2
  - Assessment files: 6
  - Week files:       39

============================================================
```

# Quality Checks

- Verify all expected files are included
- Confirm folder structure is preserved in ZIP
- Check ZIP file size is reasonable
- Ensure no markdown source files (.md) are included

# Prerequisites

- All content generation must be complete
- All DOCX exports must be done (`/export-docx`)
- Quiz consolidation should be done (`/consolidate-quiz`)
- Slides must have speaker notes added (`/add-speaker-notes`)
- Exam revision guide created (`assessments/final-exam-revision.md`)

# Notes

- This is the **final step** in the workflow
- Run after all other steps are complete
- Only packages deliverable formats (.docx, .pptx, .gift)
- Markdown source files are excluded
- Package folder is created automatically

---

Run the packaging script:

```bash
source venv/bin/activate && python3 tools/package_course.py $COURSE_CODE
```
