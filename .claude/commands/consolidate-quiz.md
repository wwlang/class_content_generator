---
description: Consolidate quiz questions from multiple weeks into a balanced quiz bank
---

You are consolidating quiz questions for a course assessment.

# Task

Consolidate quiz questions from multiple weeks into a quiz bank with balanced Bloom's taxonomy distribution.

# Process

1. **Gather Requirements**
   - Ask the user for:
     - Course code (e.g., "BCI2AU")
     - Quiz ID (e.g., "quiz-1", "quiz-2", "quiz-3")
     - Week numbers to consolidate (e.g., 1, 2, 3)
     - Target question count (default: 30)
     - Target distribution (default: 15 Remembering, 15 Understanding)

2. **Preview Available Questions**
   - Use the CLI to check available questions:
     ```bash
     python3 tools/assessment_cli.py list-questions [COURSE_CODE] --weeks [WEEKS]
     ```
   - Show the user:
     - Total questions available
     - Bloom's distribution
     - Week distribution
     - Whether consolidation is possible

3. **Run Consolidation**
   - If user confirms, run consolidation with preview:
     ```bash
     python3 tools/assessment_cli.py consolidate [COURSE_CODE] [QUIZ_ID] \
       --weeks [WEEKS] \
       --target-total [TOTAL] \
       --target-remembering [R] \
       --target-understanding [U] \
       --preview
     ```
   - The CLI will show a preview and ask for confirmation

4. **Export to GIFT**
   - After successful consolidation, offer to export:
     ```bash
     python3 tools/assessment_cli.py consolidate [COURSE_CODE] [QUIZ_ID] \
       --weeks [WEEKS] \
       --export-gift \
       --output courses/[COURSE]/assessments/[QUIZ_ID].gift \
       --yes
     ```

5. **Report Results**
   - Show user:
     - Number of questions selected
     - Final Bloom's distribution
     - Any warnings
     - Output file path (if exported)

# Example

```bash
# Check available questions
python3 tools/assessment_cli.py list-questions BCI2AU --weeks 1 2 3

# Consolidate with preview
python3 tools/assessment_cli.py consolidate BCI2AU quiz-1 \
  --weeks 1 2 3 \
  --target-total 30 \
  --target-remembering 15 \
  --target-understanding 15 \
  --preview \
  --export-gift \
  --output courses/BCI2AU-business-communication/assessments/quiz-1.gift
```

# Quality Checks

- Ensure all selected questions are valid
- Verify Bloom's distribution is balanced
- Check week distribution is reasonable
- Confirm GIFT file is generated correctly

# Notes

- The consolidation service automatically ranks questions by quality score
- It attempts to balance questions evenly across source weeks
- Manual review of selected questions is recommended
- GIFT files can be imported directly into Moodle
