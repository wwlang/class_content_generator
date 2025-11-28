# Assessment Automation System

Automated tools for quiz bank consolidation and assessment brief generation using clean architecture principles.

## Overview

This system automates two key assessment workflows:

1. **Quiz Bank Consolidation**: Select the best questions from multiple weeks, balance Bloom's taxonomy distribution, and export to Moodle GIFT format
2. **Assessment Brief Generation**: Convert assessment handbook markdown to professional PDF briefs with rubrics

## Architecture

```
tools/assessment_domain/
├── models/              # Domain models (Question, QuizBank, Assessment, Rubric)
├── repositories/        # Data access layer (file loading, caching)
├── services/           # Business logic (consolidation algorithm)
├── parsers/            # Markdown parsing (quiz-questions.md, handbook.md)
└── exporters/          # Export formats (GIFT, PDF)

tools/assessment_cli.py  # Command-line interface
```

### Design Principles

- **Clean Architecture**: Clear separation of concerns across layers
- **Domain-Driven Design**: Rich domain models with business logic
- **Repository Pattern**: Abstract file system access
- **Service Layer**: Encapsulate complex business operations

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Or in virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Dependencies

- **Core**: python-pptx, python-docx, lxml, pillow
- **Testing**: pytest, pytest-cov
- **PDF Export**: weasyprint>=60.0 (optional, falls back to HTML)

## Usage

### Command-Line Interface

#### List Questions

```bash
python3 tools/assessment_cli.py list-questions BCI2AU --weeks 1 2 3
```

Output:
- Total questions available
- Bloom's distribution (Remembering/Understanding)
- Week distribution
- Quality metrics

#### List Assessments

```bash
python3 tools/assessment_cli.py list-assessments BCI2AU
```

Output:
- All assessments with metadata
- Types, weights, due dates
- Rubric and scenario availability

#### Consolidate Quiz

```bash
# With preview
python3 tools/assessment_cli.py consolidate BCI2AU quiz-1 \
  --weeks 1 2 3 \
  --target-total 30 \
  --target-remembering 15 \
  --target-understanding 15 \
  --preview

# Direct export to GIFT
python3 tools/assessment_cli.py consolidate BCI2AU quiz-1 \
  --weeks 1 2 3 \
  --export-gift \
  --output courses/BCI2AU-business-communication/assessments/quiz-1.gift \
  --yes
```

Features:
- Quality-based question selection
- Automatic Bloom's balancing
- Week distribution analysis
- Preview before committing
- Direct GIFT export

#### Export to GIFT

```bash
python3 tools/assessment_cli.py export-gift BCI2AU quiz-1 \
  --weeks 1 2 3 \
  --output quiz-1.gift \
  --category "Quiz 1 - Weeks 1-3"
```

GIFT format features:
- Per-option feedback
- Moodle category organization
- Metadata headers
- Special character escaping

#### Generate Assessment Brief

```bash
# PDF (requires WeasyPrint)
python3 tools/assessment_cli.py brief BCI2AU persuasive-proposal \
  --output proposal-brief.pdf

# HTML (fallback or preview)
python3 tools/assessment_cli.py brief BCI2AU persuasive-proposal \
  --format html \
  --output proposal-brief.html
```

Brief includes:
- Assessment metadata (weight, due date)
- Task overview
- Scenario options
- Requirements checklist
- Full rubric table
- Professional styling

### Claude Code Slash Commands

#### `/consolidate-quiz`

Interactive workflow for quiz consolidation:
1. Prompts for course, quiz ID, weeks
2. Shows preview of available questions
3. Runs consolidation with quality scoring
4. Exports to GIFT format
5. Reports results and warnings

#### `/generate-brief`

Generate assessment brief:
1. Lists available assessments
2. Prompts for assessment ID and format
3. Generates PDF or HTML brief
4. Reports output location

## Programmatic API

### Basic Example

```python
from tools.assessment_domain import (
    QuestionRepository,
    QuizConsolidationService,
    GIFTExporter
)

# Initialize
repo = QuestionRepository()
service = QuizConsolidationService(repo)

# Consolidate quiz
result = service.consolidate_quiz(
    course_code="BCI2AU",
    quiz_id="quiz-1",
    weeks=[1, 2, 3],
    target_total=30,
    target_remembering=15,
    target_understanding=15
)

# Export to GIFT
if result.success:
    exporter = GIFTExporter()
    exporter.export_to_file(
        result.quiz_bank,
        "output/quiz-1.gift"
    )
```

### Preview Before Consolidation

```python
# Check what's available first
preview = service.preview_consolidation(
    "BCI2AU",
    weeks=[1, 2, 3],
    target_total=30
)

print(f"Available: {preview['available']}")
print(f"Can consolidate: {preview['can_consolidate']}")
print(f"Remembering: {preview['remembering']}")
print(f"Understanding: {preview['understanding']}")
```

### Assessment Brief Generation

```python
from tools.assessment_domain import (
    AssessmentRepository,
    PDFExporter
)

# Load assessment
repo = AssessmentRepository()
assessment = repo.get_assessment("BCI2AU", "persuasive-proposal")

# Export to PDF
exporter = PDFExporter()
exporter.export_to_pdf(
    assessment,
    "output/proposal-brief.pdf",
    course_code="BCI2AU"
)
```

## Quality Rules

### Question Validation

All questions must pass:
1. Exactly 4 options (A-D)
2. One clearly correct answer
3. Feedback for all options
4. No "all/none of the above"
5. No double negatives
6. Substantive content (≥10 chars)
7. Valid week number (1-10)
8. Proper ID format: `W[week]-Q[number]-[topic]`

### Bloom's Taxonomy

- **Remembering**: Recall facts, definitions, concepts
  - Keywords: "what is", "define", "list", "identify"
- **Understanding**: Explain ideas, interpret meaning
  - Keywords: "why", "how", "explain", "compare"
  - Scenario-based questions preferred

### Quality Scoring

Questions ranked by:
- **Base score**: 10 points
- **Scenario-based**: +2 (tests application)
- **Detailed feedback**: +2 (≥30 chars per option)
- **Valid**: +2 (passes all validation rules)

## File Formats

### Input: quiz-questions.md

```markdown
**Topic:** Week Topic
**Prepares for:** Quiz 1

### Q1: Topic Name
**Type:** Multiple Choice

Question text here?

A) Option A
B) Option B
C) Option C
D) Option D

**Answer:** C
**Feedback:** Explanation with details for all options.

---
```

### Input: assessment-handbook.md

```markdown
## Assessment Overview

| Assessment | Type | Weight | Due Week | Learning Objectives |
|-----------|------|--------|----------|-------------------|
| Email + Memo | Portfolio | 10% | Week 3 | 1, 2, 9, 12 |

### 1. Email + Memo (10%)

#### Overview
Task description...

#### Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Rubrics

### Written Communication Rubric

| Criteria | Excellent | Good | Satisfactory | Poor | Failing |
|----------|-----------|------|--------------|------|---------|
| Content | ... | ... | ... | ... | ... |
```

### Output: GIFT Format

```
// Quiz 1 - Weeks 1-3
// Questions: 30
// Bloom distribution: 15 Remembering, 15 Understanding

$CATEGORY: Quiz 1 - Weeks 1-3

::Topic Name::Question text?{
=Correct option #Explanation why correct
~Wrong option #Explanation why wrong
~Wrong option #Explanation why wrong
~Wrong option #Explanation why wrong
}
```

## Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=tools/assessment_domain --cov-report=html

# Specific test file
pytest tests/test_question_model.py -v
```

## Troubleshooting

### "Not enough questions to consolidate"

**Problem**: Insufficient questions for target distribution.

**Solutions**:
1. Reduce target totals: `--target-total 20`
2. Adjust Bloom distribution: `--target-remembering 13 --target-understanding 7`
3. Add more weeks: `--weeks 1 2 3 4`
4. Generate more questions per week (15-20 recommended)

### "WeasyPrint not installed"

**Problem**: PDF export fails.

**Solutions**:
1. Install: `pip install weasyprint>=60.0`
2. Use HTML format: `--format html`
3. Convert HTML to PDF with browser print function

### "Question validation errors"

**Problem**: Questions fail quality rules.

**Solutions**:
1. Check for "all/none of the above" phrases
2. Ensure all 4 options present (A-D)
3. Verify feedback for each option
4. Fix double negatives
5. Use `list-questions` to see specific errors

## Performance

- **Caching**: Repositories cache parsed questions/assessments
- **Batch loading**: Load multiple weeks efficiently
- **Quality sorting**: O(n log n) for question ranking
- **File I/O**: Minimal with smart caching

Clear cache when updating source files:
```python
repo.clear_cache("BCI2AU")
```

## Future Enhancements

- [ ] Web interface for manual question selection
- [ ] Bulk operations across multiple courses
- [ ] Question difficulty analysis
- [ ] Quiz preview with answer key
- [ ] Integration with LMS APIs
- [ ] Automated question generation suggestions
- [ ] Historical quality tracking

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for:
- Code style guidelines (PEP 8)
- Testing requirements (80%+ coverage)
- SOLID principles
- Max file size (500 lines)
- Type hints required

## Support

- **Issues**: GitHub issues
- **Documentation**: `docs/` directory
- **Examples**: `courses/BCI2AU-business-communication/`

## License

Part of the Class Content Generator project.
