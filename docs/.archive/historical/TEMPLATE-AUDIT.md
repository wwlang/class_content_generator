# Template Audit - Phase 1

**Date:** November 24, 2025
**Purpose:** Verify all referenced templates exist and identify missing templates

---

## Summary

**Total Templates Referenced:** 13
**Templates Existing:** 12 ✓
**Templates Missing:** 1 ⚠️
**Action Required:** Create 1 missing template

---

## Audit Results

### ✓ Course Structure Templates (All Exist)

| Template | Location | Status | Referenced By |
|----------|----------|--------|---------------|
| Syllabus Base | `templates/syllabus-base-template.md` | ✓ EXISTS | generate-syllabus.md |
| Week Topic Spec | `templates/week-topic-specification.md` | ✓ EXISTS | generate-week.md |
| Grading Systems | `templates/grading-systems.md` | ✓ EXISTS | generate-syllabus.md |
| Vocabulary Translation | `templates/vocabulary-translation-template.md` | ✓ EXISTS | generate-week.md (optional) |

### ✓ Assessment Structure Templates (All Exist)

| Template | Location | Status | Referenced By |
|----------|----------|--------|---------------|
| Portfolio+Presentation+Quiz | `templates/syllabus-components/assessment-structures/portfolio-presentation-quiz.md` | ✓ EXISTS | generate-syllabus.md Step 3 |
| Exam+Project+Quiz | `templates/syllabus-components/assessment-structures/exam-project-quiz.md` | ✓ EXISTS | generate-syllabus.md Step 3 |

### ✓ Rubric Templates (All Exist)

| Template | Location | Status | Referenced By |
|----------|----------|--------|---------------|
| Written Work Rubric | `templates/syllabus-components/rubric-structures/written-work-rubric.md` | ✓ EXISTS | generate-syllabus.md Step 5 |
| Presentation Rubric | `templates/syllabus-components/rubric-structures/presentation-rubric.md` | ✓ EXISTS | generate-syllabus.md Step 5 |
| Project Rubric | `templates/syllabus-components/rubric-structures/project-rubric.md` | ✓ EXISTS | generate-syllabus.md Step 5 |
| Vietnamese Weighted Rubric | `templates/syllabus-components/rubric-structures/vietnamese-weighted-rubric.md` | ✓ EXISTS | generate-syllabus.md Step 5 |

### ✓ Claude Code Templates (Existing)

| Template | Location | Status | Referenced By |
|----------|----------|--------|---------------|
| Desktop Master Prompt | `.claude/templates/desktop-master-prompt-template.md` | ✓ EXISTS | generate-syllabus.md Step 3D |
| Desktop Research with Auto-Write | `.claude/templates/desktop-research-with-autowrite.md` | ✓ EXISTS | import-research.md, RESEARCH-HANDOFF-GUIDE.md |

### ⚠️ Missing Templates

| Template | Location | Status | Impact | Priority |
|----------|----------|--------|--------|----------|
| Research Output Format (Manual) | `.claude/templates/research-output-format.md` | ⚠️ MISSING | Manual paste workflow harder without template | MEDIUM |

---

## Analysis: Missing Template

### `.claude/templates/research-output-format.md`

**Referenced In:**
- `.claude/commands/import-research.md` (line 98): "Option B (Manual): Used template from `.claude/templates/research-output-format.md` (if it exists)"
- `docs/RESEARCH-HANDOFF-GUIDE.md` (lines 327, 382, 440, 568, 1263, 1267, 1277)

**Purpose:**
- Provides simplified prompt for Claude Desktop manual workflow
- Used when MCP auto-write is not configured
- Contains prompt template + output format specification
- Enables manual copy/paste research handoff

**Current Workaround:**
- Users can use `desktop-research-with-autowrite.md` and ignore auto-write instructions
- Marked as "(if it exists)" in import-research.md, suggesting optional

**Impact of Missing Template:**
- Manual workflow users have no clear template to follow
- RESEARCH-HANDOFF-GUIDE.md references non-existent file (lines 382, 440)
- Reduces usability for users without MCP setup

**Recommendation:** CREATE
- Extract manual-workflow portions from `desktop-research-with-autowrite.md`
- Create simplified version without MCP/auto-write instructions
- Maintain consistency with auto-write template for output format
- Ensure backward compatibility

---

## Template Usage Patterns

### Primary Workflows Using Templates:

1. **Syllabus Generation (`/generate-syllabus`)**
   - Uses: syllabus-base-template.md
   - Uses: assessment-structures/* (portfolio or exam-based)
   - Uses: rubric-structures/* (written-work, presentation, project, vietnamese-weighted)
   - Uses: grading-systems.md
   - Uses: desktop-master-prompt-template.md (for research)
   - **All templates exist ✓**

2. **Research Import (`/import-research`)**
   - Uses: desktop-research-with-autowrite.md (auto-write workflow)
   - Uses: research-output-format.md (manual workflow) **⚠️ MISSING**
   - **Partial support - auto-write works, manual harder**

3. **Week Generation (`/generate-week`)**
   - Uses: week-topic-specification.md
   - Uses: vocabulary-translation-template.md (optional)
   - **All templates exist ✓**

---

## Recommendations

### Immediate Action Required

**Create: `.claude/templates/research-output-format.md`**

**Approach:**
1. Extract manual-workflow sections from `desktop-research-with-autowrite.md`
2. Remove MCP/auto-write specific instructions
3. Focus on:
   - 4-stage research process
   - Output format specification (START/END markers)
   - Validation checklist
   - Prompt template for Desktop
4. Add examples from actual courses
5. Ensure output format matches auto-write template exactly

**Time Estimate:** 15-20 minutes

**Benefits:**
- Complete manual workflow support
- Fixes broken references in RESEARCH-HANDOFF-GUIDE.md
- Provides simpler alternative for users without MCP
- Maintains backward compatibility
- Fulfills documentation promises

### Optional Future Enhancements

1. **Template Testing:**
   - Create test script to verify all referenced templates exist
   - Run as pre-commit hook or CI check
   - Prevent future broken references

2. **Template Documentation:**
   - Add README.md in `templates/` directory
   - Document purpose and usage of each template
   - Include examples of when to use each

3. **Template Versioning:**
   - Add version numbers to templates
   - Track changes over time
   - Ensure compatibility with workflows

---

## Validation Checklist

- [x] Scanned all .md files for template references
- [x] Verified existence of all referenced templates
- [x] Identified missing templates with impact analysis
- [x] Documented all template locations
- [x] Created recommendations for missing templates
- [ ] Create missing template: research-output-format.md
- [ ] Test template with manual workflow
- [ ] Update RESEARCH-HANDOFF-GUIDE.md if needed
- [ ] Verify all cross-references work

---

## Next Steps

1. **Create missing template** (15-20 min)
   - File: `.claude/templates/research-output-format.md`
   - Based on: `desktop-research-with-autowrite.md` (manual portions)
   - Purpose: Support manual paste workflow

2. **Test template** (5 min)
   - Verify output format matches auto-write template
   - Ensure all required sections present
   - Check examples are clear

3. **Mark Phase 1 Complete**
   - All 5 tasks completed
   - Ready for end-to-end testing

---

*Audit completed as part of Phase 1 implementation (Task 5/5)*
