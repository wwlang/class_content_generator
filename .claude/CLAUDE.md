# Class Content Generator

Generate world-class university course content with research validation and assessment alignment.

## Quick Reference

| Task | Command |
|------|---------|
| Create course | `/new-course [CODE] [Name]` |
| Build syllabus | `/generate-syllabus` |
| Generate week | `/generate-week [N]` |
| Batch generate | `/generate-course [CODE]` |
| Assessment handbook | `/generate-handbook [CODE]` |
| Validate quality | `/validate-content [CODE]` |
| Gemini prompt | `/gemini-handoff [CODE] [N]` |
| Add speaker notes | `/add-speaker-notes [CODE] [N]` |
| Export DOCX | `/export-docx [CODE] [N]` |
| Research articles | `/research-topic "[Topic]" "[Concepts]"` |
| Validate XML slides | `python tools/validate_lecture_xml.py [CODE]` |
| Normalize headers | `python tools/normalize_lecture_headers.py [CODE]` |
| Renumber slides | `python tools/renumber_slides.py [CODE] [N]` |

**Skills** (loaded automatically): `content-generation/`, `assessment-design/`, `research/`

## Core Principles

1. **Syllabus-First** - Complete syllabus before weekly content
2. **Assessment Alignment** - Every tutorial prepares for graded work
3. **Research-Backed** - Top schools (M7, UK Triple Crown), peer-reviewed sources
4. **Strict Validation** - All concepts must be covered (no partial matches)
5. **Quality Over Speed** - Better to find perfect articles than settle

## Workflow

```
1. /new-course [CODE] [Name]
2. /generate-syllabus
3. /generate-handbook [CODE]       (BEFORE weekly content)
4. /generate-course [CODE]
   OR /generate-week [N]
5. /validate-content [CODE]
6. /enhance-coherence [CODE]
7. /gemini-handoff [CODE] [N]      (generates prompt → paste into Gemini)
8. /add-speaker-notes [CODE] [N]   (merge speaker notes into Gemini PPTX)
9. Create exam revision guide      (assessments/final-exam-revision.md)
10. /package-course [CODE]         (converts all markdown → DOCX, creates ZIP)
```

**Why this order:**
- Syllabus provides course structure, assessment overview, and framework schedule
- Assessment Handbook uses syllabus frameworks to create scenarios and rubrics
- Tutorials reference Assessment Handbook scenarios and rubric criteria
- Weekly content can now align with specific assessment requirements
- **Validation catches issues BEFORE polishing** - fix critical problems first
- Gemini creates visual slides from lecture-content.md; Claude adds speaker notes back
- Exam revision guide helps students prepare using weekly quizzes and slides

## Documentation

| Topic | Location |
|-------|----------|
| All docs index | `docs/INDEX.md` |
| System architecture | `docs/ARCHITECTURE.md` |
| Layout vocabulary | `docs/LAYOUT-VOCABULARY.md` |
| Research handoff | `docs/RESEARCH-HANDOFF-GUIDE.md` |
| Troubleshooting | `docs/TROUBLESHOOTING.md` |
| Writing skills/prompts | `.claude/skills/writing-instructions.md` |
| LLM prompting guidelines | `.claude/skills/self-prompting-instructions.md` |

## Project-Specific Standards

- 80%+ test coverage for Python tools
