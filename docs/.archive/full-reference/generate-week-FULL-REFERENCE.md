# Generate Week Content

Generate complete weekly content including lecture materials and tutorial activities based on the course syllabus. This command creates assessment-aligned content following all established best practices and quality standards.

---

## STEP 0: ENFORCED WORKFLOW (DO THIS FIRST)

**CRITICAL: Before generating ANY content, you MUST complete this checklist:**

### 0.0: Check for Auto-Imported Research (NEW - Phase 2)

**Check for validation flags from Claude Desktop:**

1. **Look for flag file:**
   - Path: `courses/[COURSE-CODE]/.working/research/.week-[N]-ready`
   - This flag indicates research was auto-written by Claude Desktop

2. **If flag file exists:**
   - Read the flag file to confirm week number matches
   - Inform user: "✓ Found auto-imported research for Week [N] from Claude Desktop"
   - Inform user: "Validating research before generating content..."
   - **Run validation checks:**
     - Format validation (week-N-research.md exists, topic stated, 4 articles present)
     - Content validation (all 4 concepts have ✓, Key Teaching Content present)
     - Quality validation (2 seminal + 2 recent balance, APA citations)
     - Key Teaching Content validation (framework definitions, applications, case studies present)
   - **If validation passes:**
     - Inform user: "✓ Research validation passed - proceeding with content generation"
     - Delete the flag file (`.week-[N]-ready`)
     - Continue to Step 0.1
   - **If validation fails:**
     - Inform user: "✗ Research validation failed - cannot generate content"
     - Show specific validation errors
     - Advise: "Please fix research issues using `/import-research [course] [week]` or regenerate research in Claude Desktop"
     - STOP - do not generate content with invalid research

3. **If flag file does not exist:**
   - Continue normally to Step 0.1
   - Research was either manually imported or will be read from syllabus

**Purpose:** This automatic validation catches research issues BEFORE spending 45-70 minutes generating content, saving significant time if errors exist.

### 0.1: Create TODO List

Use the TodoWrite tool to create this checklist:

```
- [ ] Check for auto-imported research validation flag
- [ ] Read course syllabus (week topic, assessments, required articles)
- [ ] Read docs/CONTENT-GENERATION-BEST-PRACTICES.md (all constraints)
- [ ] Understand assessment schedule for tutorial alignment
- [ ] Generate lecture content (22-30 slides with all requirements)
- [ ] Validate lecture: splitting rules, speaker notes, layout variety, citations
- [ ] Generate tutorial content (student-facing, 90-minute structure)
- [ ] Generate tutorial tutor notes (instructor-facing with answer keys)
- [ ] Export GIFT quiz file (Moodle-ready format)
- [ ] Final validation: all checklists pass
- [ ] Present to user for approval
```

### 0.2: Read Required Documentation

**You MUST read these files BEFORE generating content:**

1. **Course syllabus** - Extract for week [N]:
   - Week topic name and key concepts
   - Required readings (2 articles)
   - Related learning objectives
   - Upcoming assessments (next 2-3 weeks)
   - Full rubric details (from assessment-handbook.md if available)

2. **docs/CONTENT-GENERATION-BEST-PRACTICES.md** - Review:
   - Slide content requirements (150-200 words, stands alone)
   - Splitting rules (5-7 bullets max, 2-3 line quotes, etc.)
   - Speaker notes rules (3-8 lines, don't repeat slide)
   - Layout variety requirements (section breaks, quotes, frameworks)
   - Tutorial structure (two separate files)
   - Quiz question rules (test slide content only)

3. **This command file** - Continue reading below for:
   - Detailed lecture structure requirements
   - Layout-specific guidance
   - Citation requirements
   - Tutorial activity design principles

### 0.3: Acknowledge Critical Constraints

**Confirm you understand these NON-NEGOTIABLE requirements:**

**Slide Content:**
- [ ] 150-200 words maximum per slide → Split if more
- [ ] Sufficient detail to stand alone (not sparse bullets)
- [ ] Examples, data, frameworks ON the slide
- [ ] Inline citations (Author, Year) for all sourced material

**Splitting Rules:**
- [ ] Max 5-7 bullets per slide → Split into 2 if more
- [ ] Quotes max 2-3 lines → Use content slide if longer
- [ ] Frameworks max 6 components → Split if 8+
- [ ] If cluttered → Split into 2 slides

**Speaker Notes:**
- [ ] 3-8 lines per slide (ruthlessly concise)
- [ ] Never repeat slide content
- [ ] Add context, timing, misconceptions, cultural notes
- [ ] No prescriptive actions ("walk around," "point to")

**Layout Variety (Content-Driven):**
- [ ] Section breaks at major topic transitions or framework introductions
- [ ] Quote slides when you have impactful quotes that merit emphasis
- [ ] Framework slides when teaching conceptual models or processes
- [ ] Comparison tables for side-by-side contrasts (vs., before/after)
- [ ] Big numbers or stats banners when you have compelling statistics
- [ ] Reflection slides when contemplative prompts fit the flow
- [ ] Dark slides for Vietnamese examples, case studies, or stories
- [ ] References slide at end WITH `<!-- LAYOUT: references -->`
- [ ] Use layouts that best present your content, not to meet quotas

**Tutorial Requirements:**
- [ ] TWO separate files (student-facing + tutor notes)
- [ ] Main activity mirrors actual assessment
- [ ] Quiz questions test SLIDE content ONLY (not speaker notes)
- [ ] 6-10 questions covering section break topics
- [ ] Complete answer keys with explanations in tutor notes

**If you skip Step 0 or cannot confirm these constraints, STOP and ask the user.**

---

## Your Task

Create both lecture content (22-30 slides with speaker notes) and tutorial content (assessment-aligned activities) for a specific course week.

## Prerequisites

**Required before running this command:**
1. Course syllabus must exist with weekly topics defined
2. Assessment schedule must be documented
3. Week topic and required readings identified
4. **Step 0 completed** (docs read, TODO list created, constraints acknowledged)

## Usage

**User provides:**
- Course code (e.g., BUS101)
- Week number (e.g., 3)

**You generate:**
- Lecture content document (22-30 slides)
- Tutorial content document (90-minute structure)
- Tutorial tutor notes document (instructor-facing)
- GIFT format quiz file (for Moodle import)
- Save all four to appropriate week folder

## Step-by-Step Process

### Step 1: Locate Course and Read Context

**Actions:**
1. Find course folder: `courses/[COURSE-CODE]-*/`
2. Read syllabus: `courses/[COURSE-CODE]-*/syllabus.md`
3. **Check for document structure:**
   - If `assessment-handbook.md` exists → Read it for detailed rubrics and instructions
   - Otherwise → Read `assessments/assessment-schedule.md` (legacy structure)
4. Read course info if available: `courses/[COURSE-CODE]-*/.working/course-info.md`
5. **Read research file:** `courses/[COURSE-CODE]-*/.working/research/week-N-research.md`

**Extract for Week [N]:**
- Week topic name
- Key concepts (4 required)
- Related learning objectives
- Upcoming assessments (what's due in next 2-3 weeks)
- **Full rubric details** (from assessment-handbook.md if available)

**From Research File (CRITICAL for lecture content):**
- **4 articles** (2 seminal + 2 recent) with full citations
- **Key Teaching Content for each article:**
  - Seminal: Framework definitions, components, how it works, applications, examples
  - Recent: Main insights, practical applications, case studies, statistics/quotes
- Coverage validation (which articles cover which concepts)

**Document Structure Awareness:**
- **2-document structure**: Syllabus (overview) + Assessment Handbook (detailed rubrics)
- **Legacy structure**: Syllabus + separate assessment-schedule.md + rubrics folder
- **Research file**: Per-week research with Key Teaching Content
- Adapt reading strategy based on what files exist

**If information missing:**
- Ask user to clarify before proceeding
- Cannot generate without topic, key concepts, AND research file

---

### Step 1.5: Syllabus-Research Alignment Filter

**Before generating content, compare research against syllabus to ensure relevance.**

**1. Extract syllabus week topics:**
- Read Week N theme from syllabus (e.g., "Strategic Communication Foundations")
- Read Week N key concepts (4 required)
- **Scan OTHER weeks' themes** to identify where content might better belong

**2. Scan research for alignment:**
For each article's Key Teaching Content, identify:
- What is the PRIMARY topic of this content?
- Does it match THIS week's syllabus theme?
- Does it match ANOTHER week's theme better?

**3. Apply filtering logic:**

| Situation | Action |
|-----------|--------|
| Content matches this week's syllabus | **INCLUDE** in lecture |
| Content matches another week's syllabus better | **EXCLUDE** (will be used in that week) |
| Content doesn't match any week clearly | **INCLUDE** (no better place for it) |

**4. Log what was filtered:**
After filtering, note what was excluded:
```
ℹ️ Syllabus Alignment Filter Applied:
- INCLUDED: Shannon-Weaver model (matches Week 1: communication process)
- INCLUDED: DISC framework (matches Week 1: self-assessment)
- EXCLUDED: Abrahams anxiety techniques (better fit for Week 5: presentation anxiety)
- EXCLUDED: "What So What Now What" framework (better fit for Week 5: impromptu speaking)
```

**Example: Week 1 Filtering**

Abrahams "How to Shine When You're Put on the Spot" contains:

| Content | Primary Topic | Week 1 Match? | Action |
|---------|---------------|---------------|--------|
| "Conversation not performance" | Audience-centered | ✓ Yes | INCLUDE |
| Self-assessment questions | Personal development | ✓ Yes | INCLUDE |
| Six-step CURFLIS methodology | Presentation anxiety | ✗ No (Week 5) | EXCLUDE |
| "What So What Now What" | Impromptu speaking | ✗ No (Week 5) | EXCLUDE |
| Deep breathing techniques | Anxiety management | ✗ No (Week 5) | EXCLUDE |

**MANDATORY: Incorporate ALIGNED Research Content**

After filtering, incorporate ALL remaining aligned content:
- **Every framework** that matches this week → Slides with full definitions
- **Every case study** that matches this week → Slides OR speaker notes
- **Every statistic/quote** that matches → Cited on relevant slides
- **Speaker notes** → Draw background context from research

Content excluded by the filter will be used in its proper week - nothing is lost, just properly allocated.

---

### Step 2: Generate Lecture Content

**Follow lecture_content_instructions.md structure exactly:**

#### Opening (5-7 slides, ~13-16 mins):
1. **Title slide** - Week number/title, course name (bolded), university, semester, instructor names
2. **Hook slide** - Question/statistic/scenario related to topic
3. **Key Vocabulary slide** - 5-8 terms with Vietnamese translations
4. **Learning objectives slide** - 3-5 student-centered objectives
5. **Assessment connection slide** - How this week connects to upcoming graded work

**Title Slide Format:**
```markdown
**SLIDE 1: Week [N]: [Week Title]**

TITLE: Week [N]: [Week Title]

SUBTITLE: [Week subtitle/topic overview]

CONTENT:

**[Course Name]**

Week [N]: [Week Title]

[University Name] - [Campus]
[Semester/Term]

Instructors: [Name 1], [Name 2]
```
**Note:** Course name should be in markdown bold `**Course Name**` - converter will render as `<strong>`

**Vietnamese ESL Support:**
- Slide 2 must include key vocabulary translations (see templates/vocabulary-translation-template.md)
- Use WebSearch to verify Vietnamese business terminology
- Include pronunciation guides and context examples
- Students need this priming to follow complex English lectures

#### Core Content (14-20 slides, ~60-65 mins):
- Organize into 3-4 major segments
- Pattern: Theory → Example → Application
- Include engagement activities every 15-20 minutes
- Incorporate current examples (2023-2025) with citations

**CRITICAL: Use Key Teaching Content from Research File**

The research file contains pre-extracted content for lecture generation. USE IT:

**From Seminal Articles (theoretical foundation):**
- **Framework definitions** → Use verbatim or paraphrase for concept slides
- **Components** → Structure framework slides around these
- **How it works** → Explain mechanism in speaker notes or content
- **Applications** → Include in "applying the theory" slides
- **Examples** → Use as illustrative examples
- **Statistics/Quotes** → Use for big-number slides, quote slides

**From Recent Articles (practical application):**
- **Main insight** → Structure applied content around this
- **Practical applications** → Use for "how to apply" slides
- **Case studies** → Use for dark slides (Vietnamese/business context)
- **Statistics/Quotes** → Use for compelling data points and quotes

**Content Integration Pattern:**
1. **Concept introduction** → Use framework definition from seminal article
2. **Components breakdown** → Use components list from seminal article
3. **How it works** → Use mechanism explanation from seminal article
4. **Real-world application** → Use case study from recent article
5. **Current relevance** → Use statistics/insights from recent article
6. **Vietnamese context** → Supplement with WebSearch if not in research

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

**⚠️ FULL REFERENCE vs INLINE CITATION:**

The HTML converter automatically extracts and separates full references from slide content:

**INLINE CITATIONS (keep in content):**
```
Parenthetical format: (Author, Year)
Example: "Research shows 67% improvement (Smith, 2023)."
Stays: IN the slide content as part of the text
```

**FULL REFERENCES (extracted to footer):**
```
Italicized APA format: *Author, Initials. (Year). Title. Source.*
Example: *Pink, D. H. (2009). Drive: The surprising truth about what motivates us. Riverhead Books.*
Extracted: AUTOMATICALLY moved to slide footer by converter
```

**When to use each:**

**Use INLINE citations for:**
- Statistics with sources: "67% of employees (Smith, 2023)"
- Research claims: "Studies show correlation (Jones et al., 2022)"
- Framework mentions: "Senge's (2006) creative tension model"
- Multiple references in same slide

**Use FULL references for:**
- Primary source for a framework slide (e.g., Pink's Drive Theory)
- Main article being discussed in detail
- One authoritative source for entire slide
- Source of case study or detailed example

**IMPORTANT: Place full references at END of slide content:**
```markdown
CONTENT:

**Component 1:** Description of component

**Component 2:** Description of component

**Component 3:** Description of component

*Pink, D. H. (2009). Drive: The surprising truth about what motivates us. Riverhead Books.*
```

The converter will:
1. Extract the italicized reference
2. Remove it from content
3. Place it in a styled footer at bottom of slide
4. Leave inline citations (Author, Year) untouched in content

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
- Major section transition → section-break (orange background, white text, bold statement, 2-6 words, use 2-3 max per lecture)

STRUCTURED CONTENT:
- Key vocabulary/terms → vocab-table-slide (bilingual table, 4-8 terms)
- Learning objectives → objectives-slide (numbered list, Bloom's verbs, 3-6 items)
- Assessment checklist → checklist-slide (categorized criteria, checkboxes)
- Academic references → references-slide (APA format, end of deck)

EMPHASIS & VISUAL IMPACT:
- Single key statistic → big-number-slide (ONE dramatic number, 135pt, cream background)
- Multiple related stats → stats-banner (2-4 metrics side-by-side, dashboard style)
- Important quote → quote-slide (2-3 lines, attribution, requires prescriptive hint)
- Dark background for emphasis → dark-slide (STRATEGIC USE - see guidance below)

COMPARISONS & RELATIONSHIPS:
- Side-by-side comparison → comparison-slide (2 boxes, equal content)
- Detailed comparison table → comparison-table-slide (2 columns, multiple rows)
- Visual framework/model → framework-slide (processes, cycles, diagrams)

INTERACTION & REFLECTION:
- Hands-on activity → activity-slide (numbered steps, timing, instructions)
- Reflection prompts → reflection-slide (questions, thinking time)

GROUPED CONTENT:
- 3-6 related concepts → card-layout (visual cards with icons/emojis, better than bullets for frameworks)

USE LAYOUT-SPECIFIC CLASSES:
When specifying non-standard layouts, add appropriate CSS class in [LAYOUT: ] tag.
Example: [LAYOUT: activity-slide] or [LAYOUT: comparison-table-slide]

**🎯 CONTENT-DRIVEN LAYOUT SELECTION:**

**Choose layouts that best present your content:**
- **Section breaks** - Use at major topic transitions or when introducing new frameworks
- **Quote slides** - Use when you have impactful quotes that merit visual emphasis
- **Framework slides** - Use when teaching conceptual models or processes (see splitting pattern below)
- **Dark slides** - Use for case studies, Vietnamese examples, or stories that benefit from emphasis
- **Card layouts** - Use when presenting 3-6 parallel concepts that benefit from visual organization
- **Big number/stats slides** - Use when you have compelling statistics that deserve dramatic presentation
- **Reflection prompts** - Use when contemplative questions fit naturally in the flow
- **Vocab table** - Use when introducing key terms that need Vietnamese translations
- **Comparison tables** - Use for side-by-side contrasts (vs., before/after scenarios)

**Principle: Match layout to content type, not arbitrary quotas. Visual variety should emerge naturally from diverse content.**

**📐 FRAMEWORK SPLITTING PATTERN (REQUIRED FOR COMPLEX FRAMEWORKS):**

**Problem:** Dense slides that combine framework presentation + explanation reduce visual variety and effectiveness.

**Solution:** Split complex frameworks into multiple slides following this pattern:

**PATTERN:**
1. **Framework slide** → Use <!-- LAYOUT: framework --> for visual model
2. **Component explanation slides** → 1-2 content slides unpacking key components
3. **Application/example slide** → Dark slide or content slide showing practical use

**EXAMPLES:**

**Example 1: Personal Mastery Framework (Senge)**
- Slide 8: **Personal Mastery Framework** → <!-- LAYOUT: framework --> showing creative tension model (visual: Current Reality → [Gap] → Vision)
- Slide 9: **Understanding Creative Tension** → Content slide explaining the gap concept
- Slide 10: **Two Response Patterns** → Content or comparison slide (productive vs. unproductive responses)
- Slide 11: **Vietnamese Context Example** → <!-- LAYOUT: dark-bg --> case study applying the framework

**Example 2: Drive Theory (Pink)**
- Slide 14: **Drive Theory: Three Elements** → <!-- LAYOUT: framework --> or card layout showing Autonomy, Mastery, Purpose
- Slide 15: **Autonomy in Development** → Content slide defining autonomy
- Slide 16: **Mastery Motivation** → Quote slide from Pink on mastery mindset
- Slide 17: **Purpose in Professional Development** → Quote slide on purpose
- Slide 18: **ASEAN Context: Applying Drive Theory** → <!-- LAYOUT: dark-bg --> with VNG Corporation case study

**Example 3: Sustainable Learning System**
- Slide 22: **Four Components Framework** → <!-- LAYOUT: framework --> showing the cycle (Outcomes → Practice → Feedback → Adjustment)
- Slide 23: **Component 1: Clear Outcomes** → Content slide with SMART goals explanation
- Slide 24: **Component 2: Feedback Loops** → Content slide with examples
- Slide 25: **Building Habits That Support Your System** → Content with Atomic Habits examples

**WHEN TO SPLIT:**
- Framework has 3+ components that need explanation
- Each component deserves 50+ words of explanation
- Framework requires both theory AND practical application
- Combining everything creates 200+ word slides

**WHEN NOT TO SPLIT:**
- Simple 2-component models (e.g., Fixed vs. Growth Mindset comparison)
- Frameworks that are self-explanatory from visual
- Checklists or step-by-step processes (keep together for reference)

**EXPECTED RESULT:**
- 30-50 slides per lecture (up from 22-30) with better pedagogical flow
- Frameworks split = 3-4 slides each (framework + 2-3 explanation/application slides)
- Visual variety increases significantly (more framework, quote, dark slides)
- Standard content slides remain ≤50% of total

---

**📋 QUICK DECISION: Lists vs Tables**

Use this guide when structuring slide content:

| Content Pattern | Use This | Example |
|----------------|----------|---------|
| **2 concepts side-by-side** | Comparison Table (2 cols) | Fixed vs Growth Mindset |
| **4-8 items, 3+ attributes each** | Structured Table (3+ cols) | Presentation timeline, Process steps |
| **3-5 sequential points** | Numbered List | Three Key Takeaways |
| **3-5 non-sequential items** | Bullet List | Benefits of X |
| **Visual framework (boxes/arrows)** | Framework Slide | Drive Theory, Creative Tension |

**⚠️ RED FLAG:** If you're writing **4+ sections** that all have the **same structure** (e.g., time + description, step + action + outcome), use a **table** instead of lists.

---

**📊 COMPARISON TABLE PATTERN (REQUIRED FOR VS/CONTRASTS):**

**🚨 AUTOMATIC DETECTION RULES - Generate Comparison Tables When:**

1. **Title contains comparison keywords:**
   - "vs", "vs.", "versus"
   - "Fixed vs Growth", "Traditional vs Modern"
   - "Two Ways to...", "Two Responses..."
   - "When to X vs What NOT to X"
   - "X or Y", "Productive vs Unproductive"

2. **Content has contrasting bullet list structure:**
   - Two distinct sections with opposing headers
   - Headers like "Fixed Mindset:" / "Growth Mindset:"
   - Headers like "Productive Response:" / "Unproductive Response:"
   - Headers like "When to Adjust:" / "What NOT to Adjust:"
   - Lists using contrasting symbols (✓ vs ❌, ✓ vs ✗)

3. **Concept requires side-by-side comparison:**
   - Comparing two theoretical approaches
   - Contrasting recommended vs not-recommended practices
   - Showing before/after transformations
   - Demonstrating opposing mindsets or strategies

**When to Use:**
- Comparing two concepts/approaches (Fixed vs Growth, Traditional vs Innovative, When vs What NOT)
- Contrasting options or alternatives
- Pros/Cons lists side-by-side
- Before/After comparisons
- Any "versus" or "comparison" content

**CRITICAL: Content MUST use markdown table format, not bullet lists!**

**⚠️ IMPORTANT: NO MANUAL CHANGES**
All content must be generated using this pattern. Do NOT manually edit lecture-content.md to add comparison tables - regenerate the content using this command so the pattern is applied consistently.

**Pattern:**
1. **Title must signal comparison**: Include "vs", "versus", "Comparison:", "When/What NOT", or "Before/After"
2. **Content must use markdown table**:
   ```markdown
   | Concept A | Concept B |
   |-----------|-----------|
   | Point 1   | Point 1   |
   | Point 2   | Point 2   |
   ```
3. **Add layout hint**: `<!-- LAYOUT: comparison-table -->`

**Examples:**

**Example 1: Fixed vs Growth Mindset**
```markdown
TITLE: Fixed Mindset vs. Growth Mindset

CONTENT:

| Fixed Mindset | Growth Mindset |
|--------------|----------------|
| Talent is innate | Abilities develop through effort |
| "I can't do this" | "I can't do this YET" |
| Avoids challenges | Embraces challenges as learning |
| Gives up when faced with obstacles | Persists using different strategies |

<!-- LAYOUT: comparison-table -->
```

**Example 2: When to Adjust Goals**
```markdown
TITLE: When to Adjust vs. What to Keep Stable

CONTENT:

| When to Adjust ✓ | What to Keep Stable ❌ |
|-----------------|----------------------|
| Feedback reveals new skill gap | Core values (these remain constant) |
| New aligned opportunity emerges | 5-year vision (guides long-term) |
| Goal achieved earlier than expected | Commitment to personal growth |
| External conditions change significantly | Goals during normal difficulty |

<!-- LAYOUT: comparison-table -->
```

**Example 3: Two Ways to Respond (Contrasting Approaches)**
```markdown
TITLE: Two Ways to Respond to the Gap

CONTENT:

When you feel the gap between current reality and vision, you have two choices:

| Unproductive Response ❌ | Productive Response ✓ |
|------------------------|---------------------|
| "That goal is too ambitious, I'll settle for less" | "The gap shows me what to work on" |
| "Maybe I'm not capable of that level" | "I'll develop the capabilities I need" |
| "I'll adjust my vision to match current reality" | "This tension motivates my learning plan" |
| **Result:** Tension disappears, but so does growth | **Result:** Tension drives continuous development |

<!-- LAYOUT: comparison-table -->
```

**❌ DON'T DO THIS (Will render as standard content, not comparison):**
```markdown
**When to Adjust:**
✓ Feedback reveals gap
✓ New opportunity

**What NOT to Adjust:**
❌ Core values
❌ 5-year vision
```

The above will NOT trigger comparison-table detection because it doesn't use markdown table format.

---

**🗂️ STRUCTURED MULTI-COLUMN CONTENT (3+ Columns):**

**When to use multi-column tables instead of lists:**

Use tables when you have **4-8 items with consistent structure** and **3+ attributes per item**:
- Timeline or schedule (Time | Section | Details)
- Process steps (Step | Action | Outcome)
- Structured frameworks (Component | Description | Example)
- Rubric criteria (Criterion | Excellent | Needs Work)
- Resource lists (Tool | Purpose | When to Use)

**⚠️ TRIGGER:** When you write 4+ sections that all follow the same pattern with multiple attributes, use a table.

**Pattern:**
1. **Title describes the structure**: "X-Minute Presentation Structure", "5-Step Process", "Assessment Rubric Overview"
2. **Content uses markdown table with 3+ columns**
3. **Add layout hint**: `<!-- LAYOUT: comparison-table -->`

**Example 1: Presentation Structure (Time-based)**
```markdown
TITLE: Structuring Your 15-Minute Presentation

CONTENT:

<!-- LAYOUT: comparison-table -->

**Suggested 10-Minute Structure:**

| Time | Section | Key Content |
|------|---------|-------------|
| **0-1 min** | **Hook + Preview** | Opening question or insight; "Today I'll show you my growth journey and 1-3-5 year plan" |
| **1-3 min** | **Self-Discovery Journey** | Key insights from VIA, MBTI, assessments; What you learned about yourself |
| **3-5 min** | **Vision & Values** | 5-year vision statement; Top strengths and core values |
| **5-7 min** | **1-3-5 Year Goals** | SMART goals with Drive theory elements (autonomy, mastery, purpose); Connection to vision |
| **7-9 min** | **Integration** | Mentorship impact and course insights; Personal Mastery and Learning System |
| **9-10 min** | **Commitment** | How you'll sustain growth; Closing thought |
```

**Example 2: Process Steps**
```markdown
TITLE: 5-Step Design Thinking Process

CONTENT:

<!-- LAYOUT: comparison-table -->

| Step | Action | Outcome |
|------|--------|---------|
| **1. Empathize** | Interview users, observe behavior | Deep understanding of user needs |
| **2. Define** | Synthesize insights, frame problem | Clear problem statement |
| **3. Ideate** | Brainstorm solutions, divergent thinking | Multiple solution concepts |
| **4. Prototype** | Build low-fidelity versions | Testable artifacts |
| **5. Test** | Get user feedback, iterate | Validated solution |
```

**❌ DON'T DO THIS (Will overflow and look cluttered):**
```markdown
**Minutes 0-1:** Hook + Preview
- Opening question or insight
- "Today I'll show you my growth journey"

**Minutes 1-3:** Self-Discovery Journey
- Key insights from VIA, MBTI, assessments
- What you learned about yourself

[... 4 more sections like this]
```

**Why tables are better:** When you have 5-8 items with multiple attributes each, lists create visual clutter and make scanning difficult. Tables provide clear structure and prevent overflow.

---

**💡 MULTI-SECTION CONTENT SLIDES:**

**Problem:** Slides with multiple sections (e.g., "Three Key Takeaways" + "Your Challenge" + "Next Steps") can feel cramped and lose visual impact.

**Solutions (Choose based on content):**

**Option 1: Split into multiple slides (Preferred for important content)**
```markdown
## Slide 37a: Three Key Takeaways

CONTENT:

1. **Personal Mastery (Senge):** Hold your vision clear, see reality honestly...
2. **Drive Theory (Pink):** Ensure your goals are driven by intrinsic motivation...
3. **Sustainable Systems:** Build habits and systems that maintain development...

## Slide 37b: Your Challenge

CONTENT:

Integrate these frameworks into your Final Oral Exam presentation to demonstrate:
- Depth of understanding
- Strategic thinking
- Commitment to lifelong learning
```

**Option 2: Use markdown headers for visual separation**
```markdown
CONTENT:

### Three Key Takeaways:

1. **Personal Mastery (Senge):** Hold your vision clear...
2. **Drive Theory (Pink):** Ensure your goals are driven...
3. **Sustainable Systems:** Build habits and systems...

### Your Challenge:

Integrate these frameworks into your Final Oral Exam presentation.

### Next Steps:

1. Practice out loud 3x before exam
2. Revise slides based on feedback
3. Integrate frameworks from today
```

Headers (###) will be styled with accent color and visual separation.

**Option 3: Use reflection slide layout for prompts**

For slides that are primarily questions/prompts:
```markdown
<!-- LAYOUT: reflection -->

**Reflect on these questions:**

1. Which framework resonates most with your Development Plan?
2. How will you apply it in the next week?
3. What's your first concrete action?

**Take 2 minutes to journal your responses.**
```

**When to use each option:**
- **Split slides**: When each section has 3+ bullet points or 100+ words
- **Markdown headers**: When combining related sections for quick reference
- **Reflection layout**: When content is primarily questions/prompts for thinking

---

**DETAILED LAYOUT GUIDANCE:**

**QUOTE SLIDES (quote-slide):**
Use for: SINGLE expert quote with attribution, opening philosophical question with attribution, thought leadership statement
Target: 2-3 per lecture at topic openings or section closings
Title patterns: Direct quote text or provocative question
Examples: "Who do you want to become?", Expert quotes from Senge, Pink, or thought leaders
Structure: ONE quote (2-3 lines max), attribution with em dash (— Author Name, Source), REQUIRES prescriptive hint <!-- LAYOUT: quote -->

**⚠️ NOT quote slides:**
- Multiple example quotes in one slide → Use content slide instead
- Quotes without attribution (instructional examples) → Use content slide
- Pattern templates like "I will [goal]... SO THAT [purpose]" → Use content slide
- Quote slides are for impactful SINGULAR quotes, not collections of examples

**CARD LAYOUT (cards-slide):**
Use for: 3-6 related concepts, framework elements (Cialdini's 6 Principles), parallel ideas with icons, multiple dimensions of model
Target: 1-2 per lecture when presenting frameworks with multiple components
Title patterns: Framework name or concept category
Examples: "Drive Theory Elements", "Cialdini's 6 Principles", "Key Components"
Structure: 3-6 cards with icon/emoji, title (bold), 2-3 line description per card

**BIG NUMBER SLIDE (big-number-slide):**
Use for: ONE impactful statistic needing dramatic emphasis, memorable data point, "the one number to remember" moments
Target: 1-2 per lecture for key research findings
Title patterns: Context for the number
Examples: "Impact of Purpose", "Online Learning Reality", dramatic single statistics
Structure: One large number (135pt), brief explanation (1-2 lines), source citation

**STATS BANNER SLIDE (stats-banner-slide):**
Use for: 2-4 related statistics presented together, dashboard-style metrics, multiple data points comparison
Target: 1-2 per lecture when showing multiple related data points
Title patterns: Context for the metrics
Examples: "Assessment Breakdown", "Course Impact Metrics", multiple related statistics
Structure: 2-4 stats in horizontal row, each with large number and short label

**SECTION BREAK SLIDE (section-break-slide):**
**CRITICAL:** Section breaks mark CORE CONCEPTS that will be tested in quizzes
Use for: Major topic transitions, part divisions between content sections, visual dramatic breaks for attention reset
Target: 3-6 per lecture (every 4-8 slides for clear structure)
**Quiz mapping:** Each section break = one core concept = 1-2 quiz questions
Title patterns: "Part 1:", "Segment:", short bold statement (1-2 lines)
Examples: "Part 1: Understanding Persuasion", "Application Phase", major section markers
Structure: Single bold statement, orange background, white text, 2-6 words ideal

**Purpose for assessment:**
- Section breaks define boundaries between core concepts
- Tutorial quiz questions map to section break topics (1-2 questions per section)
- Graded quiz assessments test ~2 questions per section break topic
- Students can use section breaks as study guide boundaries
- Tutors can reference section breaks when explaining quiz question scope

**DARK SLIDES (dark-slide):**
Use for: Case studies, Vietnamese/ASEAN examples, expert quotes, stories, warnings
Target: 3-6 per lecture (up to 25%), distributed throughout
Title patterns: "Case Study:", "Vietnamese Context:", "Story:", "Warning:", "Quote:"
Examples: "Vietnamese Context: Autonomy in Hierarchy", "Warning: Why Plans Fail"
Structure: 100-150 words, focused narrative, clear takeaway

**FRAMEWORK/DIAGRAM SLIDES (framework-slide, diagram-slide, model-slide):**
Use for: Visual models, process flows, cyclical frameworks, system diagrams
Target: 1-2 per lecture when teaching conceptual models
Title patterns: "Framework:", "Model:", "Cycle:", "The [X] Process"
Examples: "Framework: Creative Tension", "Model: 70-20-10 Learning", "Cycle: Gibbs' Reflection"
Structure: Labeled components (3-6 elements), arrows showing relationships, minimal text

**REFLECTION SLIDES (reflection-slide, thinking-prompt):**
Use for: Pause for contemplation, self-assessment, journaling prompts, values exploration
Target: 1-2 per lecture before/after major concepts
Title patterns: "Reflection:", "Think:", "Consider:", "Question:"
Examples: "Reflection: What Drives Your Motivation?", "Think: Your Learning System"
Structure: 2-4 open-ended questions, thinking time indicator (e.g., "2 minutes"), note-taking space

**⚠️ REFLECTION vs FRAMEWORK DISTINCTION:**

**Use REFLECTION layout when:**
- Open-ended contemplative questions ("What drives you?", "How do you feel about...")
- Single paragraph/question prompting deep thought
- Journaling or personal exploration time
- No structured evaluation criteria
- Example: "Reflect on these questions: (2 minutes) 1. What motivates you most? 2. Where do you see yourself growing?"

**Use FRAMEWORK layout when:**
- Structured evaluation/assessment with multiple criteria (e.g., "Autonomy Check:", "Mastery Check:")
- Integration/summary slides listing multiple framework components
- Multi-component content with bold headings and descriptions
- Systematic self-assessment against specific dimensions
- Example: "Evaluate Your Goals: **Autonomy Check:** Did I choose this? **Mastery Check:** Am I pursuing growth? **Purpose Check:** Does this serve something larger?"

**FRAMEWORK FORMAT (component-based):**
For framework slides, use this structure:

```markdown
<!-- LAYOUT: framework -->

**Component 1 Name:** Brief description of this element

**Component 2 Name:** Brief description of this element

**Component 3 Name:** Brief description of this element
```

This generates visual component cards in the skill exporter.

**CHECKLIST SLIDES (checklist-slide):**
Use for: Assessment criteria, requirements overview, rubric preview, task lists
Target: 1-2 per lecture when introducing assessments or complex deliverables
Title patterns: "Checklist:", "Requirements:", "Assessment Criteria:", "What to Include"
Examples: "Development Plan Checklist", "Presentation Requirements"
Structure: 3-5 categories with 2-4 items each, checkbox symbols, point values if applicable

---

**PRESCRIPTIVE LAYOUT HINTS (CRITICAL FOR CERTAIN LAYOUTS):**

For layouts where visual formatting is critical, use HTML comments to FORCE specific layout (overrides auto-detection):

**Layouts requiring prescriptive hints:**
- Quote slides: `<!-- LAYOUT: quote -->`
- References: `<!-- LAYOUT: references -->`
- Framework diagrams: `<!-- LAYOUT: framework -->`
- Reflection prompts: `<!-- LAYOUT: reflection -->`
- Comparison tables: `<!-- LAYOUT: comparison-table -->`

**When to use hints:**
- Visual formatting is critical (quotes, references, frameworks)
- Content might be ambiguous (questions that should be reflections vs. regular content)
- Guaranteed results needed (student-facing materials with specific design requirements)

**Placement in markdown:**
Place hint BEFORE slide content, immediately after slide separator:

```markdown
---

<!-- LAYOUT: quote -->

"Your quote text here - keep to 2-3 lines maximum"
— Attribution Name, Source/Title (Year)

---
```

**Example - Quote slide with hint:**
```markdown
---

<!-- LAYOUT: quote -->

"Personal mastery is the discipline of continually clarifying and deepening our personal vision, of focusing our energies, of developing patience, and of seeing reality objectively."

— Peter Senge, The Fifth Discipline (2006)

---
```

**Example - Framework slide with hint:**
```markdown
---

<!-- LAYOUT: framework -->

## The Creative Tension Model

**Current Reality** ← [GAP: Creative Tension] → **Vision**

The gap between where you are and where you want to be creates natural energy for change.

*Senge, P. M. (2006). The fifth discipline. Currency/Doubleday.*

---
```
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
- [ ] Missing or superficial speaker notes = incomplete lecture file

**Layout Variety (Content-Driven - REVIEW BEFORE FINALIZING):**
- [ ] **Section breaks** used at major topic transitions and framework introductions
- [ ] **Quote slides** used when you have impactful quotes (with `<!-- LAYOUT: quote -->`)
- [ ] **Framework slides** used for conceptual models and processes
- [ ] **Dark slides** used for Vietnamese case studies, examples, or stories that merit emphasis
- [ ] **Card layouts** used when 3-6 parallel concepts benefit from visual organization
- [ ] **Big number or stats slides** used when you have compelling statistics
- [ ] **Reflection prompts** used when contemplative questions fit the flow
- [ ] **Vocab table** used if introducing key terms needing Vietnamese translations
- [ ] **Comparison tables** used for side-by-side contrasts (vs., before/after)
- [ ] Prescriptive hints added for quotes, references, frameworks (<!-- LAYOUT: type -->)

**Principle: Layouts should match content type. If all slides are standard content, revisit whether you're presenting diverse content appropriately.**

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

**File:** `courses/[COURSE-CODE]-*/weeks/week-[N]/tutorial-content.md`

**IMPORTANT: This file is STUDENT-FACING only**
- Write as if students are reading it directly
- Include high-level section timings (helps students pace themselves)
- NO "Tutor:" instructions, NO "Expected:" answers, NO facilitation notes
- All tutor guidance goes in tutorial-tutor-notes.md (Step 3.5)

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

---

#### Tutorial Activity Design Principles

**CRITICAL DISTINCTION - Quiz vs. Tutorial Questions:**

**Quiz Questions (Closed - Remembering/Understanding):**
- Direct, unambiguous questions with ONE correct answer
- NO scenarios or complex contexts
- Based on slide content only (not speaker notes)
- Test foundational knowledge
- See [QUIZ-QUESTION-GUIDELINES.md](../../docs/QUIZ-QUESTION-GUIDELINES.md)

**Tutorial Activities (Open - Application/Analysis/Evaluation):**
- USE scenarios and case studies with realistic complexity
- ENCOURAGE defensible arguments and multiple valid approaches
- WELCOME open interpretation and divergent thinking
- Practice higher-order thinking skills for assessments
- See [TUTORIAL-DESIGN-GUIDELINES.md](../../docs/TUTORIAL-DESIGN-GUIDELINES.md)

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

**Activity structure (task-based, not prescriptive):**

```markdown
### MAIN ACTIVITY: [Name] (55-60 minutes)

### The Scenario
[Brief, realistic business scenario - 2-3 sentences]

**Your task:** [Clear deliverable - what to produce]

**Note:** [Acknowledge multiple valid approaches if applicable]

---

### The Data / Materials
[Provide dataset, templates, or materials needed - organized clearly]

---

### Individual/Pair Work (25 minutes)

**Deliverable:**
- [Specific output expected]
- [Format/structure required]

**Considerations:**
- [Key tip or starting point]
- [Framework to apply]
- [Quality criteria to remember]
- [Reminder about multiple approaches]

---

### Peer Review (15 minutes)

**Exchange work with another pair.**

**Review using these criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
- [ ] [Criterion 4]

**Provide feedback:**
- One specific strength: [Example format]
- One area to strengthen: [Example format]

**Remember:** [Cultural note about comparing vs. critiquing]

---

### Revision & Debrief (15 minutes)

**Revision (10 min):** [What to focus on - no need to change approach, strengthen reasoning]

**Debrief (5 min):** [Brief note about class discussion]
```

**KEY PRINCIPLES for student-facing content:**
- **Task-based, not step-based:** Give clear task + deliverable, not micro-steps
- **Considerations, not steps:** Provide tips and frameworks, not procedures
- **Trust student autonomy:** They figure out sequencing and approach
- **Minimal time granularity:** Phase times only (25 min, 15 min), not "Step 1: 5 min"
- **Examples for guidance:** Show format, not dictate process

#### Quiz Preparation (15-20 mins):

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

**Format in tutorial-content.md:**
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
- See Step 3.5 for tutor notes format

**For complete quiz design guidelines:**
- See [docs/QUIZ-QUESTION-GUIDELINES.md](../../docs/QUIZ-QUESTION-GUIDELINES.md)

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

### Step 3.5: Generate Tutorial Tutor Notes

**Create comprehensive tutor notes document for tutorial facilitation**

**File:** `courses/[COURSE-CODE]-*/weeks/week-[N]/tutorial-tutor-notes.md`

**Purpose:** Provide tutors with quiz answer keys, expected student responses, and facilitation guidance.

**IMPORTANT FILE SEPARATION:**
- **tutorial-content.md** = Student-facing only (activity instructions, dataset, quiz questions)
- **tutorial-tutor-notes.md** = Tutor-facing only (answer keys, facilitation guidance, expected approaches)

**Do NOT include in tutorial-content.md:**
- "Tutor:" instructions
- "Expected:" answers
- Timing checkpoints for tutors ("5 minutes in, students should have...")
- Scaffolding questions tutors should ask
- Cultural considerations for tutors
- Facilitation notes

**DO include in tutorial-content.md:**
- High-level section timings (helps students pace themselves)
- Clear activity instructions
- Dataset/scenario
- Quiz questions (without answers)
- Rubric checklist
- Peer review sentence starters

**Document Structure:**

```markdown
# Week [N] Tutorial: Tutor Notes

**Course:** [Course Name]
**Tutorial:** [Week Topic]
**Duration:** 90 minutes

---

## Tutorial Goals

- [Primary goal - what this tutorial prepares students for]
- [Secondary goal if applicable]
- [Additional goal if needed]

## Key Outcomes

By the end of this tutorial, students should be able to:
- [Specific skill or understanding 1]
- [Specific skill or understanding 2]
- [Specific skill or understanding 3]
- [Specific skill or understanding 4]

---

## Quiz Solutions

### Question 1: [Topic/Concept]
**Correct: [Letter]**

**Why [Letter] is correct:**
[Explanation referencing specific slide or lecture content]

**Why wrong:**
- [Letter]: [Common misconception this represents]
- [Letter]: [Common misconception this represents]
- [Letter]: [Common misconception this represents]

**Common confusion:** [What students typically get wrong]
**Teaching tip:** [Quick strategy to clarify - analogy, example, or visual aid]

---

### Question 2: [Topic/Concept]

[Same structure for all 6-10 questions]

---

## Facilitating the Main Activity

**Context:**

[2-3 sentences explaining the activity's purpose and connection to assessment. Note any important pedagogical considerations like "deliberately open-ended" or "mirrors real professional scenario"]

**What Good Work Looks Like:**

- [Quality indicator 1 - specific, observable]
- [Quality indicator 2]
- [Quality indicator 3]
- [Quality indicator 4]
- [Quality indicator 5]

**Critical Moments:**

**During [Phase Name] ([X] minutes):**

[Paragraph describing what to watch for, when to intervene, what prompts to use. Include specific timing notes like "Around the 10-minute mark..." Include cultural considerations if relevant to this phase, woven naturally into the guidance.]

**During [Next Phase] ([X] minutes):**

[Paragraph with guidance for this phase]

**During [Final Phase] ([X] minutes):**

[Paragraph with guidance, including key insights to draw out or connections to make]

**Timing Flexibility:**

[2-3 sentences with practical timing advice. Include option to assign quiz as homework if needed. Note what to prioritize and when to let discussion run.]

---

**END OF TUTOR NOTES**
```

**Required Content:**

1. **Tutorial Goals** (2-3 goals that connect to assessments and course objectives)

2. **Key Outcomes** (4-5 specific skills or understandings students should demonstrate)

3. **Quiz Solutions Section** (ALL 6-10 questions):
   - Correct answer letter
   - Why correct (reference specific slide)
   - Why each distractor wrong (misconception it represents)
   - Teaching tip for confusing concepts (analogy, example, or visual aid)

4. **Facilitating the Main Activity**:
   - Context paragraph (2-3 sentences on purpose and pedagogical approach)
   - "What Good Work Looks Like" (5 quality indicators)
   - Critical Moments organized by phase (paragraphs, not bullet lists)
   - Timing Flexibility (2-3 sentences including quiz-as-homework option)

**Quality Check for Tutor Notes:**
- [ ] All quiz questions have complete answer explanations
- [ ] Tutorial goals clearly stated (2-3)
- [ ] Key outcomes specific and observable (4-5)
- [ ] Quality indicators are concrete, not vague
- [ ] Critical Moments guidance is professional conversational, not prescriptive
- [ ] Cultural considerations woven naturally into phase guidance (not separate section)
- [ ] Timing flexibility includes quiz-as-homework option
- [ ] Overall tone: colleague-to-colleague, trusts tutor judgment

---

### Step 3.6: Generate GIFT Format Quiz Export

**MANDATORY: Export quiz questions to GIFT format for Moodle upload**

**File:** `courses/[COURSE-CODE]-*/weeks/week-[N]/week-[N]-quiz.gift`

**Purpose:** Automate export of tutorial quiz questions in Moodle-ready GIFT format with answer feedback.

**Process:**

1. **Run export tool:**
   ```bash
   python tools/export_quiz_to_gift.py courses/[COURSE-CODE]-*/weeks/week-[N]
   ```

2. **Tool automatically:**
   - Reads quiz questions from `tutorial-content.md`
   - Reads answer explanations from `tutorial-tutor-notes.md`
   - Validates question/answer alignment
   - Formats to GIFT with feedback for correct/incorrect answers
   - Outputs `week-[N]-quiz.gift` in same directory

**GIFT Format Features:**
- Multiple-choice questions with single correct answer
- Feedback for correct answer ("Why X is correct")
- Feedback for each distractor ("Why wrong")
- Category assignment (Week [N])
- Question titles based on topics
- Ready for direct Moodle import

**Quality Check for GIFT Export:**
- [ ] File generated successfully: `week-[N]-quiz.gift`
- [ ] Question count matches tutorial quiz (6-10 questions)
- [ ] All questions have correct answer marked with `=`
- [ ] All distractors marked with `~`
- [ ] Feedback included for correct and incorrect options
- [ ] Special characters properly escaped
- [ ] Category set to `Week [N]`

**Example GIFT Output:**
```
// Week 1 Quiz: Business Communication Fundamentals
// Generated from tutorial quiz practice questions
// Questions: 8

$CATEGORY: Week 1

::Hofstede's Power Distance::According to Hofstede's framework, which dimension measures the extent to which less powerful members accept unequal power distribution?{
=Power Distance #Power distance specifically measures acceptance of hierarchical inequality in organizations and societies.
~Uncertainty Avoidance #This measures comfort with ambiguity, not power distribution.
~Individualism vs. Collectivism #This measures group orientation, not power acceptance.
~Long-term Orientation #This measures time perspective, not power dynamics.
}
```

**Error Handling:**

If export fails, check:
1. Both `tutorial-content.md` and `tutorial-tutor-notes.md` exist
2. Quiz questions properly formatted in tutorial-content.md
3. Quiz solutions properly formatted in tutorial-tutor-notes.md
4. Question numbers match between files
5. All questions have A, B, C, D options

**Troubleshooting:**
- **"No quiz questions found"** → Check tutorial-content.md has `## QUIZ PRACTICE` section
- **"Question number mismatch"** → Ensure question numbers consistent across both files
- **"Correct answer not in options"** → Verify answer key letter matches available options

---

### Step 3.7: Generate Gemini Slide Handoff Prompt

**Create ready-to-use Gemini prompt for slide creation**

**File:** `courses/[COURSE-CODE]-*/weeks/week-[N]/gemini-handoff.md`

**Purpose:** Generate a complete prompt that can be copied directly to Google Gemini for professional slide creation.

**Template:** Use `.claude/templates/gemini-slide-handoff-prompt.md`

**Process:**

1. **Read the template** from `.claude/templates/gemini-slide-handoff-prompt.md`
2. **Replace placeholders:**
   - `{{COURSE_CODE}}` → Course code (e.g., BCI2AU)
   - `{{COURSE_NAME}}` → Course name (e.g., Business Communication)
   - `{{WEEK_NUMBER}}` → Week number
   - `{{TOPIC}}` → Week topic from syllabus
3. **Append lecture content:** Add the full `lecture-content.md` at the end
4. **Save** to `gemini-handoff.md` in the week folder

**Output Format:**

```markdown
Create a visually engaging Google Slides presentation from the lecture content below.

## Course Details

- **Course:** [COURSE_CODE] [COURSE_NAME]
- **Week:** [N] - [TOPIC]
- **Awarding University:** Andrews University
- **Campus:** National Economics University (NEU), Vietnam

## Requirements

1. **Style:** Use **The Executive** style archetype.

2. **Branding:** Include Andrews University logo (prominent) and NEU Vietnam logo (smaller) on the title slide.

3. **Format:** Use 4:3 aspect ratio (not widescreen).

4. **Visuals:** Make it visually rich - use relevant images, infographics for frameworks, charts for data, and icons. Let visuals do the heavy lifting, not text.

5. **Citations:** When referencing a framework or theory, include the citation in the slide footer, e.g., (Minto, 1987), (Cialdini, 1984).

6. **Speaker notes:** Include condensed presenter guidance for each slide.

## Lecture Content

[FULL LECTURE-CONTENT.MD PASTED HERE]
```

**Quality Check:**
- [ ] All placeholders replaced with actual values
- [ ] Full lecture content appended (not truncated)
- [ ] File saved to correct location

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
3. `courses/[COURSE-CODE]-*/weeks/week-[N]/tutorial-tutor-notes.md`
4. `courses/[COURSE-CODE]-*/weeks/week-[N]/week-[N]-quiz.gift` **[NEW - MANDATORY]**

**Update course-info.md:**
- Mark week [N] lecture as ✓ completed
- Mark week [N] tutorial as ✓ completed
- Mark week [N] tutor notes as ✓ completed
- Mark week [N] GIFT quiz as ✓ completed
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

📄 **Tutorial Tutor Notes:** courses/[COURSE-CODE]-[slug]/weeks/week-[N]/tutorial-tutor-notes.md
   - Quiz answer key with explanations ([X] questions)
   - Facilitation guidance for each activity phase
   - Quality indicators for student work
   - Cultural considerations and timing flexibility

📄 **GIFT Quiz Export:** courses/[COURSE-CODE]-[slug]/weeks/week-[N]/week-[N]-quiz.gift **[NEW - MANDATORY]**
   - [X] questions ready for Moodle import
   - Includes feedback for correct and incorrect answers
   - Category: Week [N]
   - Format: Moodle GIFT (direct upload)

## Next Steps

1. **Review content** for accuracy and appropriateness
2. **Upload GIFT file** to Moodle (optional - can batch upload at end of semester)
3. **Create slides** using /export-slides [N] (after content approval)
4. **Generate next week** using /generate-week [N+1]

## Quick Links

- Lecture: `courses/[COURSE-CODE]-[slug]/weeks/week-[N]/lecture-content.md`
- Tutorial: `courses/[COURSE-CODE]-[slug]/weeks/week-[N]/tutorial-content.md`
- Tutor Notes: `courses/[COURSE-CODE]-[slug]/weeks/week-[N]/tutorial-tutor-notes.md`
- GIFT Quiz: `courses/[COURSE-CODE]-[slug]/weeks/week-[N]/week-[N]-quiz.gift`
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
