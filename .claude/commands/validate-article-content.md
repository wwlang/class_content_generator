# /validate-article-content [URL] "[concepts]"

Quick validation of specific article against required concepts.

## Usage

```
/validate-article-content "https://hbr.org/article" "Cialdini's principles, ethical persuasion, message structure"
```

## Process 🔐

### Step 1: Fetch Article

WebFetch the URL and extract:
- Title, author, publication, year
- Frameworks and models
- Key concepts covered
- Practical examples

### Step 2: Validate Each Concept 🔒

For each required concept:

| Found? | Depth | Accept? |
|--------|-------|---------|
| No | - | REJECT |
| Yes | Mentioned (1-2 sentences) | REJECT |
| Yes | Explained (paragraph) | PASS |
| Yes | In-depth (multiple paragraphs) | PASS |

### Step 3: Report

```
VALIDATION: PASS / FAIL

✓ Concept 1: In-depth (Section 2)
✓ Concept 2: Explained (p. 12-15)
✗ Concept 3: Not found

Recommendation: [Use / Find alternative]
```

## Pass Criteria 🔒

ALL must be true:
- Every concept found
- Every concept at least "Explained"
- Definitions or clear descriptions provided
- Article accessible (not paywalled, or seminal if paywalled)

## Quick vs Detailed Mode

**Quick:** Pass/fail with brief summary
**Detailed:** Full report with locations, quotes, alternatives

Ask user preference or default to quick.

## Time

- Quick: 2-5 minutes
- Detailed: 5-10 minutes

## Example

```
/validate-article-content "https://hbr.org/2001/10/harnessing-science-of-persuasion" "Cialdini's 6 principles, ethical persuasion"

VALIDATION: PASS

✓ Cialdini's 6 principles: In-depth (entire article)
✓ Ethical persuasion: Explained (Section 4)

Recommendation: Use for Week 4
```

## If Things Go Wrong

- **URL inaccessible:** Try Wayback Machine or author's site
- **Paywall:** Override if seminal (1000+ citations) with justification
- **Partial coverage:** Suggest complementary article for gaps
