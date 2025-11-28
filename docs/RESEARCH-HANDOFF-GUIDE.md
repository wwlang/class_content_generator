# Research Handoff Guide

**Leverage Claude Desktop's Superior Research → Generate Content in Claude Code**

---

## Table of Contents

1. [Overview](#overview)
2. [Why Use Manual Handoff?](#why-use-manual-handoff)
3. [Quick Start](#quick-start)
4. [Step-by-Step Workflow](#step-by-step-workflow)
5. [Research Template](#research-template)
6. [Import Process](#import-process)
7. [Validation & Quality Control](#validation--quality-control)
8. [Troubleshooting](#troubleshooting)
9. [Examples](#examples)
10. [FAQs](#faqs)

---

## Overview

This guide describes how to perform article research in **Claude Desktop** (which has superior research capabilities) and transfer the results to **Claude Code** for content generation.

### Two Handoff Methods

**Method 1: Auto-Write via MCP (NEW - Recommended)**
```
┌─────────────────────┐
│ Claude Desktop      │
│ - Superior research │──┐
│ - Deep web access   │  │ Auto-write via MCP
│ - Better validation │  │ (file system access)
│ - Writes to file   │  │
└─────────────────────┘  │
                          ↓
                   article-research-summary.md
                          ↓
┌─────────────────────┐  │
│ Claude Code         │←─┘
│ - Validate format   │
│ - Generate syllabus │
│ - Create content    │
└─────────────────────┘
```

**Method 2: Manual Copy/Paste (Fallback)**
```
┌─────────────────────┐
│ Claude Desktop      │
│ - Superior research │──┐
│ - Deep web access   │  │ Manual Handoff
│ - Better validation │  │ (copy/paste)
└─────────────────────┘  │
                          ↓
┌─────────────────────┐  │
│ Claude Code         │←─┘
│ - Validate format   │
│ - Generate syllabus │
│ - Create content    │
└─────────────────────┘
```

### Time Investment

**Research in Claude Desktop:** 30-50 min/week (same for both methods)

**Import into Claude Code:**
- **Auto-write:** 1-2 min/week (validation only, no copy/paste)
- **Manual paste:** 3-7 min/week (copy/paste + validation)

**Time saved with auto-write:** 2-5 min/week → **20-50 min per 10-week course**

**Benefit:** Superior article quality + strict validation maintained + reduced errors

---

## Why Use Manual Handoff?

### Claude Desktop Advantages

✓ **Better research capabilities** - More sophisticated web search and content extraction
✓ **Deeper content analysis** - Superior at validating concept coverage
✓ **Better source access** - May have access to more academic databases
✓ **Iterative refinement** - More advanced multi-step research processes

### When to Use This Workflow

**Use manual handoff when:**
- Quality is paramount (flagship courses, first run)
- You have time for thorough research upfront
- You're researching multiple courses at once (batch efficiency)
- You want complete control over article selection
- Claude Code's WebSearch isn't finding suitable articles

**Don't use when:**
- Claude Code's WebSearch is working well
- Speed is more important than marginal quality gains
- You want end-to-end automation
- Single-course generation with tight timeline

### Time Comparison

**10-Week Course Research:**

| Approach | Time | Quality | Notes |
|----------|------|---------|-------|
| Claude Code only | 5-8 hours | Good | WebSearch/WebFetch |
| Claude Desktop → Code | 5-8 hours + 30-60 min | Excellent | Research time similar, import overhead |
| Hybrid (mix both) | Variable | Very Good | Use Desktop for difficult weeks |

**Verdict:** Minimal time difference, potentially significant quality improvement.

---

## MCP Auto-Write Setup (Optional but Recommended)

### What is Auto-Write?

Auto-write enables Claude Desktop to write research files **directly to your Claude Code workspace** using the Model Context Protocol (MCP). This eliminates manual copy/paste entirely.

### One-Time Setup (15 minutes)

**Step 1: Install MCP Filesystem Server**

Claude Desktop needs filesystem access to write to your workspace.

**Option A: Using Desktop Extensions (Recommended)**
1. Open Claude Desktop Settings
2. Navigate to "Desktop Extensions" or "MCP Servers"
3. Install "@modelcontextprotocol/server-filesystem"
4. Configure allowed directory: `/Users/YOUR_USERNAME/Projects/class_content_generator/courses`

**Option B: Manual Configuration**
1. Locate configuration file: `.claude/mcp-config/desktop-commander-research.json`
2. Update path with your actual username:
   ```json
   "args": ["-y", "@modelcontextprotocol/server-filesystem",
            "/Users/YOUR_USERNAME/Projects/class_content_generator/courses"]
   ```
3. Add configuration to Claude Desktop's MCP settings
4. Restart Claude Desktop

**Step 2: Test MCP Access**

In Claude Desktop, test filesystem access:
```
Can you list the directories in courses/?
```

If successful, you'll see your course directories (or empty list if no courses yet).

**Step 3: Use Auto-Write Template**

Use the auto-write template for research:
- **Template location:** `.claude/templates/desktop-research-with-autowrite.md`
- **Key difference:** Includes instructions for Claude Desktop to write research to file system
- **User approval:** You'll approve file write once per session

### Auto-Write Workflow

**In Claude Desktop:**
1. Open auto-write template
2. Customize with your topic/concepts
3. Paste to Claude Desktop
4. Claude Desktop performs 4-stage research (30-50 min)
5. User selects 2 articles
6. **Claude Desktop writes to file** (asks for approval)
7. Confirmation: "✓ Research saved to article-research-summary.md"

**In Claude Code:**
1. Run: `/import-research [course-code] [week-number]`
2. Claude Code detects existing research
3. Choose: "Validate existing research"
4. Claude Code validates format/content
5. Ready for: `/generate-week [week-number]`

**Total time:** 32-52 min (30-50 research + 2 validation)
**Compare to manual:** 33-57 min (30-50 research + 3-7 copy/paste/validation)
**Saved:** 2-5 min per week, **20-50 min per 10-week course**

### Benefits Over Manual

✓ **Zero copy/paste errors** - No transcription mistakes
✓ **Format guaranteed** - Template-driven generation
✓ **Seamless handoff** - File written directly to workspace
✓ **Batch efficiency** - Approve once, research multiple weeks
✓ **Audit trail** - MCP logs all file operations
✓ **Backward compatible** - Manual paste still works if MCP unavailable

### Troubleshooting MCP Setup

**"I don't have permission to write files"**
- Ensure MCP Filesystem server is installed in Claude Desktop
- Check allowed directories include your workspace path
- Restart Claude Desktop after configuration changes

**"Directory not found"**
- Ensure course structure exists: `/new-course [COURSE-CODE] [Name]`
- Verify path in MCP config matches your actual workspace location
- Use absolute paths, not relative paths

**"MCP not working"**
- Use manual copy/paste method as fallback
- All features work identically, just requires manual transfer
- See "Method 2: Manual Copy/Paste" section below

---

## Validation Flags (Phase 2 - Automatic Validation)

### What Are Validation Flags?

Validation flags are small marker files that Claude Desktop creates after writing research. They signal to Claude Code that research is ready and needs validation **before content generation begins**.

### How It Works

**Traditional Flow (Phase 1):**
```
Desktop writes research → User runs /import-research → Validates → User runs /generate-week
```

**With Validation Flags (Phase 2):**
```
Desktop writes research → Desktop creates .week-[N]-ready flag → User runs /generate-week → Auto-validates → Generates content
```

### Benefits

✓ **Catches errors proactively** - Validation happens right before content generation
✓ **Saves time** - Prevents wasting 45-70 min generating content with bad research
✓ **Zero extra steps** - Validation happens automatically, no separate command needed
✓ **User-friendly** - Just run `/generate-week` like normal

### Flag File Structure

**Location:** `courses/[COURSE-CODE]/.working/research/.week-[N]-ready`

**Content:**
```
Week [N] research completed
Timestamp: 2025-01-20 14:30:00
Course: BCI2AU
Topic: Persuasive Communication
```

**Purpose:** Simple marker file that indicates research is complete and ready for validation.

### Workflow with Flags

**In Claude Desktop:**
1. Research articles (30-50 min)
2. User selects 2 articles
3. Claude Desktop writes to `article-research-summary.md` ✓
4. Claude Desktop creates `.week-[N]-ready` flag ✓
5. Confirmation: "✓ Validation flag created - ready for `/generate-week [N]`"

**In Claude Code:**
1. Run: `/generate-week [N]`
2. Claude Code detects `.week-[N]-ready` flag ✓
3. Auto-validates research ✓
4. **If valid:**
   - Deletes flag file
   - Proceeds with content generation
5. **If invalid:**
   - Shows specific errors
   - Stops content generation
   - User fixes issues, then re-runs `/generate-week`

### What Gets Validated

Same validation as `/import-research`:
- ✓ Format (START/END markers, all sections)
- ✓ Content (all concepts have ✓, specific details)
- ✓ Quality (APA citations, URLs, rationales)
- ✓ Accessibility (open access preferred; paywalls OK if seminal + validated)

### Error Handling

**If validation finds issues:**
```
User: /generate-week 5

Claude Code: ✓ Found auto-imported research for Week 5
Claude Code: Validating research before generating content...
Claude Code: ✗ Research validation failed - cannot generate content

Issues found:
- Article 2 missing Content Match for Concept 3
- Article 1 URL returns 404 (broken link)

Please fix research issues using /import-research BCI2AU 5 or regenerate in Claude Desktop.
```

**User options:**
1. Fix in Claude Desktop, rewrite research file
2. Fix manually in `article-research-summary.md`
3. Use `/import-research` to replace with corrected research

### Flag Cleanup

Flags are **automatically deleted** after successful validation. If generation is interrupted:
- Old flags remain in `.working/research/`
- Next `/generate-week` run will re-validate (safe to re-run)
- Manual cleanup: Delete `.week-[N]-ready` files if needed

### Disabling Flags

Don't want automatic validation? Simply don't create flag files:
- Use Phase 1 auto-write (writes research, no flag)
- Or use manual copy/paste method
- `/generate-week` works normally without flags

---

## Quick Start

### 1. Choose Your Method & Get the Template

**Method 1: Auto-Write (Recommended if MCP configured)**
- **Template:** `.claude/templates/desktop-research-with-autowrite.md`
- **Benefits:** No copy/paste, fewer errors, faster handoff
- **Requires:** One-time MCP setup (see section above)

**Method 2: Manual Copy/Paste (Fallback)**
- **Template:** `.claude/templates/research-output-format.md` (if exists, or use auto-write template)
- **Benefits:** Works without MCP, familiar workflow
- **Requires:** Manual copy/paste step

**Both templates contain:**
- Prompt to give Claude Desktop
- 4-stage research process instructions
- Exact output format required
- Validation checklist
- Examples

### 2. Research in Claude Desktop

```
1. Open Claude Desktop
2. Paste the template prompt (customize with your topic/concepts)
3. Let Claude Desktop perform 4-stage research
4. Copy the formatted output (between START/END markers)
```

### 3. Import into Claude Code

**If using auto-write:**
```
/import-research [course-code] [week-number]
[Claude Code detects existing research]
[Choose: "Validate existing research"]
```

**If using manual paste:**
```
Option A: During syllabus generation
/generate-syllabus
[At Step 4A, paste your research]

Option B: Standalone import
/import-research [course-code] [week-number]
[Paste your research when prompted]
```

### 4. Generate Content

```
/generate-week [week-number]
[Claude Code uses imported articles automatically]
```

---

## Step-by-Step Workflow

### Phase 1: Setup (One Time)

**1. Read the Research Template**

Location: `.claude/templates/research-output-format.md`

This file contains:
- Complete prompt for Claude Desktop
- Required output format
- Validation checklist
- Real examples from actual courses

**2. Understand the 4-Stage Process**

Both Claude Desktop and Claude Code use the same research process:

```
STAGE 1: Discovery
├─ Find 10-15 candidate articles
├─ Cast wide net across sources
└─ Top schools, academic, practitioner

STAGE 2: Quick Filter
├─ Check accessibility (prefer open access; paywalls OK if seminal + validated)
├─ Review relevance
└─ Reduce to 5-6 candidates

STAGE 3: Content Validation
├─ Deep analysis of each candidate
├─ Validate ALL concepts covered
├─ STRICT: Reject partial matches
└─ Reduce to 2-3 finalists

STAGE 4: Final Selection
├─ Present finalists to user
├─ User selects 2 articles
└─ Document selections with rationale
```

### Phase 2: Research in Claude Desktop

**1. Prepare Your Topic Information**

You need:
- Week number
- Topic name
- Key concepts required (3-5 specific concepts)
- Optional: Course context, student level, Vietnamese relevance

**Example:**
```
Week: 5
Topic: Persuasive Communication
Key Concepts:
1. Cialdini's six principles of influence
2. Message structure and framing
3. Audience analysis techniques
4. Ethical persuasion practices
```

**2. Create the Research Prompt**

Open `.claude/templates/research-output-format.md` and copy the "Prompt for Claude Desktop" section.

Customize it:
```markdown
I need you to research articles for Persuasive Communication using a rigorous 4-stage validation process.

**Week Number:** 5
**Topic:** Persuasive Communication in Business

**Key Concepts Required:**
1. Cialdini's six principles of influence
2. Message structure and framing techniques
3. Audience analysis and adaptation
4. Ethical considerations in persuasion

**Context:** Undergraduate business communication course, Vietnamese students, focus on business applications

[Rest of template prompt remains the same]
```

**3. Run the Research**

In Claude Desktop:
1. Paste your customized prompt
2. Claude Desktop will perform 4-stage research (30-50 minutes)
3. Review the finalists presented
4. Select 2 articles (ideally 1 theoretical + 1 applied)
5. Claude Desktop provides formatted output

**4. Copy the Formatted Output**

Look for the output between these markers:
```
---START RESEARCH OUTPUT---
[All your research results]
---END RESEARCH OUTPUT---
```

Copy everything including the markers.

### Phase 3: Import into Claude Code

**Option A: Import During Syllabus Generation**

```bash
# In Claude Code terminal
/generate-syllabus
```

Complete Steps 1-3 normally (course basics, objectives, assessments).

At Step 4A, you'll be asked:
```
"Do you have pre-researched articles from Claude Desktop for any weeks?"
```

Respond:
```
Yes, I have research for weeks 1, 3, 5, and 7. Here's the output:

---START RESEARCH OUTPUT---
[Paste your research here]
---END RESEARCH OUTPUT---
```

Claude Code will:
1. Validate the format ✓
2. Check content completeness ✓
3. Verify accessibility ✓
4. Save to `.working/research/article-research-summary.md` ✓
5. Skip research for those weeks
6. Research only the remaining weeks

**Option B: Standalone Import**

```bash
# In Claude Code terminal
/import-research BCI2AU 5
```

When prompted:
```
Please provide the research output from Claude Desktop.
Paste the complete output including ---START RESEARCH OUTPUT--- and ---END RESEARCH OUTPUT--- markers.
```

Paste your research output.

Claude Code validates and saves automatically.

**Option C: Batch Import (Multiple Weeks)**

```bash
/import-research BCI2AU all
```

Follow prompts to paste research for each week.

Or provide a file path with all weeks' research combined.

### Phase 4: Content Generation

**Generate Weekly Content**

```bash
/generate-week 5
```

Claude Code will:
1. Read syllabus for week 5 topic
2. Find imported research in `.working/research/article-research-summary.md`
3. Use the 2 articles for lecture citations
4. Reference specific article sections in speaker notes
5. Generate tutorial content aligned with readings
6. Create quiz questions from key concepts

**Benefits of imported research:**
- Better citations (you validated content coverage)
- Specific page/section references in notes
- Aligned tutorial activities (articles support concepts)
- Quiz questions grounded in readings

---

## Research Template

### Full Template Location

`.claude/templates/research-output-format.md`

### Quick Reference Format

```markdown
---START RESEARCH OUTPUT---

## Week [N]: [Topic Name]

**Topics:** [1-2 sentence description]

**Key Concepts Required:**
1. [Concept 1]
2. [Concept 2]
3. [Concept 3]
4. [Concept 4]

**FINAL SELECTIONS:**

### Article 1: [Full APA Citation]
- **URL:** [Verified accessible URL]
- **PDF:** [Direct PDF link or "N/A"]
- **Type:** [Peer-reviewed / HBR / Report / etc.]
- **Access:** [Open access / Freely available / etc.]
- **Content Match:**
  - ✓ [Concept 1]: [Specific details - how/where covered, depth, page/section]
  - ✓ [Concept 2]: [Specific details]
  - ✓ [Concept 3]: [Specific details]
  - ✓ [Concept 4]: [Specific details]
- **Why Selected:** [2-3 sentences]

### Article 2: [Full APA Citation]
- [Same structure as Article 1]

**Complementary Coverage:**
[How these 2 articles work together]

**Citation Format:**
```
[APA 7th format for both articles]
```

**Research Notes:**
- **Alternatives Considered:** [List 2-3 other candidates and why not selected]
- **Coverage Gaps:** [Any gaps or "None - complete coverage"]
- **Vietnamese Context:** [Any Vietnam-specific examples found or "To be developed in content"]

---END RESEARCH OUTPUT---
```

### Required Fields

Every research output MUST include:

**For the Week:**
- [ ] Week number
- [ ] Topic name
- [ ] Topics description
- [ ] Key concepts list (3-5 concepts)

**For Each Article (2 required):**
- [ ] Full APA 7th citation
- [ ] URL (verified accessible)
- [ ] PDF link (or "N/A")
- [ ] Type classification
- [ ] Access status
- [ ] Content Match section
- [ ] Checkmark (✓) for EVERY key concept
- [ ] Specific details for each concept
- [ ] "Why Selected" rationale

**Additional Sections:**
- [ ] Complementary Coverage explanation
- [ ] Citation Format block with both articles
- [ ] Research Notes with alternatives and gaps

---

## Import Process

### What Happens During Import

**Step 1: Format Validation**

Claude Code checks:
```
✓ START/END markers present?
✓ All required sections included?
✓ Proper markdown formatting?
✓ Week number matches (if specified)?
```

**Step 2: Content Validation**

Claude Code checks:
```
✓ Full APA citations provided?
✓ URLs formatted correctly?
✓ All key concepts have checkmarks (✓)?
✓ Specific details provided (not just "covered")?
✓ "Why Selected" rationales present?
```

**Step 3: Quality Validation**

Claude Code warns (but doesn't fail) if:
```
⚠ Article older than 2020 (unless seminal)
⚠ Only one article type (prefer theory + applied mix)
⚠ Coverage gaps noted in research notes
```

**Step 4: Accessibility Validation**

Claude Code tests:
```
⚠ URLs return 200 status?
⚠ Check access type:
  - Open access: EXCELLENT
  - Paywalled seminal (1000+ citations, top-tier journal, foundational): ACCEPTABLE if content validated
  - Paywalled non-seminal: REJECT
⚠ For paywalled: Verify high-quality seminal work with validated content
```

**Step 5: Save**

If all validations pass (or warnings accepted):
```
✓ Save to courses/[COURSE-CODE]/.working/research/article-research-summary.md
✓ Append to existing file if other weeks already present
✓ Create import log entry
✓ Confirm ready for content generation
```

### Validation Outcomes

**PASS - All validations successful**
```
✓ Format validation passed
✓ Content validation passed (4/4 concepts covered)
✓ Quality validation passed
✓ Accessibility verified

Week 5 research imported successfully!
Ready for: /generate-week 5
```

**WARNINGS - Minor issues detected**
```
✓ Format validation passed
✓ Content validation passed
⚠ Quality warnings:
  - Article 1 published 2015 (prefer 2020+)
  - Both articles from same source type

Continue anyway? (yes/no/replace)
```

**FAIL - Critical issues found**
```
✗ Validation failed: Missing required fields

Missing from Article 1:
- Content Match for Concept 3
- "Why Selected" rationale

Please provide complete research or fix these issues.
```

### Override Options

For warnings (not errors), you can override:

```
⚠ Warning: Article 1 is from 2015 (prefer 2020+)
Continue anyway? (yes/no/replace)

> yes
Justification: Seminal work by Cialdini, highly cited (10,000+ citations), foundational theory still current

✓ Override accepted with justification
✓ Continuing import...
```

---

## Validation & Quality Control

### Strict Requirements (Must Pass)

These will cause import to **fail**:

1. **Format Issues:**
   - Missing START/END markers
   - Missing required sections
   - Incomplete article information

2. **Content Issues:**
   - Missing checkmarks (✓) for any concept
   - Missing URL for any article
   - Missing APA citation
   - No "Why Selected" rationale

3. **Coverage Issues:**
   - Any required concept not addressed
   - Less than 2 articles provided
   - No specific details in Content Match

### Warning Level (Can Override)

These will generate **warnings** but allow override:

1. **Quality Concerns:**
   - Article published before 2020
   - Both articles same type (no theory/applied mix)
   - Single-source research (both HBR, or both peer-reviewed)

2. **Accessibility Concerns:**
   - URL returns non-200 status (timeout, redirect, etc.)
   - Cannot verify accessibility due to network error
   - Unknown access status

3. **Completeness Concerns:**
   - Research notes incomplete
   - No alternatives documented
   - Vietnamese context not addressed

### Best Practices for Quality

**In Claude Desktop Research:**

1. **Be thorough in Stage 3 (content validation)**
   - Don't accept "mentioned" level coverage
   - Require "explained" or "in-depth" for each concept
   - Document specific page/section numbers

2. **Document your decision-making**
   - Why you selected each article
   - Why you rejected strong alternatives
   - How the 2 articles complement each other

3. **Test accessibility**
   - Open URLs in incognito/private browser
   - Verify PDF links work
   - **Open access preferred** - Always prioritize freely available articles
   - **Paywalls OK if seminal:**
     - 1000+ citations (established) or 100+ (recent)
     - Top-tier journal (A*/A ranked)
     - Foundational/field-defining work
     - Full content validated via abstracts/previews/cached versions
   - **Reject low-quality paywalled articles**
   - Note institutional access (students can access via university library)

**In Claude Code Import:**

1. **Review validation output carefully**
   - Don't blindly override warnings
   - Understand what's being flagged
   - Provide thoughtful justifications

2. **Verify alignment with course**
   - Do concepts match learning objectives?
   - Are articles appropriate for student level?
   - Is Vietnamese context considered?

3. **Check cross-references**
   - If importing multiple weeks, check for redundancy
   - Ensure weeks build on each other
   - Verify topic progression makes sense

---

## Troubleshooting

### Problem: "Format validation failed - Missing START marker"

**Cause:** Research output not copied correctly

**Solution:**
1. Go back to Claude Desktop conversation
2. Find the formatted output
3. Copy EVERYTHING including `---START RESEARCH OUTPUT---`
4. Make sure you copied `---END RESEARCH OUTPUT---` too
5. Try import again

### Problem: "Content validation failed - Concept 3 missing checkmark"

**Cause:** Article doesn't cover all required concepts, or formatting issue

**Solution:**
1. Review Article 1 and Article 2 Content Match sections
2. Every concept in "Key Concepts Required" must appear with ✓ in BOTH articles
3. If concept truly missing: Return to Claude Desktop to find better article
4. If just formatting: Add the missing `✓ Concept 3: [details]` line

### Problem: "Accessibility validation warning - Article appears paywalled"

**Cause:** URL returns 403 Forbidden or "subscription required" detected

**Solution:**
```
Option 1: Verify if seminal work (AUTO-ACCEPT if criteria met)
- Check citations: 1000+ (established) or 100+ (recent)?
- Check journal: Top-tier (A*/A ranked, field-defining)?
- Check foundational status: Is this a paradigm-shifting work?
- Verify content validation: Can validate all concepts via abstract/preview/cached?
- If YES to all → Article is acceptable (students have institutional access)

Option 2: Find open access alternative (PREFERRED for non-seminal)
- Search for author preprint on ResearchGate
- Check Google Scholar for open version
- Look for institutional repository copy
- Find different but equally good open access article

Option 3: Replace with better article
- Go back to Claude Desktop
- Request higher-quality open access article
- Or request different seminal work
- Re-import with new article
```

### Problem: "Week 5 research already exists - Overwrite?"

**Cause:** You previously imported or researched Week 5

**Solution:**
```
Options presented:
1. Overwrite with new research (replaces existing)
2. Merge with existing (3 articles total for week)
3. Cancel import (keep existing)

Choose based on:
- Is new research better quality? → Overwrite
- Do both have value? → Merge
- Was this a mistake? → Cancel
```

### Problem: "Cannot find course directory"

**Cause:** Course hasn't been created yet

**Solution:**
```bash
# First create the course structure
/new-course BCI2AU Business Communication

# Then import research
/import-research BCI2AU 5
```

### Problem: "APA citation format incorrect"

**Cause:** Citation doesn't follow APA 7th format

**Solution:**
Review APA 7th format requirements:

**Journal article:**
```
Author, A. A., & Author, B. B. (Year). Title of article. Title of Journal, volume(issue), pages. https://doi.org/xxxxx
```

**HBR article:**
```
Author, A. A. (Year, Month). Title of article. Harvard Business Review. https://hbr.org/year/month/article-slug
```

**Report:**
```
Organization. (Year). Title of report. Publisher. https://www.example.com/report
```

### Problem: "Batch import stopped at Week 3"

**Cause:** Validation error in Week 3, or interrupted process

**Solution:**
```
1. Check what was imported successfully:
   Read: courses/[COURSE]/. working/research/article-research-summary.md

2. Fix Week 3 research if validation failed

3. Continue batch import for remaining weeks:
   /import-research [COURSE] all
   [Paste only Week 4-10 research]
```

---

## Examples

### Example 1: Single Week Import

**Research in Claude Desktop:**

```
User: [Pastes template with Week 5 Persuasive Communication topic]

Claude Desktop: [Performs 4-stage research over 35 minutes]

Claude Desktop: Here are 3 finalists:

Option A: Cialdini, R. (2021). Harnessing the science of persuasion...
[Shows content match analysis]

Option B: Petty, R. & Cacioppo, J. (2018). The Elaboration Likelihood Model...
[Shows content match analysis]

Option C: Harvard Business Review (2023). The New Rules of Persuasion...
[Shows content match analysis]

User: I'll take Option A (Cialdini) and Option B (Petty & Cacioppo)

Claude Desktop: [Generates formatted output]

---START RESEARCH OUTPUT---
[Complete research with both articles, content match, etc.]
---END RESEARCH OUTPUT---

User: [Copies output]
```

**Import into Claude Code:**

```
User: /import-research BCI2AU 5

Claude Code: Importing research for Week 5 of BCI2AU...
Claude Code: Please provide research output from Claude Desktop:

User: [Pastes the research output]

Claude Code: Validating research...
Claude Code: ✓ Format validation passed
Claude Code: ✓ Content validation passed (4/4 concepts)
Claude Code: ✓ Quality validation passed
Claude Code: ✓ Accessibility verified for both articles
Claude Code:
Claude Code: Imported successfully:
Claude Code: Topic: Persuasive Communication
Claude Code: Articles: 2
Claude Code:   1. Cialdini (2021) - HBR
Claude Code:   2. Petty & Cacioppo (2018) - Journal article
Claude Code: Concepts covered: 4/4
Claude Code:
Claude Code: Saved to: courses/BCI2AU/.working/research/article-research-summary.md
Claude Code: Ready for: /generate-week 5
```

### Example 2: Batch Import During Syllabus Generation

**Research in Claude Desktop:**

```
[Research Week 1 - outputs formatted result]
[Research Week 2 - outputs formatted result]
...
[Research Week 10 - outputs formatted result]

[User combines all 10 weeks into one file: all-weeks-research.md]
```

**Import during syllabus:**

```
User: /generate-syllabus

[Claude Code completes Steps 1-3: Course basics, objectives, assessments]

Claude Code: Step 4A: Check for Existing Research
Claude Code: Do you have pre-researched articles from Claude Desktop for any weeks?

User: Yes, I have all 10 weeks researched. File: ~/Desktop/all-weeks-research.md

Claude Code: Reading file...
Claude Code: Found research for weeks: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

Claude Code: Validating Week 1... ✓
Claude Code: Validating Week 2... ✓
Claude Code: Validating Week 3... ✓
Claude Code: Validating Week 4... ⚠ Warning: Article 2 from 2017
Claude Code: Continue with Week 4? (yes/no/replace)

User: yes - This is a seminal work, highly cited

Claude Code: ✓ Override accepted
Claude Code: Validating Week 5... ✓
[Continues through Week 10]

Claude Code: ✓ All 10 weeks imported successfully!
Claude Code: Skipping research step - using imported articles
Claude Code: Proceeding to Step 4B: Build course calendar...
```

### Example 3: Partial Import (Mixed Research Sources)

**Scenario:** You researched Weeks 1, 5, and 10 in Desktop, but want Claude Code to research the rest.

```
User: /generate-syllabus

[Complete Steps 1-3]

Claude Code: Step 4A: Do you have pre-researched articles?

User: Yes, for weeks 1, 5, and 10 only. Here's the research:

---START RESEARCH OUTPUT---

## Week 1: Introduction to Business Communication
[Full research for Week 1]

## Week 5: Persuasive Communication
[Full research for Week 5]

## Week 10: Presentations and Public Speaking
[Full research for Week 10]

---END RESEARCH OUTPUT---

Claude Code: ✓ Imported weeks 1, 5, 10
Claude Code: I'll research the remaining weeks: 2, 3, 4, 6, 7, 8, 9
Claude Code:
Claude Code: Step 4B: Present weekly outline...
[Shows all 10 weeks]
Claude Code:
Claude Code: Step 4C: Research Week 2...
[Performs 4-stage research for Week 2]
[Continues for remaining weeks]
```

---

## FAQs

### General Questions

**Q: Is manual handoff worth the extra effort?**

A: It depends on your priorities:
- **Worth it:** If you need top-tier quality, have access to Claude Desktop, and value complete control
- **Not worth it:** If Claude Code's research is good enough and you prefer full automation

**Time cost:** ~5-10 minutes per week overhead
**Quality benefit:** Potentially significant, especially for complex topics

**Q: Can I mix approaches (some weeks Desktop, some weeks Code)?**

A: Yes! This is actually a great strategy:
- Use Desktop for difficult/complex weeks
- Let Code research straightforward weeks
- Import partial research at Step 4A

**Q: Do I need to use the exact template format?**

A: Yes, for validation to work. The template format ensures:
- All required information captured
- Consistent quality across weeks
- Automatic validation possible
- Integration with content generation

**Q: Can I edit research after importing?**

A: Yes, you can edit `.working/research/article-research-summary.md` directly. Just maintain the format.

### Research Process Questions

**Q: What if Claude Desktop can't find articles covering all concepts?**

A: Several options:
1. **Broaden search** - Try alternative keywords, older date range
2. **Use 3 articles** - Ask user if 3 articles acceptable for this week
3. **Adjust concepts** - Ask user if concept list can be refined
4. **Supplementary source** - Add a 3rd article for missing concepts

**Q: What if all good articles are paywalled?**

A: Paywalls are now acceptable for seminal works! Strategies:
1. **Accept seminal paywalled articles** - If criteria met:
   - 1000+ citations (established) or 100+ (recent)
   - Top-tier journal (A*/A ranked)
   - Foundational/field-defining work
   - Full content validated via abstracts/previews/cached
   - Students have institutional access via university library
2. **Search for open access alternatives** (preferred for non-seminal):
   - ResearchGate, author websites, SSRN for preprints
   - Google Scholar "All versions" for open access
   - Institutional repositories
3. **Reject low-quality paywalled articles** - Mid-tier journals, incremental research

**Q: How strict is the "all concepts covered" requirement?**

A: Very strict by default:
- **Preferred:** Each article covers all concepts
- **Acceptable:** Combined coverage across 2 articles (all concepts present)
- **Rejected:** Any concept missing entirely

You can override with justification, but maintain quality.

**Q: Can I import research from sources other than Claude Desktop?**

A: Yes! As long as it follows the required format:
- Manual research (you did it yourself)
- Another AI tool (formatted to match template)
- Collaborative research (team member researched)
- Previous course (re-using vetted articles)

### Technical Questions

**Q: Where is imported research stored?**

A: Primary location: `courses/[COURSE-CODE]/.working/research/article-research-summary.md`

This file contains all weeks' research, formatted as:
```
## Week 1: [Topic]
[Research output]

## Week 2: [Topic]
[Research output]
...
```

**Q: What if I accidentally import wrong week number?**

A: You can fix it:
1. Edit `.working/research/article-research-summary.md`
2. Change the week number
3. Or re-import with correct week number (choose "overwrite")

**Q: Can I import research before creating the course?**

A: No, course structure must exist first:
```bash
# First
/new-course BCI2AU Business Communication

# Then
/import-research BCI2AU 5
```

**Q: Does imported research expire or need updating?**

A: No expiration, but best practices:
- Review quarterly (links can break)
- Update annually (newer articles may emerge)
- Check before each course run (accessibility can change)

### Integration Questions

**Q: How does /generate-week use imported research?**

A: Automatically:
1. Reads syllabus for week topic
2. Finds week in `.working/research/article-research-summary.md`
3. Uses Content Match analysis for precise citations
4. References specific article sections in speaker notes
5. Generates tutorial aligned with article concepts

**Q: Can I use imported research with /research-topic command?**

A: Not directly - `/research-topic` performs new research. But you can:
- Use template to research in Desktop
- Save output for future import
- Import later during `/generate-syllabus`

**Q: What if I import research but then change the topic?**

A: You'll need to:
1. Delete or archive old research for that week
2. Research new topic (Desktop or Code)
3. Re-import or let Code research fresh

**Q: Does import work with both syllabus structures (single vs. two-doc)?**

A: Yes, imported research works with both:
- **Single-doc:** Articles listed in course calendar
- **Two-doc:** Articles in syllabus, referenced in handbook

---

## Summary

### Key Takeaways

1. **Manual handoff bridges the gap** between Claude Desktop's superior research and Claude Code's content generation

2. **Time investment is minimal** (~5-10 min per week overhead) for potentially significant quality improvement

3. **Validation ensures quality** - Strict format and content checks maintain standards

4. **Flexibility is built-in** - Use for all weeks, some weeks, or none (your choice)

5. **Template is essential** - Follow `.claude/templates/research-output-format.md` exactly

### Getting Started Checklist

- [ ] Read `.claude/templates/research-output-format.md`
- [ ] Understand the 4-stage research process
- [ ] Try researching one week in Claude Desktop
- [ ] Practice importing into Claude Code
- [ ] Verify validation works correctly
- [ ] Generate content using imported research
- [ ] Decide if handoff workflow suits your needs

### Support Resources

- **Research template:** `.claude/templates/research-output-format.md`
- **Import command:** `.claude/commands/import-research.md`
- **Syllabus workflow:** `.claude/commands/generate-syllabus.md`
- **Main documentation:** `.claude/CLAUDE.md`
- **Architecture:** `docs/ARCHITECTURE.md`
- **All documentation:** `docs/INDEX.md`

---

*This manual handoff workflow allows you to leverage the best of both worlds: Claude Desktop's superior research capabilities combined with Claude Code's powerful content generation and file management.*
