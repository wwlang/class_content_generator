# /generate-course [course-code]

Batch generate all weeks + slides in one command.

## Prerequisites

- Course structure exists (`/new-course`)
- Syllabus complete (`/generate-syllabus`)
- Research imported for all weeks

## Process

### Step 0: Pre-Flight Validation 🔒

1. Verify syllabus exists
2. Count weeks in syllabus
3. Check research availability per week
4. Estimate time (~50 min/week)
5. Ask user to confirm

**If weeks missing research:**
- Option 1: Skip those weeks, continue with others
- Option 2: Research now
- Option 3: Cancel

### Step 1: Batch Generation Loop

For each week:

```
1. Show progress: "Week 5/10: [Topic] [█████░░░░░] 50%"
2. Validate research (auto-validates if .week-N-ready flag exists)
3. Generate lecture (load content-generation/* skills)
4. Generate tutorial (load assessment-design/* skills)
5. Generate tutor notes
6. Export quiz (GIFT format)
7. Export slides (HTML)
8. Save progress for recovery
```

**If validation fails:** Skip week, continue with others, report at end.

### Step 2: Completion Report

Show summary:
- Weeks generated vs skipped
- Files created per week
- Skipped weeks with specific errors
- Next steps

## Recovery 🔐

If interrupted, re-running detects progress and offers to resume from interrupted week.

## Outputs

Per week:
- `lecture-content.md`
- `tutorial-content.md`
- `tutorial-tutor-notes.md`
- `week-N-quiz.gift`
- `slides.html`

Plus: `generation-report.md`

## Time

~50 min/week × N weeks
- 10-week course: 7-12 hours (can run overnight)

## Example

```
/generate-course BCI2AU

✓ Found syllabus: 10-week course
✓ Research ready for 9/10 weeks

Starting batch generation...
[Progress shown per week]

COMPLETE: 9/10 weeks generated
Skipped: Week 3 (research validation failed)
```

## If Things Go Wrong

- **Syllabus not found:** Run `/generate-syllabus` first
- **All weeks missing research:** Use `/import-research` or research in Desktop
- **Interrupted:** Re-run command to resume
- **Week fails validation:** Skipped automatically, fix later with `/generate-week`

**Full reference:** `generate-course-FULL-REFERENCE.md` (edge cases, detailed output formats)
