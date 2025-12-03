# Writing Instructions Skill

How to write effective skills, commands, and prompts for this project.

## Core Rules

### 1. Only Add What Claude Doesn't Know
Claude already knows: APA format, Bloom's taxonomy, what speaker notes are, basic pedagogy.

**Delete:** "Speaker notes guide the instructor through each slide."
**Keep:** "Structure: Opening → Key Points → Example → Check → Transition"

### 2. 50 Tokens Beats 150 Tokens
A concrete example beats verbose prose.

**Before (verbose):**
```markdown
When writing speaker notes, you should ensure that each note follows a
consistent structure that includes an opening transition, the key points
to emphasize, an example or story, a check for understanding, and a
transition to the next slide.
```

**After (concrete):**
```markdown
## Speaker Notes Structure
Opening → Key Points (3-5) → Example → Check Understanding → Transition
```

### 3. Freedom Levels

Mark sections by how strictly they must be followed:

| Marker | Meaning | Example |
|--------|---------|---------|
| 🔒 | Exact syntax required | GIFT format, file paths |
| 🔐 | Follow pattern, vary content | Slide structure, rubric format |
| 🔓 | Adapt freely | Examples, engagement activities |

**Example usage:**
```markdown
## GIFT Format 🔒
::Question:: What is X? {=correct ~wrong}

## Lecture Structure 🔐
Opening (4-6) → Core (14-20) → Wrap-up (4-6)

## Vietnamese Examples 🔓
Use local businesses, cultural contexts as appropriate
```

### 4. Concrete Examples Required

Every skill needs at least one filled-in example, not just templates.

**Template only (insufficient):**
```markdown
| Concept | Found? | Depth |
|---------|--------|-------|
| [Concept 1] | YES/NO | Level |
```

**With example (better):**
```markdown
| Concept | Found? | Depth |
|---------|--------|-------|
| Cialdini's 6 principles | YES | In-depth (pp. 12-18) |
| Ethical persuasion | YES | Explained (Section 3) |
| Message structure | NO | - |
**Result:** REJECT (missing message structure)
```

### 5. Error Recovery Paths

Don't just show the happy path. Include what to do when things fail.

**Happy path only (insufficient):**
```markdown
## Process
1. Search for articles
2. Validate content
3. Present to user
```

**With recovery (better):**
```markdown
## Process
1. Search for articles
2. Validate content
   - If <2 pass: broaden search terms, try practitioner sources
   - If all paywalled: check ResearchGate, author sites
3. Present to user
```

## Anti-Patterns

| Don't | Do Instead | Why |
|-------|------------|-----|
| Explain concepts Claude knows | Jump to project-specific rules | Wastes tokens, adds noise |
| Multiple terms for same thing | Pick one term, use everywhere | Prevents confusion, enables search |
| Abstract templates | Filled-in examples | Concrete examples are more effective |
| Magic numbers without justification | "3-6 breaks (rhythm every 4-8 slides)" | Claude needs rationale to adapt |
| Happy path only | Include failure recovery | Real workflows hit errors |
| Everything same priority | Use freedom level markers | Claude needs to know what's flexible |

## Skill Structure Template

```markdown
# [Skill Name]

[One line: what this enables]

## When to Invoke
- Trigger 1
- Trigger 2

## Quick Reference 🔐
[Most-used info in compact form]

## [Main Section] 🔒/🔐/🔓
[Content with freedom level marked]

## Example
[Concrete, filled-in example]

## If Things Go Wrong
- Problem 1 → Solution
- Problem 2 → Solution
```

## Checklist Before Committing

- [ ] Removed explanations Claude already knows?
- [ ] <100 lines for sub-skills, <500 for SKILL.md?
- [ ] At least one concrete example (not just template)?
- [ ] Freedom levels marked where helpful?
- [ ] Error recovery for critical steps?
- [ ] Consistent terminology throughout?
- [ ] Specific triggers in "When to Invoke"?
