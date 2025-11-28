# Validate Course Content Quality

Run AI-powered validation on course content using Claude Code directly.

## Arguments
- `$ARGUMENTS` - Course code (e.g., BCI2AU) and optional phase flag

## Usage
```
/validate-content BCI2AU
/validate-content BCI2AU --phase1
/validate-content BCI2AU --phase2
```

## Instructions

Load the content-validation skill from `.claude/skills/content-validation/SKILL.md`.

### Step 1: Locate Course

Find course directory matching the code:
```
courses/{CODE}-*/
```

### Step 2: Load Reference Files

Read these files to understand course structure:
1. `syllabus.md` - Learning objectives, framework schedule
2. `assessment-handbook.md` - Assessment scenarios, rubrics
3. `course-info.md` - Week-assessment mapping (if exists)

### Step 3: Run Validation

For each week with content, read:
- `weeks/week-NN/lecture-content.md`
- `weeks/week-NN/tutorial-content.md`
- `weeks/week-NN/quiz-questions.md`

Run all 8 validators (or Phase 1/2 only if specified):

**Phase 1 - Critical Alignment:**
1. Bloom's Level Accuracy (quiz questions)
2. Tutorial-Assessment Alignment
3. Lecture-Quiz Alignment
4. Framework Scaffolding

**Phase 2 - Quality Checks:**
5. Learning Objective Coverage
6. Rubric Specificity
7. Terminology Consistency
8. Cultural Sensitivity & ESL

### Step 4: Report Results

Group issues by severity:

```markdown
## Validation Results: [COURSE_CODE]

### Summary
- **Status:** PASSED / FAILED
- **Critical Issues:** X
- **Warnings:** Y
- **Suggestions:** Z

### Critical Issues (Must Fix)
[List each with location and fix suggestion]

### Warnings (Should Fix)
[List each with location]

### Suggestions (Nice to Have)
[List if --verbose or few issues]
```

### Step 5: Offer Fixes

If critical issues found:
1. Ask if user wants to fix specific issues
2. Read the file with the issue
3. Apply the suggested fix
4. Re-validate that specific check

## Validation Details

See `.claude/skills/content-validation/` for detailed validation criteria:
- `SKILL.md` - Overview of all 8 validators
- `bloom-levels.md` - Bloom's taxonomy definitions
- `tutorial-assessment.md` - Alignment requirements
