# Troubleshooting Guide

Common issues and solutions for the Class Content Generator.

---

## Research Issues

### "Can't find articles covering all concepts"

**Solutions:**
1. Search each concept individually (not combined)
2. Look for review articles or meta-analyses
3. Consider 3 articles instead of 2 (ask user)
4. Try broader search terms, then validate specific concepts

### "All good articles are paywalled"

**Solutions:**
1. Check author's ResearchGate/preprint
2. Use practitioner sources (HBR, MIT Sloan Review)
3. Accept seminal paywalled works (1000+ citations) with confidence in content
4. Search for working paper versions on SSRN

### "Research validation failed"

**Cause:** Research file doesn't meet format or quality requirements.

**Solutions:**
1. Check research file has 4 articles (2 seminal + 2 recent)
2. Verify all concepts have ✓ checkmarks
3. Ensure Key Teaching Content is present for each article
4. Re-run `/import-research [CODE] [N]` to see specific errors

---

## Content Generation Issues

### "Tutorial doesn't align with assessment"

**Solutions:**
1. Verify `assessment-schedule.md` is current
2. Check simplified rubric in tutorial matches full rubric in handbook
3. Confirm tutorial activity practices skills from the rubric
4. Re-read `assessment-handbook.md` before generating

### "Lecture too long (>30 slides)"

**Solutions:**
1. Split complex concepts across multiple slides
2. Remove redundant content
3. Combine related points into single slides
4. Focus on 3-4 key concepts per lecture segment

### "Speaker notes repeat slide content"

**Solutions:**
1. Notes should add context, not repeat
2. Include: timing, misconceptions, cultural tips, transitions
3. Avoid prescriptive actions ("walk around," "point to")
4. See `content-generation/speaker-notes.md` for structure

---

## Export Issues

### "DOCX export fails"

**Solutions:**
1. Check `venv` is activated: `source venv/bin/activate`
2. Verify `course-info.md` exists (for footer data)
3. Check file paths in command match actual structure
4. Run: `python3 tools/markdown_to_docx.py [CODE] [N]`

### "GIFT format errors on Moodle import"

**Solutions:**
1. Check for unescaped special characters (`:`, `{`, `}`, `~`, `=`, `#`)
2. Verify each question has title: `::Title::`
3. Ensure feedback is properly formatted
4. Test import with single question first

### "Speaker notes not appearing in PPTX"

**Solutions:**
1. Run `/add-speaker-notes [CODE] [N]` after Gemini PPTX is downloaded
2. Check `lecture-content.md` has `<speaker-notes>` sections
3. Verify slide count matches between content and PPTX
4. Check output in `output/slides.pptx`

---

## Workflow Issues

### "No course directory found"

**Solutions:**
1. Run `/new-course [CODE] [Name]` first
2. Check course code matches exactly (case-sensitive)
3. Verify directory exists: `courses/[CODE]-[name]/`

### "Research file not found"

**Expected path:** `courses/[CODE]/.working/research/week-N-research.md`

**Solutions:**
1. Run `/import-research [CODE] [N]` to create/validate
2. Check `.week-N-ready` flag exists (Desktop auto-import)
3. Manually create file using research template

### "Syllabus missing required information"

**Solutions:**
1. Ensure weekly topics include key concepts (3-5 per week)
2. Add assessment schedule with due dates
3. Include learning objectives per week
4. Run `/generate-syllabus` if starting fresh

---

## MCP/Desktop Issues

### "MCP auto-write not working"

**Solutions:**
1. Verify MCP Filesystem Server installed in Claude Desktop
2. Check `.claude/mcp-config/desktop-commander-research.json` exists
3. Confirm write access to `courses/` directory
4. Fall back to manual paste method

### "Desktop research doesn't validate"

**Solutions:**
1. Use template: `.claude/templates/desktop-course-research-template.md`
2. Ensure 4 articles per week (2 seminal + 2 recent)
3. Include Key Teaching Content for each article
4. Verify all concepts have explicit checkmarks (✓)

---

## Quick Checks

| Issue | First Thing to Check |
|-------|---------------------|
| Missing files | Course directory exists? |
| Validation fails | Research has 4 articles? |
| Wrong output | Pre-flight step completed? |
| Export fails | Virtual environment activated? |
| Alignment issues | Assessment handbook read? |

---

**For technical issues with HTML/PPTX converter:** See `docs/ARCHITECTURE.md`

**For research workflow details:** See `docs/RESEARCH-HANDOFF-GUIDE.md`
