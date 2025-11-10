# Generate Week Content

Generate complete weekly content including lecture materials and tutorial activities based on the course syllabus. This command creates assessment-aligned content following the lecture_content_instructions.md guidelines.

## Your Task

Create both lecture content (22-30 slides with speaker notes) and tutorial content (assessment-aligned activities) for a specific course week.

## Prerequisites

**Required before running this command:**
1. Course syllabus must exist with weekly topics defined
2. Assessment schedule must be documented
3. Week topic and required readings identified

## Usage

**User provides:**
- Course code (e.g., BUS101)
- Week number (e.g., 3)

**You generate:**
- Lecture content document (22-30 slides)
- Tutorial content document (90-minute structure)
- Save both to appropriate week folder

## Step-by-Step Process

### Step 1: Locate Course and Read Context

**Actions:**
1. Find course folder: `courses/[COURSE-CODE]-*/`
2. Read syllabus: `courses/[COURSE-CODE]-*/syllabus.md`
3. **Check for document structure:**
   - If `assessment-handbook.md` exists → Read it for detailed rubrics and instructions
   - Otherwise → Read `assessments/assessment-schedule.md` (legacy structure)
4. Read course info if available: `courses/[COURSE-CODE]-*/.working/course-info.md`

**Extract for Week [N]:**
- Week topic name
- Required readings (2 articles)
- Key concepts (from syllabus or ask user)
- Related learning objectives
- Upcoming assessments (what's due in next 2-3 weeks)
- **Full rubric details** (from assessment-handbook.md if available)

**Document Structure Awareness:**
- **2-document structure**: Syllabus (overview) + Assessment Handbook (detailed rubrics)
- **Legacy structure**: Syllabus + separate assessment-schedule.md + rubrics folder
- Adapt reading strategy based on what files exist

**If information missing:**
- Ask user to clarify before proceeding
- Cannot generate without topic and key concepts

---

### Step 2: Generate Lecture Content

**Follow lecture_content_instructions.md structure exactly:**

#### Opening (5-7 slides, ~13-16 mins):
1. **Hook slide** - Question/statistic/scenario related to topic
2. **Key Vocabulary slide** - 5-8 terms with Vietnamese translations
3. **Learning objectives slide** - 3-5 student-centered objectives
4. **Assessment connection slide** - How this week connects to upcoming graded work

**Vietnamese ESL Support:**
- Slide 2 must include key vocabulary translations (see templates/vocabulary-translation-template.md)
- Use WebSearch to verify Vietnamese business terminology
- Include pronunciation guides and context examples
- Students need this priming to follow complex English lectures

#### Core Content (14-20 slides, ~60-65 mins):
- Organize into 3-4 major segments
- Pattern: Theory → Example → Application
- Include engagement activities every 15-20 minutes
- Reference required readings explicitly
- Incorporate current examples (2023-2025) with citations

**Research integration (REQUIRED):**
Use WebSearch to find Vietnamese market context:
  - **Vietnam-specific examples:** "[topic] Vietnam business 2024"
  - **Vietnamese companies:** "[concept] Vietnamese companies examples"
  - **ASEAN applications:** "[topic] Southeast Asia"
  - **Current Vietnamese statistics:** "[industry] Vietnam market size 2024"
  - **Vietnamese case studies:** "[concept] Vietnam case study English"
  - **Regional comparisons:** "Vietnam vs [country] [topic]"

**Goal:** Every lecture should have 2-3 Vietnamese or ASEAN examples
**Note:** Search in English (Vietnamese students' medium of instruction)

**Citation requirements (STRICTLY ENFORCED):**

**CRITICAL: Every statistical claim, research finding, or framework MUST have inline citation.**

**What requires citation:**
- ANY statistic or percentage ("X% of employees...", "3 times more likely...")
- Research findings about human behavior or organizational outcomes
- Framework attributions (Drive theory, 70-20-10 model, Gibbs cycle, etc.)
- Expert opinions or thought leadership quotes
- Survey results or study findings
- Claims about effectiveness, correlation, or causation

**Citation format:**
- Inline: (Author, Year) immediately after the claim
- Example: "Employees who find purpose are 3x more likely to stay (Steger et al., 2012)."
- Full APA reference on References slide at end of lecture
- Include DOI or URL for verification
- References slide: Alphabetical order by first author's last name (APA 7th format)

**Research process:**
- Use WebSearch to find actual research backing statistical claims
- Search: "[specific claim] research study" or "[topic] [year range] peer reviewed"
- Verify source quality (peer-reviewed journal, HBR, top management schools)
- NEVER fabricate sources - if you can't find research, don't make the claim
- If using Vietnamese examples, cite local sources or news when available

**Quality check before finalizing:**
- [ ] Every percentage has citation
- [ ] Every "X times more likely" has citation
- [ ] Every framework has attribution (first mention)
- [ ] Every research claim has source
- [ ] All citations appear on References slide at end

#### Wrap-up (4-6 slides, ~13-15 mins):
1. **Synthesis slide** - Key concepts summary
2. **Tutorial preview slide** - What they'll practice in tutorial
3. **Assessment bridge slide** - How to apply in upcoming assessment
4. **References slide** - All sources cited in alphabetical order by first author's last name

**Content Limits (Aligned with Slide Converter Layouts):**

**CRITICAL: Enforce these limits to prevent overly verbose slides:**

```
SLIDE CONTENT LIMITS:
- Maximum 150-200 words per slide body
- Maximum 6-8 bullet points per slide
- Maximum 20 words per bullet point
- One main concept per slide

IF CONTENT EXCEEDS LIMITS:
- Auto-split into Part 1 & Part 2 slides
- Move supporting detail to speaker notes
- Use two-column layout if comparing (future capability)
- Split into separate slides if covering 5+ related items

LAYOUT TYPE GUIDANCE:
Specify layout type based on content structure (aligned with HTML converter capabilities):

FOUNDATIONAL LAYOUTS:
- Standard content → content-slide (default - bullets, paragraphs, mixed)
- Course/module opening → title-slide (first slide only)
- Major section transition → section-break (single bold statement, 2-6 words)

STRUCTURED CONTENT:
- Key vocabulary/terms → vocab-table-slide (bilingual table, 4-8 terms)
- Learning objectives → objectives-slide (numbered list, Bloom's verbs, 3-6 items)
- Assessment checklist → checklist-slide (categorized criteria, checkboxes)
- Academic references → references-slide (APA format, end of deck)

EMPHASIS & VISUAL IMPACT:
- Single key statistic → big-number-slide (one large number with context)
- Multiple related stats → stats-banner (2-4 metrics side-by-side)
- Important quote → quote-slide (quotation marks, attribution)
- Dark background for emphasis → dark-slide (STRATEGIC USE - see guidance below)

COMPARISONS & RELATIONSHIPS:
- Side-by-side comparison → comparison-slide (2 boxes, equal content)
- Detailed comparison table → comparison-table-slide (2 columns, multiple rows)
- Visual framework/model → framework-slide (processes, cycles, diagrams)

INTERACTION & REFLECTION:
- Hands-on activity → activity-slide (numbered steps, timing, instructions)
- Reflection prompts → reflection-slide (questions, thinking time)

GROUPED CONTENT:
- 2-4 related concepts → card-layout (visual cards with borders)

USE LAYOUT-SPECIFIC CLASSES:
When specifying non-standard layouts, add appropriate CSS class in [LAYOUT: ] tag.
Example: [LAYOUT: activity-slide] or [LAYOUT: comparison-table-slide]

**STRATEGIC USE OF DARK SLIDES (dark-slide):**

Dark slides create visual contrast and emphasis. Use them strategically 2-4 times per lecture for:

✓ **WHEN TO USE DARK SLIDES:**

1. **Real-world case studies**
   - Company examples (Vietnamese or international)
   - Success/failure stories
   - "How [Company] Applied [Concept]" slides
   - Example: "Vietnamese Context: How Vinamilk Built Brand Loyalty"

2. **Vietnamese/ASEAN context examples**
   - Local market applications
   - Cultural adaptations of Western theories
   - Regional business practices
   - Example: "ASEAN Example: Grab's Regional Expansion Strategy"

3. **Important quotes from experts**
   - Thought leadership statements
   - Research findings with high impact
   - Inspirational messages
   - Example: Quote from Peter Drucker, Simon Sinek, or local business leaders

4. **Storytelling/narrative moments**
   - Before/after transformation stories
   - Personal development journeys
   - Problem → Solution narratives
   - Example: "Story: A Graduate's First Year Applying Drive Theory"

5. **Critical emphasis points**
   - Common mistakes to avoid (with examples)
   - Key insights that deserve dramatic emphasis
   - "What NOT to do" warnings
   - Example: "Warning: Why Most Development Plans Fail"

6. **Contrast with surrounding content**
   - After 3-4 standard slides, use dark slide for variety
   - Signals transition to practical application
   - Breaks lecture monotony

✓ **TARGET: Include 2-4 dark slides per 22-30 slide lecture**

✓ **PLACEMENT STRATEGY:**
- Distribute throughout lecture (not clustered)
- Use after introducing theory to show application
- Use before/after activities to frame context
- End segments with dark slide case study

✓ **CONTENT INDICATORS FOR DARK SLIDES:**
Title patterns that signal dark slide use:
- "Case Study: [Company/Person]"
- "Vietnamese Context: [Topic]"
- "Real-World Example: [Application]"
- "Story: [Narrative]"
- "Warning: [Common Mistake]"
- "Quote: [Expert Name]"
- "[Country/Region] Application: [Concept]"

❌ **WHEN NOT TO USE DARK SLIDES:**
- Definitions or theory (use standard content-slide)
- Lists of concepts (use standard or card layout)
- Data tables (use standard or comparison-table)
- Activities (use activity-slide)
```

**Slide format:**
```markdown
---

**SLIDE [#]: [Active, Specific Title]**
[LAYOUT: content-slide / section-break / big-number-slide / activity-slide]

CONTENT:
[Core concepts - MAX 150-200 words]
[Examples, data, frameworks ON the slide]
[Inline citations IMMEDIATELY after claims - NO EXCEPTIONS]
[Keep bullets to 6-8 max, 20 words each]

**CITATION EXAMPLES (follow these patterns):**

✅ CORRECT - Statistical claim with inline citation:
"Employees who find purpose are 3x more likely to stay with their organization (Steger et al., 2012)."

✅ CORRECT - Framework attribution:
"According to Pink's Drive theory (Pink, 2009), intrinsic motivation comes from autonomy, mastery, and purpose."

✅ CORRECT - Research finding:
"The 70-20-10 model shows that 70% of professional development comes from on-the-job experience (Lombardo & Eichinger, 1996)."

❌ WRONG - No citation:
"Research shows employees with purpose are more engaged." [Which research? Add citation!]

❌ WRONG - Vague attribution:
"Studies show 90% of online courses aren't completed." [Which studies? Add citation!]

[If source is key to entire slide, include full reference at bottom:]
*Senge, P. M. (2006). The fifth discipline: The art and practice of the learning organization. Currency/Doubleday.*

[PURPOSE: Inform/Persuade/Inspire]
[TIMING: X minutes]

---

## Speaker Notes

**CRITICAL: EVERY slide MUST have speaker notes in BULLET FORMAT (150-200 words).**

**FORMAT: Bullet points with key teaching points - NOT word-for-word scripts.**

**Opening:** (1-2 bullets)
- Hook, transition, or connection from previous slide
- How to introduce this slide's concept

**Key Teaching Points:** (3-5 bullets)
- Main concepts to emphasize and explain
- Important definitions or distinctions to clarify
- Analogies or metaphors to aid understanding

**Examples/Stories:** (1-2 bullets)
- Concrete examples to share (Vietnamese context when possible)
- Real-world applications or case stories
- Cultural nuances to acknowledge

**Common Misconceptions:** (if applicable)
- What students typically get wrong about this concept
- Clarifications to provide

**Check for Understanding:** (1 bullet)
- Question to ask class or quick activity to gauge comprehension
- Expected responses and how to handle them

**Transition:** (1 bullet)
- How to bridge to next slide
- Connection to make explicit

**Length:** 150-200 words total
**Tone:** Conversational key points, as if briefing an instructor
**Do NOT:** Write paragraphs or word-for-word scripts to read aloud
**DO:** Use bullets with specific phrases, questions, examples, and teaching tactics

[Example of good speaker notes - DO THIS for every slide:]

**Opening:**
- Start with validation: "How many of you have felt frustrated when reality doesn't match your goals?" [Show of hands creates connection]

**Key Teaching Points:**
- Personal mastery is NOT perfection - it's a discipline you practice daily
- Emphasize the lifelong nature: "This isn't a course module; it's a life practice"
- Write on board: "Creative Tension = Vision - Current Reality"

**Examples/Stories:**
- Vietnamese example: Student who balanced traditional family expectations with personal career vision
- Show how tension can be productive, not just stressful

**Common Misconceptions:**
- Students think personal mastery means being perfect at everything → Clarify: It's about continuous growth in areas you choose

**Check for Understanding:**
- "Can someone share an area where they're practicing personal mastery right now?" [Take 1-2 responses]

**Transition:**
- "Now let's break down the specific elements of personal mastery, starting with vision vs. goals..."
```

**Target:** 22-30 content slides total

**Quality check:** Before finalizing lecture content, verify:

**Content & Structure:**
- [ ] EVERY slide has speaker notes in bullet format (150-200 words each)
- [ ] NO slide exceeds 200 words of content (if so, split into Part 1/Part 2)
- [ ] Bullets limited to 6-8 per slide, 20 words each
- [ ] Layout type specified where non-standard
- [ ] 2-4 dark slides included for case studies, Vietnamese examples, or quotes
- [ ] Missing or superficial speaker notes = incomplete lecture file

**Citations & Research (CRITICAL):**
- [ ] EVERY statistical claim has inline citation (Author, Year)
- [ ] EVERY "X times more likely" statement has source
- [ ] EVERY "X% of people" claim has citation
- [ ] EVERY framework attributed on first mention (Senge, 2006; Pink, 2009)
- [ ] NO "research shows" without naming the research
- [ ] All inline citations appear in References slide at end
- [ ] All References have DOI or URL for verification
- [ ] References slide entries in ALPHABETICAL ORDER by first author's last name
- [ ] No fabricated sources - if can't verify, remove the claim

**If any citation missing → STOP and conduct WebSearch to find source OR remove claim**

---

### Step 3: Generate Tutorial Content

**Follow lecture_content_instructions.md tutorial structure:**

#### Opening (10 mins):
- Quick concept review (3 key points from lecture)
- Preview of assessment being prepared for
- Show simplified rubric for today's practice
- **Reference**: "See Assessment Handbook Section X for complete rubric"

#### Main Activity (55-60 mins):
**CRITICAL: Design ONE substantial activity that mirrors actual assessment**

**Based on assessment schedule and handbook, determine focus:**
- Check assessment-handbook.md (or assessment-schedule.md if legacy) for:
  - What's due in next 2-3 weeks
  - Full rubric criteria for that assessment
  - Specific requirements and deliverables
- If portfolio piece due soon → Practice creating that document type
- If presentation coming up → Practice presentation skills
- If quiz next week → Extended quiz prep with practice problems
- If project milestone due → Work on project component

**Pull from Assessment Handbook:**
- Use actual rubric criteria (simplified to 3-4 key dimensions)
- Reference specific submission requirements
- Include preparation checklist items if available
- Model peer review language from handbook examples

**Activity structure:**
```markdown
### MAIN ACTIVITY: [Name - Mirrors Actual Assessment] (55-60 minutes)

**Setup** (5 minutes):
- Clear, numbered instructions
- Distribute materials/templates
- Form pairs/groups if needed

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
```

#### Quiz Preparation (15-20 mins):
- 5-8 practice questions in quiz format
- Review answers with explanations
- Connect to key concepts

#### Wrap-up (5-10 mins):
- Self-assessment against rubric
- What to revise before submission
- Next steps for assessment preparation

**Include throughout:**
- **Simplified rubric** (3-4 key criteria from full assessment rubric in handbook)
  - Example format: "Today we're practicing [Assessment Name]. The full rubric has [X] criteria (see Assessment Handbook Section X), but today we'll focus on these key areas: [list 3-4]"
- **Clear references** to where students can find complete details:
  - "For complete submission requirements, see Assessment Handbook Section X"
  - "The full rubric with all performance levels is in Assessment Handbook Section X"
- Peer review sentence starters
- Cultural considerations for Vietnamese students
- Clear time allocations

---

### Step 4: Quality Check

**Lecture content checklist:**
- [ ] 22-30 content slides total
- [ ] 3-5 verified sources with DOI/URLs
- [ ] Inline citations for all sourced material
- [ ] Examples current (2023-2025) and culturally diverse
- [ ] Direct link to assessment stated
- [ ] Speaker notes appropriate for slide type
- [ ] Engagement activities every 15-20 mins

**Tutorial content checklist:**
- [ ] ONE main activity that mirrors actual assessment
- [ ] Simplified rubric provided (3-4 criteria)
- [ ] 5-8 quiz practice questions included
- [ ] Peer review structured with rubric
- [ ] Clear connection to upcoming graded work
- [ ] Time allocated correctly (10 + 55-60 + 15-20 + 5-10)
- [ ] Cultural considerations for Vietnamese context

---

### Step 5: Save and Update Tracking

**Save files:**
1. `courses/[COURSE-CODE]-*/weeks/week-[N]/lecture-content.md`
2. `courses/[COURSE-CODE]-*/weeks/week-[N]/tutorial-content.md`

**Update course-info.md:**
- Mark week [N] lecture as ✓ completed
- Mark week [N] tutorial as ✓ completed
- Update status

**Output to user:**
```markdown
✓ Week [N] content generated successfully!

## Generated Files

📄 **Lecture Content:** courses/[COURSE-CODE]-[slug]/weeks/week-[N]/lecture-content.md
   - [X] slides created
   - [X] sources cited
   - Assessment connection: [Assessment name]

📄 **Tutorial Content:** courses/[COURSE-CODE]-[slug]/weeks/week-[N]/tutorial-content.md
   - Main activity: [Activity name - mirrors assessment]
   - Assessment prep: [Assessment name, due Week X]
   - Quiz prep: [X] practice questions

## Next Steps

1. **Review content** for accuracy and appropriateness
2. **Create slides** using /export-slides [N] (after content approval)
3. **Generate next week** using /generate-week [N+1]

## Quick Links

- Lecture: `courses/[COURSE-CODE]-[slug]/weeks/week-[N]/lecture-content.md`
- Tutorial: `courses/[COURSE-CODE]-[slug]/weeks/week-[N]/tutorial-content.md`
```

---

## Assessment Alignment Logic

**Determine tutorial focus by checking assessment schedule:**

```
IF portfolio piece due in Week [N] or [N+1]:
   → Tutorial activity = Draft that specific portfolio piece
   → Use full rubric for that assignment
   → Peer review focuses on rubric criteria

ELSE IF presentation due in Week [N] to [N+2]:
   → Tutorial activity = Practice presentation skills
   → Use presentation rubric
   → Include practice presentations with feedback

ELSE IF quiz scheduled in Week [N+1]:
   → Tutorial activity = Extended quiz prep (40 mins instead of 20)
   → Include 10-15 practice questions
   → Review challenging concepts

ELSE IF project milestone due soon:
   → Tutorial activity = Work on specific project component
   → Use project rubric
   → Peer review of project drafts

ELSE:
   → Tutorial activity = General skill practice related to topic
   → Use generic rubric
   → Focus on application of lecture concepts
```

---

## Research Integration

**During lecture content generation:**

**For current examples (use WebSearch):**
```
"[topic] [current year] business example"
"[concept] Vietnam application"
"[framework] [year range] case study"
"[topic] statistics [recent year]"
```

**For Vietnam-specific content:**
```
"[topic] Vietnam business"
"[concept] Vietnamese companies"
"[framework] application Southeast Asia"
```

**Always cite sources:**
- Web sources → Full URL and access date
- News articles → Publication, date, URL
- Statistics → Original source with verification

---

## Cultural Adaptation

**For Vietnamese university context:**

**Lecture adaptations:**
- Include Vietnamese business examples when possible
- Reference regional (ASEAN) context
- Use culturally relevant scenarios
- Consider local business practices

**Tutorial adaptations:**
- Structured peer interaction (Vietnamese students may need guidance)
- Provide sentence starters for feedback:
  - "One strength I notice is..."
  - "One suggestion for improvement is..."
- Build confidence gradually for presentations
- Use local examples for case discussions

---

## Templates and Resources

**Load as needed:**
- Lecture template: `templates/lecture-template.md` (if exists)
- Tutorial template: `templates/tutorial-template.md` (if exists)
- Assessment rubrics: `courses/[COURSE-CODE]-*/rubrics/`
- Week specification: `templates/week-topic-specification.md`

**Reference throughout:**
- Lecture content instructions: `lecture_content_instructions.md`
- Syllabus: Course-specific
- Assessment schedule: Course-specific

---

## Error Handling

**If syllabus missing:**
```
❌ Error: Syllabus not found for this course.

Please run /generate-syllabus first to create the course syllabus.
```

**If week number invalid:**
```
❌ Error: Week [N] is outside course range (1-[MAX_WEEKS]).

Available weeks: 1-[MAX_WEEKS]
```

**If week already has content:**
```
⚠️ Warning: Week [N] already has content.

Options:
1. Regenerate (overwrites existing content)
2. Edit existing content instead
3. Cancel

What would you like to do?
```

---

## Estimated Time

**Per week:**
- Research and context gathering: 5-10 minutes
- Lecture content generation: 20-30 minutes
- Tutorial content generation: 15-20 minutes
- Quality check and formatting: 5-10 minutes

**Total: 45-70 minutes per week** for high-quality, research-backed, assessment-aligned content

This investment ensures students receive world-class materials that directly prepare them for success in assessments.
