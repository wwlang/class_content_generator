---
name: content-generation
description: Generate lecture content, speaker notes, and ensure layout variety for engaging presentations
version: 1.0.0
---

# Content Generation Skill

Generate world-class lecture content with proper structure, speaker notes, and visual variety.

## When to Invoke

Auto-invoke when:
- `/generate-week [N]` is called
- User asks to create lecture content
- User asks about slide structure or speaker notes

## Sub-Skills (Load as Needed)

| Need | Load |
|------|------|
| Lecture structure | `lecture-structure.md` |
| Speaker notes format | `speaker-notes.md` |
| Slide layout variety | `layout-variety.md` |
| Citation formatting | `citations.md` |

## Quick Reference 🔐

**Lecture Structure:** 22-30 slides total
- Opening: 4-6 slides (hook, objectives, roadmap)
- Core: 14-20 slides (3-4 segments, ~5 slides each)
- Wrap-up: 4-6 slides (synthesis, preview, resources)

**Content Limits Per Slide:**
- 150-200 words body text
- 6-8 bullet points max
- 1 main concept per slide

**Layout Variety Targets:** See `layout-variety.md` for distribution rules.

## Freedom Levels in This Skill

| Component | Level | Notes |
|-----------|-------|-------|
| Slide count (22-30) | 🔐 | Range is firm |
| Structure (open/core/wrap) | 🔐 | Pattern consistent |
| Speaker note format | 🔐 | Structure consistent |
| Examples & stories | 🔓 | Adapt to topic |
| Vietnamese context | 🔓 | Add where natural |
| Citation format | 🔒 | APA 7th exact |
