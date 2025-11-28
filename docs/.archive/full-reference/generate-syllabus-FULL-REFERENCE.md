# Generate Comprehensive Course Syllabus

You are creating a world-class university course syllabus using the research-enhanced workflow. Follow these steps precisely to ensure quality, consistency, and evidence-based content.

## Your Task

Guide the user through creating a complete course syllabus that:
1. Incorporates research from top management schools ONLY (US: M7 + Berkeley, Yale, Tuck; UK: LBS, Oxford, Cambridge, LSE, Imperial, Warwick, Edinburgh, Manchester, Cranfield)
2. Includes 2 validated, accessible articles per week with strict content matching
3. Aligns course structure with approved description promises
4. Designs assessments based on actual course content (not just topic headings)

## Step-by-Step Process

### STEP 1: Course Basics & Research-Backed Description

Gather essential information:

**Ask the user:**
1. University awarding the qualification (e.g., "Andrews University", "UWE")
2. Qualification program (e.g., "BA in Banking and Finance", "BA International Business")
3. Campus location (e.g., "National Economics University campus", "Phenikaa campus")
4. Course Code (e.g., BUS101, ECON201)
5. Course Title (e.g., "Business Communication", "Microeconomic Theory")
6. Semester and Year (e.g., "Fall 2025")
7. Number of weeks (typically 10-11, but can vary)
8. **Grading System:** "Which grading system does your institution use?"
   - **US System** (60% pass, A = 90-100%)
   - **UK System** (40% pass, First Class = 70-100%)
   - **Vietnamese Adapted** (varies by institution)
   - **Other** (specify pass threshold)

   **Note:** Consult `templates/grading-systems.md` for complete reference

6. **Sample Documents (Optional):** "Do you have any existing course descriptions, syllabi, or program documentation I should reference?"
   - If YES: Read provided files
   - If NO: Proceed with research-only approach

**Research Course Description:**

Explain to user: "I'll research how top schools describe this course to create a research-backed course description."

**Research Process:**
1. Use WebSearch to find course descriptions from:
   - Top US/UK business schools: M7, Berkeley, Yale, Tuck, LBS, Oxford, Cambridge, LSE, Imperial, Warwick, Edinburgh, Manchester, Cranfield
   - Top universities for the subject area
   - Program catalogs and course listings

2. Use WebFetch to extract course descriptions from promising sources

3. Analyze and synthesize:
   - **Purpose:** Why does this course exist? What need does it address?
   - **Content:** What topics/skills are covered?
   - **Value Proposition:** What will students gain? How does it prepare them?
   - **Unique Elements:** What distinguishes this course?

4. Draft 2-3 paragraph course description following this structure:
   - **Paragraph 1:** Purpose and foundational content
   - **Paragraph 2:** Pedagogical approach and hands-on application
   - **Paragraph 3:** Value proposition and career/academic relevance

5. Present draft to user for approval/adjustment

**Your action:**
- Load the syllabus-base-template.md
- Research and draft course description
- Get user approval on description
- Populate: {{UNIVERSITY}}, {{QUALIFICATION}}, {{CAMPUS}}, {{COURSE_TITLE}}, {{SEMESTER_YEAR}}, {{COURSE_DESCRIPTION}}
- Select appropriate grading scale table from templates/grading-systems.md
- Populate: {{GRADING_SCALE_TABLE}}, {{GRADING_SYSTEM}}, {{PASS_THRESHOLD}}

**IMPORTANT - Save Progress:**
- Create course directory: `courses/[COURSE-CODE]-[course-name]/`
- Create subdirectories: `rubrics/`, `assessments/`, `weeks/`, `resources/`
- Save course-info.md with all Step 1 information
- Save course description research to `shared/research/[course-topic]/course-description-research.md`

---

### STEP 1.5: Extract Description Promises (CRITICAL VALIDATION STEP)

**Purpose:** Ensure the course structure aligns with ALL promises made in the approved description.

**Process:**

1. **Extract specific topics mentioned in approved description:**
   - Read through the approved course description carefully
   - Identify EVERY specific topic, technology, or skill explicitly mentioned
   - Note any unique differentiators or special emphases

2. **Create validation checklist:**
```markdown
## Description Promises Checklist

Based on approved description, the course MUST include:

□ [Specific topic 1] - e.g., "AI and emerging technologies"
□ [Specific topic 2] - e.g., "Data storytelling"
□ [Specific topic 3] - e.g., "Virtual collaboration"
□ [Specific topic 4] - e.g., "Crisis management"
□ [Specific topic 5] - e.g., "Ethical communication"
□ [Unique element 1] - e.g., "Cultural intelligence"
□ [Special emphasis 1] - e.g., "Hands-on application"
□ [Any other promises from description]

**Validation Rule:** Every checkbox MUST map to specific week(s) in course structure.
```

3. **Save checklist:**
   - Save to `.working/description-promises-checklist.md`
   - Keep visible during Step 2 (structure creation)
   - Use for validation before presenting structure to user

**CRITICAL:** Before presenting any course structure to the user:
- Verify EVERY promise is explicitly addressed in specific week(s)
- If any promise is missing, revise structure
- Generic/traditional topics cannot replace promised modern content
- Special emphases must be prominent, not buried

**Example validation:**
```
✓ "AI and emerging technologies" → Week 2 (explicit AI tools week)
✗ "AI and emerging technologies" → Mentioned briefly in Week 3 (INSUFFICIENT)
```

---

### STEP 2: Research Top Schools for Learning Objectives AND Course Structure

**Explain to user:**
"I'll research how top management schools (US: M7, Berkeley, Yale, Tuck; UK: LBS, Oxford, Cambridge, LSE, Imperial, Warwick, Edinburgh, Manchester, Cranfield) teach this subject to extract both learning objectives and weekly course structure."

**IMPORTANT - Research from TOP SCHOOLS ONLY:**
- **DO NOT use textbook table of contents** as primary structure
- **DO NOT default to traditional/generic course outlines**
- Focus on actual syllabi from leading business schools
- Look for modern, current approaches (2023-2025 courses preferred)
- Prioritize innovative/cutting-edge topic coverage

**Research Process:**

1. **Search for actual syllabi and course descriptions:**
   - Use WebSearch to find syllabi from top US/UK business schools (M7, Berkeley, Yale, Tuck, LBS, Oxford, Cambridge, LSE, Imperial, Warwick, Edinburgh, Manchester, Cranfield)
   - Use WebFetch to extract detailed course information
   - **Focus:** Real course materials, not textbook chapters
   - **Goal:** Understand how leading schools structure modern courses

2. **Extract THREE key elements:**

   **A. Learning Objectives** (organized in 4 Bloom's Taxonomy categories)
   - Understand & Apply (3-5 objectives)
   - Analyze & Evaluate (3-5 objectives)
   - Create & Present (3-5 objectives)
   - Collaborate (2-3 objectives)

   **B. Course Structure** (weekly topics and progression)
   - Week-by-week topics from actual school syllabi
   - Key concepts covered each week
   - Logical progression and scaffolding
   - Common themes across schools
   - Modern topics and emerging areas

   **C. Foundational Frameworks per Week (CRITICAL FOR RESEARCH BALANCE)**
   For each week, identify:
   - **Seminal/foundational work(s)** that define the topic (e.g., "Cialdini's 6 principles", "Monroe's Motivated Sequence", "Shannon-Weaver model")
   - **Why it's foundational** (highly cited, field-defining, still taught today)
   - These become REQUIRED in research - ensures balance of seminal + recent

   **Example structure per week:**
   ```
   Week 4: Persuasive Communication
   - Key concepts: Persuasion frameworks, pitching, proposals, influence
   - FOUNDATIONAL: Cialdini's 6 Principles of Persuasion (seminal, 1984/2001)
   - FOUNDATIONAL: Monroe's Motivated Sequence (classic presentation structure)
   - Recent applications: Current HBR/practitioner articles on pitching
   ```

   **Topics that may NOT have seminal works (acceptable):**
   - AI & Digital Tools (too new - all recent is fine)
   - Virtual Collaboration (post-pandemic - all recent is fine)

3. **Validate against description promises (Step 1.5 checklist):**
   - Load the description promises checklist
   - Ensure synthesized structure addresses EVERY promise
   - Map each promise to specific week(s)
   - Revise structure if any promises missing

4. **Synthesize and present:**
   - Present synthesized learning objectives for user approval
   - Present synthesized weekly course outline for user approval
   - Show which schools teach which topics
   - Explain the pedagogical progression
   - **Show validation:** How each description promise maps to specific weeks

**Your action:**
- Populate: {{UNDERSTAND_APPLY_OBJECTIVES}}, {{ANALYZE_EVALUATE_OBJECTIVES}}, {{CREATE_PRESENT_OBJECTIVES}}, {{COLLABORATE_OBJECTIVES}}
- Create draft weekly outline based on research (to be used in Step 4)

**IMPORTANT - Save Progress:**
- Update course-info.md with learning objectives
- Save learning objectives research to `shared/research/[course-topic]/learning-objectives-research.md`

---

### STEP 3: Course Calendar with Research-Backed Articles

**IMPORTANT - Do Research BEFORE Designing Assessments:**
- Assessments must test what we actually teach, not just topic headings
- We need to know specific frameworks/articles before designing tests
- Example: If Week 6 teaches Cialdini's 6 principles, assessment should test those specific principles

This is the most intensive step. For each week:

#### 3A: Choose Research Method (Claude Desktop Recommended)

**RECOMMENDED: Use Claude Desktop for Superior Research Quality**

**Ask user:** "Do you have Claude Desktop available for article research?"

**Option 1: Claude Desktop Handoff (RECOMMENDED - Superior Quality)**
- Better research capabilities and thoroughness
- Time: 5-8 hours for 10 weeks
- Quality: More comprehensive validation
- Process: Create research prompts → User researches in Desktop → Import results back

**Option 2: Direct Research in This Conversation (Fallback)**
- Use WebSearch/WebFetch directly here
- Time: 8-10 hours for 10 weeks
- Process: 4-stage validation conducted in this session

**If Option 1 (Desktop - Creates Master Prompt):**

**Your action:**
1. Load template: `.claude/templates/desktop-master-prompt-template.md`
2. Replace all placeholders with actual course info:
   - [COURSE-CODE] → actual code
   - [COURSE-NAME] → actual name
   - [course-slug] → lowercase-hyphenated name
   - [TOPIC] → each week's topic
   - [Concept 1/2/3] → key concepts for each week
3. Save generated prompt to: `courses/[COURSE-CODE]/.working/desktop-master-prompt.md`
4. Tell user: "I've created a master research prompt. Copy the contents of `.working/desktop-master-prompt.md` and paste into Claude Desktop. Desktop will spawn 10 parallel research agents automatically. Return here when complete."

**Desktop will:**
- Spawn 10 Task agents (one per week)
- Run all in parallel for speed
- Each agent conducts 4-stage research
- Each saves to `week-N-research.md` via MCP
- Each creates `.week-N-ready` flag when done
- Shows progress: "Week 3/10 complete..."
- Notifies when all complete

**User returns to Code when Desktop finishes** → Proceed to Step 3B for auto-validation

---

**If Option 2 (Direct):**
- Proceed with 4-stage research process below (Step 3C)

---

#### 3B: Batch Validation - Auto-Detect and Validate All Research

**If using Claude Desktop (user returns after Desktop research):**

**AUTO-DETECTION PROCESS:**

1. **Scan for completion flags:**
   ```python
   # Check for .week-N-ready flags
   research_dir = f"courses/{COURSE_CODE}/.working/research/"
   completed_weeks = []
   for week_num in range(1, NUM_WEEKS + 1):
       flag_file = f"{research_dir}/.week-{week_num}-ready"
       if file_exists(flag_file):
           completed_weeks.append(week_num)
   ```

2. **Show initial status:**
   ```
   📊 Research Status Dashboard
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Detected: {len(completed_weeks)}/{NUM_WEEKS} weeks with ready flags

   Proceeding to validate each week...
   ```

3. **Validate each completed week in parallel:**

   For each week in completed_weeks:

   **Validation Checks:**
   - ✓ **File exists:** `week-N-research.md` present?
   - ✓ **Format:** Has required sections (Key Concepts, Final Articles)?
   - ✓ **Concepts:** All key concepts listed?
   - ✓ **Articles:** Exactly 2 articles present?
   - ✓ **Citations:** Full APA 7th format?
   - ✓ **URLs:** Present and accessible (WebFetch check)?
   - ✓ **Content Match:** Checkmarks (✓) for all concepts?
   - ✓ **Details:** Specific coverage details (not generic)?
   - ✓ **Rationale:** "Why Selected" section present?
   - ✓ **Accessibility:** Not paywalled OR (seminal + validated)?

4. **Generate Validation Report:**
   ```
   📊 Validation Results
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   ✓ Week 1: Valid (2 articles, all concepts covered)
   ✓ Week 2: Valid (2 articles, all concepts covered)
   ⚠ Week 3: Issues found
      - Missing concept: "Data visualization frameworks"
      - Article 2 URL returns 404
   ✓ Week 4: Valid (2 articles, all concepts covered)
   ✓ Week 5: Valid (2 articles, all concepts covered)
   ✗ Week 6: No research file found (flag exists but file missing)
   ✓ Week 7: Valid (2 articles, all concepts covered)
   ✓ Week 8: Valid (2 articles, all concepts covered)
   ✓ Week 9: Valid (2 articles, all concepts covered)
   ✓ Week 10: Valid (2 articles, all concepts covered)

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Summary: 8/10 valid ✓ | 1 with issues ⚠ | 1 failed ✗
   ```

5. **Handle Issues:**

   **If ALL valid (✓):**
   - "Excellent! All 10 weeks validated successfully."
   - "Proceeding to Step 4 (Assessment Design)..."

   **If some have issues (⚠ or ✗):**
   - "Would you like to:"
     - **Option A:** Fix issues in Desktop and re-validate
     - **Option B:** I'll research the failed weeks directly in Code
     - **Option C:** Proceed with valid weeks only (skip failed)

   **User chooses, then:**
   - Option A: User fixes, run validation again
   - Option B: Research failed weeks using Step 3C process
   - Option C: Mark failed weeks as "needs research later"

6. **Save validation results:**
   - `.working/research/validation-report.md`
   - Includes timestamp, results, any actions taken
   - Can review later if needed

**If NO research detected:**
- No .week-N-ready flags found
- User hasn't done Desktop research yet
- Proceed to Step 3C (present weekly outline)
- Or offer to create Desktop prompts now

**Validation Checklist for Imported Research:**
```
□ Week number and topic present
□ Key concepts listed (minimum 3)
□ 3-4 final articles provided
□ Full APA citations present
□ URLs provided and accessible
□ Content Match section shows which concepts each article covers
□ Coverage Validation confirms ALL concepts covered across article set
□ Specific details provided (not just "covered")
□ "Why Selected" rationale present for each article
□ Complementary coverage explanation provided
□ Accessibility verified (open access preferred; paywalls OK if seminal + validated)
```

**Time saved:** If importing 10 weeks of research: ~5-8 hours (30-50 min per week)

---

#### 3C: Present Research-Backed Weekly Outline

**Present the synthesized weekly outline from Step 2:**
- Show all weeks with topics and key concepts from top school research
- Explain the pedagogical progression
- Identify which schools teach similar topics
- Ask user: "Does this structure work, or would you like to adjust any weeks?"

**User can:**
- Approve as-is
- Adjust specific week topics
- Reorder weeks
- Add/remove concepts

**Once approved, proceed to article research for each week (skip weeks with imported research).**

---

#### 3D: Four-Stage Article Research Process

**IMPORTANT - Check Current Date First:**
1. **Check `<env>` tag for today's date:** [Note the current date]
2. **If searching for recent sources** (e.g., "past 6 months", "2023-2025"):
   - Calculate date range explicitly
   - Example: If today is November 24, 2025 and you need "past 6 months"
   - Date range = May 2025 to November 2025
   - Include this in search queries: "2025" or "May 2025..November 2025"
3. **Avoid assumptions:** Don't assume "2025" means "early 2025" - check the actual date

**STAGE 1: Discovery (Find 10-15 candidates)**

Use WebSearch to cast wide net:
```
- "site:hbs.edu [topic] syllabus"
- "site:gsb.stanford.edu [topic] MBA"
- "site:wharton.upenn.edu [topic] course"
- "site:mitsloan.mit.edu [topic]"
- "[key concept] seminal article"
- "[key concept] highly cited peer reviewed"
- "site:hbr.org [topic]"
- "[topic] Harvard Business Review 2020..2025"
```

Create initial list of 10-15 candidate articles.

**STAGE 2: Quick Filter (Reduce to 5-6)**

For each candidate:
1. Use WebFetch to check URL accessibility
2. Check access type:
   - **Open access:** EXCELLENT
   - **Paywalled:** ACCEPTABLE ONLY if high-quality seminal work (1000+ citations for established, 100+ for recent, top-tier journal, foundational) AND can validate content via abstract/preview/cached
   - **No content available:** REJECT
3. Review title and abstract for relevance
4. Verify source quality (peer-reviewed journal, HBR, MIT Sloan Review, etc.)
5. Check date (prefer recent unless true seminal work)

Eliminate any that fail accessibility or quality checks. Reduce to 5-6 candidates.

**STAGE 3: Content Validation (Deep analysis to 2-3 finalists)**

For each of the 5-6 candidates:

1. Use WebFetch to retrieve article content with this prompt:
```
"Analyze this article and extract:
1. Main frameworks, models, or theories presented
2. Key concepts and principles explained in depth
3. Practical applications and examples provided
4. Target audience level and writing style
5. Geographic/cultural context of examples"
```

2. Compare extracted content against required key concepts
3. Create validation checklist:
```
Required Concepts for Week [#]:
□ [Concept 1] - Is this explained in depth?
□ [Concept 2] - Is this covered adequately?
□ [Concept 3] - Is this addressed?
□ [Concept 4] - Is this included?

If ALL ✓ = PASS → Finalist
If ANY ✗ = REJECT → Discard
```

4. **STRICT RULE:** Article must cover ALL key concepts. Reject partial matches.

Reduce to 2-3 finalists that pass full content validation.

**STAGE 4: Present Finalists to User**

For each finalist, present:
```markdown
**Option [A/B/C]:**
[Full APA 7th citation]
[Verified accessible URL]

Content Match Analysis:
✓ [Concept 1]: [Briefly explain how covered]
✓ [Concept 2]: [Briefly explain how covered]
✓ [Concept 3]: [Briefly explain how covered]
✓ [Concept 4]: [Briefly explain how covered]

Additional strengths:
- [Practical examples, writing quality, etc.]

Selection rationale: [Why this is perfect for this week]
```

**Ask user to select 3-4 articles** that together cover ALL concepts
- Each article focuses deeply on 1-2 main concepts
- Mix of theoretical/foundational + applied/practitioner
- Complementary coverage across the set

---

#### 3E: Document Research

**CRITICAL - Save After Each Week:**
Save research notes to `shared/research/[course-topic]/article-research-summary.md` documenting:
- Candidates considered for this week
- Validation results (which passed/failed and why)
- Final selections with justifications
- Update the file after EACH week is completed

This ensures no work is lost if conversation is interrupted.

---

#### 3F: Build Calendar Entry and SAVE DRAFT

Add to course calendar table:
```markdown
| Week [#]: [Topic] | [Topic details] [Key frameworks] [Learning focus] | [Article 1 citation with URL] [Article 2 citation with URL] |
```

**CRITICAL - Save Draft Syllabus After Every 2-3 Weeks:**
- Update `courses/[COURSE-CODE]/syllabus-DRAFT.md` with completed weeks
- This ensures work is preserved even if conversation interrupts
- Mark draft status clearly at top of file

**Repeat Steps 3C-3F for all weeks (or only weeks without imported research)**

---

### STEP 4: Assessment Structure

**NOW Design Assessments Based on Actual Content**

After completing article research, you now know:
- Specific frameworks being taught (e.g., Cialdini's 6 principles, AIDA model)
- Actual skills students will practice (e.g., prompt engineering, crisis response)
- Content depth and complexity for each week

**Ask the user:** "Which assessment structure best fits this course?"

**Options:**
1. Portfolio + Presentation + Quiz (skills-based courses)
2. Exam + Project + Quiz (content-heavy courses)
3. Custom mix

**For options 1 or 2:**
- Load appropriate template from `templates/syllabus-components/assessment-structures/`
- Ask for specific weights, due weeks, and assignment names
- **Align assessments with specific content taught:**
  - Example: "Week 6 teaches Cialdini's principles → Quiz 2 includes questions on those principles"
  - Example: "Week 7 teaches data storytelling → Portfolio piece tests data visualization skills"
- Populate all assessment tables

**For option 3:**
- Guide user through custom structure matching template format

**Your action:**
- Populate: {{GRADING_DISTRIBUTION_TABLE}}, {{DETAILED_ASSESSMENTS}}
- **SAVE IMMEDIATELY:** Create assessment schedule in `courses/[COURSE-CODE]/assessments/assessment-schedule.md`
- Update course-info.md with assessment structure
- **Validate alignment:** Each assessment tests specific content from researched articles

---

### STEP 5: Select and Customize Rubrics

**Ask user:** "Which types of rubrics do you need based on your assessments?"

**Load from templates:**
- `templates/syllabus-components/rubric-structures/written-work-rubric.md`
- `templates/syllabus-components/rubric-structures/presentation-rubric.md`
- `templates/syllabus-components/rubric-structures/project-rubric.md`

**Your action:**
- Customize rubrics for specific assignments if needed
- Prepare rubrics for document structure decision

**IMPORTANT - Do NOT save rubrics yet** - wait for Step 5.5 decision on document structure

---

### STEP 5.5: Choose Document Structure

**Explain to user:**
"For comprehensive courses with detailed assessments, we have two document structure options:"

**Option 1: Single Comprehensive Syllabus (Traditional)**
- One document containing everything
- All rubrics embedded in syllabus
- All detailed instructions inline
- Best for: Simple courses with 2-3 assessments, shorter rubrics

**Option 2: Two-Document Structure (Recommended for Complex Courses)**
- **syllabus.md** (15-20 pages): Overview document
  - Course description and learning objectives
  - Course calendar with reading list
  - Assessment overview table with weights and due dates
  - Brief assessment descriptions
  - Cross-references: "See Assessment Handbook Section X"
  - Course policies and resources

- **assessment-handbook.md** (25-40 pages): Complete assessment guide
  - Section 1: [Assessment 1] - Full instructions + rubric
  - Section 2: [Assessment 2] - Full instructions + rubric
  - Section 3: [Assessment 3] - Full instructions + rubric
  - Section 4: [Assessment 4] - Full instructions + rubric
  - Appendix: Submission procedures

- Best for: Courses with 3+ assessments, detailed rubrics, complex requirements

**Benefits of 2-Document Structure:**
- Syllabus remains scannable overview
- Handbook provides depth when needed
- Clear referential integrity
- Students reference syllabus for "what/when", handbook for "how"
- Each document serves distinct purpose

**Ask user:** "Which structure works best for this course?"

**Your action based on choice:**

**If Option 1 (Single Document):**
- Populate: {{COURSE_RUBRICS}} inline
- Include all detailed instructions in syllabus
- Save to `courses/[COURSE-CODE]/syllabus.md`

**If Option 2 (Two Documents):**
- Create syllabus.md with:
  - Assessment overview table with "See Handbook Section X" references
  - Brief descriptions only (2-3 paragraphs per assessment)
  - Clear cross-references throughout

- Create assessment-handbook.md with:
  - Table of contents linking to sections
  - One section per assessment with:
    - Complete instructions
    - Full rubric with all performance levels
    - Preparation guides/checklists
    - Examples/templates if applicable
    - Submission requirements
  - Appendix with common procedures

**IMPORTANT - Save Progress:**
- Option 1: Save all to `courses/[COURSE-CODE]/syllabus.md`
- Option 2: Save both `courses/[COURSE-CODE]/syllabus.md` AND `courses/[COURSE-CODE]/assessment-handbook.md`
- Update course-info.md with chosen structure

---

### STEP 6: Final Assembly and Quality Check

**Your actions:**
1. Combine all sections using syllabus-base-template.md structure
2. Verify all placeholders are filled
3. Check formatting consistency
4. Validate all URLs are accessible
5. **SAVE FINAL VERSION(S):**
   - Single document: Save to `courses/[COURSE-CODE]/syllabus.md`
   - Two documents: Save `syllabus.md` AND `assessment-handbook.md`
6. Archive draft versions to `.archive/[date]-syllabus-DRAFT.md`
7. Create COMPLETION-REPORT.md summarizing all deliverables

**Quality Checklist:**
- [ ] All course info populated
- [ ] 3-5 learning objectives in each of 4 categories
- [ ] Assessment structure complete with weights and due dates
- [ ] Every week has 2 validated articles (open access preferred; paywalls OK if seminal)
- [ ] All articles passed strict content validation (all concepts covered)
- [ ] Rubrics appropriate for assessments (in syllabus OR handbook)
- [ ] All URLs tested and accessible
- [ ] Professional formatting throughout
- [ ] Cross-references correct (if two-document structure)
- [ ] Referential integrity maintained between documents

**Present final document(s) to user for review.**

---

## Important Research Principles

1. **Strict Content Validation**: Only include articles that cover ALL required key concepts. No partial matches.

2. **BALANCED Coverage (2 Seminal + 2 Recent) - CRITICAL**:
   - **Each week requires 4 articles:**
     - 2 **seminal/foundational** works (highly cited, field-defining, theoretical grounding)
     - 2 **recent applied** articles (2020-2025, current practices, examples)
   - **Seminal works:** Theoretical foundation, classic frameworks, field-defining concepts (1000+ citations)
   - **Recent works:** Current applications, modern examples, from top-tier sources
   - **Recent article selection criteria (priority order):**
     1. Covers required concepts deeply (mandatory)
     2. Top-tier source (HBR, MIT Sloan, business school publications)
     3. Most recent (2023-2025 > 2020-2022)
     4. Has practical examples/case studies
     5. Open access preferred
     6. Cultural relevance (local context is bonus)
   - **Exceptions (all recent acceptable):**
     - AI & Digital Tools (field too new for seminal works)
     - Virtual/Hybrid Collaboration (post-pandemic phenomenon)
   - **Validation:** Research is INCOMPLETE if missing 2 seminal foundations (unless exception applies)

3. **Accessibility Standards**:
   - **Prefer open access** - Freely available articles are best
   - **Paywalls acceptable ONLY for high-quality seminal works:**
     - 1000+ citations (established) or 100+ (recent)
     - Top-tier journal (A*/A ranked)
     - Foundational/field-defining work
     - Full content validated via abstracts/previews/cached versions
     - Claude highly confident of concept coverage
   - **Reject low-quality paywalled articles** - Mid-tier journals, incremental research
   - **Note:** Students can access seminal paywalled works via institutional library access

4. **Quality Sources**: Prioritize peer-reviewed journals, HBR, MIT Sloan Review, top school publications.

5. **Document Everything**: Save research process for transparency and future reference.

6. **Top School Standards**: Research what top US/UK business schools (M7, Berkeley, Yale, Tuck, LBS, Oxford, Cambridge, LSE, Imperial, Warwick, Edinburgh, Manchester, Cranfield) teach on each topic.

## Files to Create

1. `courses/[COURSE-CODE]/syllabus.md` - Final syllabus
2. `courses/[COURSE-CODE]/assessments/assessment-schedule.md` - Extracted schedule
3. `shared/research/school-syllabi-analysis/[course-topic]-research.md` - Research documentation
4. Week-specific research notes as needed

## Estimated Time

**With Claude Desktop (Recommended):**
- Steps 1-2: 20-30 minutes (description + structure with validation)
- Step 3 (handoff creation): 15-20 minutes (create research prompts)
- **Claude Desktop research:** 5-8 hours (user does in Desktop)
- Step 3 (import validation): 30-45 minutes
- Step 4 (assessments): 20-30 minutes (based on actual content)
- Steps 5-6: 10-15 minutes (rubrics + assembly)

**Total Claude Code time: 2-2.5 hours** (Desktop does the heavy lifting)
**Total project time: 7-10.5 hours** (includes Desktop research)

**With Direct Research (Fallback):**
- Steps 1-2: 20-30 minutes
- Step 3 (research): 30-50 minutes per week × 10 weeks = 5-8 hours
- Step 4-6: 30-45 minutes

**Total: 6-9.5 hours** (all in one conversation)

**Recommendation:** Use Claude Desktop for superior research quality and better time management.

The investment ensures world-class, evidence-based course content that truly prepares students for success.
