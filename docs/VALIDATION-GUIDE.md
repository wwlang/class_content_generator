# HTML to PPTX Conversion Validation Guide

**Comprehensive guide to automated quality testing for slide conversions**

**Version:** 2.0 (Consolidated)
**Last Updated:** January 10, 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Validation Features](#validation-features)
4. [Understanding Results](#understanding-results)
5. [Validation Checks Reference](#validation-checks-reference)
6. [Customization](#customization)
7. [Integration](#integration)
8. [Troubleshooting](#troubleshooting)
9. [Enhancement Roadmap](#enhancement-roadmap)
10. [Development Guide](#development-guide)

---

## Overview

The validation system performs **comprehensive automated quality checks** on HTML and PPTX files to catch issues like missing content, overlapping shapes, wrong colors, and structural problems.

### Purpose

- **Catch quality issues early** - Before students see slides
- **Ensure design consistency** - Verify brand standards applied
- **Prevent content loss** - Detect missing elements after conversion
- **Automate QA** - No manual checking of 30-slide decks

### When Validation Runs

**Automatically after every conversion:**
```bash
python3 html_to_pptx_converter.py input.html output.pptx
# Validation runs automatically
```

**Exit codes:**
- `0` = Success (or warnings only)
- `1` = Errors found (conversion still completed, but issues flagged)

### Validation Categories

1. **HTML Validation** - Check source content quality
2. **PPTX Validation** - Check output slide quality
3. **Cross-Validation** - Compare HTML → PPTX accuracy

---

## Quick Start

### Automatic Validation (Recommended)

Validation runs automatically with every conversion:

```bash
python3 html_to_pptx_converter.py lecture-week-12.html lecture-week-12.pptx
```

Output includes validation report:
```
Converted 28 slides → lecture-week-12.pptx

======================================================================
VALIDATION REPORT
======================================================================
✅ All checks passed!
```

### Skip Validation

For quick iterations:

```bash
python3 html_to_pptx_converter.py input.html output.pptx --no-validate
```

### Manual Validation

Run validation independently:

```bash
python3 tools/validate_conversion.py input.html output.pptx
```

### Validate All Week Content

```bash
for week in week-*/lecture.html; do
    pptx="${week%.html}.pptx"
    python3 tools/validate_conversion.py "$week" "$pptx" || echo "Failed: $week"
done
```

---

## Validation Features

### HTML Validation

Checks **source content** before conversion:

#### 1. Empty Slides
- **Detects:** Slides with < 10 characters of content
- **Severity:** Error
- **Why it matters:** Empty slides indicate missing content or generation errors

#### 2. Required Elements
- **Quote slides:** Must have `<blockquote>` element
- **Table slides:** Must have `<table>` element
- **References slides:** Should have list structure
- **Severity:** Error (missing required elements)
- **Why it matters:** Layout won't render correctly without proper HTML structure

#### 3. Duplicate Content
- **Detects:** Suspiciously repeated text blocks (>20 characters)
- **Severity:** Warning
- **Why it matters:** May indicate copy-paste errors or generation issues

---

### PPTX Validation

Checks **output slide quality** after conversion:

#### 1. Content Completeness
- **Empty slides:** 0 text shapes (Error)
- **Minimal content:** ≤2 shapes with <10 chars (Warning)
- **Why it matters:** Ensures content extracted successfully

#### 2. Shape Positioning
- **Overlapping text boxes:** Any overlap detected (Error)
- **Why it matters:** Overlapping text is unreadable
- **Example:** Two text boxes at same position will layer incorrectly

#### 3. Boundary Checking
- **Out of bounds:** Content extending beyond slide + 0.01" (Warning)
- **Why it matters:** Content may be cut off in presentation mode
- **Note:** Small overhang acceptable (decorative elements)

#### 4. Background Colors ✨ *Recently Added*
- **Detects:** Wrong or missing background colors
- **Expected:** Cream (#f4f3f1) or Dark (#131313)
- **Severity:** Warning
- **Why it matters:** Brand consistency, visual coherence

#### 5. Font Consistency
- **Expected fonts:** Cal Sans (headers), Plus Jakarta Sans (body)
- **Unexpected fonts:** Times New Roman, Arial, etc.
- **Severity:** Warning
- **Why it matters:** Professional appearance, brand consistency

#### 6. Font Size Validation ✨ *Recently Added*
- **Too small:** < 8pt (Warning - readability issue)
- **Too large:** > 150pt (Info - may be decorative)
- **Why it matters:** Readability, accessibility

#### 7. Text Truncation
- **Detects:** Long text (>100 chars) without word wrap
- **Severity:** Warning
- **Why it matters:** Text may overflow text box

#### 8. Missing Content
- **Detects:** >3 empty text boxes when total > 5 shapes
- **Severity:** Warning
- **Why it matters:** May indicate extraction failures

---

### Cross-Validation

Checks **HTML → PPTX accuracy**:

#### 1. Slide Count Match
- **Checks:** HTML slide count = PPTX slide count
- **Severity:** Error
- **Why it matters:** Missing slides = incomplete presentation

#### 2. Content Length Match
- **Checks:** Character count difference < 10%
- **Severity:** Warning if >10% difference
- **Why it matters:** Significant loss may indicate missing content
- **Note:** Some difference expected (footers, formatting)

#### 3. Visual Consistency ✨ *Recently Added*
- **Images in HTML** → Should appear in PPTX (Warning if missing)
- **Tables in HTML** → May convert to shapes (Info only)
- **Why it matters:** Visual elements enhance understanding

---

## Understanding Results

### Severity Levels

#### ❌ **Errors** (Critical - Must Fix)

Issues that significantly impact presentation quality:

- Empty slides
- Missing required HTML elements
- Significant overlapping content
- Structure problems
- Slide count mismatch

**Example:**
```
❌ ERROR: Slide 5 [structure]
   Missing <blockquote> element on quote slide
   → Add <blockquote> tag to HTML source
```

#### ⚠️ **Warnings** (Review Recommended)

Issues that may be intentional but should be reviewed:

- Shapes slightly beyond boundaries
- Content length differences (often due to footers)
- Font inconsistencies
- Empty decorative shapes
- Wrong background colors
- Font sizes too small

**Example:**
```
⚠️  WARNING: Slide 12 [background]
   Background color doesn't match expected (cream or dark)
   → Current: #ffffff (white), Expected: #f4f3f1 (cream)
```

#### ℹ️ **Info** (Informational)

Non-issues or expected differences:

- Large font sizes (likely decorative)
- Tables converted to shapes
- Minor formatting differences

**Example:**
```
ℹ️  INFO: Slide 3
   Large font size detected (120pt) - likely decorative quote mark
```

### Exit Codes

- **`0`** - All checks passed OR only warnings/info
- **`1`** - Errors found (serious issues detected)

**In automatic mode (after conversion):**
- Exit code 1 indicates problems but PPTX still created
- Review issues and decide whether to regenerate

**In CI/CD:**
- Use exit code to block builds with errors
- Allow warnings but track them

---

## Validation Checks Reference

### Complete Check Matrix

| Category | Check | Severity | Threshold | When Added |
|----------|-------|----------|-----------|------------|
| **HTML** | | | | |
| | Empty slide | Error | < 10 chars | v1.0 |
| | Missing blockquote (quote) | Error | Element not found | v1.0 |
| | Missing table (table slides) | Error | Element not found | v1.0 |
| | Missing list (references) | Warning | Element not found | v1.0 |
| | Duplicate content | Warning | >20 char duplicates | v1.0 |
| **PPTX** | | | | |
| | Empty slide | Error | 0 text shapes | v1.0 |
| | Minimal content | Warning | ≤2 shapes, <10 chars | v1.0 |
| | Overlapping text | Error | Any overlap | v1.0 |
| | Out of bounds | Warning | Beyond slide + 0.01" | v1.0 |
| | Unexpected fonts | Warning | Not Cal Sans/Plus Jakarta Sans | v1.0 |
| | Text truncation | Warning | No wrap + >100 chars | v1.0 |
| | Empty text boxes | Warning | >3 empty of >5 total | v1.0 |
| | Background color | Warning | Not cream or dark | v1.2 |
| | Font size too small | Warning | < 8pt | v1.2 |
| | Font size very large | Info | > 150pt | v1.2 |
| **Cross** | | | | |
| | Slide count mismatch | Error | Any difference | v1.0 |
| | Content length diff | Warning | >10% difference | v1.0 |
| | Missing images | Warning | HTML image not in PPTX | v1.2 |
| | Missing tables | Info | HTML table not in PPTX | v1.2 |

---

## Customization

### Adjust Thresholds

Edit `tools/validate_conversion.py` to customize validation:

#### Example 1: Increase Content Tolerance

```python
# In CrossValidator._check_content_match()
if diff_pct > 20:  # Changed from 10%
    issues.append(ValidationIssue(
        severity='warning',
        category='content',
        slide_number=slide_num,
        message=f'Content length difference: {diff_pct:.1f}%'
    ))
```

#### Example 2: Change Font Size Limits

```python
# In PPTXValidator._check_font_sizes()
MIN_FONT_SIZE = 6  # Changed from 8pt
MAX_FONT_SIZE = 200  # Changed from 150pt
```

#### Example 3: Add Custom Color

```python
# In PPTXValidator._check_background_color()
EXPECTED_BACKGROUNDS = [
    (244, 243, 241),  # Cream
    (19, 19, 19),     # Dark
    (255, 255, 255),  # White (new)
]
```

### Disable Specific Checks

Comment out check calls in `validate()` method:

```python
def validate(self):
    issues = []
    # ... other checks ...
    # issues.extend(self._check_background_color(slide, i))  # Disabled
    return issues
```

### Create Custom Validators

Add new check methods:

```python
class PPTXValidator:
    def _check_my_custom_rule(self, slide, slide_num: int) -> List[ValidationIssue]:
        """Check for custom quality rule."""
        issues = []

        # Your custom logic here
        if problem_detected:
            issues.append(ValidationIssue(
                severity='warning',
                category='custom',
                slide_number=slide_num,
                message='Description of problem',
                details='How to fix it'
            ))

        return issues
```

Call from `validate()` method:

```python
def validate(self):
    issues = []
    for i, slide in enumerate(self.prs.slides, start=1):
        issues.extend(self._check_my_custom_rule(slide, i))
    return issues
```

---

## Integration

### CI/CD Integration

#### GitHub Actions Example

```yaml
name: Validate Slides
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Convert and validate all lectures
        run: |
          for html in courses/*/weeks/week-*/lecture.html; do
            pptx="${html%.html}.pptx"
            python3 html_to_pptx_converter.py "$html" "$pptx" || exit 1
          done
```

#### Quality Gates

Set thresholds for CI/CD:

```bash
# Fail build if any errors
if grep -q "❌ ERROR" validation.log; then
    echo "Validation failed - blocking build"
    exit 1
fi

# Warn but allow if only warnings
if grep -q "⚠️  WARNING" validation.log; then
    echo "Warnings detected - review recommended"
    exit 0  # Still pass
fi
```

### Batch Processing

Validate multiple files:

```bash
#!/bin/bash
# validate_all_weeks.sh

success=0
failed=0

for week in week-*/lecture.html; do
    pptx="${week%.html}.pptx"
    echo "Validating: $week"

    python3 html_to_pptx_converter.py "$week" "$pptx"

    if [ $? -eq 0 ]; then
        ((success++))
    else
        ((failed++))
        echo "❌ Failed: $week"
    fi
done

echo "Results: $success passed, $failed failed"
```

### Pre-Commit Hook

Validate before git commit:

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Find staged PPTX files
staged_pptx=$(git diff --cached --name-only --diff-filter=ACM | grep '\.pptx$')

for pptx in $staged_pptx; do
    html="${pptx%.pptx}.html"

    if [ -f "$html" ]; then
        python3 tools/validate_conversion.py "$html" "$pptx"
        if [ $? -ne 0 ]; then
            echo "Validation failed for $pptx - commit blocked"
            exit 1
        fi
    fi
done
```

---

## Troubleshooting

### Common Issues

#### Issue: "Module not found" Error

**Problem:**
```
ModuleNotFoundError: No module named 'lxml'
```

**Solution:**
```bash
# Ensure you're in project root
cd /path/to/class_content_generator

# Install dependencies
pip install -r requirements.txt

# Or install individually
pip install python-pptx lxml
```

---

#### Issue: False Positive - Shapes Beyond Boundaries

**Problem:**
```
⚠️  WARNING: Slide 2 [positioning]
   2 content shapes may extend beyond boundaries
```

**Cause:** Decorative elements intentionally extend slightly (e.g., title slide circles)

**Solutions:**
1. **Review slide** - Check if overhang is intentional
2. **Increase tolerance** in `_check_shapes_within_bounds()`:
   ```python
   BOUNDARY_TOLERANCE = 0.05  # Changed from 0.01 inches
   ```
3. **Suppress for specific slide types** (e.g., title slides)

---

#### Issue: Content Length Differences

**Problem:**
```
⚠️  WARNING: Slide 18 [content]
   Significant content length difference
   HTML: 245 chars, PPTX: 272 chars (11.0% diff)
```

**Cause:** Footers, page numbers, formatting differences

**When acceptable:**
- Difference < 30%
- Footer text added in PPTX
- Formatting characters (bold, italic markers)

**When problematic:**
- Difference > 50%
- Missing entire paragraphs
- Extraction errors

**Solution:**
- Review slide manually
- If acceptable, increase threshold in config
- If problematic, check HTML source and regenerate

---

#### Issue: Empty Text Boxes Warning

**Problem:**
```
⚠️  WARNING: Slide 1 [content]
   3 empty text boxes (out of 5 shapes)
```

**Cause:**
- Decorative shapes (no text by design)
- Extraction failures

**When acceptable:**
- Decorative circles on title slide
- Spacer shapes
- < 5 total shapes

**When problematic:**
- Many empty boxes (>5)
- Expected content missing

**Solution:**
- Review slide visually
- If decorative, ignore warning
- If content missing, check HTML source

---

#### Issue: Validation Too Strict

**Problem:** Too many warnings for intentional design choices

**Solution:**

**Option 1: Skip validation for specific files**
```bash
python3 html_to_pptx_converter.py special-case.html special-case.pptx --no-validate
```

**Option 2: Adjust thresholds globally**
Edit `tools/validate_conversion.py`:
```python
# More lenient settings
MIN_CONTENT_LENGTH = 5  # From 10
CONTENT_DIFF_THRESHOLD = 30  # From 10%
BOUNDARY_TOLERANCE = 0.1  # From 0.01
```

**Option 3: Disable specific checks**
Comment out in `validate()` method

---

### Debugging Validation

#### Enable Verbose Output

Add debug logging to validator:

```python
# In tools/validate_conversion.py
import logging
logging.basicConfig(level=logging.DEBUG)

# In check methods:
logging.debug(f"Checking slide {slide_num}: {len(shapes)} shapes")
```

#### Inspect Specific Slide

```python
# Open PPTX in Python
from pptx import Presentation
prs = Presentation('lecture.pptx')

slide = prs.slides[11]  # 0-indexed (Slide 12)

for shape in slide.shapes:
    print(f"Shape: {shape.shape_type}")
    if hasattr(shape, 'text'):
        print(f"  Text: {shape.text[:50]}")
    print(f"  Position: ({shape.left}, {shape.top})")
    print(f"  Size: ({shape.width}, {shape.height})")
```

---

## Enhancement Roadmap

The following features are **planned but not yet implemented**. This section documents future validation improvements.

### Phase 1: Critical Visual Checks (High Priority ⭐)

#### 1. Color Accuracy Validation

**Status:** Planned
**Priority:** High
**Complexity:** Medium

**What it will check:**
- Text colors match between HTML CSS and PPTX shapes
- Accent colors (orange #ed5e29) used consistently
- No unexpected colors introduced during conversion

**Expected colors:**
- Primary text: #131313 (dark gray)
- Accent: #ed5e29 (orange)
- Muted: #64748b (slate gray)
- Background: #f4f3f1 (cream) or #131313 (dark)

**Implementation approach:**
```python
def _check_color_consistency(self, html_slide, pptx_slide, slide_num):
    """Verify colors in PPTX match HTML CSS."""
    # Extract HTML colors from CSS classes
    # Compare with PPTX shape RGB colors
    # Flag unexpected color variations (tolerance: ±5 RGB)
```

---

#### 2. Spacing and Layout Validation

**Status:** Planned
**Priority:** High
**Complexity:** High

**What it will check:**
- Consistent padding/margins across slides
- Elements properly aligned (left, center, right as expected)
- Vertical spacing between elements uniform
- Title positions consistent across slide types

**Thresholds:**
- Padding variance: ±0.05 inches acceptable
- Title Y position: Should match `LayoutConfig.TITLE_Y` (0.62")
- Footer Y position: Within 0.02 inches across all slides

**Implementation approach:**
```python
def _check_layout_consistency(self, slide, slide_num):
    """Check for consistent spacing and alignment."""
    # Verify padding matches LayoutConfig.PADDING (0.625")
    # Check title Y position = 0.62" (±0.05")
    # Verify footer at FOOTER_Y across all slides
```

---

#### 3. Slide Dimension Validation

**Status:** Planned
**Priority:** High
**Complexity:** Low

**What it will check:**
- All slides exactly 10.67" × 8.0" (16:9 aspect ratio)
- Presentation dimensions consistent across all slides
- Content doesn't extend beyond slide bounds (stricter than current check)

**Implementation approach:**
```python
def _check_dimensions(self, slide, slide_num):
    """Verify slide dimensions and aspect ratio."""
    width = self.prs.slide_width
    height = self.prs.slide_height

    expected_width = Inches(10.67)
    expected_height = Inches(8.0)

    if abs(width - expected_width) > Inches(0.01):
        # Issue: Incorrect slide width
```

---

### Phase 2: Styling Refinements (Medium Priority 🔸)

#### 4. Shadow and Effects Validation

**Status:** Planned
**Priority:** Medium
**Complexity:** Low

**What it will check:**
- Shadows disabled on all shapes (clean design principle)
- No unexpected borders or outlines
- Consistent shape styling (no gradient fills, etc.)

---

#### 5. Text Alignment Validation

**Status:** Planned
**Priority:** Medium
**Complexity:** Medium

**What it will check:**
- Title text left-aligned (default)
- Centered text where appropriate (quotes, big numbers)
- No accidentally right-aligned text

**Alignment rules:**
- Titles: LEFT (default)
- Quote text: LEFT or CENTER
- Big numbers: CENTER
- Attribution: LEFT

---

#### 6. Decorative Elements Validation

**Status:** Planned
**Priority:** Medium
**Complexity:** Medium

**What it will check:**
- Title slides have 3 decorative circles at bottom-left
- Section breaks have proper background color
- Elements properly positioned per layout specification

---

### Phase 3: Accessibility (Medium Priority 🔸)

#### 7. Accessibility Validation

**Status:** Planned
**Priority:** Medium
**Complexity:** High

**What it will check:**
- Color contrast ratios meet WCAG AA standards (4.5:1 minimum)
- Minimum font sizes (12pt body, 8pt footnotes)
- Alt text for images
- Logical reading order

**Standards:**
- Color contrast: 4.5:1 minimum (WCAG AA)
- Minimum font size: 12pt body text, 8pt footnotes
- Images: Should have descriptive alt text
- Reading order: Top-to-bottom, left-to-right

---

### Phase 4: Future-Proofing (Low Priority 🔹)

#### 8. Image Quality Validation
- Aspect ratios preserved
- Images not over-compressed
- Proper positioning

#### 9. Hyperlink Validation
- Links preserved from HTML
- URLs functional
- Link text matches

#### 10. Animation/Transition Validation
- No unwanted animations
- Consistent transitions (if we add them)

---

### Performance Estimates

**Current validation time:**
- 17 slides: ~2-3 seconds
- 30 slides: ~4-5 seconds

**With all Phase 1-2 enhancements:**
- 30 slides: ~5-7 seconds (estimated)
- Still acceptable for automatic validation

**Optimization options:**
- Parallel validation (check slides concurrently)
- Lazy evaluation (only check on failures)
- Caching (reuse results for unchanged slides)

---

## Development Guide

### Adding New Validation Checks

#### Step 1: Create Check Method

Add to appropriate validator class (`HTMLValidator`, `PPTXValidator`, or `CrossValidator`):

```python
def _check_my_new_feature(self, slide, slide_num: int) -> List[ValidationIssue]:
    """
    Check for specific quality issue.

    Args:
        slide: PPTX slide object
        slide_num: Slide number (1-indexed)

    Returns:
        List of ValidationIssue objects
    """
    issues = []

    # Your validation logic here
    if problem_detected:
        issues.append(ValidationIssue(
            severity='warning',  # or 'error', 'info'
            category='styling',  # or 'content', 'structure', 'positioning'
            slide_number=slide_num,
            message='Brief description of problem',
            details='How to fix it or additional context'
        ))

    return issues
```

#### Step 2: Call from validate() Method

```python
def validate(self):
    """Run all validation checks."""
    issues = []

    for i, slide in enumerate(self.prs.slides, start=1):
        # ... existing checks ...
        issues.extend(self._check_my_new_feature(slide, i))  # ADD THIS

    return issues
```

#### Step 3: Test

Create test case:

```python
# tests/test_validators.py
def test_detects_my_feature():
    # Create test slide with problem
    validator = PPTXValidator("test_file.pptx")
    issues = validator._check_my_new_feature(slide, 1)

    # Verify issue detected
    assert len(issues) > 0
    assert "expected message" in issues[0].message.lower()
```

#### Step 4: Document

Update this guide with new check in [Validation Checks Reference](#validation-checks-reference).

---

### Testing Validators

#### Test with Example Files

```bash
# Note: slide-exporter examples archived to docs/.archive/slide-technical/
python3 tools/validate_conversion.py \
    docs/.archive/slide-technical/skill-backup/resources/examples/enhanced-sample-slides.html \
    docs/.archive/slide-technical/skill-backup/resources/examples/enhanced-sample-slides.pptx
```

#### Create Test Suite

**Test files to create:**
- `test-all-layouts.html/pptx` - Every layout type
- `test-color-variations.html/pptx` - Different color schemes
- `test-edge-cases.html/pptx` - Boundary conditions
- `test-errors.html/pptx` - Intentional errors to catch

#### Test-Driven Development

1. **Create failing test case**
2. **Implement validator**
3. **Verify test passes**
4. **Test on real files**

---

### Configuration System (Future)

Allow users to customize validation:

```python
# validation_config.py (proposed)
class ValidationConfig:
    """Configuration for validation thresholds and rules."""

    # Enable/disable specific checks
    CHECK_BACKGROUND_COLORS = True
    CHECK_FONT_SIZES = True
    CHECK_ALIGNMENT = True
    CHECK_SHADOWS = True

    # Thresholds
    MIN_FONT_SIZE = 8  # pt
    MAX_FONT_SIZE = 150  # pt
    PADDING_TOLERANCE = 0.05  # inches
    CONTENT_DIFF_THRESHOLD = 10  # percent

    # Color definitions
    EXPECTED_BACKGROUNDS = [
        (244, 243, 241),  # Cream
        (19, 19, 19),      # Dark
    ]
    COLOR_TOLERANCE = 5  # RGB difference acceptable
```

---

## See Also

### Related Documentation

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical architecture of converter
- **[LAYOUT-VOCABULARY.md](LAYOUT-VOCABULARY.md)** - Layout vocabulary reference
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Development guidelines

### Implementation Files

- **`tools/validate_conversion.py`** - Validation implementation
- **`html_to_pptx_converter.py`** - Converter with auto-validation integration

---

## Version History

### Version 2.0 (January 10, 2025) - Consolidated

- **Merged VALIDATION-SYSTEM.md and VALIDATION-ENHANCEMENTS.md**
- Added comprehensive enhancement roadmap with priorities
- Improved troubleshooting section
- Enhanced integration examples
- Added development guide

**Previous versions:**
- VALIDATION-SYSTEM.md (deprecated)
- VALIDATION-ENHANCEMENTS.md (deprecated)

### Version 1.2 (January 2025)

- Added background color validation
- Added font size validation
- Added visual consistency cross-check (images/tables)

### Version 1.0 (December 2024)

- Initial validation system
- HTML, PPTX, and cross-validation checks
- Automatic integration with converter

---

**This is the single authoritative reference for conversion validation. For technical implementation details, see `tools/validate_conversion.py`.**
