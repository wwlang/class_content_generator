# Class Content Generator

Generate world-class university course content with research validation and assessment alignment.

## Quick Reference

| Task | Command |
|------|---------|
| Create course | `/new-course [CODE] [Name]` |
| Build syllabus | `/generate-syllabus` |
| Generate week | `/generate-week [N]` |
| Batch generate | `/generate-course [CODE]` |
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
2. /generate-syllabus              (7-10 hrs with Desktop research)
3. /generate-course [CODE]         (7-12 hrs batch)
   OR /generate-week [N]           (45-70 min each)
4. /add-speaker-notes [CODE] [N]   (after Gemini PPTX)
5. /export-docx [CODE] [N]
6. /enhance-coherence [CODE]       (15-30 min polish)
```

## Documentation

| Topic | Location |
|-------|----------|
| All docs index | `docs/INDEX.md` |
| System architecture | `docs/ARCHITECTURE.md` |
| Layout vocabulary | `docs/LAYOUT-VOCABULARY.md` |
| Research handoff | `docs/RESEARCH-HANDOFF-GUIDE.md` |
| Troubleshooting | `docs/TROUBLESHOOTING.md` |
| Writing skills/prompts | `.claude/skills/writing-instructions.md` |

## Coding Standards

- SOLID principles, PEP 8, type hints required
- Max 500 lines/file, 50 lines/function
- 80%+ test coverage
- Use Context7 (`mcp__context7__resolve-library-id` → `mcp__context7__get-library-docs`) for library APIs
