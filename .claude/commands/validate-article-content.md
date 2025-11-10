# Validate Article Content

Quick validation tool to check if a specific article covers required key concepts for a course week. Use this when you have a specific article in mind and want to verify its content match.

## Your Task

Analyze a given article and determine if it adequately covers all required key concepts using strict validation criteria.

## Usage

**User provides:**
1. Article URL
2. Key concepts required (comma-separated list)
3. (Optional) Topic/week context

**Your output:**
- PASS/FAIL decision
- Detailed content mapping
- Specific gaps if any

## Validation Process

### Step 1: Fetch Article Content

Use WebFetch to retrieve the article:
```
WebFetch: [URL]
Prompt: "Analyze this article comprehensively and extract:

1. TITLE & METADATA
   - Full title
   - Author(s)
   - Publication/Journal
   - Year
   - DOI/URL

2. MAIN FRAMEWORKS & MODELS
   - List each framework/model name
   - Provide 2-3 sentence description of each

3. KEY CONCEPTS EXPLAINED
   - List all major concepts covered
   - Note depth: Mentioned / Explained / In-depth analysis

4. PRACTICAL EXAMPLES & APPLICATIONS
   - Describe any case studies, examples, or applications
   - Note context (industry, geography, scenario)

5. ARTICLE STRUCTURE
   - Main sections or headings
   - Flow and organization

6. TARGET AUDIENCE & STYLE
   - Academic or practitioner-focused?
   - Technical level
   - Writing accessibility"
```

### Step 2: Parse Required Concepts

Take the user's key concepts list and parse into individual validation items.

**Example:**
User input: "Cialdini's 6 principles, persuasive message structure, ethical persuasion, objection handling"

Parse to:
1. Cialdini's 6 principles (or: principles of persuasion)
2. Persuasive message structure
3. Ethical persuasion
4. Objection handling (or: overcoming objections)

### Step 3: Create Validation Matrix

For EACH required concept, determine:

```markdown
### Concept: [Name]

**Found in article?** YES / NO

**If YES:**
- **Location:** [Which section(s) of article]
- **Coverage depth:**
  - [ ] Only mentioned (1-2 sentences)
  - [ ] Explained (paragraph-level, defines concept)
  - [ ] In-depth (multiple paragraphs, examples, applications)
- **Quality of coverage:**
  - [ ] Defines concept clearly
  - [ ] Provides examples or applications
  - [ ] Discusses implications or applications
  - [ ] Offers practical guidance

**If NO:**
- **Searched for alternatives:** [List related terms searched]
- **Closest mention:** [Any related content found]
```

### Step 4: Apply Validation Criteria

**PASS Criteria (ALL must be true):**
- ✓ Every required concept is found in the article
- ✓ Every concept has at minimum "Explained" depth (not just mentioned)
- ✓ Definitions or clear descriptions are provided
- ✓ At least some practical examples or applications are included

**FAIL Criteria (ANY triggers fail):**
- ✗ Any required concept is completely missing
- ✗ Any required concept is only briefly mentioned (1-2 sentences)
- ✗ Concepts are present but not explained clearly
- ✗ No practical examples or applications provided

### Step 5: Generate Validation Report

**Format:**

```markdown
# Article Content Validation Report

## Article Details
**Title:** [Full title]
**Author(s):** [Names]
**Source:** [Journal/Publication]
**Year:** [Year]
**URL:** [URL provided]
**Access Status:** [Verified accessible: YES/NO]

---

## Validation Request
**Topic/Context:** [Week topic if provided]
**Required Key Concepts:**
1. [Concept 1]
2. [Concept 2]
3. [Concept 3]
4. [Concept 4]

---

## Content Analysis

### Concept 1: [Name]
**Status:** ✓ FOUND / ✗ NOT FOUND

[If FOUND:]
**Coverage Depth:** Mentioned / Explained / In-depth
**Location:** [Section names or page numbers]
**Details:**
- [Describe how concept is covered]
- [Note quality: definitions, examples, frameworks]
- [Quote or paraphrase key passages if helpful]

[If NOT FOUND:]
**Search Attempts:** [Terms searched for]
**Closest Content:** [Any related material]
**Gap Impact:** [How this affects article's usefulness]

---

[Repeat for each concept]

---

## Overall Assessment

### Coverage Summary
| Required Concept | Found? | Depth | Quality |
|---|---|---|---|
| [Concept 1] | ✓ | In-depth | Excellent |
| [Concept 2] | ✓ | Explained | Good |
| [Concept 3] | ✗ | N/A | N/A |
| [Concept 4] | ✓ | Mentioned only | Insufficient |

### Validation Decision: **PASS** / **FAIL**

**Reasoning:**
[2-3 sentences explaining the decision based on criteria]

---

## Recommendations

[If PASS:]
**✓ RECOMMENDED FOR USE**
- This article adequately covers all required concepts
- [Note any particular strengths]
- [Suggest pairing with complementary article if helpful]

[If FAIL:]
**✗ NOT RECOMMENDED - GAPS IDENTIFIED**

**Missing/Insufficient Coverage:**
- [Concept X]: [Describe the gap]
- [Concept Y]: [Describe the gap]

**Suggestions:**
1. [Find supplementary article covering missing concepts]
2. [Alternative search terms to find better match]
3. [Consider if concept is essential or can be adjusted]

---

## Additional Notes

**Article Strengths:**
- [List any positive aspects even if article failed]

**Article Weaknesses:**
- [List limitations beyond concept coverage]

**Alternative Use:**
- [Suggest if article could work for different week/topic]
```

---

## Examples

### Example 1: PASS

```markdown
## Validation Decision: **PASS**

**Reasoning:**
This article comprehensively covers all 4 required concepts. Cialdini's 6 principles are explained in-depth with examples (Section 2). Persuasive message structure is outlined clearly with templates (Section 3). Ethical persuasion is discussed throughout with guidelines (Section 4). Objection handling techniques are provided with case studies (Section 5). All concepts have "Explained" or "In-depth" coverage with practical applications.

✓ RECOMMENDED FOR USE
```

### Example 2: FAIL

```markdown
## Validation Decision: **FAIL**

**Reasoning:**
While this article excellently covers Cialdini's 6 principles (in-depth, Section 2-4) and persuasive message structure (explained, Section 5), it fails validation because: (1) Ethical persuasion is only briefly mentioned in one paragraph without guidance, and (2) Objection handling is completely absent from the article. These gaps mean students would not receive complete coverage of required concepts.

✗ NOT RECOMMENDED - GAPS IDENTIFIED

**Suggestions:**
1. Search for companion article specifically on "ethical persuasion guidelines" and "overcoming objections in business"
2. Consider Cialdini's newer work which may address ethics more thoroughly
3. This article could work well for a week focused only on persuasion principles
```

---

## Quick Validation Mode

For faster validation when user just needs yes/no:

**Ask:** "Do you want a full detailed report or quick validation?"

**If quick validation:**
1. Fetch and analyze article content
2. Check each required concept (found/not found)
3. Apply pass/fail criteria
4. Provide brief output:

```
VALIDATION RESULT: PASS / FAIL

Concept Coverage:
✓ Concept 1 - Covered adequately
✓ Concept 2 - Covered adequately
✗ Concept 3 - Missing
✓ Concept 4 - Mentioned only (insufficient)

Decision: FAIL - Missing/insufficient coverage of Concepts 3 and 4

Recommendation: Do not use for this week. Search for article covering [missing concepts].
```

---

## Accessibility Check

Always verify URL accessibility as part of validation:

```
WebFetch [URL]

Check for:
- ✓ Loads successfully
- ✓ Full text accessible (not just abstract)
- ✗ Paywall detected
- ✗ Login required
- ✗ "Access denied" message

If accessibility issues: Report as FAIL even if content is good
Rationale: Students cannot use what they cannot access
```

---

## Best Practices

1. **Be strict:** When in doubt, FAIL the article. Better to find perfect match than settle.

2. **Document thoroughly:** User needs to understand WHY article passed or failed.

3. **Suggest alternatives:** If article fails, provide concrete next steps.

4. **Consider pairing:** Sometimes article is excellent but needs companion piece.

5. **Save time:** Quick mode for rapid screening, detailed mode for final selection.

6. **Respect user's time:** If article clearly fails early (missing multiple concepts), can stop analysis and report FAIL immediately.

---

## Estimated Time

- Quick validation: 2-5 minutes
- Detailed validation: 5-10 minutes

Use this tool frequently during article research to efficiently filter candidates before deep reading.
