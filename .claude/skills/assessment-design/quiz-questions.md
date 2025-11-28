# Quiz Questions Skill

## Authoring Quiz Questions

Quiz questions derive from **lecture content**, not tutorial activities. Create `quiz-questions.md` in the week folder before exporting to GIFT format.

### File Template

```markdown
# Week [N] Quiz Questions

**Topic:** [Week topic from syllabus]
**Prepares for:** Quiz [1/2/3] (Week [X])
**Source:** lecture-content.md key concepts

---

## Questions

### Q1: [Concept Name]
**Type:** Multiple Choice

[Question text - scenario-based preferred]

A) [Option]
B) [Option]
C) [Option]
D) [Option]

**Answer:** [Letter]
**Feedback:** [Why correct, what incorrect options miss]

---

### Q2: [Concept Name]
**Type:** True/False

[Statement to evaluate]

**Answer:** True/False
**Feedback:** [Explanation]

[Repeat for 5-8 questions total]
```

### Source Material

Pull questions from:
- Lecture slide key concepts and frameworks
- Week learning objectives (from syllabus)
- Assessment schedule (to know which quiz this prepares for)

Do NOT pull from:
- Tutorial activities (those practice assessment skills, not quiz content)
- Tutor notes (facilitation guidance, not source material)

---

## Question Types 🔐

| Type | When to Use | Example |
|------|-------------|---------|
| Multiple choice | Concept recognition | "Which principle does this illustrate?" |
| True/False | Common misconceptions | "Email is always the best channel for urgent messages." |
| Matching | Term/definition pairs | Match framework components to descriptions |
| Short answer | Key term recall | "Name two of Cialdini's principles" |

## Question Quality Rules

**Good questions:**
- Test understanding, not memorization
- Have one clearly correct answer
- Use scenarios/examples from lecture
- Include plausible distractors

**Bad questions:**
- Trick questions or wordplay
- "All of the above" / "None of the above"
- Double negatives
- Trivial details not covered in lecture

## Bad → Good Transformation

**Bad question:**
```
What did Cialdini say about reciprocity?
a) It's important
b) It's the first principle
c) People feel obligated to return favors
d) All of the above
```
Problems: Vague, "all of the above," tests recall not understanding

**Good question:**
```
A sales representative sends a free sample before asking for a meeting.
Which principle of persuasion is being applied?
a) Authority - establishing expertise
b) Reciprocity - creating obligation through giving
c) Scarcity - implying limited availability
d) Social proof - showing others have bought
```
Better: Scenario-based, clear correct answer, plausible distractors

## GIFT Format (Moodle) 🔒

```gift
// Multiple Choice
::Question Title:: What is the primary purpose of X? {
  =Correct answer
  ~Wrong answer with feedback#Feedback for wrong answer
  ~Another wrong answer#Why this is incorrect
}

// True/False
::TF Question:: Statement to evaluate. {TRUE#Correct! Here's why.#Actually, this is true because...}

// Short Answer
::Short Question:: What term describes X? {=answer1 =answer2}
```

## Feedback Requirements

Every answer option needs feedback:
- **Correct:** Reinforce why it's right
- **Incorrect:** Explain the misconception, point to correct concept

## Quiz Structure (5-8 Questions)

| Bloom's Level | Question Type | Count |
|---------------|---------------|-------|
| **Remember** | Concept recognition (MC), matching, short answer | 2-4 |
| **Understand** | Application scenarios (MC), true/false misconceptions | 2-4 |

1. 2-3 concept recognition (MC) - Remember
2. 1-2 application scenarios (MC) - Understand
3. 1-2 true/false on misconceptions - Understand
4. 1 matching or short answer - Remember

**Time:** 15-20 min for students to complete with review

> **Note:** For quiz consolidation, questions are categorized as "Remembering" or "Understanding" to match `/consolidate-quiz` CLI.
