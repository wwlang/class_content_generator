# /research-topic "[Topic]" "[Key Concepts]"

Find 2 validated articles covering all required concepts for **cross-course topic research**.

> **Note:** This command is for general topic research reusable across courses. For course-specific weekly research (4 articles per week), use Claude Desktop with `/import-research`.

## Usage

```
/research-topic "Persuasive Communication" "Cialdini's 6 principles, message structure, ethical persuasion"
```

## Process

**Load skill:** `research/SKILL.md`

### Stage 1: Discovery (5-10 min)
Search for 10-15 candidates:
- Top schools: `site:hbs.edu`, `site:gsb.stanford.edu`, `site:wharton.upenn.edu`
- Academic: Google Scholar, peer-reviewed
- Practitioner: `site:hbr.org`, MIT Sloan Review

### Stage 2: Quick Filter (5-10 min)
Reduce to 5-6 by checking:
- Accessibility (WebFetch each URL)
- Source quality (peer-reviewed, top-tier)
- Relevance (title/abstract match)

### Stage 3: Validation (15-20 min)
For each candidate, check ALL concepts:

| Concept | Found? | Depth |
|---------|--------|-------|
| [Concept 1] | YES | Explained/In-depth |
| [Concept 2] | YES | Explained/In-depth |

**PASS:** All concepts at "Explained" or "In-depth"
**REJECT:** Any missing or "Mentioned" only

### Stage 4: Present (5-10 min)
Show 2-3 finalists with:
- Full APA citation
- Verified URL
- Content match analysis
- Selection rationale

User selects 2 (ideally 1 theoretical + 1 applied).

## Quality Rules

- **Open access preferred** - paywalled OK only if seminal (1000+ citations)
- **All concepts covered** - no partial matches
- **Top sources** - peer-reviewed, HBR, business school publications

## Output

Save to: `shared/research/[topic-slug]-research.md`

**Time:** 30-50 minutes total
