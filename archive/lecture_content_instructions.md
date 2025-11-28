# Lecture Content Generator - Revised Instructions

Generate **world-class university lecture materials** that directly prepare students for assessments through aligned tutorials and practice.

## Core Philosophy
- **Lectures** introduce concepts and frameworks
- **Tutorials** practice exact skills needed for assessments
- **Every activity** builds toward graded work
- **Quality over quantity** - one deep activity beats three shallow ones

## Document Structure Awareness

**Before generating content, check course document structure:**

1. **Two-Document Structure** (Recommended for complex courses):
   - `syllabus.md` - Course overview, calendar, learning objectives
   - `assessment-handbook.md` - Complete assessment instructions, rubrics, submission requirements
   - **When referencing assessments**: "See Assessment Handbook Section X"

2. **Single-Document Structure** (Traditional):
   - `syllabus.md` - Everything in one document
   - `rubrics/` folder - May have separate rubric files
   - **When referencing assessments**: "See syllabus section on [Assessment Name]" or "See [filename].md in rubrics folder"

**Adapt your language based on which structure the course uses.**

---

## Syllabus-Research Alignment

**Content must match the week's syllabus theme, not just cover concepts.**

Before generating content, verify that research aligns with this week's syllabus:

1. **Read syllabus week theme** - What is this week about?
2. **Compare research content** - Does each piece of research match the theme?
3. **Filter misaligned content** - Exclude content that fits other weeks better

**Filtering Rule:**
> If research content's PRIMARY topic matches another week's syllabus theme better, EXCLUDE it from this week. It will be used in its proper week.

**Example:**
- Week 1 theme: "Strategic Communication Foundations" (DISC, audience-centered)
- Week 5 theme: "Presentation Delivery" (anxiety management, impromptu speaking)
- Research includes Abrahams' anxiety techniques → **Exclude from Week 1**, include in Week 5

**Why this matters:**
- Prevents content overload in one week
- Ensures logical course progression
- Students learn topics when syllabus intends
- Avoids teaching Week 5 material in Week 1

---

## PART 1: LECTURE CONTENT (90 minutes)

### Structure Requirements

**TARGET: 22-30 content slides for 90 minutes**

**Opening (4-6 slides, ~10-12 mins):**
- Hook (question/statistic/scenario)
- Learning objectives (3-5, student-centered)
- Direct connection to upcoming assessment

**Core Content (14-20 slides, ~60-65 mins):**
- 3-4 major segments
- Pattern: Theory → Example → Application
- Include engagement every 15-20 minutes

**Wrap-up (4-6 slides, ~13-15 mins):**
- Synthesis of key concepts
- Preview of tutorial practice
- Bridge to assessment

### Research & Citation Requirements

**Strategic Research Approach:**

✅ **DO research (3-5 sources per lecture):**
- Current examples and case studies (2023-2025)
- Recent statistics or emerging trends
- Vietnam-specific applications

❌ **DON'T research:**
- Well-established theories from your training
- Classic frameworks you know well

**Citation Requirements:**
- **Inline citations required** for all statistics, research, frameworks: (Author, Year)
- **Full APA 7th reference** integrated at bottom of slide content when source is heavily used
- **Complete reference list** compiled at end of lecture document
- Never fabricate sources - verify all details
- Include DOI/URL for all sources

### Slide Content Format

```
---

**SLIDE [#]: [Active, Specific Title]**

CONTENT:
[Core concepts with sufficient detail to stand alone]
[Include examples, data, frameworks ON the slide]
[Inline citations for all sourced material (Author, Year)]
[Include full APA reference at bottom of slide if source is heavily referenced]

Example:
"According to Porter (1996), competitive advantage comes from making strategic
trade-offs that competitors cannot easily replicate."

*Porter, M. E. (1996). What is strategy? Harvard Business Review, 74(6), 61-78.
https://hbr.org/1996/11/what-is-strategy*

[PURPOSE: Inform/Persuade/Inspire]
[TIMING: X minutes]

---

## Speaker Notes

**Purpose:** Coach the instructor through delivery with practical, concise guidance. Never repeat what's already visible on the slide.

**Voice:** Professional and succinct. Get the main message across efficiently. Use complete sentences that flow naturally when read aloud. Avoid both formal academic language and overly casual tone.

**Length:** Aim for 3-8 lines per slide. Be ruthlessly concise.

**Core Principles:**

1. **Don't repeat slide content** - If students can read it, don't narrate it
2. **Add what's NOT visible** - Context, nuances, common errors, timing needs
3. **Speak directly to instructor** - "Point out that..." not "Students will see..."
4. **Stay neutral** - Avoid dramatic language ("Stop them right there!", "Watch for...")
5. **Match the slide type** - Different slides need different support
6. **Trust instructor judgment** - Provide the "why" and timing, not step-by-step "how." Avoid prescribing specific physical actions like "walk around" or "look at students"

**What to Include (as relevant):**

- **Deeper context** students can't get from reading alone
- **Background details from research notes** - The week's research file (`.working/research/week-N-research.md`) contains rich context: case study details, framework origins, author credentials, key quotes, statistics, and examples. Speaker notes should draw from this research to provide the presenter with background they need to speak confidently. Don't make them do additional research - the research is already done.
- **Common misconceptions** or confusion points to address
- **Timing guidance** - how long to pause, when to move on
- **Key questions** to ask (but not scripting the exact wording)
- **Cultural considerations** specific to Vietnamese context
- **Concrete examples** not already on the slide
- **Connections** to prior concepts or upcoming assessments
- **What successful responses look like**

**What to Avoid:**

- Restating definitions or frameworks already visible
- Generic transitions ("Now let's move to...")
- Over-explaining self-evident content
- Dramatic or prescriptive language
- Scripting exact words for instructor to say
- **Prescribing physical actions** like "walk around," "circulate," "make eye contact," "point to the slide"

**Examples by Slide Type:**

**Quote Slide:**
```markdown
## Speaker Notes

Students typically interpret "mastery" as perfection or being the best. Clarify that Senge means discipline - daily practice, not a destination.

The four verbs (clarifying, deepening, focusing, seeing) are all ongoing actions, never complete. This is lifelong commitment to growth in chosen areas.

After reading, pause briefly. Then ask which of the four verbs resonates most with where they are now. Take 2-3 responses.
```

**Framework Slide:**
```markdown
## Speaker Notes

Students have already practiced all four components this semester: Clear Outcomes (Week 11), Deliberate Practice (Week 8), Feedback Loops (mentorship meetings), Adaptive Adjustment (Week 6). This is synthesis, not new material.

Common mistake: setting time-based goals ("practice 10 hours/week") without clear outcomes or feedback mechanisms. This creates directionless effort.

Have students identify which component is weakest in their Development Plan. Give them 30 seconds.
```

**Comparison Table:**
```markdown
## Speaker Notes

The unproductive response is natural - our brains seek to reduce discomfort quickly. The cost: tension disappears along with growth.

Help students recognize their pattern through self-talk. "I'm not a tech person" is left column. "I need better resources" is right column.

Vietnamese context: When family pressure says "Be realistic, get stable job," the productive response addresses the concern through capability: "I'm building skills that create stability in an emerging field."
```

**Case Study (Internal/Fictional):**
```markdown
## Speaker Notes

After reading, pause before moving on. Many students are navigating this tension between personal vision and family expectations.

Key learning: Minh found a third path honoring both her vision and family values. She used the gap (needing coding skills) as motivation while working at the bank - creative tension in action.

Ask how many feel similar tension between personal vision and family expectations. Show of hands normalizes the experience.
```

**Slide Using Framework/Case Study from Research:**
```markdown
## Speaker Notes

[Draw details from week-N-research.md - the research file contains the context you need]

**Bezos/Kindle context (from research):** In 2007, Bezos explained revolutionary cloud technology at a 7th-grade reading level: "If you come across a word you don't recognize, you can look it up easily. You can search your books... Kindle keeps your place." No mention of cloud infrastructure, DRM protocols, or backend architecture. Result: Kindle sold out in 5.5 hours, Amazon captured 60%+ e-reader market by 2010.

**Buffett's moat metaphor (from research):** Introduced at 1995 Berkshire Hathaway meeting: "The most important thing we do is to find a business with a wide and long-lasting moat around it, protecting a terrific economic castle with an honest lord in charge." The metaphor became standard investment analysis language worldwide.

**Medtronic mission (from research):** Founder Earl Bakken created the first battery-powered pacemaker after a hospital power outage killed a patient. Established six-word mission: "Alleviate pain, restore health, extend life." 50+ years later, 90,000+ employees worldwide still driven by those words.

Key teaching point: All three examples show Gallo's strategies in action - simple language (Bezos), sticky metaphors (Buffett), mission as mantra (Medtronic).
```

**Reflection Activity:**
```markdown
## Speaker Notes

Give them 2 minutes. Remind them to write answers rather than just think - writing surfaces insights that thinking alone misses.

Maintain silence during reflection. This needs genuine thinking time.

When time's up, ask if anyone discovered something surprising. Take one volunteer if offered. Remind them they'll use these notes in today's tutorial.
```

**Section Break / Title Slide:**
```markdown
## Speaker Notes

Major shift from self-awareness tools to integration frameworks. Senge's work from MIT Sloan, used by Google, Toyota, and Vietnamese firms like Vingroup. This framework structures how students present Development Plans in the oral exam.
```

**Style Comparison:**

❌ **Too formal/written:**
- "It is important to note that students may interpret 'mastery' incorrectly."
- "The instructor should clarify the distinction between discipline and perfection."
- "Facilitate a brief discussion regarding student perspectives on the concept."

❌ **Too casual/chatty:**
- "Your students hear 'mastery' and they're thinking perfection - being the absolute best. That's not it."
- "Here's the thing - they've already done all four of these."
- "Watch for the students nodding. That means they're feeling it right now."

❌ **Too prescriptive (over-directing physical actions):**
- "Walk around the room slowly. Make eye contact with students in the back."
- "Point to the slide with your right hand while speaking."
- "Circulate between the rows. Stop at each student's desk for 3 seconds."

✓ **Professional and succinct:**
- "Students typically interpret 'mastery' as perfection or being the best. Clarify that Senge means discipline."
- "Students have already practiced all four components this semester. This is synthesis."
- "Give them 2 minutes. Remind them to write answers rather than just think."

---

## References Compilation

**Note:** All references used in the lecture should be compiled in a complete
reference list at the end of the lecture document for easy student access.
```

### Slide Layout Hints

**NEW: Prescriptive Layout Control**

You can now specify exact slide layouts using HTML comment hints. This ensures optimal visual presentation for different content types.

**Available Layout Types:**

1. **Quote Layout** - Impactful quotes with attribution
   ```
   <!-- LAYOUT: quote -->
   "Who do you want to become in the next chapter of your life?"
   — Robert Fritz, The Path of Least Resistance (1989)
   ```

2. **References Layout** - Academic citations with proper formatting
   ```
   <!-- LAYOUT: references -->
   - Fritz, R. (1989). *The Path of Least Resistance*. Ballantine Books.
   - Senge, P. M. (2006). *The Fifth Discipline*. Doubleday.
   ```

3. **Framework/Diagram Layout** - Visual models with components
   ```
   <!-- LAYOUT: framework -->
   **Component 1**: Description
   **Component 2**: Description
   **Component 3**: Description
   ```

4. **Reflection Prompt Layout** - Contemplative questions
   ```
   <!-- LAYOUT: reflection -->
   What is one area of your life where you feel stuck between
   your current reality and your desired future?
   ```

5. **Comparison Table Layout** - Side-by-side 2-column comparisons
   ```
   <!-- LAYOUT: comparison-table -->
   | Personal Vision | Goals |
   |-----------------|-------|
   | Long-term state | Milestones |
   | Intrinsic | External |
   ```

**When to Use Layout Hints:**

✅ **USE when:**
- Content strongly matches a specialized layout
- Visual impact is important (quotes, frameworks)
- You want guaranteed formatting (references)

⚠️ **OPTIONAL when:**
- Content will auto-detect correctly (most cases)
- Using standard bullet points or paragraphs

**Auto-Detection Still Works:**
- The system will detect layouts automatically based on content patterns
- Layout hints are prescriptive overrides for guaranteed results
- Most slides work perfectly without hints

**Placement:**
- Place the layout hint on its own line before slide content
- Use exactly as shown (case-insensitive)
- One hint per slide

### Quality Checklist - Lecture
- [ ] 22-30 content slides total
- [ ] 3-5 verified sources with DOI/URLs
- [ ] Inline citations for all sourced material
- [ ] Examples current and culturally diverse
- [ ] Direct link to assessment stated

---

## PART 2: TUTORIAL CONTENT (90 minutes)

### File Structure

**TWO separate files are generated:**

1. **tutorial-content.md** - STUDENT-FACING ONLY
   - Activity instructions, dataset, quiz questions (no answers)
   - High-level section timings
   - Rubric checklist, peer review sentence starters
   - NO "Tutor:" notes, NO "Expected:" answers, NO facilitation guidance

2. **tutorial-tutor-notes.md** - TUTOR-FACING ONLY
   - Tutorial goals and key outcomes
   - Quiz answer keys with detailed explanations
   - Facilitating the Main Activity: context, quality indicators, critical moments
   - Timing flexibility (including quiz-as-homework option)
   - Professional conversational tone, not prescriptive

### Assessment-Aligned Structure

**CRITICAL: Each tutorial directly prepares students for specific graded work**

**Opening (10 mins):**
- Quick concept review (3 key points from lecture)
- Preview of assessment being prepared for
- Show simplified rubric for today's practice
- **Reference where to find full details**: "See Assessment Handbook Section X" (or syllabus if single-document structure)

**Main Activity (55-60 mins):**
- ONE substantial activity that mirrors actual assessment
- Use simplified version of real grading rubric (pull from assessment-handbook.md or rubrics folder)
- Include peer review using rubric criteria
- Instructor circulates with rubric checklist
- **Reference complete requirements**: Direct students to Assessment Handbook for submission guidelines, full rubric, examples

**Quiz Preparation (15-20 mins):**
- 5-8 practice questions in quiz format
- Review answers with explanations
- Connect to key concepts for upcoming quiz

**Wrap-up (5-10 mins):**
- Self-assessment against rubric
- What to revise before submission
- Next steps for assessment preparation

### Tutorial Planning Framework

**Week-by-Week Alignment (Example for typical assessment schedule):**

| Week | Tutorial Focus | Main Activity | Quiz Prep |
|------|---------------|--------------|-----------|
| 1-2 | Foundation skills | Basic writing exercise | Concept definitions |
| 3-4 | Portfolio prep | Draft portfolio piece #1 | Application scenarios |
| 5-6 | Portfolio refinement | Revise portfolio piece #2 | Analysis questions |
| 7-8 | Advanced documents | Executive summary draft | Synthesis problems |
| 9-10 | Presentation prep | Practice presentations | Comprehensive review |

**Adjust this framework based on actual syllabus assessments**

### Tutorial Content Format

```
---

## TUTORIAL WEEK [#]: [Topic]
**Assessment Focus**: [Which graded work this prepares for]
**Due Date Awareness**: [When the related assessment is due]

---

### OPENING (10 minutes)

**Quick Review** (3 minutes):
- Key concept 1: [One sentence]
- Key concept 2: [One sentence]  
- Key concept 3: [One sentence]

**Assessment Connection** (5 minutes):
Today's practice directly prepares you for [specific assessment].
We'll use these rubric criteria:
1. [Simplified criterion 1]
2. [Simplified criterion 2]
3. [Simplified criterion 3]

*For complete rubric and submission requirements, see Assessment Handbook Section X* (or relevant section in syllabus if single-document)

**Success Looks Like** (2 minutes):
[Show exemplar or describe A-level work]

---

### Tutorial Activity Design Principles

**CRITICAL DISTINCTION - Quiz vs. Tutorial Questions:**

**Quiz Questions (Closed - Remembering/Understanding):**
- Direct, unambiguous questions with ONE correct answer
- NO scenarios or complex contexts
- Based on slide content only (not speaker notes)
- Test foundational knowledge
- See [docs/QUIZ-QUESTION-GUIDELINES.md](docs/QUIZ-QUESTION-GUIDELINES.md)

**Tutorial Activities (Open - Application/Analysis/Evaluation):**
- USE scenarios and case studies with realistic complexity
- ENCOURAGE defensible arguments and multiple valid approaches
- WELCOME open interpretation and divergent thinking
- Practice higher-order thinking skills for assessments
- See [docs/TUTORIAL-DESIGN-GUIDELINES.md](docs/TUTORIAL-DESIGN-GUIDELINES.md)

**Higher-Order Thinking in Tutorial Activities:**

**Application Level:**
- Apply frameworks to real situations ("Use Cialdini's principles to design this email")
- Use concepts to solve problems ("How would you communicate this delay?")
- Transfer knowledge to new contexts ("Adapt your approach for Vietnamese market")
- Execute procedures in specific scenarios ("Draft a crisis communication response")

**Analysis Level:**
- Break down complex situations ("Analyze what went wrong in this communication")
- Compare multiple approaches ("Evaluate these two persuasive strategies")
- Identify assumptions and implications ("What cultural assumptions are present?")
- Examine relationships between elements ("How do stakeholder interests conflict?")

**Evaluation Level:**
- Judge effectiveness of strategies ("Assess this presentation using the rubric")
- Defend recommendations with reasoning ("Which approach would you recommend and why?")
- Critique arguments using criteria ("Evaluate this proposal against professional standards")
- Make and justify decisions ("Choose a communication channel and defend your choice")

**Designing Open-Ended Activities:**

1. **Use realistic scenarios** - Authentic situations students might face
2. **Ask "What would you do?" not "What is the answer?"** - Invite personal strategy
3. **Require justification** - Students must explain reasoning and connect to course concepts
4. **Welcome multiple solutions** - Different strategies can work depending on priorities/context
5. **Peer review compares approaches** - Not error-finding, but comparing strategies
6. **Debrief explores variety** - Highlight 2-3 valid approaches and discuss trade-offs

**Cultural Considerations for Vietnamese Students:**

- **Frame as comparison, not criticism:** "What did your partner do differently?" vs. "What's wrong?"
- **Provide sentence starters:** "One strength I notice is...", "I took a different approach by..."
- **Emphasize learning over judgment:** "We're exploring strategies together"
- **Build confidence gradually:** Start structured, increase ambiguity as semester progresses
- **Explicitly state:** "Today's activity has no single right answer - your reasoning matters most"

---

### MAIN ACTIVITY: [Name] (55-60 minutes)

**WRITING STYLE: Task-based, not prescriptive**
- Give clear task + deliverable, not micro-steps
- Provide "Considerations" not "Steps 1-4"
- Trust student autonomy to figure out approach
- Phase-level timings only (25 min, 15 min, 10 min) - NOT "Step 1: 5 min"

**Structure:**

**The Scenario**
[Brief, realistic business scenario - 2-3 sentences max]

**Your task:** [One clear sentence describing deliverable]

**Note:** [If multiple valid approaches exist, acknowledge this]

---

**The Data / Materials**
[Provide dataset, templates, or materials - organized clearly, no fluff]

---

**Individual/Pair Work (25 minutes)**

**Deliverable:**
- [Specific output 1]
- [Specific output 2]

**Considerations:**
- [Starting tip]
- [Framework to apply]
- [Quality criteria]
- [Reminder about multiple approaches if applicable]

---

**Peer Review (15 minutes)**

**Exchange work with another pair.**

**Review using these criteria:**
- [ ] [Rubric criterion 1]
- [ ] [Rubric criterion 2]
- [ ] [Rubric criterion 3]
- [ ] [Rubric criterion 4]

**Provide feedback:**
- One specific strength: [Show example format]
- One area to strengthen: [Show example format]

**Remember:** [Note about comparing approaches vs. finding errors]

---

**Revision & Debrief (15 minutes)**

**Revision (10 min):** [Brief note - refine work, don't need to change approach]

**Debrief (5 min):** [Brief note about class discussion]

---

### QUIZ PREPARATION (15-20 minutes)

**IMPORTANT: Two types of quiz questions serve different purposes**

**1. Tutorial Quiz Practice (6-10 questions weekly):**
- Covers THIS week's content thoroughly
- Prepares students for graded quizzes
- Tests Bloom's Remembering + Understanding only
- Includes answer key with explanations in tutor notes

**2. Graded Quiz Assessments (~2 questions per core concept):**
- Covers multiple weeks (e.g., Quiz 2 covers Weeks 4-6)
- Generated separately from tutorial content
- Not part of weekly tutorial generation

**Tutorial Quiz Practice Guidelines:**

**Learning Objectives:**
- **Remembering:** Recall key terms, definitions, frameworks, major theorists
- **Understanding:** Classify concepts, compare/contrast, explain differences, identify examples

**Content Source (CRITICAL):**
- ✅ **ONLY test slide content** (consistent across all instructors)
- ❌ **NEVER test speaker notes** (varies by instructor - unfair assessment)
- ✅ **Test core concepts:** Section break topics + major framework citations
- ❌ **Skip:** Vocabulary slides, references (except major theorists), minor examples

**Question Format:**
- Direct questions, NOT scenarios (scenarios = tutorial activities for higher-order thinking)
- ONE clearly correct answer based on slide content
- 3-4 plausible distractors based on common misconceptions
- Test ONE concept per question

**Core Question Writing Rules:**

1. **Direct, not scenarios:** "What is power distance?" NOT "You're managing a diverse team..."
2. **One concept per question:** Don't combine multiple ideas
3. **Clear stems:** Use question format, not incomplete statements
4. **3-4 plausible distractors:** Based on actual student misconceptions
5. **ONE correct answer:** Definitively supported by slide content
6. **NEVER use:** "All of the above" or "None of the above"
7. **Parallel structure:** All options same grammar, similar length
8. **No clues:** Avoid grammar/length cues to correct answer
9. **Simple language:** Test content knowledge, not reading comprehension
10. **Match Bloom's level:** Remembering = recall/define; Understanding = classify/compare

**Identifying Core Concepts for Questions:**
- Count section breaks in lecture (typically 3-6 per week)
- Each section break = one core concept
- Generate 1-2 questions per section break topic
- Include major framework creators (e.g., "Who developed Drive Theory?" → Pink)

**Question Distribution (6-10 total):**
- 3-4 Remembering-level questions (definitions, recall, recognition)
- 3-4 Understanding-level questions (classification, comparison, interpretation)
- 1-2 questions on major theorists/frameworks
- Balance across section break topics

**Example Remembering Question:**
```
According to Hofstede's framework, which dimension measures the extent to which less powerful members accept unequal power distribution?

A) Uncertainty Avoidance
B) Power Distance ← CORRECT
C) Individualism vs. Collectivism
D) Long-term Orientation
```

**Example Understanding Question:**
```
What is the key difference between high-context and low-context communication?

A) High-context is formal while low-context is informal
B) High-context relies on implicit messages while low-context is explicit ← CORRECT
C) High-context is written while low-context is verbal
D) High-context is for business while low-context is personal
```

**Practice Questions Format:**
```markdown
### QUIZ PRACTICE (15-20 minutes)

**Instructions:** Answer these questions individually, then we'll review together.

**Question 1: [Concept from Section 1]**
[Question stem]

A) [Distractor based on misconception]
B) [Correct answer]
C) [Distractor based on misconception]
D) [Distractor based on misconception]

**Question 2: [Concept from Section 2]**
...

[Continue for 6-10 questions]

**Review Process:**
- Students answer individually (5-8 minutes)
- Review answers together (10-12 minutes)
- Instructor explains why correct answer is right and why distractors are wrong
- Connect to upcoming graded quiz format
```

**Answer Key Requirements (in tutorial-tutor-notes.md):**
- Correct answer letter for each question
- Explanation of WHY it's correct (reference to specific slide)
- Explanation of WHY each distractor is wrong
- Common misconception notes

**For complete quiz design guidelines:**
- See [docs/QUIZ-QUESTION-GUIDELINES.md](docs/QUIZ-QUESTION-GUIDELINES.md)

---

### WRAP-UP (5-10 minutes)

**Self-Assessment Checklist**:
□ I can [specific skill from today]
□ I understand [key concept]
□ I know what to improve for [assessment]

**Before Next Class**:
- Revise your draft based on feedback
- Review these concepts for quiz: [list]
- Bring [materials] for next tutorial

**Assessment Readiness Check**:
On a scale of 1-5, how ready do you feel for [upcoming assessment]?
What one thing will you practice before submission?

---

---

## PART 3: TUTORIAL TUTOR NOTES

**File:** `tutorial-tutor-notes.md` (generated alongside lecture and tutorial content)

**Purpose:** Provide tutors with quiz answer keys, expected student responses, facilitation guidance

### Tutorial Tutor Notes Template

```markdown
# Week [N] Tutorial - Tutor Notes

**Course:** [Course Name]
**Topic:** [Week Topic]
**Assessment Focus:** [Which assessment this prepares for]

---

## QUIZ SOLUTIONS

### Question 1: [Question stem]

**Correct Answer:** B

**Why B is correct:**
[Explanation referencing specific slide number and content from lecture]

**Why A is wrong:**
[Common misconception this represents]

**Why C is wrong:**
[Common misconception this represents]

**Why D is wrong:**
[Common misconception this represents]

**Teaching note:** [How to address common confusions about this concept]

---

### Question 2: [Question stem]

[Repeat for all 6-10 questions]

---

## MAIN ACTIVITY FACILITATION GUIDE

### Expected Responses/Approaches

**Approach 1: [Strategy name]**
- **Description:** [What this approach looks like]
- **Strengths:** [Why it's effective]
- **Reasoning:** [Typical student rationale for choosing this]
- **Rubric alignment:** [Which criteria this meets]

**Approach 2: [Alternative strategy]**
- [Same structure]

**Approach 3: [Another valid approach]**
- [Same structure]

[Document 3-5 defensible approaches]

---

### Sample Student Work

**Strong Example (A-level work):**
[What excellent work looks like for this activity - concrete example]
- Demonstrates [rubric criterion 1]
- Shows [rubric criterion 2]
- Includes [rubric criterion 3]

**Needs Improvement Example (C-level work):**
[Common weaknesses to address in feedback]
- Missing [what's absent]
- Weak [what needs strengthening]
- Opportunity to improve [specific area]

---

### Facilitation Tips

**Setup (5 minutes):**
- Emphasize [key point students must understand]
- Clarify [common confusion about instructions]
- Remind students: [important constraint or principle]

**Individual Work (20 minutes):**
- Circulate and check for [specific criterion from rubric]
- If students struggle with X, suggest Y
- Timing checkpoint at 10 min: Most should have [milestone]
- Look for: Students using [framework/concept from lecture]

**Peer Review (15 minutes):**
- Model one example review together first (use sample work)
- Remind: "Compare approaches, not find errors"
- Listen for: Students using rubric language in feedback
- Cultural note: Vietnamese students may need encouragement to provide specific feedback

**Revision (10 minutes):**
- Students should be strengthening reasoning, not changing approaches
- Check: Are they connecting to course concepts?
- Guide: "Add a reference to [framework] to strengthen your justification"

**Debrief (10 minutes):**
- Ask: "What different approaches did you see?"
- Expected: 2-3 students share different strategies
- Highlight: "Notice how all these meet the rubric because..."
- Connect: "In your [assessment name], you'll need to..."

---

### Key Discussion Questions for Debrief

1. "What different approaches did people take to [main task]?"
   - Expected responses: [List 2-3 approaches]

2. "What did all effective approaches have in common?"
   - Expected responses: [Rubric criteria all met]

3. "What trade-offs exist between these strategies?"
   - Expected responses: [Context dependency, priorities]

4. "How does this activity connect to your upcoming [assessment name]?"
   - Expected responses: [Skills practiced, rubric criteria]

---

### Cultural Considerations for This Activity

- [Specific cultural adaptations for Vietnamese students in this activity]
- [Sentence starters to provide if students hesitate]
- [How to frame peer review as collaborative learning]
- [Ways to build confidence for open-ended tasks]

---

### Timing Flexibility

| Activity Phase | Planned Time | Can Compress To | Can Extend To |
|---------------|--------------|-----------------|---------------|
| Quiz Review | 15-20 min | 12 min | 25 min |
| Main Activity | 55-60 min | 45 min | 65 min |
| Wrap-up | 5-10 min | 5 min | 15 min |

**If running short on time:** Compress quiz review, focus debrief on 1-2 key approaches
**If students need more time:** Extend individual work, compress revision phase
**If rich discussion emerges:** Extend debrief, it's valuable learning
```

---

### Design Principles for Tutorials

**Assessment Backward Design:**
1. Start with the actual assessment requirements
2. Simplify rubric to 3-4 key criteria for practice
3. Create activity that mirrors assessment format
4. Include peer review with rubric language
5. Add quiz prep for upcoming test

**Progressive Skill Building:**
- Week 1-3: Foundation skills with heavy scaffolding
- Week 4-6: Apply skills to portfolio pieces
- Week 7-9: Refine and combine skills
- Week 10+: Presentation and synthesis

**Cultural Considerations:**
- Vietnamese students may need structured peer interaction
- Provide sentence starters for feedback
- Build confidence gradually for presentations
- Use local business examples when possible

---

## PART 3: ACTUAL PRESENTATION SLIDES

### When to Create
Create actual slides ONLY after lecture content document is approved.

### Format Example

```markdown
---

# Why Stories Sell: The Neuroscience of Persuasion

• **Neural coupling:** Brain-to-brain synchronization (Zak, 2015)
• **22x more memorable** than facts alone
• **Emotional centers** activate with character-driven narratives

**Case Study**: How Grab used driver stories to build trust in Vietnam
- 87% increase in app downloads after story campaign (Grab, 2024)
- "Real people, real stories" approach

---
```

---

## WORKFLOW SUMMARY

### Three Deliverables for Each Week

1. **Lecture Content Document**
   - 22-30 slides with speaker notes
   - Full citations and references
   - Connection to assessments explicit

2. **Tutorial Content Document**  
   - ONE main activity mirroring assessment
   - Quiz preparation segment
   - Simplified rubric for practice

3. **Actual Presentation Slides**
   - Clean, student-facing slides
   - Created after content approval

---

## QUALITY CHECKLIST

### Lecture Content
- [ ] Direct assessment connection stated
- [ ] 3-5 verified sources cited
- [ ] Examples current and relevant
- [ ] Speaker notes adapted to slide type

### Tutorial Content  
- [ ] ONE main activity that mirrors actual assessment
- [ ] Simplified rubric provided (3-4 criteria)
- [ ] 5-8 quiz practice questions included
- [ ] Peer review structured with rubric
- [ ] Clear connection to upcoming graded work
- [ ] Time allocated: 10 min opening, 55-60 min activity, 15-20 min quiz, 10 min wrap

### Assessment Alignment
- [ ] Students practice exact skills needed for graded work
- [ ] Rubric language introduced and used
- [ ] Quiz questions match test format
- [ ] Progressive difficulty across weeks

---

## REQUEST TEMPLATE

**To generate week content, specify:**

1. **Week number and topic**
2. **Related assessments** (what's due when)
3. **Specific deliverables needed**:
   - Lecture content only
   - Tutorial content only  
   - Both lecture and tutorial
   - All three (including slides)

**Example Request:**
"Create Week 4 content on Persuasive Communication. Students have Portfolio Piece 1 (professional emails) due Week 5 and Quiz 1 in Week 4. Need both lecture content and tutorial. Tutorial should focus on drafting professional emails using the assessment rubric. Quiz prep should cover Weeks 1-3 concepts."

---

## SPECIAL NOTES

**For Syllabi with Different Assessment Structures:**
- Map tutorials to YOUR specific assessments
- Adjust quiz prep timing to match quiz schedule  
- Shift to presentation practice when appropriate
- Always prioritize upcoming graded work

**Remember**: Students should leave each tutorial having practiced exactly what they'll be graded on, using the same criteria they'll be evaluated against.