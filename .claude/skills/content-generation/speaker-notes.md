# Speaker Notes Skill

## Structure Per Slide 🔐

Speaker notes use XML tags within slides:

```xml
<speaker-notes>
Opening context or transition from previous slide.

Key points to emphasize:
- Main concept with brief explanation
- Definition to clarify if needed
- Analogy or comparison (fully explained)

Example or story for illustration.

Question to check understanding or prompt discussion.

Transition to next slide topic.
</speaker-notes>
```

## Length Guidelines

| Slide Type | Target Words |
|------------|--------------|
| Title/Section | 50-75 |
| Standard content | 150-200 |
| Framework/Model | 200-250 |
| Activity instruction | 100-150 |

## Anti-Patterns

- Reading slide content verbatim
- Generic notes ("explain this concept")
- Missing transitions between slides
- No engagement prompts
- **Directive actions** ("Draw this", "Hand out") → use suggestive ("You could draw...", "The worksheet works well here")
- **Unexplained references** → speaker notes should be self-contained; explain analogies/examples so the speaker doesn't need outside knowledge

## Example (Filled In)

```xml
<speaker-notes>
Transition from the 6 principles overview—now showing them in action.

Key points:
- Scarcity works because of loss aversion (Kahneman's research on how people fear losing more than they value gaining)
- "Limited time" framing more effective than generic "sale" messaging
- Vietnamese e-commerce uses countdown timers heavily on platforms like Shopee and Lazada

Example: Shopee flash sales combine timer + "only 3 left" messaging, layering scarcity with social proof for maximum urgency.

Quick engagement: "Show of hands—who's bought something because of a countdown timer?" Most students will raise hands, validating the concept's real-world impact.

Next: examining when scarcity backfires and ethical boundaries.
</speaker-notes>
```

## Cultural Notes 🔓

- Vietnamese business examples when relevant
- Quiet groups: suggest pair-share before full class discussion
