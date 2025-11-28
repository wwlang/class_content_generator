---
name: research
description: Find and validate academic articles from top business schools with strict content matching
version: 1.0.0
---

# Research Skill

Find high-quality, accessible articles that **inform lecture content** to ensure accuracy and prevent hallucinations.

> **Key Purpose:** Research isn't just validation—articles provide the factual foundation for detailed lecture material. Content must be comprehensive enough to write accurate, well-sourced lectures.

## When to Invoke

Auto-invoke when:
- `/research-topic` is called
- `/generate-syllabus` reaches article research phase
- User asks to find articles for a topic

## Sub-Skills

| Need | Load |
|------|------|
| Article validation | `article-validation.md` |

## 4-Stage Process (Summary)

### Stage 1: Discovery (10-15 candidates)
Search top schools + academic sources:
- `site:hbs.edu [topic] syllabus`
- `site:gsb.stanford.edu [topic]`
- `site:hbr.org [topic]`
- `[concept] peer reviewed highly cited`

**Example searches for "Persuasive Communication":**
```
site:hbs.edu persuasion influence syllabus
site:hbr.org Cialdini persuasion
"persuasive communication" peer reviewed 2020..2025
ethical persuasion business communication journal
```

### Stage 2: Quick Filter (5-6 candidates)
WebFetch each to check:
- Accessibility (open preferred, paywalled OK if seminal)
- Source quality (peer-reviewed, HBR, top school)
- Relevance (title/abstract match)

### Stage 3: Content Validation (2-3 finalists)
For each candidate, validate ALL concepts with **lecture-informing depth**:

| Concept | Found? | Depth | Teaching Value |
|---------|--------|-------|----------------|
| [Concept 1] | YES/NO | Mentioned/Explained/In-depth | Can inform 1+ lecture slides? |
| [Concept 2] | YES/NO | Mentioned/Explained/In-depth | Has examples/frameworks/models? |

**PASS:** All concepts at "Explained" or "In-depth" with extractable teaching content
**REJECT:** Any concept missing, "Mentioned" only, or lacks teachable depth

### Stage 4: Present to User
Show 2-3 finalists with content match analysis. User selects 2.

## Quality Rules 🔒

- **Open access preferred** - Students must access content
- **Paywalled OK if:** Seminal (1000+ citations), top-tier journal, content validated
- **All concepts covered** - No partial matches accepted
- **Balance:** 1 theoretical + 1 applied ideal

## If Research Stalls

- **<10 candidates:** Broaden search; try synonyms, adjacent topics
- **All paywalled:** Check ResearchGate, author websites, preprint servers
- **No article covers all concepts:** Accept 3 articles instead of 2 (ask user)
