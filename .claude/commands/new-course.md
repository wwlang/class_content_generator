# /new-course [CODE] [Name]

Create course directory structure with templates.

## Usage

```
/new-course BCI2AU Business Communication
```

## What It Creates 🔒

```
courses/BCI2AU-business-communication/
├── syllabus.md (placeholder)
├── course-info.md (metadata template)
├── rubrics/
│   ├── written-work-rubric.md
│   ├── presentation-rubric.md
│   └── project-rubric.md
├── weeks/
│   └── week-01/ through week-N/
│       ├── lecture-content.md (placeholder)
│       ├── tutorial-content.md (placeholder)
│       └── slides.md (placeholder)
├── assessments/
│   └── assessment-schedule.md (template)
└── resources/
    ├── case-studies/
    └── examples/
```

## Process

1. **Gather:** Course code, name, number of weeks
2. **Create:** Directory structure with mkdir
3. **Copy:** Rubric templates from `templates/syllabus-components/rubric-structures/`
4. **Generate:** course-info.md with metadata and tracking table
5. **Confirm:** Show created structure and next steps

## Inputs

| Input | Example | Notes |
|-------|---------|-------|
| Course code | BCI2AU | Uppercase, no spaces |
| Course name | Business Communication | Title case |
| Number of weeks | 11 | Typically 10-12 |

## Time

2-3 minutes

## Example Output

```
✓ Course structure created!

📁 courses/BCI2AU-business-communication/
   ├── syllabus.md (placeholder)
   ├── course-info.md (tracking)
   ├── rubrics/ (3 templates)
   ├── weeks/ (11 folders)
   ├── assessments/
   └── resources/

Next: /generate-syllabus
```

## If Things Go Wrong

- **Folder exists:** Choose different code, delete existing, or work with existing
- **Invalid code:** Prompt again (must be uppercase, no spaces)
- **Unusual week count:** Confirm if <5 or >15 weeks
