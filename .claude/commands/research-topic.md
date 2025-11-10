# Research Topic Articles

Standalone command for researching and validating articles for a specific course week or topic. Uses the same rigorous 4-stage validation process as /generate-syllabus.

## Your Task

Research articles for a specific topic with strict content validation. Find 2 articles that:
1. Cover ALL required key concepts (no partial matches)
2. Are openly accessible (no paywalls)
3. Are from high-quality sources (peer-reviewed or top-tier practitioner outlets)
4. Are current and relevant

## Usage

**User provides:**
1. Topic name (e.g., "Persuasive Communication & Influence")
2. Key concepts required (e.g., "Cialdini's 6 principles, persuasive message structure, ethical persuasion, objection handling")
3. (Optional) Course context and level (undergraduate/graduate)

## Four-Stage Research Process

### STAGE 1: Discovery (10-15 candidates)

**Use WebSearch to find candidates:**

1. **Top school syllabi:**
   ```
   site:hbs.edu [topic] syllabus
   site:gsb.stanford.edu [topic] MBA course
   site:wharton.upenn.edu [topic] syllabus
   site:mitsloan.mit.edu [topic] course
   ```

2. **Academic articles:**
   ```
   [key concept A] seminal article
   [key concept B] peer reviewed highly cited
   [topic] research article 2020..2025
   ```

3. **Practitioner sources:**
   ```
   site:hbr.org [topic]
   site:sloanreview.mit.edu [topic]
   [topic] Harvard Business Review
   ```

4. **Open access sources:**
   ```
   [key concept] open access
   [author name if known] [topic] ResearchGate
   ```

5. **Vietnamese context research:**
   ```
   [topic] Vietnam business
   [concept] Vietnamese market
   [topic] ASEAN application
   [key concept] Southeast Asia
   site:vn [topic] English
   ```
   **Note:** Look for articles with Vietnam/ASEAN examples, case studies, or applications

**Create initial pool of 10-15 candidate articles.** Document all candidates found.

---

### STAGE 2: Quick Filter (5-6 candidates)

For each candidate, check:

**Accessibility:**
- Use WebFetch to test URL
- Check access type:
  - **Freely accessible:** No barriers → EXCELLENT
  - **Institutional access:** Requires university login → ACCEPTABLE for seminal works
  - **Paywall only:** Cannot access even with institution → REJECT
- Confirm full-text access (not just abstract)
- **For paywalled seminal works:** Mark clearly as "Requires institutional access"

**Quality:**
- Publication source credible? (peer-reviewed journal, HBR, MIT Sloan Review, academic press)
- Author credentials strong?
- Publication date appropriate? (recent unless true seminal work)
- **If paywalled:** Must be seminal/foundational work (1000+ citations or field-defining)

**Relevance:**
- Title clearly related to topic?
- Abstract mentions key concepts?

**Eliminate articles that fail any check. Reduce to 5-6 accessible, high-quality, relevant candidates.**

---

### STAGE 3: Content Validation (2-3 finalists)

This is the CRITICAL stage. For each of the 5-6 candidates:

**3A: Extract Content**

Use WebFetch with this prompt:
```
"Analyze this article and provide a detailed extraction:

1. FRAMEWORKS & MODELS: List all frameworks, models, or theories presented with brief descriptions

2. KEY CONCEPTS: Identify all major concepts and principles explained in depth

3. PRACTICAL APPLICATIONS: Describe examples, case studies, or applications provided

4. TARGET AUDIENCE: Assess the academic level and writing style (academic vs. practitioner-focused)

5. GEOGRAPHIC/CULTURAL CONTEXT: Note any regional focus or cultural assumptions

6. STRUCTURE & COVERAGE: Outline the main sections and what each covers"
```

**3B: Validate Against Required Concepts**

Create strict validation checklist:

```
CONTENT VALIDATION CHECKLIST
Topic: [Topic Name]

Required Key Concepts:
□ [Concept 1 name]
  - Found in article? YES / NO
  - Coverage depth: None / Mentioned / Explained / In-depth
  - Specific section(s): [Where in article]

□ [Concept 2 name]
  - Found in article? YES / NO
  - Coverage depth: None / Mentioned / Explained / In-depth
  - Specific section(s): [Where in article]

□ [Concept 3 name]
  - Found in article? YES / NO
  - Coverage depth: None / Mentioned / Explained / In-depth
  - Specific section(s): [Where in article]

□ [Concept 4 name]
  - Found in article? YES / NO
  - Coverage depth: None / Mentioned / Explained / In-depth
  - Specific section(s): [Where in article]

VALIDATION RESULT:
- All concepts found with "Explained" or "In-depth" coverage? YES → PASS
- Any concept missing or only "Mentioned"? NO → REJECT

DECISION: PASS / REJECT
```

**3C: Apply Strict Standard**

**PASS Criteria:**
- ALL required concepts are found in the article
- ALL concepts have "Explained" or "In-depth" coverage (not just mentioned)
- Content is accurate and current
- Examples/applications are provided

**REJECT if:**
- ANY required concept is missing
- ANY concept is only briefly mentioned
- Content is outdated or inaccurate
- No practical examples or applications

**Reduce to 2-3 finalists that pass ALL validation checks.**

---

### STAGE 4: Present Finalists to User

For each finalist (2-3 articles), present in this format:

```markdown
---

## FINALIST [A/B/C]

### Citation
[Full APA 7th edition citation]

### Accessibility
**URL:** [verified accessible link]
**Access Type:** Open access / Freely available / Institutional access (seminal work)
**Verified:** [Date you verified access]
**Note:** [If institutional access: "Students can access via university library database"]

### Content Match Analysis

**Key Concepts Coverage:**

✓ **[Concept 1 Name]**
  - Coverage: [Explain how and where this is covered]
  - Depth: [Specific details: definitions, examples, frameworks provided]

✓ **[Concept 2 Name]**
  - Coverage: [Explain how and where this is covered]
  - Depth: [Specific details provided]

✓ **[Concept 3 Name]**
  - Coverage: [Explain how and where this is covered]
  - Depth: [Specific details provided]

✓ **[Concept 4 Name]**
  - Coverage: [Explain how and where this is covered]
  - Depth: [Specific details provided]

### Additional Strengths
- [e.g., "Includes 5 real-world business examples from Fortune 500 companies"]
- [e.g., "Accessible, practitioner-focused writing style"]
- [e.g., "Recently updated with 2024 data"]
- [e.g., "Highly cited (2,500+ citations) foundational work"]

### Selection Rationale
[2-3 sentences explaining why this article is perfect for this topic]

### Source Quality
- **Type:** [Peer-reviewed journal / Practitioner publication / Book chapter]
- **Publication:** [Journal or publication name]
- **Year:** [Publication year]
- **Citations:** [Approximate citation count if known]
- **Authority:** [Why this source is credible]

---
```

**After presenting all finalists, ask user:** "Please select 2 articles from the finalists above. Ideally, choose:
- 1 theoretical/foundational article (peer-reviewed, seminal work)
- 1 applied/practitioner article (HBR, case study, practical focus)"

---

## Document Research Process

After user selects final 2 articles, create documentation:

**File:** `shared/research/article-candidates/[topic-slug]-research.md`

```markdown
# Article Research: [Topic Name]

**Research Date:** [Date]
**Key Concepts Required:** [List all]

## Stage 1: Discovery (Candidates Found)
1. [Article 1 title] - [Source]
2. [Article 2 title] - [Source]
...
[List all 10-15 found]

## Stage 2: Quick Filter Results
**Passed to Stage 3:**
1. [Article title] - Accessible, high-quality, relevant
...

**Rejected:**
1. [Article title] - [Reason: Paywall / Low quality / Not relevant]
...

## Stage 3: Content Validation Results
**Finalist A:** [Article title]
- Validation: PASS
- All concepts covered: YES
- Notes: [Brief notes]

**Finalist B:** [Article title]
- Validation: PASS
- All concepts covered: YES
- Notes: [Brief notes]

**Rejected from Stage 3:**
1. [Article title] - Missing coverage of [Concept X]
...

## Final Selection
**Article 1:** [Full citation and URL]
**Article 2:** [Full citation and URL]

**Selection rationale:** [Why these 2 articles together provide complete coverage]
```

---

## Output to User

Provide user with:

1. **2 final selected articles** with full citations and verified URLs
2. **Content validation summary** showing how all key concepts are covered
3. **Saved documentation** in research folder for future reference
4. **Formatted for syllabus** ready to copy into course calendar

---

## Fallback Strategies

**If Stage 3 finds no articles covering all concepts:**

1. **Adjust search strategy:**
   - Search for each key concept individually
   - Look for more recent review articles or meta-analyses
   - Check if concepts are known by alternative names

2. **Consider using 3 articles instead of 2** (ask user permission first):
   - Article 1 covers concepts A & B
   - Article 2 covers concepts C & D
   - Better to fully cover content with 3 articles than use 2 incomplete ones

3. **Research alternative concepts:**
   - Ask user: "I found excellent articles covering [alternative concepts]. Would these work instead?"

4. **Document the gap:**
   - Inform user which concepts lack accessible articles
   - Suggest supplementing with lecture content or video resources

---

## Quality Principles

**Remember:**
- **Strict content validation**: No partial matches
- **Accessibility is mandatory**: No paywalls
- **Quality matters**: Peer-reviewed or top-tier sources only
- **Document everything**: Transparent research process
- **Students benefit**: They get exactly what they need to learn

**Better to spend extra time finding perfect articles than to settle for incomplete coverage.**

---

## Estimated Time

- Stage 1 (Discovery): 5-10 minutes
- Stage 2 (Filter): 5-10 minutes
- Stage 3 (Validation): 15-20 minutes (most intensive)
- Stage 4 (Present & Document): 5-10 minutes

**Total: 30-50 minutes per topic** for thorough, validated research
