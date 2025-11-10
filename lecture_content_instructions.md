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

[Adapt to slide type - brief or extensive as needed]
- Concept slides: Explanations, analogies, misconceptions
- Case slides: Discussion questions, teaching points
- Activity slides: Instructions, timing, debrief plan

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

### MAIN ACTIVITY: [Name - Mirrors Actual Assessment] (55-60 minutes)

**Setup** (5 minutes):
- [Clear, numbered instructions]
- [Distribute materials/templates]
- [Form pairs/groups if needed]

**Individual Work** (20 minutes):
- Students create [specific deliverable matching assessment]
- Using [template/framework provided]
- Instructor circulates with rubric checklist

**Peer Review** (15 minutes):
- Exchange work with partner
- Review using simplified rubric (3-4 criteria)
- Provide one strength, one improvement

**Revision** (10 minutes):
- Incorporate peer feedback
- Self-assess against rubric
- Mark one area for further improvement

**Instructor Debrief** (10 minutes):
- Common strengths observed
- Typical areas needing work
- How this connects to graded assessment

---

### QUIZ PREPARATION (15-20 minutes)

**Practice Questions** (10 minutes):
[5-8 multiple choice questions matching quiz format]

Example Question Types:
1. **Concept Recognition**: According to [framework], which element...
2. **Application**: In this scenario, the best approach would be...
3. **Analysis**: This communication example demonstrates...

**Review & Discussion** (5-10 minutes):
- Students self-check answers
- Discuss why correct answers are right
- Identify concepts needing more study

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

### INSTRUCTOR NOTES

**Circulation Priorities**:
Watch for these common issues:
1. [Typical mistake in this task]
2. [Misunderstanding to correct]
3. [Skill that needs reinforcement]

**Differentiation**:
- Struggling students: [Provide template/example]
- Advanced students: [Add complexity/challenge]

**Assessment Alignment Checklist**:
□ Activity directly mirrors graded work
□ Rubric criteria introduced and practiced
□ Peer review uses assessment language
□ Quiz prep covers testable concepts
```

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