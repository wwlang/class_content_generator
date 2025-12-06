# /generate-course [course-code]

Batch generate all weeks using **parallel agents** for maximum efficiency.

## Prerequisites

- Course structure exists (`/new-course`)
- Syllabus complete (`/generate-syllabus`)
- Research imported for all weeks

## Process

### Step 0: Pre-Flight Validation 🔒

1. Verify syllabus exists
2. Count weeks in syllabus
3. Check research availability per week
4. Identify which weeks need generation (skip experiential weeks like field trips/guest speakers)
5. Confirm with user before launching parallel agents

**If weeks missing research:**
- Option 1: Skip those weeks, continue with others
- Option 2: Research now
- Option 3: Cancel

### Step 1: Parallel Generation 🔐

**CRITICAL: Launch ALL weeks in parallel using Task agents in a SINGLE message.**

For each standard lecture week, spawn one Task agent with:
- Course context (syllabus, assessment-handbook, course-info)
- Week-specific research file
- Skill instructions (lecture-structure, tutorial-activities, quiz-questions)
- Output file paths

```
Launch in parallel (single message with multiple Task tool calls):
- Week 1 Agent → generates all Week 1 content
- Week 2 Agent → generates all Week 2 content
- Week 3 Agent → generates all Week 3 content
...etc
```

Each agent generates:
1. `lecture-content.md` (24+ slides in XML format)
2. `tutorial-content.md`
3. `tutorial-tutor-notes.md`
4. `quiz-questions.md` (YAML format)
5. `gemini-prompt.md`
6. Runs GIFT export

**Do NOT generate weeks sequentially.** Parallel execution reduces generation time from ~7 hours to ~45 minutes.

**If agent fails:** Continue with others, report failures at end.

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

**Parallel execution:** ~30-45 minutes total (all weeks simultaneously)
**Sequential execution:** ~50 min/week × N weeks (7-12 hours for 10 weeks)

Always use parallel agents unless specifically debugging a single week.

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
