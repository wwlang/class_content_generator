# Syllabus Generator Updates Log

## Update: January 5, 2025 - Part 3

### Change 3: Simplified Syllabus & Institution Customization

**Issues Identified:**
1. Template hardcoded "Andrews University - National Economics University Campus"
2. AI policy too detailed for needs
3. Core textbook section unnecessary (articles are sufficient)
4. Group work policy too prescriptive

**Solutions Implemented:**

#### 1. Institution Information Collection
**Step 1 now asks:**
- University awarding the qualification (e.g., "Andrews University", "UWE")
- Qualification program (e.g., "BA in Banking and Finance", "BA International Business")
- Campus location (e.g., "National Economics University campus", "Phenikaa campus")

**Syllabus header updated to:**
```markdown
## **{{SEMESTER_YEAR}} - {{UNIVERSITY}} - {{CAMPUS}}**
**Qualification:** {{QUALIFICATION}}
```

**Benefits:**
- ✅ Supports multiple universities (Andrews, UWE, etc.)
- ✅ Supports multiple campuses (NEU, Phenikaa, etc.)
- ✅ Shows qualification context for students
- ✅ Professional header customized per institution

#### 2. Removed AI and Technology Use Policy
**Deleted entire section including:**
- Permitted uses
- Not permitted uses
- Required disclosure
- Example disclosure
- Philosophy statement

**Academic Integrity now includes only:**
- Plagiarism
- Cheating
- Fabrication
- Consequences

**Benefits:**
- ✅ Simpler, cleaner syllabus
- ✅ Focus on core academic integrity principles
- ✅ Less prescriptive about technology use
- ✅ Instructor flexibility to address AI as needed

#### 3. Removed Core Reference Textbook Section
**Deleted:**
- `## **Core Reference Text**` section
- `{{CORE_TEXTBOOK}}` placeholder

**Required Materials now contains only:**
- Required Articles section
- Note that articles are openly accessible

**Benefits:**
- ✅ Reduces cost burden on students
- ✅ All learning materials are open access
- ✅ Simpler materials section
- ✅ Consistent with research-first philosophy

#### 4. Simplified Group Work Policy
**Reduced from 7 points to 2 points:**
- Groups must be formed with a maximum of 4 students by Week 4
- Non-contributing members may receive significantly reduced grades

**Removed:**
- Intentional diversity requirement
- Peer evaluation details
- Grade adjustment specifications (±5%)
- Team charter requirements

**Benefits:**
- ✅ Clear, minimal requirements
- ✅ Instructor flexibility in implementation
- ✅ Less bureaucracy for students
- ✅ Focus on essentials only

**Files Modified:**
- `.claude/commands/generate-syllabus.md` (Step 1 questions updated)
- `templates/syllabus-base-template.md` (all 4 changes implemented)
- `.claude/CLAUDE.md` (documentation updated)

---

## Update: January 5, 2025 - Part 2

### Change 2: Progress Saving at Each Step

**Issue Identified:**
Original generator built everything in memory without saving intermediate results. If conversation interrupted, all work would be lost.

**Solution Implemented:**
Added save points after each major step:

**Step 1:**
- Create course directory structure
- Save `course-info.md` with basics
- Save `course-description-research.md`

**Step 2:**
- Update `course-info.md` with learning objectives
- Save `learning-objectives-research.md`

**Step 3:**
- **SAVE IMMEDIATELY:** `assessments/assessment-schedule.md`
- Update `course-info.md`

**Step 4:**
- **CRITICAL:** Save article research after EACH week to `article-research-summary.md`
- Update `syllabus-DRAFT.md` every 2-3 weeks
- Mark draft status clearly

**Step 5:**
- Save each rubric as separate file in `rubrics/`
- Update draft syllabus with rubrics section

**Step 6:**
- Save final syllabus to `syllabus.md`
- Keep `syllabus-DRAFT.md` as backup
- Create completion summary

**Benefits:**
- ✅ Work preserved if conversation interrupts
- ✅ Progress trackable at any point
- ✅ Can resume from any step
- ✅ Research documented for future reference
- ✅ Audit trail of all decisions

**Files Modified:**
- `.claude/commands/generate-syllabus.md` (save points added throughout)

---

## Update: January 5, 2025 - Part 1

### Change 1: Research-Backed Course Descriptions

**Issue Identified:**
Original generator asked users to provide course descriptions directly in Step 1, which wasn't consistent with the research-first philosophy used for learning objectives and article selection.

**Solution Implemented:**
Modified Step 1 to research and synthesize course descriptions from top schools:

1. **Research Phase Added:**
   - Search top schools (HBS, Stanford GSB, Wharton, MIT Sloan for business; appropriate schools for other subjects)
   - Extract course descriptions using WebFetch
   - Analyze for: Purpose, Content, Value Proposition, Unique Elements

2. **Synthesis Structure:**
   - Paragraph 1: Purpose and foundational content
   - Paragraph 2: Pedagogical approach and hands-on application
   - Paragraph 3: Value proposition and career/academic relevance

3. **User Options:**
   - Can provide sample documents for reference (optional)
   - Review and approve/adjust synthesized description
   - Maintains quality control while ensuring research backing

4. **Documentation:**
   - Research saved to `shared/research/[course-topic]/course-description-research.md`
   - Audit trail of how description was derived

**Benefits:**
- ✅ Consistent research-first approach across all syllabus components
- ✅ Leverages best practices from top institutions
- ✅ Still allows user customization and approval
- ✅ Documents research process for transparency
- ✅ Reduces user burden while maintaining quality

**Files Modified:**
- `.claude/commands/generate-syllabus.md` (Step 1 updated)
- `.claude/CLAUDE.md` (documentation updated)

---

## Testing Results

### Test Case: BCI2AU Business Communication Syllabus
- **Status:** Successfully completed
- **Total Time:** ~3 hours
- **All Components:** Research-backed and documented
- **Files Generated:** 7 files including final syllabus, research docs, progress tracking
- **Interruption Recovery:** Tested - all work preserved in files

**Quality Metrics:**
- 20 validated articles
- 15 learning objectives from top school research
- 4 comprehensive rubrics
- Complete 11-week course structure
- Professional formatting maintained
- Institution-customized header
- Simplified policies

---

## Planned Updates (Not Yet Implemented)

### Framework-Specific Rubrics (Pending)

**Issue:**
Current rubrics are generic and don't reference specific course frameworks, models, and techniques that will be taught.

**Proposed Solution:**
1. Add Step 3: Framework Research (30-45 min)
   - Research key frameworks taught at top schools
   - Present 8-12 core frameworks to user
   - Save to `core-frameworks.md`

2. Redesign Step 4: Framework-Referenced Rubrics
   - Inject framework names into rubric criteria
   - Example: "Applies Cialdini's 6 principles to analyze..."
   - Make rubrics course-specific but general enough to share Day 1

3. Modify Step 5: Framework-Validated Article Research
   - Validate articles teach frameworks referenced in rubrics
   - Ensures perfect alignment

**Benefits:**
- Backward design compliant
- Constructively aligned
- Students know exactly what to learn
- All research supports assessment

**Status:** Researched and planned, awaiting implementation decision

---

## Next Planned Updates

### Future Enhancements (Not Yet Implemented)

1. **Assessment Prompt Generator**
   - Auto-generate detailed assignment prompts based on course content
   - Align prompts with learning objectives and rubrics

2. **Quiz Question Bank**
   - Generate sample quiz questions during article research
   - Based on key concepts validated in articles

3. **Course Calendar Integration**
   - Auto-populate specific dates based on semester start/end
   - Account for holidays and break weeks

4. **Multi-Language Support**
   - Generate syllabi in multiple languages
   - Culturally adapt examples and references

5. **Version Control**
   - Track syllabus versions over time
   - Show what changed between versions

---

## Maintenance Notes

### When to Update Generator

Update `/generate-syllabus` when:
- New research sources become available
- Pedagogical best practices evolve
- User feedback identifies gaps
- Quality issues discovered in testing
- Institution requirements change

### Testing Protocol

Before deploying generator updates:
1. Test with sample course (business course recommended)
2. Verify all save points work
3. Test interruption recovery
4. Validate URL accessibility
5. Check formatting consistency
6. Review research quality
7. Verify institution customization works
8. Check simplified policies are clear

---

**Last Updated:** January 5, 2025
**Version:** 1.2
**Tested By:** Generator development team
