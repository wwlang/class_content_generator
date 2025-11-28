# Question Ambiguity Validation

Automated detection and correction of multiple-choice questions with ambiguous answers.

---

## Overview

The **Question Ambiguity Analyzer** uses Claude to detect when multiple-choice questions have more than one plausible correct answer, then automatically rewords them to ensure only one clearly correct option.

**Problem Solved:** Students may select "wrong" answers that are technically correct, leading to frustration and invalid assessment results.

**Solution:** LLM-based semantic analysis identifies plausible distractors and rewrites questions to eliminate ambiguity.

---

## Quick Start

### Analyze a Week's Questions

```bash
# Analyze all questions from week 1, auto-reword ambiguous ones
python tools/analyze_question_ambiguity.py BCI2AU 1

# Export detailed report
python tools/analyze_question_ambiguity.py BCI2AU 1 --export reports/week-1-ambiguity.md
```

### Manual Review Only (No Auto-Reword)

```bash
# Flag ambiguous questions but don't reword
python tools/analyze_question_ambiguity.py BCI2AU 1 --no-reword
```

### Set Quality Threshold for Manual Review

```bash
# Questions with quality score < 0.8 flagged for review
python tools/analyze_question_ambiguity.py BCI2AU 1 --threshold 0.8
```

---

## How It Works

### 1. **Plausibility Analysis**

For each answer option, Claude evaluates:

- **CLEARLY_CORRECT**: The definitively correct answer
- **PLAUSIBLE**: Could reasonably be considered correct by someone with domain knowledge
- **DEBATABLE**: Reasonable people could disagree
- **CLEARLY_WRONG**: Obviously incorrect

**Example Analysis:**

```
Question: What is a benefit of cloud computing?

A. Scalability              → CLEARLY_CORRECT (primary architectural benefit)
B. Cost reduction           → PLAUSIBLE (also a valid benefit)
C. Flexibility              → PLAUSIBLE (also a key benefit)
D. Increased complexity     → CLEARLY_WRONG (this is a challenge, not a benefit)

Result: AMBIGUOUS (3 plausible options)
```

### 2. **Automatic Rewording**

If multiple plausible answers detected, Claude rewrites the question to make only one answer clearly correct.

**Rewording Strategies:**

1. **Make question more SPECIFIC** - Add qualifying details
2. **Narrow the scope** - Focus on a specific aspect
3. **Add context** - Clarify what type of answer is expected
4. **Reword distractors** - Make wrong options less plausible

**Example Rewrite:**

```
ORIGINAL:
What is a benefit of cloud computing?
A. Scalability ✓
B. Cost reduction (also plausible!)
C. Flexibility (also plausible!)
D. Increased complexity

REWORDED:
What is the PRIMARY architectural benefit of cloud computing that enables automatic resource adjustment based on demand?
A. Scalability and elasticity ✓
B. Lower fixed infrastructure costs (economic, not architectural)
C. Multi-platform deployment options (deployment, not automatic adjustment)
D. Vendor lock-in complexity (challenge, not benefit)

Result: CLEAR (only A is plausible)
```

### 3. **Quality Scoring Integration**

Questions flagged for manual review if:
- Multiple plausible answers detected
- Quality score below threshold (default: 0.7)
- Low feedback detail (<20 chars per option)

---

## Usage Patterns

### Pattern 1: Weekly Content Generation

Analyze questions immediately after generation:

```bash
# Generate week content
/generate-week 1

# Validate question quality
python tools/analyze_question_ambiguity.py BCI2AU 1 --export reports/week-1-validation.md
```

### Pattern 2: Quiz Consolidation Pre-Check

Validate before consolidating into quiz bank:

```bash
# Analyze weeks 1-3
for week in {1..3}; do
    python tools/analyze_question_ambiguity.py BCI2AU $week --threshold 0.8
done

# Then consolidate
python tools/consolidate_quiz.py BCI2AU quiz-1 1 2 3
```

### Pattern 3: Batch Course Audit

Review all questions in existing course:

```bash
# Create audit script
for week in {1..12}; do
    python tools/analyze_question_ambiguity.py BCI2AU $week \
        --no-reword \
        --export reports/week-$week-audit.md
done

# Generate summary
cat reports/week-*-audit.md > reports/full-course-audit.md
```

---

## Programmatic Usage

### Basic Analysis

```python
from tools.assessment_domain.services import QuestionAmbiguityAnalyzer
from tools.assessment_domain.models import Question

# Initialize analyzer (requires ANTHROPIC_API_KEY)
analyzer = QuestionAmbiguityAnalyzer()

# Analyze single question
question = Question(
    id="W1-Q1",
    week=1,
    topic="Cloud Computing",
    question_text="What is a benefit of cloud computing?",
    options={
        'A': 'Scalability',
        'B': 'Cost reduction',
        'C': 'Flexibility',
        'D': 'Increased complexity'
    },
    correct_answer='A',
    # ... feedback, bloom_level, etc.
)

# Get analysis report
report = analyzer.analyze_question(question, context="Intro to Cloud Services")

# Check if ambiguous
if report.is_ambiguous:
    print(f"Ambiguous! Plausible options: {report.plausible_options}")
    print(f"Recommendation: {report.recommendation}")
```

### Analyze and Auto-Reword

```python
# Analyze and get reworded version
report = analyzer.analyze_and_reword(question, context="Cloud Computing")

if report.reworded_question:
    print(f"Original: {question.question_text}")
    print(f"Reworded: {report.reworded_question.question_text}")

    # Use reworded question
    question = report.reworded_question
```

### Batch Analysis

```python
from tools.assessment_domain.repositories import QuestionRepository

# Load questions
repo = QuestionRepository()
questions = repo.get_questions_by_week("BCI2AU", 1)

# Analyze all
reports = analyzer.batch_analyze(
    questions,
    context="Business Communication Week 1",
    reword_ambiguous=True
)

# Generate summary
summary = analyzer.generate_report_summary(reports)
print(summary)

# Get ambiguous questions
ambiguous = [r for r in reports if r.is_ambiguous]
print(f"Found {len(ambiguous)} ambiguous questions")
```

---

## Integration with Existing Workflows

### With Quiz Consolidation

```python
from tools.assessment_domain.services import (
    QuizConsolidationService,
    QuestionAmbiguityAnalyzer
)

# 1. Load and validate questions
analyzer = QuestionAmbiguityAnalyzer()
questions = repo.get_questions_by_week("BCI2AU", 1)

# 2. Analyze for ambiguity
reports = analyzer.batch_analyze(questions, reword_ambiguous=True)

# 3. Use reworded questions
validated_questions = []
for question, report in zip(questions, reports):
    if report.reworded_question:
        validated_questions.append(report.reworded_question)
    else:
        validated_questions.append(question)

# 4. Consolidate validated questions
service = QuizConsolidationService(repo)
result = service.consolidate_quiz(
    course_code="BCI2AU",
    quiz_id="quiz-1",
    weeks=[1, 2, 3],
    target_total=30
)
```

### With Manual Review Workflow

```python
# Flag questions for instructor review
def flag_for_review(questions: List[Question], threshold: float = 0.7):
    """Flag questions needing manual review."""
    analyzer = QuestionAmbiguityAnalyzer()
    flagged = []

    for question in questions:
        report = analyzer.analyze_question(question)
        quality = question.calculate_quality_score()

        if report.is_ambiguous or quality < threshold:
            flagged.append({
                'question': question,
                'report': report,
                'quality': quality,
                'reason': 'ambiguous' if report.is_ambiguous else 'low_quality'
            })

    return flagged

# Get flagged questions
flagged = flag_for_review(questions, threshold=0.8)

# Export for instructor review
with open('review-queue.md', 'w') as f:
    f.write("# Questions Requiring Review\n\n")
    for item in flagged:
        f.write(f"## {item['question'].id}\n")
        f.write(f"**Reason:** {item['reason']}\n")
        f.write(f"**Quality Score:** {item['quality']:.2f}\n")
        if item['report'].is_ambiguous:
            f.write(f"**Plausible Options:** {', '.join(item['report'].plausible_options)}\n")
```

---

## Output Examples

### Console Output

```
Analyzing 10 questions from week 1...
  [1/10] W1-Q1-cloud-benefits... ⚠️  NEEDS REVIEW (quality: 0.65)
  [2/10] W1-Q2-https-protocol... ✓ OK
  [3/10] W1-Q3-database-types... ✓ Reworded
  [4/10] W1-Q4-network-topology... ✓ OK
  [5/10] W1-Q5-encryption-methods... ⚠️  NEEDS REVIEW (quality: 0.58)
  ...

============================================================
Question Ambiguity Analysis Summary
============================================================

Total questions analyzed: 10
Ambiguous questions found: 2 (20.0%)
Questions reworded: 2

Ambiguous Questions:
--------------------------------------------------

Question ID: W1-Q1-cloud-benefits
  Plausible options: A, B, C
  Correct answer: A
  Recommendation: Reword to make only option A clearly correct.
  ✓ Reworded version available

⚠️  Questions flagged for manual review: 2
  - W1-Q1-cloud-benefits
  - W1-Q5-encryption-methods
```

### Exported Report (Markdown)

See example at `docs/examples/ambiguity-report-example.md`

---

## Configuration

### Environment Variables

```bash
# Required: Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional: Custom model
export AMBIGUITY_ANALYZER_MODEL="claude-sonnet-4-5-20250929"
```

### Quality Thresholds

```python
# Default thresholds
AMBIGUITY_THRESHOLD = 2  # Number of plausible options to trigger reword
QUALITY_THRESHOLD = 0.7  # Quality score below which manual review needed
FEEDBACK_MIN_LENGTH = 20  # Minimum feedback characters per option
```

---

## Best Practices

### ✅ DO

1. **Run after content generation** - Validate questions immediately
2. **Review reworded questions** - Auto-reword is good, human review is better
3. **Set appropriate thresholds** - Adjust based on course difficulty
4. **Export reports** - Keep validation history for audit trail
5. **Integrate with consolidation** - Validate before creating quiz banks

### ❌ DON'T

1. **Don't skip validation** - Even experienced instructors create ambiguous questions
2. **Don't blindly apply rewording** - Review suggests, don't auto-apply to source files
3. **Don't lower thresholds too much** - Quality matters more than quantity
4. **Don't ignore low-quality questions** - Address feedback and structure issues

---

## Limitations

### What It CAN Detect

- ✅ Multiple semantically plausible answers
- ✅ Distractors that are technically correct
- ✅ Questions that are too broad/vague
- ✅ Missing qualifying details

### What It CANNOT Detect

- ❌ Domain-specific errors (requires expert review)
- ❌ Culturally biased questions
- ❌ Outdated information
- ❌ Typos and formatting issues

### API Costs

- ~2,000 tokens per question analyzed
- ~4,000 tokens per question reworded
- Approximate cost: $0.01-0.02 per question (Claude Sonnet)

**Budget estimate:**
- 30-question quiz: $0.30-0.60
- 12-week course (120 questions): $1.20-2.40

---

## Troubleshooting

### API Key Not Found

```
Error: ANTHROPIC_API_KEY not found in environment
```

**Solution:**
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### Analysis Shows No Ambiguity (False Negative)

**Possible causes:**
- Question genuinely clear
- LLM misunderstood context
- Domain knowledge gap

**Solution:**
- Manually review questionable cases
- Lower quality threshold to flag more questions
- Add more course context

### Analysis Flags Everything (False Positive)

**Possible causes:**
- Threshold too high
- Questions genuinely need improvement
- Context missing

**Solution:**
- Review flagged questions - may actually be ambiguous
- Adjust threshold: `--threshold 0.6` (lower = less strict)
- Provide better course context

---

## Future Enhancements

Planned features:

1. **Statistical Analysis** - Track student answer distributions to identify ambiguous questions in practice
2. **Batch Rewording Templates** - Common ambiguity patterns with pre-defined fixes
3. **Confidence Scores** - Quantify certainty of ambiguity detection
4. **Multi-Language Support** - Analyze questions in languages other than English
5. **Integration with LMS** - Direct import/export from Moodle, Canvas, etc.

---

## Related Documentation

- [TESTING.md](TESTING.md) - Unit tests for ambiguity analyzer
- [VALIDATION-GUIDE.md](VALIDATION-GUIDE.md) - Overall validation checks
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture including services layer

---

*For questions or issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)*
