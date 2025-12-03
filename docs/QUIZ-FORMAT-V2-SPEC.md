# Quiz Format Specification v2.0

**Version:** 2.0
**Status:** ✅ APPROVED
**Replaces:** Markdown format v1.0
**Effective Date:** 2025-11-29

---

## Overview

This specification defines the YAML frontmatter format for quiz questions used in the Class Content Generator system. This format is designed for:

- **Machine parseability** - Zero regex, structured data
- **Type safety** - Pydantic validation
- **General feedback** - GIFT `####` syntax support
- **Extensibility** - Easy to add new fields
- **Human readability** - Clear structure, easy to edit

---

## Core Principles

1. **YAML Frontmatter** - All quiz data in YAML block at file start
2. **Single Source of Truth** - Pydantic schemas validate format
3. **Zero Regex Parsing** - Use `python-frontmatter` library
4. **Explicit Fields** - No implicit data, all fields declared
5. **General Feedback Required** - All questions must include general feedback

---

## File Structure

```yaml
---
metadata:
  week: [1-10]
  topic: "[Week topic from syllabus]"
  prepares_for: "[Assessment name]"
  source: "lecture-content.md"

questions:
  - [Question object]
  - [Question object]
  - ...
---
```

**After frontmatter:** No content required (all data in YAML)

---

## Question Types

### 1. Multiple Choice

**Format:**

```yaml
- id: "W2-Q1-freeman-definition"
  type: "multiple_choice"
  bloom_level: "remembering"
  topic: "Freeman's Stakeholder Definition"

  question: |
    According to R. Edward Freeman (1984), what is a stakeholder?

  options:
    - key: "A"
      text: "Any individual or group who owns shares in a company"
      feedback: "This describes shareholders only, not stakeholders. Freeman's definition is much broader and includes anyone who affects or is affected by the organization."

    - key: "B"
      text: "Any group or individual who can affect or is affected by the achievement of the organization's objectives"
      feedback: "Freeman's 1984 definition includes bidirectional influence—stakeholders both affect and are affected by the organization. This broad view was revolutionary in moving beyond shareholder primacy."
      correct: true

    - key: "C"
      text: "Only customers and employees who directly interact with the company"
      feedback: "This is too narrow. Freeman includes indirect stakeholders like communities, suppliers, and even competitors in his framework."

    - key: "D"
      text: "Government regulators and legal entities only"
      feedback: "Regulators are one type of stakeholder, but Freeman's definition encompasses far more groups including customers, employees, suppliers, and communities."

  general_feedback: |
    Freeman's stakeholder theory (1984) was revolutionary because it expanded management thinking beyond shareholders to include all groups with a stake in organizational decisions. The key insight is **bidirectional influence**—stakeholders both affect (e.g., customers buying products) and are affected by (e.g., employees receiving wages) organizational actions. In your Group Presentation (Assessment 3), you'll apply this framework to identify and analyze stakeholders for a business communication scenario. Review Week 2 slides 15-22 for stakeholder mapping techniques.
```

**Field Requirements:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `id` | string | ✅ | Pattern: `W\d+-Q\d+-[\w-]+` |
| `type` | string | ✅ | Must be `"multiple_choice"` |
| `bloom_level` | string | ✅ | `"remembering"` or `"understanding"` |
| `topic` | string | ✅ | 5-100 characters |
| `question` | string | ✅ | 20-1000 characters |
| `options` | array | ✅ | Exactly 4 options |
| `general_feedback` | string | ✅ | 50-1000 characters |

**Option Requirements:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `key` | string | ✅ | Must be `A`, `B`, `C`, or `D` |
| `text` | string | ✅ | 10-500 characters |
| `feedback` | string | ✅ | 20-500 characters |
| `correct` | boolean | Optional | Default: `false` |

**Constraints:**
- Exactly 4 options (A, B, C, D)
- Exactly 1 option with `correct: true`
- Options must be in A, B, C, D order
- No duplicate keys

---

### 2. True/False

**Format:**

```yaml
- id: "W8-Q5-passive-voice-always-bad"
  type: "true_false"
  bloom_level: "understanding"
  topic: "Passive Voice Usage"

  question: |
    True or False: Passive voice should always be avoided in business writing.

  correct_answer: false

  feedback:
    if_true: "This is a common misconception. While active voice is generally preferred for clarity and directness, passive voice has legitimate uses in business writing—such as when the action is more important than the actor (e.g., 'The report was submitted on time') or when you want to diplomatically avoid assigning blame (e.g., 'An error was made in the calculation')."

    if_false: "While passive voice is often overused, it has legitimate applications in business writing. Use passive voice strategically when: (1) the action matters more than who did it, (2) the actor is unknown or obvious, or (3) you want to soften criticism. The key is conscious choice, not blanket avoidance."

  general_feedback: |
    The passive voice debate in business writing is about **strategic choice**, not absolute rules. Week 8 slides 28-31 cover the "Passive Voice Decision Tree"—use it to decide when passive voice serves your communication goals (e.g., emphasizing results over responsibility) versus when active voice creates clearer, more direct messages. In your Business Memo (Assessment 1), you'll make these voice choices based on tone and audience expectations.
```

**Field Requirements:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `id` | string | ✅ | Pattern: `W\d+-Q\d+-[\w-]+` |
| `type` | string | ✅ | Must be `"true_false"` |
| `bloom_level` | string | ✅ | `"remembering"` or `"understanding"` |
| `topic` | string | ✅ | 5-100 characters |
| `question` | string | ✅ | 20-1000 characters |
| `correct_answer` | boolean | ✅ | `true` or `false` |
| `feedback` | object | ✅ | Must have `if_true` and `if_false` |
| `general_feedback` | string | ✅ | 50-1000 characters |

**Feedback Object Requirements:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `if_true` | string | ✅ | 20-500 characters |
| `if_false` | string | ✅ | 20-500 characters |

---

### 3. Matching

**Format:**

```yaml
- id: "W3-Q6-communication-models-match"
  type: "matching"
  bloom_level: "remembering"
  topic: "Communication Models"

  question: |
    Match each communication model to its key distinguishing feature.

  pairs:
    - item: "Shannon-Weaver Model"
      match: "Focuses on technical transmission and noise"
      item_key: "1"
      match_key: "A"
      feedback: "The Shannon-Weaver model (1948) was developed by engineers for telecommunications, emphasizing signal transmission, encoding/decoding, and interference (noise). It's linear and technical."

    - item: "Schramm's Model"
      match: "Emphasizes shared field of experience"
      item_key: "2"
      match_key: "B"
      feedback: "Wilbur Schramm's model (1954) introduced the concept of overlapping 'fields of experience'—the idea that effective communication requires shared context, culture, and knowledge between sender and receiver."

    - item: "Berlo's SMCR Model"
      match: "Breaks communication into Source-Message-Channel-Receiver"
      item_key: "3"
      match_key: "C"
      feedback: "David Berlo's SMCR model (1960) systematically analyzes each component of communication (Source skills/attitudes, Message elements, Channel selection, Receiver capabilities) to identify potential breakdowns."

  general_feedback: |
    These three models represent the evolution of communication theory from technical (Shannon-Weaver) to psychological (Schramm) to systematic analysis (Berlo). Each model helps diagnose different communication problems: Shannon-Weaver for clarity issues, Schramm for cultural misunderstandings, and Berlo for comprehensive communication planning. Week 3 slides 8-18 compare these models visually. You'll apply model selection in your Executive Summary (Assessment 2) when analyzing communication strategies.
```

**Field Requirements:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `id` | string | ✅ | Pattern: `W\d+-Q\d+-[\w-]+` |
| `type` | string | ✅ | Must be `"matching"` |
| `bloom_level` | string | ✅ | `"remembering"` or `"understanding"` |
| `topic` | string | ✅ | 5-100 characters |
| `question` | string | ✅ | 20-1000 characters |
| `pairs` | array | ✅ | 3-6 pairs |
| `general_feedback` | string | ✅ | 50-1000 characters |

**Pair Requirements:**

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `item` | string | ✅ | 5-200 characters |
| `match` | string | ✅ | 5-200 characters |
| `item_key` | string | ✅ | Must be `"1"`, `"2"`, `"3"`, etc. |
| `match_key` | string | ✅ | Must be `"A"`, `"B"`, `"C"`, etc. |
| `feedback` | string | ✅ | 20-500 characters |

**Constraints:**
- 3-6 pairs (recommended: 3-4 for clarity)
- `item_key` must be sequential integers as strings: `"1"`, `"2"`, `"3"`
- `match_key` must be sequential letters as strings: `"A"`, `"B"`, `"C"`
- Each pair has dedicated feedback explaining why that pairing is correct

---

## General Feedback Guidelines

General feedback appears to ALL students after submitting an answer, regardless of whether they answered correctly. It serves a different purpose than per-option feedback.

### Purpose

1. **Explain the underlying concept** - Not just why an answer is right/wrong
2. **Aid transfer learning** - Help students answer similar questions in the future
3. **Point to resources** - Reference specific lecture slides, readings, or assessments
4. **Provide memory aids** - Mnemonics, frameworks, analogies

### Quality Criteria

| Criterion | Requirement |
|-----------|-------------|
| **Length** | 50-1000 characters (aim for 100-200 words) |
| **Structure** | 2-4 sentences |
| **Conceptual** | Explains "why" behind the concept |
| **Actionable** | Points to specific study resources |
| **Connected** | Links to assessments or practical application |

### Template by Bloom Level

**Remembering Questions:**
```
[Concept name] is [definition]. The key components/features are [list].
Remember this by [mnemonic/analogy/visual]. This concept appears in
[lecture week/slides] and will be applied in [assessment name].
```

**Understanding Questions:**
```
This question tests [skill/distinction]. The key difference between [X] and [Y]
is [explanation]. In practice, you would apply this by [example scenario].
Review [lecture slides] for the [framework/model name] and see how it's used
in [assessment].
```

### Examples

**Good General Feedback:**
```
Freeman's stakeholder theory (1984) was revolutionary because it expanded
management thinking beyond shareholders to include all groups with a stake in
organizational decisions. The key insight is bidirectional influence—stakeholders
both affect (e.g., customers buying products) and are affected by (e.g., employees
receiving wages) organizational actions. In your Group Presentation (Assessment 3),
you'll apply this framework to identify and analyze stakeholders for a business
communication scenario. Review Week 2 slides 15-22 for stakeholder mapping techniques.
```

**Poor General Feedback (too answer-specific):**
```
The correct answer is B because Freeman defined stakeholders broadly.
```

**Poor General Feedback (too vague):**
```
Stakeholder theory is important in business communication.
```

---

## Metadata Fields

### Document-Level Metadata

```yaml
metadata:
  week: 2
  topic: "Stakeholder Analysis and Audience Adaptation"
  prepares_for: "Quiz 1 (Week 11)"
  source: "lecture-content.md"
```

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `week` | integer | ✅ | 1-12 |
| `topic` | string | ✅ | Must match syllabus week topic |
| `prepares_for` | string | ✅ | Assessment name from syllabus |
| `source` | string | ✅ | Usually `"lecture-content.md"` |

---

## Bloom's Taxonomy Levels

Only two levels are used for quiz questions:

### Remembering (Lower-Order)

**Definition:** Recall facts, terms, definitions, models

**Question Verbs:**
- Define, identify, list, name, state, describe, recognize, recall

**Example:**
```
According to R. Edward Freeman (1984), what is a stakeholder?
```

**General Feedback Focus:**
- Define the concept clearly
- Provide memory aids (mnemonics, acronyms)
- Point to specific lecture slides with definitions

---

### Understanding (Lower-Order)

**Definition:** Explain concepts, compare/contrast, interpret, apply frameworks

**Question Verbs:**
- Explain, compare, contrast, distinguish, interpret, classify, exemplify

**Example:**
```
What is the key difference between stakeholder mapping and stakeholder salience?
```

**General Feedback Focus:**
- Explain the distinction or relationship
- Provide decision frameworks
- Show practical application examples

---

## GIFT Export Mapping

### Multiple Choice → GIFT

**YAML:**
```yaml
question: "What is a stakeholder?"
options:
  - key: "A"
    text: "A shareholder"
    feedback: "Too narrow..."
  - key: "B"
    text: "Anyone affected..."
    feedback: "Correct definition..."
    correct: true
general_feedback: "Freeman's theory expanded..."
```

**GIFT Output:**
```gift
::Freeman's Stakeholder Definition::What is a stakeholder?{
~A shareholder #Too narrow...
=Anyone affected... #Correct definition...
####Freeman's theory expanded...
}
```

**Key Mappings:**
- `=` prefix for correct option (`correct: true`)
- `~` prefix for incorrect options
- `#` per-option feedback
- `####` general feedback (4 hashes)

---

### True/False → GIFT

**YAML:**
```yaml
question: "Passive voice should always be avoided."
correct_answer: false
feedback:
  if_true: "Common misconception..."
  if_false: "Correct, passive has uses..."
general_feedback: "Strategic choice, not absolute rule..."
```

**GIFT Output:**
```gift
::Passive Voice Usage::Passive voice should always be avoided.{
FALSE #Correct, passive has uses... #Common misconception...
####Strategic choice, not absolute rule...
}
```

**Key Mappings:**
- `TRUE` or `FALSE` correct answer
- First `#` = correct answer feedback
- Second `#` = incorrect answer feedback
- `####` general feedback

---

### Matching → GIFT

**YAML:**
```yaml
pairs:
  - item: "Shannon-Weaver"
    match: "Technical transmission"
    feedback: "Developed by engineers..."
  - item: "Schramm"
    match: "Shared experience"
    feedback: "Overlapping fields..."
general_feedback: "Evolution from technical to psychological..."
```

**GIFT Output:**
```gift
::Communication Models::Match each model to its feature.{
=Shannon-Weaver -> Technical transmission #Developed by engineers...
=Schramm -> Shared experience #Overlapping fields...
####Evolution from technical to psychological...
}
```

**Key Mappings:**
- `=Item -> Match` format
- `#` per-pair feedback
- `####` general feedback

---

## Validation Layers

All questions pass through 4 validation layers before export:

### Layer 1: Format Validation (Pydantic Schemas)

**Validates:**
- Required fields present
- Field types correct (string, int, boolean, array)
- String lengths within bounds
- Pattern matching (e.g., ID format)
- Enum values (e.g., bloom_level must be "remembering" or "understanding")

**Blocks Export:** ✅ YES (errors prevent export)

---

### Layer 2: Content Quality Validation

**Validates:**
- Feedback explains WHY, not just right/wrong
- No prohibited phrases ("all of the above", "none of the above")
- Question clarity (no ambiguous wording)
- Option distinctiveness (no near-duplicates)
- General feedback length and structure

**Blocks Export:** ⚠️ WARNINGS (should fix but not blocking)

---

### Layer 3: Pedagogical Validation

**Validates:**
- Bloom level matches question verb
- Distractors are plausible (wrong but tempting)
- Feedback references lecture resources
- General feedback aids transfer learning
- Question aligns with assessment preparation

**Blocks Export:** ℹ️ INFO (suggestions for improvement)

---

### Layer 4: GIFT Export Validation

**Validates:**
- GIFT syntax correctness
- Special character escaping
- Round-trip validation (export → re-import → compare)
- Moodle compatibility

**Blocks Export:** ✅ YES (export errors prevent deployment)

---

## Migration from v1.0 to v2.0

### Automated Conversion

The migration script `tools/migrate_quiz_format.py` handles:

1. **Parse v1.0 markdown** using old regex-based parser
2. **Generate general feedback** using LLM with prompt template
3. **Convert to v2.0 YAML** using Pydantic schemas
4. **Validate output** through all 4 layers
5. **Output report** of issues requiring manual review

### Manual Review Checklist

After automated migration, review:

- [ ] General feedback is conceptual (not answer-specific)
- [ ] General feedback references correct lecture slides
- [ ] General feedback mentions relevant assessment
- [ ] General feedback length is 50-200 words
- [ ] All validation warnings addressed

### LLM General Feedback Generation

**Prompt Template:**
```
Generate general feedback (50-150 words) for this quiz question.

**Question:** {question_text}
**Topic:** {topic}
**Bloom Level:** {bloom_level}
**Week:** {week}
**Prepares For:** {assessment}

General feedback should:
1. Explain the underlying concept (not just the answer)
2. Help students answer similar questions in the future
3. Reference specific lecture resources (Week {week}, slides X-Y)
4. Connect to {assessment} practical application
5. Provide memory aids or frameworks if applicable

General feedback:
```

---

## File Naming Convention

**Weekly Quizzes:**
- Format: `quiz-questions.md`
- Location: `courses/{COURSE_CODE}/weeks/week-{NN}/quiz-questions.md`
- Example: `courses/BCI2AU-business-communication/weeks/week-02/quiz-questions.md`

**Final Quiz Banks:**
- Format: `final-quiz-bank.md`
- Location: `courses/{COURSE_CODE}/assessments/final-quiz-bank.md`
- Example: `courses/BCI2AU-business-communication/assessments/final-quiz-bank.md`

---

## Complete Example File

```yaml
---
metadata:
  week: 2
  topic: "Stakeholder Analysis and Audience Adaptation"
  prepares_for: "Quiz 1 (Week 11)"
  source: "lecture-content.md"

questions:
  - id: "W2-Q1-freeman-definition"
    type: "multiple_choice"
    bloom_level: "remembering"
    topic: "Freeman's Stakeholder Definition"

    question: |
      According to R. Edward Freeman (1984), what is a stakeholder?

    options:
      - key: "A"
        text: "Any individual or group who owns shares in a company"
        feedback: "This describes shareholders only, not stakeholders. Freeman's definition is much broader and includes anyone who affects or is affected by the organization."

      - key: "B"
        text: "Any group or individual who can affect or is affected by the achievement of the organization's objectives"
        feedback: "Freeman's 1984 definition includes bidirectional influence—stakeholders both affect and are affected by the organization. This broad view was revolutionary in moving beyond shareholder primacy."
        correct: true

      - key: "C"
        text: "Only customers and employees who directly interact with the company"
        feedback: "This is too narrow. Freeman includes indirect stakeholders like communities, suppliers, and even competitors in his framework."

      - key: "D"
        text: "Government regulators and legal entities only"
        feedback: "Regulators are one type of stakeholder, but Freeman's definition encompasses far more groups including customers, employees, suppliers, and communities."

    general_feedback: |
      Freeman's stakeholder theory (1984) was revolutionary because it expanded management thinking beyond shareholders to include all groups with a stake in organizational decisions. The key insight is **bidirectional influence**—stakeholders both affect (e.g., customers buying products) and are affected by (e.g., employees receiving wages) organizational actions. In your Group Presentation (Assessment 3), you'll apply this framework to identify and analyze stakeholders for a business communication scenario. Review Week 2 slides 15-22 for stakeholder mapping techniques.

  - id: "W2-Q2-stakeholder-vs-shareholder"
    type: "true_false"
    bloom_level: "understanding"
    topic: "Stakeholder vs. Shareholder Primacy"

    question: |
      True or False: Stakeholder theory argues that maximizing shareholder value should be a company's only objective.

    correct_answer: false

    feedback:
      if_true: "This describes shareholder primacy (Milton Friedman's view), not stakeholder theory. Freeman's stakeholder theory explicitly challenges this narrow focus, arguing that companies must balance the interests of all stakeholders—employees, customers, suppliers, communities—not just shareholders."

      if_false: "Stakeholder theory directly challenges shareholder primacy. While Friedman (1970) argued profit maximization for shareholders is the sole corporate responsibility, Freeman (1984) countered that companies must balance multiple stakeholder interests. This debate continues in modern corporate governance discussions about ESG (Environmental, Social, Governance) responsibilities."

    general_feedback: |
      The stakeholder vs. shareholder debate is central to business ethics and corporate strategy. Shareholder primacy (Friedman) = maximize profits for owners. Stakeholder theory (Freeman) = balance interests of all affected groups. Modern corporations increasingly adopt stakeholder approaches through ESG frameworks, recognizing that long-term success requires satisfying customers, retaining employees, and maintaining community trust—not just quarterly earnings. Your Persuasive Proposal (Assessment 4) will require stakeholder analysis to build a compelling business case. See Week 2 slides 23-27 for stakeholder vs. shareholder comparison.

  - id: "W2-Q3-communication-models"
    type: "matching"
    bloom_level: "remembering"
    topic: "Communication Models"

    question: |
      Match each communication model to its key distinguishing feature.

    pairs:
      - item: "Shannon-Weaver Model"
        match: "Focuses on technical transmission and noise"
        item_key: "1"
        match_key: "A"
        feedback: "The Shannon-Weaver model (1948) was developed by engineers for telecommunications, emphasizing signal transmission, encoding/decoding, and interference (noise). It's linear and technical."

      - item: "Schramm's Model"
        match: "Emphasizes shared field of experience"
        item_key: "2"
        match_key: "B"
        feedback: "Wilbur Schramm's model (1954) introduced the concept of overlapping 'fields of experience'—the idea that effective communication requires shared context, culture, and knowledge between sender and receiver."

      - item: "Berlo's SMCR Model"
        match: "Breaks communication into Source-Message-Channel-Receiver"
        item_key: "3"
        match_key: "C"
        feedback: "David Berlo's SMCR model (1960) systematically analyzes each component of communication (Source skills/attitudes, Message elements, Channel selection, Receiver capabilities) to identify potential breakdowns."

    general_feedback: |
      These three models represent the evolution of communication theory from technical (Shannon-Weaver) to psychological (Schramm) to systematic analysis (Berlo). Each model helps diagnose different communication problems: Shannon-Weaver for clarity issues, Schramm for cultural misunderstandings, and Berlo for comprehensive communication planning. Week 2 slides 8-18 compare these models visually. You'll apply model selection in your Executive Summary (Assessment 2) when analyzing communication strategies.
---
```

---

## Dependencies

**Python Libraries:**
```bash
pip install pydantic python-frontmatter pyyaml
```

**Versions:**
- `pydantic>=2.0` (v2.x required for updated validation features)
- `python-frontmatter>=1.0.0`
- `pyyaml>=6.0`

---

## Related Documentation

- **Implementation Plan:** `/Users/williamlang/.claude/plans/shimmying-marinating-meadow.md`
- **Pydantic Schemas:** `tools/assessment_domain/schemas/quiz_schema.py` (to be created)
- **Structured Parser:** `tools/assessment_domain/parsers/structured_quiz_parser.py` (to be created)
- **Migration Script:** `tools/migrate_quiz_format.py` (to be created)
- **Validation Framework:** `tools/assessment_domain/validators/` (to be created)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2025-11-29 | Initial v2.0 specification with YAML frontmatter format |
| 1.0 | 2025-11-01 | Legacy markdown format (deprecated) |

---

**End of Specification**
