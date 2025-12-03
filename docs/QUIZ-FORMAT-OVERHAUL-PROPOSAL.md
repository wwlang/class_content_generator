# Quiz Format Overhaul Proposal

**Date:** 2025-11-29
**Purpose:** Improve quiz question format for parseability and add general feedback support
**Status:** 📋 PROPOSAL

---

## Executive Summary

**Current State:** Quiz questions are stored in markdown with inconsistent field formats requiring complex regex parsing.

**Proposed State:** Structured, machine-parseable format with clear field boundaries and explicit general feedback support.

**Benefits:**
- ✅ Easier to parse (less fragile regex)
- ✅ Supports GIFT general feedback natively
- ✅ Clearer separation between per-option and general feedback
- ✅ More maintainable and extensible
- ✅ Reduces parser workarounds

---

## Current Format Analysis

### Current Multiple Choice Format

```markdown
### Q1: Shannon-Weaver Model Components
**Type:** Multiple Choice
**Category:** Remembering

In the Shannon-Weaver communication model, what is the correct sequence...?

A) Source → Channel → Encoder → Noise → Decoder → Destination
B) Source → Encoder → Channel (with Noise) → Decoder → Destination
C) Encoder → Source → Destination → Decoder → Channel
D) Channel → Source → Encoder → Destination → Decoder

**Answer:** B

**Feedback:**
- **A) Incorrect.** The encoder comes BEFORE the channel...
- **B) Correct!** The Shannon-Weaver model shows...
- **C) Incorrect.** This sequence is completely jumbled...
- **D) Incorrect.** The channel cannot come first...
```

### Problems with Current Format

1. **Per-option feedback parsing is fragile**
   - Requires complex regex: `rf'-\s*\*\*{letter}\)\s*(Correct[^*]*|Incorrect[^*]*)\*\*\s*(.+?)(?=-\s*\*\*[A-D]\)|\Z)'`
   - Breaks if formatting varies slightly
   - Hard to distinguish between "Incorrect." and "Incorrect answer choice."

2. **No general feedback field**
   - Can't add conceptual explanations that apply to the question overall
   - All feedback is tied to specific options

3. **Mixed content and metadata**
   - Question text mixed with options
   - Hard to validate field presence

4. **Inconsistent field names**
   - Week 9 uses `**Category:**`
   - Week 3 uses `**Bloom's Level:**`
   - Parsers need to handle both

---

## GIFT General Feedback

### What is General Feedback?

**General Feedback** in GIFT appears after a student submits an answer, regardless of which option they chose. It provides:
- Conceptual explanation of the topic
- Teaching moment for the underlying concept
- Context that helps students answer similar questions

### GIFT Syntax for General Feedback

**Multiple Choice:**
```gift
::Question Title::Question text{
=Correct answer #Answer-specific feedback
~Wrong answer #Answer-specific feedback
~Wrong answer #Answer-specific feedback
~Wrong answer #Answer-specific feedback
####General feedback shown to all students
}
```

**True/False:**
```gift
::Question Title::Question text{
TRUE #True feedback #False feedback
####General feedback shown to all students
}
```

**Matching:**
```gift
::Question Title::Question text{
=Item 1 -> Match 1
=Item 2 -> Match 2
=Item 3 -> Match 3
####General feedback shown to all students
}
```

**Key:** Four hashes `####` indicate general feedback

---

## Proposed New Format

### Option A: Enhanced Markdown (Minimal Change)

Add explicit `**General Feedback:**` field while keeping current structure:

```markdown
### Q1: Shannon-Weaver Model Components
**Type:** Multiple Choice
**Bloom Level:** Remembering

**Question:**
In the Shannon-Weaver communication model, what is the correct sequence of components through which a message travels?

**Options:**
A) Source → Channel → Encoder → Noise → Decoder → Destination
B) Source → Encoder → Channel (with Noise) → Decoder → Destination
C) Encoder → Source → Destination → Decoder → Channel
D) Channel → Source → Encoder → Destination → Decoder

**Correct Answer:** B

**Option Feedback:**
- **A)** The encoder comes BEFORE the channel, not after. The source must encode the message before transmitting it through the channel.
- **B)** The Shannon-Weaver model shows communication flowing from Source (originates message) → Encoder (converts to signals) → Channel (medium of transmission, where Noise can interfere) → Decoder (interprets signals) → Destination (final recipient).
- **C)** This sequence is completely jumbled. The source must come first, and the destination comes last.
- **D)** The channel cannot come first—there must be a source and encoded message to transmit through it.

**General Feedback:**
The Shannon-Weaver model (1948) is a foundational communication framework. Remember the sequence by thinking of the sender's journey: originate (Source) → encode for transmission (Encoder) → send through medium (Channel, where Noise interferes) → decode at destination (Decoder) → receive (Destination). Understanding this flow helps diagnose where communication breakdowns occur in business contexts.
```

**Changes:**
1. Standardized field name: `**Bloom Level:**` (not Category)
2. Explicit `**Question:**` section
3. Explicit `**Options:**` section
4. Renamed `**Feedback:**` to `**Option Feedback:**` for clarity
5. Removed "Correct!" and "Incorrect." prefixes (implicit from correct answer)
6. Added `**General Feedback:**` field

**Parsing Advantages:**
- Clear field boundaries using `**Field Name:**` markers
- Per-option feedback: `- **A)** explanation` (simpler regex)
- General feedback: everything after `**General Feedback:**` until `---`

---

### Option B: YAML Front Matter (Structured)

Use YAML for metadata, markdown for content:

```markdown
### Q1: Shannon-Weaver Model Components

```yaml
type: multiple_choice
bloom_level: remembering
correct_answer: B
```

**Question:**
In the Shannon-Weaver communication model, what is the correct sequence of components through which a message travels?

**Options:**
- **A)** Source → Channel → Encoder → Noise → Decoder → Destination
- **B)** Source → Encoder → Channel (with Noise) → Decoder → Destination
- **C)** Encoder → Source → Destination → Decoder → Channel
- **D)** Channel → Source → Encoder → Destination → Decoder

**Option Feedback:**
- **A)** The encoder comes BEFORE the channel...
- **B)** The Shannon-Weaver model shows communication flowing...
- **C)** This sequence is completely jumbled...
- **D)** The channel cannot come first...

**General Feedback:**
The Shannon-Weaver model (1948) is a foundational communication framework...
```

**Parsing Advantages:**
- YAML provides structured metadata (type, bloom_level, correct_answer)
- No regex needed for metadata parsing
- Still human-readable and editable

**Disadvantages:**
- More complex to generate
- YAML parsing dependency
- Mixing YAML and markdown

---

### Option C: Full JSON (Machine-First)

```json
{
  "id": "W1-Q1-Shannon-Weaver-Model",
  "week": 1,
  "topic": "Shannon-Weaver Model Components",
  "type": "multiple_choice",
  "bloom_level": "remembering",
  "question_text": "In the Shannon-Weaver communication model, what is the correct sequence of components through which a message travels?",
  "options": {
    "A": "Source → Channel → Encoder → Noise → Decoder → Destination",
    "B": "Source → Encoder → Channel (with Noise) → Decoder → Destination",
    "C": "Encoder → Source → Destination → Decoder → Channel",
    "D": "Channel → Source → Encoder → Destination → Decoder"
  },
  "correct_answer": "B",
  "option_feedback": {
    "A": "The encoder comes BEFORE the channel, not after...",
    "B": "The Shannon-Weaver model shows communication flowing...",
    "C": "This sequence is completely jumbled...",
    "D": "The channel cannot come first..."
  },
  "general_feedback": "The Shannon-Weaver model (1948) is a foundational communication framework. Remember the sequence by thinking of the sender's journey..."
}
```

**Parsing Advantages:**
- Zero regex needed
- Perfect structure validation
- Easy to extend
- Machine-parseable

**Disadvantages:**
- Not human-friendly for editing
- Harder to review in text editor
- JSON syntax errors break parsing

---

## Recommendation: **Option A (Enhanced Markdown)**

### Rationale

1. **Minimal disruption** - Similar to current format, easy migration
2. **Human-readable** - Instructional designers can edit directly
3. **Parse-friendly** - Clear field boundaries reduce regex complexity
4. **Supports general feedback** - New `**General Feedback:**` field
5. **Backwards compatible** - Can parse old format with fallback

### Migration Strategy

**Phase 1: Update Generator**
- Modify quiz question generator to use new format
- Add general feedback generation prompt
- Update templates

**Phase 2: Update Parser**
- Add support for new format in both parsers:
  - `export_quiz_to_gift.py`
  - `assessment_domain/parsers/quiz_markdown_parser.py`
- Maintain backward compatibility with old format

**Phase 3: Regenerate Content**
- Regenerate all 10 weekly quiz files with new format
- Add general feedback to all questions

**Phase 4: Deprecate Old Format**
- Remove backward compatibility after all content migrated

---

## New Format Specification

### Multiple Choice

```markdown
### Q#: [Topic]
**Type:** Multiple Choice
**Bloom Level:** [Remembering|Understanding]

**Question:**
[Question text]

**Options:**
A) [Option A text]
B) [Option B text]
C) [Option C text]
D) [Option D text]

**Correct Answer:** [A|B|C|D]

**Option Feedback:**
- **A)** [Explanation for option A]
- **B)** [Explanation for option B]
- **C)** [Explanation for option C]
- **D)** [Explanation for option D]

**General Feedback:**
[Conceptual explanation that helps students understand the underlying concept and answer similar questions in the future]

---
```

### True/False

```markdown
### Q#: [Topic]
**Type:** True/False
**Bloom Level:** [Remembering|Understanding]

**Question:**
[Question text]

**Correct Answer:** [True|False]

**Option Feedback:**
- **If True:** [Explanation if student answers True]
- **If False:** [Explanation if student answers False]

**General Feedback:**
[Conceptual explanation...]

---
```

### Matching

```markdown
### Q#: [Topic]
**Type:** Matching
**Bloom Level:** [Remembering|Understanding]

**Question:**
[Question text/instruction]

**Items:**
1. [Item 1]
2. [Item 2]
3. [Item 3]

**Matches:**
A) [Match A]
B) [Match B]
C) [Match C]

**Correct Pairs:**
- 1 → [A|B|C]
- 2 → [A|B|C]
- 3 → [A|B|C]

**Pair Feedback:**
- **1-[A|B|C]:** [Explanation for this pairing]
- **2-[A|B|C]:** [Explanation for this pairing]
- **3-[A|B|C]:** [Explanation for this pairing]

**General Feedback:**
[Conceptual explanation...]

---
```

---

## Parser Implementation

### Simplified Parsing Logic

```python
def parse_question(block: str) -> Question:
    """Parse question using clear field boundaries."""

    # Extract metadata
    type_match = re.search(r'\*\*Type:\*\*\s*(.+)', block)
    bloom_match = re.search(r'\*\*Bloom Level:\*\*\s*(.+)', block)

    # Extract question text
    question_match = re.search(
        r'\*\*Question:\*\*\s*\n(.+?)(?=\n\*\*Options:)',
        block, re.DOTALL
    )

    # Extract options
    options = {}
    options_section = re.search(
        r'\*\*Options:\*\*\s*\n(.+?)(?=\n\*\*Correct Answer:)',
        block, re.DOTALL
    )
    for match in re.finditer(r'([A-D])\)\s*(.+)', options_section.group(1)):
        options[match.group(1)] = match.group(2).strip()

    # Extract correct answer
    answer_match = re.search(r'\*\*Correct Answer:\*\*\s*([A-D])', block)

    # Extract per-option feedback (SIMPLE!)
    option_feedback = {}
    feedback_section = re.search(
        r'\*\*Option Feedback:\*\*\s*\n(.+?)(?=\n\*\*General Feedback:)',
        block, re.DOTALL
    )
    for match in re.finditer(
        r'-\s*\*\*([A-D])\)\*\*\s*(.+?)(?=\n\s*-\s*\*\*[A-D]\)|\Z)',
        feedback_section.group(1), re.DOTALL
    ):
        option_feedback[match.group(1)] = match.group(2).strip()

    # Extract general feedback (SIMPLE!)
    general_feedback_match = re.search(
        r'\*\*General Feedback:\*\*\s*\n(.+?)(?=\n---|$)',
        block, re.DOTALL
    )
    general_feedback = general_feedback_match.group(1).strip() if general_feedback_match else ""

    return Question(...)
```

**Benefits:**
- Each field has clear start (`**Field Name:**`) and end (next `**Field Name:**` or `---`)
- No ambiguity in parsing
- Easy to add new fields

---

## GIFT Export with General Feedback

### Multiple Choice Example

```gift
::Shannon-Weaver Model Components::In the Shannon-Weaver communication model, what is the correct sequence of components through which a message travels?{
~Source → Channel → Encoder → Noise → Decoder → Destination #The encoder comes BEFORE the channel, not after. The source must encode the message before transmitting it through the channel.
=Source → Encoder → Channel (with Noise) → Decoder → Destination #The Shannon-Weaver model shows communication flowing from Source (originates message) → Encoder (converts to signals) → Channel (medium of transmission, where Noise can interfere) → Decoder (interprets signals) → Destination (final recipient).
~Encoder → Source → Destination → Decoder → Channel #This sequence is completely jumbled. The source must come first, and the destination comes last.
~Channel → Source → Encoder → Destination → Decoder #The channel cannot come first—there must be a source and encoded message to transmit through it.
####The Shannon-Weaver model (1948) is a foundational communication framework. Remember the sequence by thinking of the sender's journey\: originate (Source) → encode for transmission (Encoder) → send through medium (Channel, where Noise interferes) → decode at destination (Decoder) → receive (Destination). Understanding this flow helps diagnose where communication breakdowns occur in business contexts.
}
```

---

## General Feedback Generation Guidelines

### What Makes Good General Feedback?

1. **Conceptual, not answer-specific**
   - Wrong: "Option B is correct because..."
   - Right: "The Shannon-Weaver model describes the flow of communication..."

2. **Helps with transfer learning**
   - Provides framework for answering similar questions
   - Explains the "why" behind the concept

3. **Concise but complete**
   - 2-4 sentences
   - 50-150 words

4. **Includes memory aids**
   - Mnemonics
   - Visual imagery
   - Analogies

### General Feedback Templates by Bloom Level

**Remembering Questions:**
```
[Concept name] is [definition]. The key components are [list].
Remember this by [mnemonic/analogy]. This framework is used in
business communication to [practical application].
```

**Understanding Questions:**
```
This question tests [skill/concept]. The key distinction is between
[X] and [Y]. [X] focuses on [aspect], while [Y] emphasizes [aspect].
In practice, you can apply this by [example scenario].
```

---

## Implementation Plan

### Step 1: Update Quiz Generation Skill (2-3 hours)

**File:** `.claude/skills/assessment-design/tutorial-activities.md`

Add general feedback section to generation instructions:

```markdown
## General Feedback Guidelines

For each question, provide general feedback that:
1. Explains the underlying concept
2. Helps students answer similar questions
3. Provides memory aids or frameworks
4. Is 50-150 words

Format: **General Feedback:** [explanation]
```

### Step 2: Create Format Migration Script (1-2 hours)

**File:** `tools/migrate_quiz_format.py`

Script to convert old format to new format:
- Parse old format questions
- Generate general feedback using LLM
- Output new format

### Step 3: Update Parsers (2-3 hours)

**Files:**
- `tools/export_quiz_to_gift.py`
- `tools/assessment_domain/parsers/quiz_markdown_parser.py`

Add:
- New format parsing logic
- General feedback extraction
- GIFT general feedback export (`####`)
- Backward compatibility

### Step 4: Regenerate All Quizzes (3-4 hours)

- Run migration script on all 10 weeks
- Review generated general feedback
- Manual polish if needed

### Step 5: Validation (1 hour)

- Export all quizzes to GIFT
- Import to Moodle staging
- Test general feedback display
- Verify both per-option and general feedback show correctly

---

## Total Effort Estimate

**Initial Implementation:** 9-13 hours
- Format specification: Done (this document)
- Generator update: 2-3 hours
- Migration script: 1-2 hours
- Parser updates: 2-3 hours
- Content regeneration: 3-4 hours
- Testing and validation: 1 hour

**Ongoing Benefit:**
- Easier quiz maintenance
- Less parser debugging
- Better student learning outcomes
- Consistent format across all courses

---

## Questions for Decision

1. **Do we want general feedback?**
   - YES → Proceed with Option A
   - NO → Still recommend Option A for parseability improvements

2. **Do we regenerate all existing quizzes?**
   - YES → Budget 3-4 hours for regeneration + review
   - NO → Use new format for future quizzes only

3. **Backward compatibility period?**
   - Keep old format parser for 1 month during migration?
   - Or hard cutover?

4. **LLM-generated general feedback?**
   - Auto-generate using LLM + review?
   - Or manual writing only?

---

## Recommendation Summary

✅ **Adopt Option A: Enhanced Markdown Format**
✅ **Add general feedback field**
✅ **Regenerate all 10 weekly quizzes with new format**
✅ **Use LLM to generate initial general feedback + manual review**
✅ **Maintain backward compatibility for 1 migration cycle**

**Next Steps:**
1. Get approval on format specification
2. Update quiz generation skill
3. Create migration script
4. Update parsers with new format support
5. Regenerate Week 1 as pilot
6. Review and validate
7. Regenerate Weeks 2-10
8. Re-export and re-package

---

**End of Proposal**
