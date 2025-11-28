# Article Validation Skill

> **Purpose:** Validate that articles provide sufficient depth to **inform accurate lecture content**. Research prevents hallucinations by grounding lectures in verifiable sources.

## Content Validation Checklist

For each required concept, check:

```markdown
□ [Concept name]
  - Found? YES / NO
  - Depth: None / Mentioned / Explained / In-depth
  - Location: [Section or page]
```

### Depth Definitions (for Lecture-Informing Content)

| Level | Description | Teaching Value | Accept? |
|-------|-------------|----------------|---------|
| None | Not found in article | Cannot inform lecture | REJECT |
| Mentioned | 1-2 sentences only | Insufficient for slides | REJECT |
| Explained | Paragraph with definition | Can write 1-2 slides | PASS |
| In-depth | Multiple paragraphs + examples | Can write full lecture segment | PASS |

## Accessibility Check

Use WebFetch to verify:

**Accept:**
- Open access (freely available)
- HBR articles (publicly accessible)
- Author's ResearchGate/personal page
- Paywalled + seminal (1000+ citations, top journal)

**Reject:**
- Paywalled non-seminal works
- Broken URLs (404)
- Login-only without institutional access

## Quality Indicators

**Strong sources:**
- Peer-reviewed journals (A*/A ranked)
- Harvard Business Review, MIT Sloan Review
- Top school publications
- 100+ citations (recent) or 1000+ (established)

**Weak sources (reject):**
- Random blogs without credentials
- Self-published without peer review
- Outdated (pre-2015 unless seminal)

## Validation Output Format 🔐

```markdown
### Article: [Title]

**URL:** [verified working]
**Access:** Open / Paywalled-Seminal / Institutional
**Source:** [Journal/Publication]

**Content Match:**
✓ Concept 1: Explained in Section 2 (p.12-15)
✓ Concept 2: In-depth coverage throughout
✗ Concept 3: Not addressed

**Result:** PASS / REJECT
**Reason:** [If reject, specify missing concept]
```

## Example (Filled In)

**Topic:** Persuasive Communication
**Required concepts:** Cialdini's 6 principles, ethical persuasion, message structure

### Article: The Science of Persuasion

**URL:** https://hbr.org/2001/10/harnessing-the-science-of-persuasion
**Access:** Open (HBR)
**Source:** Harvard Business Review

**Content Match:**
✓ Cialdini's 6 principles: In-depth (entire article organized by principle)
✓ Ethical persuasion: Explained (Section: "The Ethics of Influence")
✗ Message structure: Not addressed (no AIDA, no structural frameworks)

**Result:** REJECT
**Reason:** Missing message structure. Strong on principles but needs pairing with structural article.

**Recovery:** Search "AIDA persuasive message structure" for complementary article.

## Common Pitfalls

- Article title mentions concept but content doesn't cover it
- Abstract promising but full text is paywalled and unvalidated
- Accepting "Mentioned" as sufficient (it's not)
- Not checking all concepts before recommending

## If Validation Fails

- **One concept missing:** Search specifically for that concept; consider 3 articles instead of 2
- **All paywalled:** Try `[author name] [topic] ResearchGate` or `[title] PDF`
- **Seminal but paywalled:** Accept if 1000+ citations AND can validate content from abstract + previews
