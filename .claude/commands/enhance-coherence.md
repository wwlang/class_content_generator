# /enhance-coherence [course-code]

Cross-week quality polish after content generation.

## Prerequisites

- At least 3 weeks generated
- Git repo recommended (creates backup commit)

## Process

### Step 1: Analysis

Reads all week content and identifies:

| Issue Type | What It Finds |
|------------|---------------|
| Terminology | Inconsistent terms, undefined jargon |
| Scaffolding | Concepts used before introduced, missing prerequisites |
| Examples | Duplicates, industry clustering, Vietnamese context gaps |
| Cross-references | Missing forward/backward/lateral connections |
| Citations | Format inconsistencies, unused citations |

Each issue scored 1-10 for quality impact.

### Step 2: Present Options 🔐

```
[1] TERMINOLOGY (12 issues) - Auto: 10/12
[2] SCAFFOLDING (8 issues) - Auto: 6/8
[3] EXAMPLES (15 issues) - Auto: 3/15 (mostly manual)
[4] CROSS-REFERENCES (24 issues) - Auto: 20/24
[5] CITATIONS (6 issues) - Auto: 6/6
[6] ALL
[7] CUSTOM selection
[8] NONE (just review report)

Select: [1,2,5] for multiple
```

### Step 3: Apply Enhancements

Auto-applies safe changes, lists manual items for review.

### Step 4: Reports

- `coherence-report.md` - Full analysis (~8,000 words)
- `enhancement-summary.md` - Executive overview
- `manual-enhancements-todo.md` - Items needing manual review

## Scoring 🔒

| Score | Priority |
|-------|----------|
| 9-10 | Critical - address first |
| 7-8 | Important |
| 4-6 | Medium |
| 1-3 | Minor polish |

## Backup

Creates git commit before changes. Revert: `git reset --hard [commit]`

## Time

15-30 minutes for 10-week course

## Example

```
/enhance-coherence BCI2AU

Analyzing 9 weeks...
Overall coherence: 7.2/10

Select enhancements: 2,4,5

Applying scaffolding + cross-references + citations...
✓ 32/38 auto-applied
⚠ 6 manual items saved to manual-enhancements-todo.md

Score improvement: 7.2 → 8.4 (estimated)
```

## Recommended Combinations

- **Conservative:** Citations only (2 min)
- **Recommended:** Scaffolding + Cross-references + Citations (20 min)
- **Comprehensive:** All (45 min with manual work)

## If Things Go Wrong

- **<3 weeks generated:** Generate more weeks first
- **No git repo:** Manual backup recommended, or init git
- **Want to undo:** `git reset --hard [commit from output]`

**Full reference:** `enhance-coherence-FULL-REFERENCE.md`
