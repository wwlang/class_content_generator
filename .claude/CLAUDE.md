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
2. /generate-syllabus              (2-3 hrs with existing research)
3. /generate-handbook [CODE]       (1-2 hrs - BEFORE weekly content)
4. /generate-course [CODE]         (7-12 hrs batch)
   OR /generate-week [N]           (45-70 min each)
5. /validate-content [CODE]        (5-10 min - AI quality checks)
6. /enhance-coherence [CODE]       (15-30 min polish)
7. /gemini-handoff [CODE] [N]      (generates prompt → paste into Gemini)
8. /add-speaker-notes [CODE] [N]   (merge speaker notes into Gemini PPTX)
9. /export-docx [CODE] [N]
```

**Why this order:**
- Syllabus provides course structure, assessment overview, and framework schedule
- Assessment Handbook uses syllabus frameworks to create scenarios and rubrics
- Tutorials reference Assessment Handbook scenarios and rubric criteria
- Weekly content can now align with specific assessment requirements
- **Validation catches issues BEFORE polishing** - fix critical problems first
- Gemini creates visual slides from lecture-content.md; Claude adds speaker notes back

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

## Coding Standards

- SOLID principles, PEP 8, type hints required
- Max 500 lines/file, 50 lines/function
- 80%+ test coverage
- Use Context7 (`mcp__context7__resolve-library-id` → `mcp__context7__get-library-docs`) for library APIs
