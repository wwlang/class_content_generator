# Layout Variety Skill

Claude writes content + hints; Gemini creates visuals.

## Targets (Per 25-Slide Lecture) 🔐

| Layout Type | Count | Why This Many |
|-------------|-------|---------------|
| Section breaks | 3-6 | Rhythm every 4-8 slides |
| Quote slides | 2-3 | Expert voice, memorability |
| Framework/diagram | 2-3 | Visual learning, complexity reduction |
| Case study | 3-6 | Application, engagement |
| Comparison | 1-2 | Decision-making, contrast |
| Big number/stats | 1-2 | Attention, credibility |
| Standard content | ~60% max | Prevents visual fatigue |

## Layout Hints (Add to Content)

Tell Gemini what you want:
```markdown
<!-- LAYOUT: section-break -->
<!-- LAYOUT: quote -->
<!-- LAYOUT: framework -->
<!-- LAYOUT: case-study -->
<!-- LAYOUT: comparison -->
<!-- LAYOUT: big-number -->
```

## When to Use Each

| Layout | Trigger |
|--------|---------|
| section-break | New segment (every 4-8 slides) |
| quote | Expert statement, key definition |
| framework | Model with 3-6 components |
| case-study | Story, example, Vietnamese context |
| comparison | Before/after, two approaches |
| big-number | Dramatic statistic |

## Example (Content + Hint)

```markdown
<!-- LAYOUT: framework -->
## Cialdini's 6 Principles of Persuasion

1. **Reciprocity** - Give first, receive later
2. **Commitment** - Small yeses lead to big yeses
3. **Social Proof** - People follow others
4. **Authority** - Experts persuade
5. **Liking** - We say yes to people we like
6. **Scarcity** - Less available = more desirable

*Gemini: Create circular diagram with icons for each principle*
```

**Result:** Gemini creates visual infographic instead of bullet list.

## Anti-Patterns

- All bullets (boring—vary every 3-4 slides)
- No section breaks (no rhythm—add every 4-8 slides)
- Frameworks as bullet lists (use `<!-- LAYOUT: framework -->`)
- Missing layout hints (Gemini guesses wrong)

## If Layout Looks Wrong

- Missing hint? Add explicit `<!-- LAYOUT: type -->`
- Wrong visual? Add instruction: "*Gemini: [specific request]*"
- Too many of same type? Redistribute variety
