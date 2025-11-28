---
name: assessment-design
description: Design aligned tutorials, quizzes, and activities that prepare students for graded assessments
version: 2.0.0
---

# Assessment Design Skill

Create tutorials and quizzes that directly prepare students for success on graded work.

## When to Invoke

Auto-invoke when:
- `/generate-week [N]` is called (tutorial/quiz portion)
- User asks to create tutorial content
- User asks about quiz questions or GIFT format

## Sub-Skills (Load as Needed)

| Need | Load |
|------|------|
| Tutorial structure | `tutorial-activities.md` |
| Quiz question writing | `quiz-questions.md` |

## Core Principle: Assessment Alignment 🔒

Every tutorial activity directly practices skills from the upcoming graded assessment:
- Reference **Assessment Handbook** for full rubric (don't duplicate)
- Students practice with **same format** they'll be graded on
- Class feedback uses **rubric language**

*This principle is non-negotiable—tutorials exist to prepare for assessments.*

## Tutorial Structure (90 min) 🔐

| Phase | Time | Purpose |
|-------|------|---------|
| Quick Review | 5 min | Lecture recap + success criteria |
| Main activity | 75 min | ONE task with deliverable + class feedback |
| Before Next Class | 10 min | 3 items only: quiz, prereading, save work |

*Quiz questions authored separately in quiz-questions.md*
*Full rubrics in Assessment Handbook (not repeated in tutorial)*
*Timing details in tutor-notes only (not in student-facing content)*

## Outputs

- `tutorial-content.md` - Student-facing activities (~80 lines)
- `tutorial-tutor-notes.md` - Timing table, facilitation guide, valid approaches
- `quiz-questions.md` - Human-readable quiz questions with answers
- `week-N-quiz.gift` - Moodle GIFT format quiz (exported from quiz-questions.md)
