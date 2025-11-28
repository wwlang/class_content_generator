# Content Validation Skill

AI-powered validation for university teaching content quality.

## When to Use

Use this skill when running `/validate-content` or when asked to check course quality.

## Validation Checks (8 Total)

### Phase 1 - Critical Alignment

1. **Bloom's Level Accuracy**
   - Quiz questions must match stated cognitive level
   - REMEMBERING: Recall facts, definitions (NO scenarios)
   - UNDERSTANDING: Explain why, distinguish concepts
   - Flag: Scenario-based questions labeled as Remembering

2. **Tutorial-Assessment Alignment**
   - Every tutorial must have explicit "Assessment Connection" statement
   - Activities must be scaled versions of assessment tasks
   - Success criteria must come from rubric, not invented

3. **Lecture-Quiz Alignment**
   - Quiz questions must test content taught in that week's lecture
   - Extract lecture concepts (headings, bold terms, frameworks)
   - Flag questions testing untaught material

4. **Framework Scaffolding**
   - Frameworks must be introduced before referenced
   - Lectures can forward-reference (suggestion level)
   - Tutorials/quizzes cannot use un-introduced frameworks (critical)

### Phase 2 - Quality Checks

5. **Learning Objective Coverage**
   - All LOs from syllabus must be covered in lectures
   - All LOs must be assessed
   - Flag: NOT_COVERED or NOT_ASSESSED

6. **Rubric Specificity**
   - Flag vague phrases: "appropriate", "adequate", "good", "clear"
   - Criteria must be measurable and actionable
   - Performance levels must be clearly differentiated

7. **Terminology Consistency**
   - Same terms should be used consistently across weeks
   - Flag variations like "Pyramid Principle" vs "Minto Pyramid"
   - Check bold terms across all content files

8. **Cultural Sensitivity & ESL**
   - Flag complex idioms for ESL students
   - Flag Western-specific references without context
   - Check for implicit bias, gendered language
   - Sentence complexity appropriate for ESL

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **CRITICAL** | Must fix | Blocks validation |
| **WARNING** | Should fix | Review needed |
| **SUGGESTION** | Nice to have | Consider |

## Output Format

For each issue found:

```
### [SEVERITY]: [Brief Description]

**Validator:** [Which check found this]
**Location:** Week X > file.md
**Issue:** [Detailed explanation]
**Suggestion:** [How to fix]
```

## Validation Process

1. Read syllabus for LOs and framework schedule
2. Read assessment-handbook.md for rubrics and scenarios
3. For each week, read lecture-content.md, tutorial-content.md, quiz-questions.md
4. Run all 8 checks
5. Report issues grouped by severity
6. Summarize pass/fail status
