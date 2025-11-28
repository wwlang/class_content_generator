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
**Category:** Remembering OR Understanding

[Question text]

A) [Option]
B) [Option]
C) [Option]
D) [Option]

**Answer:** [Letter]

**Feedback:**
- **A) Incorrect.** [Why this is wrong]
- **B) Correct!** [Why this is right]
- **C) Incorrect.** [Why this is wrong]
- **D) Incorrect.** [Why this is wrong]

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

**Bad question (vague, "all of the above"):**
```
What did Cialdini say about reciprocity?
a) It's important
b) It's the first principle
c) People feel obligated to return favors
d) All of the above
```
Problems: Vague options, "all of the above," unclear what's being tested

**Good Remembering question:**
```
According to Cialdini, what is the core mechanism of the reciprocity principle?
a) People follow what others are doing
b) People feel obligated to return favors after receiving something
c) People comply with requests from authority figures
d) People value things more when they are scarce
```
Better: Clear definition recall, plausible distractors from other principles

**Good Understanding question:**
```
Why does the reciprocity principle work, according to Cialdini?
a) People want to appear consistent with their past behavior
b) People feel uncomfortable owing others and want to balance the exchange
c) People trust experts more than non-experts
d) People fear missing out on opportunities
```
Better: Tests understanding of WHY, not just WHAT

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

## Quiz Structure (10 Questions)

| Bloom's Level | Question Type | Count |
|---------------|---------------|-------|
| **Remembering** | Definitions, sequences, identification, matching | 5 |
| **Understanding** | Explaining why, distinguishing concepts, interpreting | 5 |

**Recommended mix (10 questions):**
1. 2-3 definition/recall questions (MC) - Remembering
2. 1-2 sequence/component identification questions - Remembering
3. 1 matching question (counts as 1) - Remembering
4. 2 true/false testing misconceptions - Understanding
5. 2-3 "what is the purpose/why" questions - Understanding

**Time:** 20-25 min for students to complete with review

---

## Bloom's Level Examples 🔐

**REMEMBERING questions ask students to recall facts, definitions, sequences:**

```markdown
### Good Remembering Question
What do the letters M, K, and S stand for in the MKS model?
A) Message, Knowledge, Source
B) Motivation, Knowledge, Skills  ← Correct
C) Medium, Key concepts, Strategy
D) Method, Knowing, Speaking
```

```markdown
### Good Remembering Question (Matching)
Match each level of communication problem to its definition:
1. Technical level → How accurately can symbols be transmitted?
2. Semantic level → How precisely do symbols convey intended meaning?
3. Effectiveness level → How effectively does meaning affect behavior?
```

```markdown
### Good Remembering Question (NOT format)
Which of the following is NOT one of Gallo's four leadership communication strategies?
A) Use short words to talk about hard things
B) Choose sticky metaphors
C) Use technical jargon to establish expertise  ← Correct (opposite of strategy 1)
D) Make mission your mantra
```

**UNDERSTANDING questions ask students to explain, interpret, or distinguish:**

```markdown
### Good Understanding Question (Explaining purpose)
What is the primary purpose of "humanizing data" in leadership communication?
A) To make statistics sound more impressive
B) To connect numbers to human impact so audiences care  ← Correct
C) To hide negative data behind positive stories
D) To simplify data for less educated audiences
```

```markdown
### Good Understanding Question (True/False misconception)
In the Shannon-Weaver model, "noise" refers only to physical sounds.
Answer: False
(Tests whether student understands noise includes semantic and psychological interference)
```

```markdown
### Good Understanding Question (Distinguishing concepts)
In the MKS model, which dimension includes BOTH desire AND confidence?
A) Knowledge
B) Skills
C) Motivation  ← Correct
D) Context
```

**BAD questions (too scenario-heavy for Remember/Understand):**

```markdown
### Bad Question (Application level, not Remember/Understand)
A manager sends an email with technical jargon and employees don't understand.
Using Shannon-Weaver, diagnose the problem and recommend a fix.
→ This is "Apply" level, not appropriate for weekly quiz
```

> **Rule:** Scenarios should be brief and used only to provide context for Understanding questions—not to test problem-solving or application skills (that's for tutorials and assessments).

> **Note:** For quiz consolidation, questions are categorized as "Remembering" or "Understanding" to match `/consolidate-quiz` CLI.
