---
description: Generate professional PDF assessment brief from handbook
---

You are generating a professional assessment brief for students.

# Task

Generate a PDF (or HTML) assessment brief from the assessment handbook.

# Process

1. **Gather Requirements**
   - Ask the user for:
     - Course code (e.g., "BCI2AU")
     - Assessment ID (e.g., "persuasive-proposal", "mini-pitch")
     - Output format (pdf or html, default: pdf)
     - Output path (optional)

2. **List Available Assessments**
   - Show user what assessments are available:
     ```bash
     python3 tools/assessment_cli.py list-assessments [COURSE_CODE]
     ```
   - Display assessment names, types, and weights

3. **Generate Brief**
   - Run the brief generation:
     ```bash
     python3 tools/assessment_cli.py brief [COURSE_CODE] [ASSESSMENT_ID] \
       --format [pdf|html] \
       --output [OUTPUT_PATH]
     ```
   - Default output: `[ASSESSMENT_ID].pdf` in current directory

4. **Handle PDF Generation**
   - If WeasyPrint is not installed, the CLI will automatically fall back to HTML
   - Inform user if HTML fallback occurs
   - HTML can be converted to PDF later or opened in browser

5. **Report Results**
   - Show user:
     - Assessment name and details
     - Output file path
     - File size
     - Format generated (PDF or HTML)

# Example

```bash
# List assessments
python3 tools/assessment_cli.py list-assessments BCI2AU

# Generate PDF brief
python3 tools/assessment_cli.py brief BCI2AU persuasive-proposal \
  --output courses/BCI2AU-business-communication/assessments/proposal-brief.pdf

# Generate HTML brief (for preview)
python3 tools/assessment_cli.py brief BCI2AU persuasive-proposal \
  --format html \
  --output courses/BCI2AU-business-communication/assessments/proposal-brief.html
```

# Brief Contents

The generated brief includes:
- Assessment title and metadata (weight, due date)
- Task overview and description
- Scenario options (if applicable)
- Requirements checklist
- Submission format instructions
- Full rubric with all performance levels
- Professional styling with headers/footers

# Quality Checks

- Verify rubric is included
- Check scenarios are formatted correctly
- Ensure requirements are clear
- Confirm page breaks are appropriate
- Test that PDF renders properly

# Notes

- PDF generation requires WeasyPrint (in requirements.txt)
- HTML fallback is automatic if WeasyPrint unavailable
- Briefs use professional styling (Georgia font, A4 size)
- Suitable for printing and distribution to students
- Can be uploaded to LMS
