# Test Run Issues - BCI2AU Business Communication
## Date: November 24, 2025

## Purpose
Testing the `/generate-syllabus` workflow to identify and fix issues before production use.

---

## Issues Identified

### Issue 1: Textbook Dependency (CRITICAL)
**Problem:** Step 2 research used Guffey textbook as primary structure source
- User explicitly stated: "I absolutely hate that textbook. Don't base anything on that."
- Workflow defaulted to textbook table of contents as course structure guide
- Should rely on top schools' modern approaches only

**Root cause:**
- `/generate-syllabus` command mentions sample syllabus uses Guffey
- Step 2 instructions don't explicitly prohibit textbook reliance
- Agent defaulted to textbook as "safe" structure

**Fix needed:**
- Remove textbook references from Step 2 research process
- Change from "Research objectives AND structure" to "Research from top schools only"
- Add explicit instruction: "Do NOT use textbook table of contents as structure"
- Focus: Actual syllabi from HBS, Stanford, Wharton, MIT, Berkeley, etc.

**Files to update:**
- `.claude/commands/generate-syllabus.md` - Step 2 instructions
- `lecture_content_instructions.md` - Remove Guffey references if present

---

### Issue 2: Course Description Alignment (CRITICAL)
**Problem:** Generated course structure didn't validate against approved description
- Description promised: AI, data storytelling, virtual collaboration, crisis management, ethical communication
- Initial structure missing: AI (explicit), crisis management, virtual collaboration (explicit)
- No validation step to ensure all promises were addressed

**Root cause:**
- No explicit validation checkpoint after Step 1 (description approval)
- Step 2 didn't extract promises from description first
- Structure created independently, then hoped it would align

**Fix needed:**
- Add Step 1.5: Extract promises from approved description
- Create checklist of topics that MUST appear in structure
- Add validation before presenting structure to user
- Format: "Every description promise must map to specific week(s)"

**Proposed Step 1.5:**
```markdown
### Step 1.5: Extract Course Description Promises

After user approves description, create a checklist:

**Topics explicitly promised in description:**
□ [Topic 1] - Must appear in Week [X]
□ [Topic 2] - Must appear in Week [Y]
□ [Emerging technology/AI] - Must have explicit coverage
□ [Any unique differentiators] - Must be addressed

**Before proceeding to Step 2:**
- Keep this checklist visible
- Ensure every checkbox gets mapped to specific week(s)
- Validate structure against checklist before presenting to user
```

**Files to update:**
- `.claude/commands/generate-syllabus.md` - Add Step 1.5
- Add validation checklist template

---

### Issue 3: Assessment Timing (PEDAGOGICAL)
**Problem:** Attempted to design assessments (Step 3) before knowing actual course content (Step 4)
- Assessments should test what we actually teach
- Can't design good assessments based only on topic headings
- Need to know specific frameworks/articles before designing tests

**Root cause:**
- Step order in workflow: Description → Objectives/Structure → Assessments → Articles
- Should be: Description → Objectives/Structure → Articles → Assessments
- Workflow prioritized documentation order over pedagogical soundness

**Fix needed:**
- Reorder steps: Move "Assessment Structure" AFTER "Article Research"
- Explain WHY in documentation: "Assessments must align with specific content, not just topic headings"
- New order:
  1. Course basics & description
  2. Learning objectives & structure
  3. **Article research for all weeks** ← BEFORE assessments
  4. **Assessment structure** ← AFTER knowing content
  5. Rubrics
  6. Document structure choice
  7. Final assembly

**Files to update:**
- `.claude/commands/generate-syllabus.md` - Reorder steps 3 and 4
- Add pedagogical rationale for order
- Update time estimates accordingly

---

### Issue 4: Research Method Default (EFFICIENCY)
**Problem:** Started doing research directly instead of recommending Claude Desktop handoff
- Documentation explicitly states Claude Desktop has superior research capability
- `/import-research` command exists for this workflow
- Should be the DEFAULT recommendation, not afterthought

**Root cause:**
- `/generate-syllabus` doesn't mention Claude Desktop handoff option in Step 4
- Presented as "do 4-stage research" not "hand off to Desktop for research"
- Only mentioned in CLAUDE.md, not in command itself

**Fix needed:**
- Add Step 4A: "Check for Claude Desktop availability"
- Make Desktop handoff the PRIMARY workflow
- Direct research = fallback if Desktop not available
- Show time savings: "Desktop research: 5-8 hours of better quality vs. Direct: 8-10 hours"

**Proposed Step 4A:**
```markdown
### Step 4A: Choose Research Method

**Ask user:** "Do you have Claude Desktop available for article research?"

**Option 1: Claude Desktop Handoff (RECOMMENDED)**
- Superior research capabilities
- Time: 5-8 hours for 10 weeks
- Quality: More thorough validation
- Process: Create research prompts → User hands off → Import results

**Option 2: Direct Research (Fallback)**
- Use WebSearch/WebFetch directly
- Time: 8-10 hours for 10 weeks
- Process: 4-stage validation in this conversation

**If Option 1:** Proceed to create Desktop research prompts
**If Option 2:** Proceed with direct 4-stage research
```

**Files to update:**
- `.claude/commands/generate-syllabus.md` - Add Step 4A choice point
- Emphasize Desktop as default

---

### Issue 5: Date Awareness (DATA QUALITY)
**Problem:** Made incorrect assumption about current date
- Assumed "January 2025" when actual date was "November 24, 2025"
- Research for "past 6 months" was miscalculated by 10 months
- Didn't check `<env>` tag carefully before starting research

**Root cause:**
- Saw "2025" and defaulted to early in year
- No explicit reminder to check current date from environment
- Easy to overlook in `<env>` tags

**Fix needed:**
- Add explicit date check at start of research steps
- Remind: "Check <env> for today's date before searching for recent sources"
- For time-sensitive research (e.g., "past 6 months"), calculate date range explicitly

**Proposed addition to research steps:**
```markdown
**Before starting research:**
1. Check `<env>` tag for current date: [INSERT DATE]
2. If searching for recent sources (e.g., "past 6 months"):
   - Calculate: Current date - 6 months = [START DATE]
   - Search range: [START DATE] to [CURRENT DATE]
3. Include date range in search queries
```

**Files to update:**
- `.claude/commands/generate-syllabus.md` - Add date check to Step 4
- `.claude/commands/research-topic.md` - Add date check
- Any research-heavy workflows

---

## Summary of Required Fixes

| Issue | Priority | Files to Update | Estimated Time |
|-------|----------|-----------------|----------------|
| Textbook dependency | CRITICAL | generate-syllabus.md | 15 min |
| Description alignment | CRITICAL | generate-syllabus.md | 30 min |
| Assessment timing | HIGH | generate-syllabus.md | 15 min |
| Research method default | MEDIUM | generate-syllabus.md | 20 min |
| Date awareness | LOW | generate-syllabus.md, research-topic.md | 10 min |

**Total estimated fix time: ~90 minutes**

---

## Process Improvements Needed

### 1. Description → Structure Validation Checklist
Create template that forces validation:
```markdown
## Description Promises Validation

Before presenting structure to user, verify:
□ Every specific topic mentioned in description has explicit week
□ Every unique differentiator is addressed
□ No generic/traditional topics replace promised modern content
□ Special emphasis areas (AI, ethics, crisis, etc.) are prominent, not buried
```

### 2. Pedagogical Sequence Enforcement
Document WHY steps are ordered this way:
- Content before assessments (pedagogical alignment)
- Articles before rubrics (assess what you teach)
- Structure before research (focus the research)

### 3. Research Handoff as Default
Make Desktop handoff the primary path:
```
Step 4: Article Research
├─ Check: Claude Desktop available?
│  ├─ YES → Create handoff prompts (proceed to 4B)
│  └─ NO → Direct research (proceed to 4C)
```

---

## Testing Notes

**What worked well:**
- Step 1: Course basics and description generation (good research, good synthesis)
- User feedback loop: User caught issues immediately
- Research agent: Found good current sources (when given correct date range)

**What needs improvement:**
- Validation checkpoints missing
- Step ordering needs pedagogical thinking
- Default workflows should leverage Desktop
- Date/time awareness needs explicit checks

---

## Next Steps

1. **Fix the workflows** (90 min estimated)
2. **Test fixes** either:
   - Continue this BCI2AU course with fixed process
   - Start fresh test course to validate fixes
3. **Document learnings** in CONTRIBUTING.md or workflow guide
4. **Update CLAUDE.md** with lessons learned

---

## Questions for User

1. Should I proceed with fixing the workflows now?
2. After fixes, should we:
   - Continue BCI2AU using corrected process?
   - Start a fresh test course to validate fixes?
3. Are there other issues you noticed that I missed?
4. Any other generator workflows needing similar scrutiny?
