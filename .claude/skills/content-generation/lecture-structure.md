# Lecture Structure Skill

## Structure (24+ Slides)

### Opening (5-7 slides)
1. **Title slide** - Topic title only (no course code, instructor, or week number)
2. **Hook** - Compelling stat, question, or story
3. **Objectives** - 3-5 measurable outcomes (Bloom's verbs)
4. **Assessment connection** - How this week prepares for graded work
5. **Roadmap** - Visual preview of lecture segments

### Core Content (14-20 slides)
Organize into **3-4 segments** of ~5 slides each:
- Segment intro (context/why this matters)
- Key concept explanation
- Framework or model (if applicable)
- Example or case study
- Application or mini-activity

**Pacing:** Switch segment every 15-20 minutes. Add engagement activity at each transition.

### Wrap-up (5-7 slides)
1. **Key takeaways** - 3-5 main points
2. **Assessment preview** - What's due, how today helps
3. **Next week preview** - Topic teaser
4. **Resources** - Further reading, tools
5. **References** - Full APA 7th citations for all sources used in lecture

## Anti-Patterns to Avoid

- Starting with definitions (boring - use hook instead)
- >8 slides without engagement break
- Concept slides without examples
- Ending without clear next steps

## Content Limits Per Slide

| Element | Limit |
|---------|-------|
| Body text | 150-200 words |
| Bullets | 6-8 max |
| Concepts | 1 main idea |

**If over:** Split into Part 1/2 or move detail to speaker notes.

---

## Speaker Notes Tone 🔐

Apply human-communication skill principles. Speaker notes should help instructors, not patronize them.

### Structure

```
Opening → Key Points (3-5) → Anticipated Questions → Transition
```

### What TO Write

| Instead of | Write |
|------------|-------|
| "Pause. Let this land." | "Key moment - the 73% stat often surprises students" |
| "Wait for silence" | "Transition point to core concept" |
| "Let it sink in" | "Students typically ask about X here" |
| "You should know this" | *(omit - trust the instructor)* |
| "Remember to..." | *(omit - trust the instructor)* |
| "Draw this on the board" | "A diagram can help here" or "You could sketch..." |
| "Hand out the worksheet" | "The worksheet works well at this point" |
| "Think of X" (unexplained) | Explain what X is first, then make the analogy |

### Red Flags ❌

- Prescriptive staging directions ("Pause", "Wait", "Let this land")
- Emotional instructions ("Let it sink in", "Build suspense", "Create tension")
- Implicit incompetence ("Obviously", "Remember to", "Don't forget")
- Stage directions for delivery ("slow down here", "raise your voice")
- **Directive actions** ("Draw this on the whiteboard", "Hand out the worksheet")
- **Unexplained references** (analogies or examples the speaker may not know)

### Good Examples

**Before (prescriptive):**
> "Pause. Let this land. Wait for students to react before continuing."

**After (helpful context):**
> "This stat typically generates discussion. Common student questions: 'Is this global?' and 'What industries are worst?'"

**Before (condescending):**
> "Let it sink in before explaining. You want them to feel the weight of this."

**After (contextual):**
> "Key insight: The 28% figure connects to Week 3's prioritization framework. Students who've done the reading may already see the link."

**Before (emotional instruction):**
> "Build suspense here. Don't reveal the answer yet."

**After (pedagogical context):**
> "The reveal works best after students attempt the calculation themselves. Common wrong answers: 50%, 75%."

**Before (directive action):**
> "Draw this on the whiteboard as you explain each component."

**After (suggestive):**
> "A whiteboard diagram can help here - drawing each component as you explain shows the flow visually."

**Before (unexplained reference):**
> "Think of the game 'telephone' - that's Shannon's problem in miniature."

**After (self-explanatory):**
> "This is like the children's game 'telephone' (also called 'Chinese whispers'): players whisper a message down a line, and it arrives distorted. Shannon's model explains why - each transmission adds noise."

---

## XML Slide Format 🔒

Use XML tags for slide structure. This format is required for new content.

### Basic Syntax

```xml
<slide number="1" layout="big-number" title="Hook">

# Only 73%

**of employees trust their manager's communication**

*(Edelman Trust Barometer, 2024)*

<speaker-notes>
Key moment - this stat often surprises students.
Common questions: "Is this global?" and "What industries are worst?"
</speaker-notes>

</slide>
```

### Attributes

| Attribute | Required | Values |
|-----------|----------|--------|
| `number` | Yes | Integer (1, 2, 3...) |
| `title` | Yes | Slide title text |
| `layout` | No | `big-number`, `quote`, `framework`, `section-break`, `content` (default) |

### Layout Types

| Layout | Use For |
|--------|---------|
| `title` | Title slide (first slide only) |
| `big-number` | Single statistic (73%, $5.2M) |
| `quote` | Quotation with attribution |
| `framework` | Models, processes, diagrams |
| `section-break` | Segment transitions |
| `references` | References slide (last slide only) |
| `content` | Default mixed content |

---

## Example Opening (5 slides)

```xml
<slide number="1" layout="title" title="Title Slide">

# The Science of Persuasion

<speaker-notes>
Welcome students. Today we explore how persuasion works in business contexts.
</speaker-notes>

</slide>

<slide number="2" layout="big-number" title="Hook">

# 73%

**of employees don't trust their manager's communication**

*(Edelman Trust Barometer, 2024)*

<speaker-notes>
Key moment - this stat typically generates discussion.
Common student questions: "Is this global?" and "What industries are worst?"
</speaker-notes>

</slide>

<slide number="3" title="Learning Objectives">

## Today's Learning Objectives

By the end of this lecture, you will be able to:
1. Apply Cialdini's 6 principles to business scenarios
2. Evaluate ethical vs. manipulative persuasion
3. Design a persuasive message using the AIDA framework

<speaker-notes>
These objectives are testable—students will see them on the quiz.
Connect each to the assessment: "Objective 2 directly relates to your proposal..."
</speaker-notes>

</slide>

<slide number="4" layout="framework" title="Assessment Connection">

## How This Prepares You

**Portfolio Piece 2 (Due Week 8):** Persuasive business proposal
- Today: Learn the principles
- Tutorial: Practice with peer feedback
- Week 7: Refine draft
- Week 8: Submit final

<speaker-notes>
Students appreciate seeing the roadmap to assessment success.
Emphasize that tutorial activities directly build toward the portfolio piece.
</speaker-notes>

</slide>

<slide number="5" layout="section-break" title="Roadmap">

## Today's Journey

1. The Science of Persuasion (20 min)
2. Ethical Boundaries (15 min)
3. Frameworks in Action (25 min)

<speaker-notes>
Visual overview helps students track progress through the lecture.
Return to this slide at each transition point.
</speaker-notes>

</slide>
```

## If Slides <24

- **<24:** Check for merged concepts; each idea needs its own slide
- **No upper limit:** Include all content needed to teach concepts thoroughly

---

## Integrating Videos into Lectures

### Pattern A: Required Video - In-Class Viewing (≤15 min)

Use when: Video is PRIMARY tier, researcher explaining own theory, essential for understanding

```xml
<slide number="X" layout="content" title="Video Title">

## [Video Title]

**[VIDEO: [Speaker Name] - "[Video Title]"]**
**Video link:** [URL]
**Duration:** [MM:SS]

**Before watching:** [Pre-viewing question to prime attention]

<speaker-notes>
Setup (30 sec): Introduce [Speaker] and their credentials. Prime with question: "[Question]". Direct attention to [key moment] in the video.

After video: Quick debrief asking "What stood out to you?" Take 2-3 responses. Connect to next section: [How video relates to upcoming content].

Transition: "Now that we've seen [speaker]'s explanation, let's dive deeper into..."
</speaker-notes>

</slide>
```

**Video Slide Counting:** Videos >5 min count as 1 slide toward total.

---

### Pattern B: Optional Video - Supplementary Resources

Use when: Video is SUPPLEMENTARY tier, enrichment for interested students

```xml
<slide number="X" layout="content" title="Further Resources">

## Further Resources (Optional)

**Videos:**
- [Speaker] – "[Title]" ([Duration]) - [URL]
  - Why watch: [1 sentence benefit]
- [Speaker] – "[Title]" ([Duration]) - [URL]
  - Why watch: [1 sentence benefit]

**Not required** - All assessed material covered in readings and lecture.

<speaker-notes>
Brief mention: "For those interested in going deeper, I've linked two excellent videos on this topic. They're optional but highly recommended if you want to see these concepts in action."
</speaker-notes>

</slide>
```

**Video Slide Counting:** Optional resource slides don't count toward total if placed at end.

---

### Pattern C: Pre-Work Assignment (15-30 min video)

Use when: Video is long but valuable, better as homework

```xml
<slide number="X" layout="content" title="Pre-Class Preparation">

## Pre-Class Preparation

**Required Viewing Before Next Class:**

**VIDEO:** [Speaker] - "[Title]"
- Duration: [MM:SS]
- Link: [URL]

**Your task:**
1. Watch the full video
2. Note: [specific aspects to focus on]
3. Prepare to discuss: [reflection question]

<speaker-notes>
Assignment instruction: "For next week's class, you must watch [Speaker]'s talk on [topic]. It's 18 minutes - watch it in one sitting and take notes on [specific aspect]. We'll start next class with a discussion of what you learned."

[NOTE FOR NEXT WEEK'S LECTURE: Begin with 5-min video debrief. Quick poll on video content, then connect to that week's topic.]
</speaker-notes>

</slide>
```

**Video Slide Counting:** Pre-work assignment slides count as 1 slide.

---

## Example References Slide

Always include a References slide as the final numbered slide:

```xml
<slide number="N" layout="references" title="References">

## References

1. Author, A. A. (Year). Title of article. *Journal Name*, volume(issue), pages. https://doi.org/xxxxx

2. Author, B. B., & Author, C. C. (Year). *Book title*. Publisher.

3. Author, D. D. (Year, Month Day). Article title. *Publication*. https://url

<speaker-notes>
Full citations for all sources referenced in lecture. Students can use these for further reading.
</speaker-notes>

</slide>
```
