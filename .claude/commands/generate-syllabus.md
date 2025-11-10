# Generate Comprehensive Course Syllabus

You are creating a world-class university course syllabus using the research-enhanced workflow. Follow these steps precisely to ensure quality, consistency, and evidence-based content.

## Your Task

Guide the user through creating a complete course syllabus that:
1. Maintains the professional structure and policies from the Business Communication template
2. Incorporates research from top management schools (HBS, Stanford GSB, Wharton, MIT Sloan)
3. Includes 2 validated, accessible articles per week with strict content matching
4. Aligns assessments with learning objectives

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
   - HBS, Stanford GSB, Wharton, MIT Sloan (for business courses)
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

### STEP 2: Research Top Schools for Learning Objectives AND Course Structure

**Explain to user:**
"I'll research how top management schools (HBS, Stanford GSB, Wharton, MIT Sloan) teach this subject to extract both learning objectives and weekly course structure."

**Research Process:**

1. **Search for syllabi and course descriptions:**
   - Use WebSearch to find syllabi from HBS, Stanford GSB, Wharton, MIT Sloan
   - Use WebFetch to extract detailed course information

2. **Extract TWO key elements:**

   **A. Learning Objectives** (organized in 4 Bloom's Taxonomy categories)
   - Understand & Apply (3-5 objectives)
   - Analyze & Evaluate (3-5 objectives)
   - Create & Present (3-5 objectives)
   - Collaborate (2-3 objectives)

   **B. Course Structure** (weekly topics and progression)
   - Week-by-week topics from each school
   - Key concepts covered each week
   - Logical progression and scaffolding
   - Common themes across schools

3. **Synthesize and present:**
   - Present synthesized learning objectives for user approval
   - Present synthesized weekly course outline for user approval
   - Show which schools teach which topics
   - Explain the pedagogical progression

**Your action:**
- Populate: {{UNDERSTAND_APPLY_OBJECTIVES}}, {{ANALYZE_EVALUATE_OBJECTIVES}}, {{CREATE_PRESENT_OBJECTIVES}}, {{COLLABORATE_OBJECTIVES}}
- Create draft weekly outline based on research (to be used in Step 4)

**IMPORTANT - Save Progress:**
- Update course-info.md with learning objectives
- Save learning objectives research to `shared/research/[course-topic]/learning-objectives-research.md`

---

### STEP 3: Assessment Structure

**Ask the user:** "Which assessment structure best fits this course?"

**Options:**
1. Portfolio + Presentation + Quiz (skills-based courses)
2. Exam + Project + Quiz (content-heavy courses)
3. Custom mix

**For options 1 or 2:**
- Load appropriate template from `templates/syllabus-components/assessment-structures/`
- Ask for specific weights, due weeks, and assignment names
- Populate all assessment tables

**For option 3:**
- Guide user through custom structure matching template format

**Your action:**
- Populate: {{GRADING_DISTRIBUTION_TABLE}}, {{DETAILED_ASSESSMENTS}}
- **SAVE IMMEDIATELY:** Create assessment schedule in `courses/[COURSE-CODE]/assessments/assessment-schedule.md`
- Update course-info.md with assessment structure

---

### STEP 4: Course Calendar with Research-Backed Articles

This is the most intensive step. For each week:

#### 4A: Present Research-Backed Weekly Outline

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

**Once approved, proceed to article research for each week.**

#### 4B: Four-Stage Article Research Process

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
2. Check for paywall (STRICT: must be openly accessible)
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

**Ask user to select 2 articles** (ideally 1 theoretical/foundational + 1 applied/practitioner)

#### 4C: Document Research

**CRITICAL - Save After Each Week:**
Save research notes to `shared/research/[course-topic]/article-research-summary.md` documenting:
- Candidates considered for this week
- Validation results (which passed/failed and why)
- Final selections with justifications
- Update the file after EACH week is completed

This ensures no work is lost if conversation is interrupted.

#### 4D: Build Calendar Entry and SAVE DRAFT

Add to course calendar table:
```markdown
| Week [#]: [Topic] | [Topic details] [Key frameworks] [Learning focus] | [Article 1 citation with URL] [Article 2 citation with URL] |
```

**CRITICAL - Save Draft Syllabus After Every 2-3 Weeks:**
- Update `courses/[COURSE-CODE]/syllabus-DRAFT.md` with completed weeks
- This ensures work is preserved even if conversation interrupts
- Mark draft status clearly at top of file

**Repeat Steps 4A-4D for all weeks**

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
- [ ] Every week has 2 validated, accessible articles
- [ ] All articles passed strict content validation
- [ ] Rubrics appropriate for assessments (in syllabus OR handbook)
- [ ] All URLs tested and accessible
- [ ] Professional formatting throughout
- [ ] Cross-references correct (if two-document structure)
- [ ] Referential integrity maintained between documents

**Present final document(s) to user for review.**

---

## Important Research Principles

1. **Strict Content Validation**: Only include articles that cover ALL required key concepts. No partial matches.

2. **Accessibility is Mandatory**: Every article must be openly accessible. If paywall detected, find open-access alternative.

3. **Quality Sources**: Prioritize peer-reviewed journals, HBR, MIT Sloan Review, top school publications.

4. **Current + Seminal**: Balance recent relevance with foundational works.

5. **Document Everything**: Save research process for transparency and future reference.

6. **Top School Standards**: Research what HBS, Stanford GSB, Wharton, and MIT Sloan teach on each topic.

## Files to Create

1. `courses/[COURSE-CODE]/syllabus.md` - Final syllabus
2. `courses/[COURSE-CODE]/assessments/assessment-schedule.md` - Extracted schedule
3. `shared/research/school-syllabi-analysis/[course-topic]-research.md` - Research documentation
4. Week-specific research notes as needed

## Estimated Time

- Steps 1-3: 15-20 minutes
- Step 4 (research): 15-20 minutes per week (intensive but thorough)
- Steps 5-6: 10-15 minutes

**Total for 10-week course: 3-4 hours of high-quality syllabus development**

The investment ensures world-class, evidence-based course content that truly prepares students for success.
