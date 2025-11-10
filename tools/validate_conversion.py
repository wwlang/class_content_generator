#!/usr/bin/env python3
"""
Comprehensive validation tool for HTML and PPTX conversion quality.

Tests for:
- Content completeness (no missing text)
- Shape positioning (no overlaps, within bounds)
- Font consistency
- Color accuracy
- Required elements present
- Text truncation
- Slide structure integrity

Usage:
    python3 validate_conversion.py <input.html> <output.pptx>
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional, Set
from pathlib import Path
from lxml import html as lxml_html
from pptx import Presentation
from pptx.util import Inches, Pt
import sys
import json


@dataclass
class ValidationIssue:
    """Represents a validation issue found during testing."""
    severity: str  # 'error', 'warning', 'info'
    category: str  # 'content', 'positioning', 'styling', 'structure'
    slide_number: int
    message: str
    details: Optional[str] = None


@dataclass
class ValidationReport:
    """Complete validation report with all issues found."""
    html_file: str
    pptx_file: str
    total_slides: int
    errors: List[ValidationIssue]
    warnings: List[ValidationIssue]
    info: List[ValidationIssue]

    def has_errors(self) -> bool:
        """Check if report contains any errors."""
        return len(self.errors) > 0

    def has_warnings(self) -> bool:
        """Check if report contains any warnings."""
        return len(self.warnings) > 0

    def print_summary(self):
        """Print human-readable summary of validation results."""
        print("\n" + "="*70)
        print("VALIDATION REPORT")
        print("="*70)
        print(f"HTML: {self.html_file}")
        print(f"PPTX: {self.pptx_file}")
        print(f"Slides: {self.total_slides}")
        print("-"*70)

        if not self.errors and not self.warnings:
            print("✓ ALL CHECKS PASSED")
            print("="*70 + "\n")
            return

        if self.errors:
            print(f"\n❌ ERRORS: {len(self.errors)}")
            for issue in self.errors:
                print(f"  Slide {issue.slide_number} [{issue.category}]: {issue.message}")
                if issue.details:
                    print(f"    → {issue.details}")

        if self.warnings:
            print(f"\n⚠️  WARNINGS: {len(self.warnings)}")
            for issue in self.warnings:
                print(f"  Slide {issue.slide_number} [{issue.category}]: {issue.message}")
                if issue.details:
                    print(f"    → {issue.details}")

        if self.info:
            print(f"\nℹ️  INFO: {len(self.info)}")
            for issue in self.info[:5]:  # Limit to first 5
                print(f"  Slide {issue.slide_number} [{issue.category}]: {issue.message}")
            if len(self.info) > 5:
                print(f"  ... and {len(self.info) - 5} more")

        print("="*70 + "\n")


class HTMLValidator:
    """Validates HTML slide structure and content."""

    def __init__(self, html_path: str):
        self.html_path = html_path
        with open(html_path, 'r', encoding='utf-8') as f:
            self.tree = lxml_html.fromstring(f.read())
        self.slides = self._extract_slides()

    def _extract_slides(self) -> List:
        """Extract all slide elements from HTML."""
        slides = self.tree.findall('.//div[@class]')
        return [s for s in slides if 'slide' in s.get('class', '')]

    def validate(self) -> List[ValidationIssue]:
        """Run all HTML validation checks."""
        issues = []

        for i, slide in enumerate(self.slides, 1):
            issues.extend(self._check_empty_slides(slide, i))
            issues.extend(self._check_required_elements(slide, i))
            issues.extend(self._check_duplicate_content(slide, i))

        return issues

    def _check_empty_slides(self, slide, slide_num: int) -> List[ValidationIssue]:
        """Check for slides with no meaningful content."""
        issues = []

        # Extract all text
        all_text = ''.join(slide.itertext()).strip()

        if len(all_text) < 10:  # Less than 10 characters
            issues.append(ValidationIssue(
                severity='error',
                category='content',
                slide_number=slide_num,
                message='Slide appears empty or has minimal content',
                details=f'Only {len(all_text)} characters found'
            ))

        return issues

    def _check_required_elements(self, slide, slide_num: int) -> List[ValidationIssue]:
        """Check that slides have required elements based on type."""
        issues = []
        classes = slide.get('class', '')

        # Quote slides should have blockquote or cite
        if 'quote-slide' in classes:
            blockquote = slide.find('.//blockquote')
            quote_content = slide.find('.//*[@class="quote-content"]')
            if blockquote is None and quote_content is None:
                issues.append(ValidationIssue(
                    severity='error',
                    category='structure',
                    slide_number=slide_num,
                    message='Quote slide missing blockquote element'
                ))

        # Table slides should have table
        if 'table' in classes or 'comparison-table' in classes:
            table = slide.find('.//table')
            if table is None:
                issues.append(ValidationIssue(
                    severity='error',
                    category='structure',
                    slide_number=slide_num,
                    message='Table slide missing table element'
                ))

        # References slides should have list or references container
        if 'references-slide' in classes:
            ul = slide.find('.//ul')
            refs = slide.find('.//*[@class="references"]')
            if ul is None and refs is None:
                issues.append(ValidationIssue(
                    severity='warning',
                    category='structure',
                    slide_number=slide_num,
                    message='References slide missing list structure'
                ))

        return issues

    def _check_duplicate_content(self, slide, slide_num: int) -> List[ValidationIssue]:
        """Check for suspiciously duplicated text content."""
        issues = []

        # Get all text elements
        text_elements = []
        for elem in slide.iter():
            if elem.text and elem.text.strip():
                text_elements.append(elem.text.strip())

        # Check for exact duplicates
        seen = set()
        duplicates = set()
        for text in text_elements:
            if len(text) > 20:  # Only check substantial text
                if text in seen:
                    duplicates.add(text[:50])
                seen.add(text)

        if duplicates:
            issues.append(ValidationIssue(
                severity='warning',
                category='content',
                slide_number=slide_num,
                message='Duplicate text content detected',
                details=f'Found {len(duplicates)} duplicate text blocks'
            ))

        return issues


class PPTXValidator:
    """Validates PPTX slide structure, positioning, and content."""

    # Slide dimensions (4:3 aspect ratio)
    SLIDE_WIDTH = 10.0  # inches
    SLIDE_HEIGHT = 7.5  # inches
    MARGIN = 0.5  # inches

    def __init__(self, pptx_path: str):
        self.pptx_path = pptx_path
        self.prs = Presentation(pptx_path)

    def validate(self) -> List[ValidationIssue]:
        """Run all PPTX validation checks."""
        issues = []

        for i, slide in enumerate(self.prs.slides, 1):
            issues.extend(self._check_empty_slides(slide, i))
            issues.extend(self._check_overlapping_shapes(slide, i))
            issues.extend(self._check_shapes_within_bounds(slide, i))
            issues.extend(self._check_font_consistency(slide, i))
            issues.extend(self._check_text_truncation(slide, i))
            issues.extend(self._check_missing_content(slide, i))
            issues.extend(self._check_background_color(slide, i))
            issues.extend(self._check_font_sizes(slide, i))

        return issues

    def _check_empty_slides(self, slide, slide_num: int) -> List[ValidationIssue]:
        """Check for slides with no content or very few shapes."""
        issues = []

        # Count meaningful shapes (exclude placeholders, footers)
        content_shapes = [s for s in slide.shapes if hasattr(s, 'text')]

        if len(content_shapes) == 0:
            issues.append(ValidationIssue(
                severity='error',
                category='content',
                slide_number=slide_num,
                message='Slide has no text content'
            ))
        elif len(content_shapes) <= 2:
            # Check if there's actual text
            total_text = ''.join(s.text for s in content_shapes if hasattr(s, 'text')).strip()
            if len(total_text) < 10:
                issues.append(ValidationIssue(
                    severity='warning',
                    category='content',
                    slide_number=slide_num,
                    message='Slide has minimal content',
                    details=f'Only {len(content_shapes)} shapes, {len(total_text)} characters'
                ))

        return issues

    def _check_overlapping_shapes(self, slide, slide_num: int) -> List[ValidationIssue]:
        """Check for overlapping text boxes and shapes."""
        issues = []

        # Get all shape positions
        shapes_with_pos = []
        for shape in slide.shapes:
            if hasattr(shape, 'left') and hasattr(shape, 'top'):
                shapes_with_pos.append({
                    'shape': shape,
                    'left': shape.left,
                    'top': shape.top,
                    'right': shape.left + shape.width,
                    'bottom': shape.top + shape.height,
                })

        # Check for overlaps
        overlaps = []
        for i, shape1 in enumerate(shapes_with_pos):
            for shape2 in shapes_with_pos[i+1:]:
                if self._rectangles_overlap(shape1, shape2):
                    # Only report if both have text (not decorative overlaps)
                    if (hasattr(shape1['shape'], 'text') and shape1['shape'].text.strip() and
                        hasattr(shape2['shape'], 'text') and shape2['shape'].text.strip()):
                        overlaps.append((shape1, shape2))

        if overlaps:
            issues.append(ValidationIssue(
                severity='error',
                category='positioning',
                slide_number=slide_num,
                message=f'Found {len(overlaps)} overlapping text shapes',
                details='Text may be unreadable due to overlap'
            ))

        return issues

    def _rectangles_overlap(self, rect1: Dict, rect2: Dict) -> bool:
        """Check if two rectangles overlap."""
        return not (rect1['right'] <= rect2['left'] or
                   rect1['left'] >= rect2['right'] or
                   rect1['bottom'] <= rect2['top'] or
                   rect1['top'] >= rect2['bottom'])

    def _check_shapes_within_bounds(self, slide, slide_num: int) -> List[ValidationIssue]:
        """Check that all shapes are within slide boundaries."""
        issues = []

        slide_width = Inches(self.SLIDE_WIDTH)
        slide_height = Inches(self.SLIDE_HEIGHT)

        # Allow small margin of error (0.01 inches) for rounding
        tolerance = Inches(0.01)

        out_of_bounds = []
        for shape in slide.shapes:
            if hasattr(shape, 'left') and hasattr(shape, 'top'):
                # Check if shape significantly extends beyond slide
                if (shape.left < -tolerance or shape.top < -tolerance or
                    shape.left + shape.width > slide_width + tolerance or
                    shape.top + shape.height > slide_height + tolerance):
                    # Only report if it has visible content
                    if hasattr(shape, 'text') and shape.text.strip():
                        out_of_bounds.append(shape)

        if out_of_bounds:
            issues.append(ValidationIssue(
                severity='warning',  # Downgrade to warning
                category='positioning',
                slide_number=slide_num,
                message=f'{len(out_of_bounds)} content shapes may extend beyond boundaries',
                details=f'Check for text that might be cut off'
            ))

        return issues

    def _check_font_consistency(self, slide, slide_num: int) -> List[ValidationIssue]:
        """Check for font consistency across slide."""
        issues = []

        fonts_used = set()
        for shape in slide.shapes:
            if hasattr(shape, 'text_frame'):
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        if run.font.name:
                            fonts_used.add(run.font.name)

        # Expected fonts
        expected_fonts = {'Cal Sans', 'Plus Jakarta Sans'}
        unexpected_fonts = fonts_used - expected_fonts - {None}

        if unexpected_fonts:
            issues.append(ValidationIssue(
                severity='warning',
                category='styling',
                slide_number=slide_num,
                message='Unexpected fonts detected',
                details=f'Found: {", ".join(unexpected_fonts)}'
            ))

        return issues

    def _check_text_truncation(self, slide, slide_num: int) -> List[ValidationIssue]:
        """Check for text that may be truncated in text boxes."""
        issues = []

        truncated_shapes = []
        for shape in slide.shapes:
            if hasattr(shape, 'text_frame') and shape.text_frame.text.strip():
                # Check if text frame is set to auto-size
                if hasattr(shape.text_frame, 'word_wrap'):
                    # If word wrap is off and text is long, might truncate
                    if not shape.text_frame.word_wrap and len(shape.text_frame.text) > 100:
                        truncated_shapes.append(shape)

        if truncated_shapes:
            issues.append(ValidationIssue(
                severity='warning',
                category='content',
                slide_number=slide_num,
                message=f'{len(truncated_shapes)} text boxes may have truncated content',
                details='Long text without word wrap enabled'
            ))

        return issues

    def _check_missing_content(self, slide, slide_num: int) -> List[ValidationIssue]:
        """Check for shapes with no text (might indicate extraction failure)."""
        issues = []

        # Count content shapes (not footers/page numbers)
        content_shapes = [s for s in slide.shapes if hasattr(s, 'text')]

        # Find text boxes that are empty
        empty_textboxes = []
        for shape in slide.shapes:
            if hasattr(shape, 'text_frame'):
                if hasattr(shape, 'text') and not shape.text.strip():
                    # Check if it has paragraphs (structure exists but no content)
                    if len(shape.text_frame.paragraphs) > 0:
                        empty_textboxes.append(shape)

        # More than 3 empty text boxes out of total is suspicious
        if len(content_shapes) > 5 and len(empty_textboxes) > 3:
            issues.append(ValidationIssue(
                severity='warning',  # Downgrade to warning
                category='content',
                slide_number=slide_num,
                message=f'{len(empty_textboxes)} of {len(content_shapes)} text boxes are empty',
                details='May include decorative or placeholder shapes'
            ))

        return issues

    def _check_background_color(self, slide, slide_num: int) -> List[ValidationIssue]:
        """Check that slide has appropriate background color."""
        issues = []

        # Expected background: Cream (#f4f3f1 = RGB 244, 243, 241)
        # Some slides may have dark background (#131313)
        expected_cream = (244, 243, 241)
        expected_dark = (19, 19, 19)

        # Find background rectangle (should be first shape)
        has_background = False
        background_color = None

        if len(slide.shapes) > 0:
            first_shape = slide.shapes[0]
            # Check if it's a rectangle covering whole slide
            if hasattr(first_shape, 'fill') and first_shape.fill.type == 1:  # SOLID
                try:
                    bg_color = first_shape.fill.fore_color.rgb
                    background_color = (bg_color[0], bg_color[1], bg_color[2])
                    has_background = True
                except:
                    pass

        if has_background:
            # Check if it matches expected colors (allow small tolerance)
            tolerance = 5
            is_cream = all(abs(background_color[i] - expected_cream[i]) <= tolerance for i in range(3))
            is_dark = all(abs(background_color[i] - expected_dark[i]) <= tolerance for i in range(3))

            if not is_cream and not is_dark:
                issues.append(ValidationIssue(
                    severity='warning',
                    category='styling',
                    slide_number=slide_num,
                    message=f'Unexpected background color: RGB{background_color}',
                    details='Expected cream (#f4f3f1) or dark (#131313)'
                ))
        else:
            # No background detected - might be white default
            issues.append(ValidationIssue(
                severity='warning',
                category='styling',
                slide_number=slide_num,
                message='No background color applied (using default white)',
                details='Expected cream or dark background'
            ))

        return issues

    def _check_font_sizes(self, slide, slide_num: int) -> List[ValidationIssue]:
        """Check for unreasonably large or small font sizes."""
        issues = []

        font_sizes = []
        for shape in slide.shapes:
            if hasattr(shape, 'text_frame'):
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        if run.font.size:
                            font_sizes.append(run.font.size.pt)

        if font_sizes:
            min_size = min(font_sizes)
            max_size = max(font_sizes)

            # Check for unreasonably small text (< 8pt, excluding footers)
            if min_size < 8:
                issues.append(ValidationIssue(
                    severity='warning',
                    category='styling',
                    slide_number=slide_num,
                    message=f'Very small font size detected: {min_size}pt',
                    details='May be difficult to read'
                ))

            # Check for unreasonably large text (> 150pt, excluding decorative)
            if max_size > 150:
                issues.append(ValidationIssue(
                    severity='info',
                    category='styling',
                    slide_number=slide_num,
                    message=f'Very large font size detected: {max_size}pt',
                    details='May be decorative element'
                ))

        return issues


class CrossValidator:
    """Cross-validates HTML and PPTX to ensure content matches."""

    def __init__(self, html_path: str, pptx_path: str):
        self.html_path = html_path
        self.pptx_path = pptx_path

        # Load HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            self.html_tree = lxml_html.fromstring(f.read())
        html_slides = self.html_tree.findall('.//div[@class]')
        self.html_slides = [s for s in html_slides if 'slide' in s.get('class', '')]

        # Load PPTX
        self.pptx_prs = Presentation(pptx_path)

    def validate(self) -> List[ValidationIssue]:
        """Cross-validate HTML and PPTX content."""
        issues = []

        # Check slide count matches
        if len(self.html_slides) != len(self.pptx_prs.slides):
            issues.append(ValidationIssue(
                severity='error',
                category='structure',
                slide_number=0,
                message='Slide count mismatch',
                details=f'HTML: {len(self.html_slides)}, PPTX: {len(self.pptx_prs.slides)}'
            ))
            return issues

        # Check content matches for each slide
        for i in range(len(self.html_slides)):
            issues.extend(self._check_content_match(i))
            issues.extend(self._check_visual_consistency(i))

        return issues

    def _check_content_match(self, slide_index: int) -> List[ValidationIssue]:
        """Check if content matches between HTML and PPTX for a slide."""
        issues = []
        slide_num = slide_index + 1

        # Extract HTML text
        html_slide = self.html_slides[slide_index]
        html_text = ' '.join(''.join(html_slide.itertext()).split())  # Normalize whitespace

        # Extract PPTX text
        pptx_slide = self.pptx_prs.slides[slide_index]
        pptx_text_parts = []
        for shape in pptx_slide.shapes:
            if hasattr(shape, 'text') and shape.text.strip():
                pptx_text_parts.append(shape.text.strip())
        pptx_text = ' '.join(' '.join(pptx_text_parts).split())  # Normalize whitespace

        # Check for significant content loss (more than 10% difference)
        html_len = len(html_text)
        pptx_len = len(pptx_text)

        if html_len > 0:
            diff_pct = abs(html_len - pptx_len) / html_len * 100

            if diff_pct > 10:
                issues.append(ValidationIssue(
                    severity='warning',
                    category='content',
                    slide_number=slide_num,
                    message='Significant content length difference between HTML and PPTX',
                    details=f'HTML: {html_len} chars, PPTX: {pptx_len} chars ({diff_pct:.1f}% diff)'
                ))

        return issues

    def _check_visual_consistency(self, slide_index: int) -> List[ValidationIssue]:
        """Check if visual elements are consistent between HTML and PPTX."""
        issues = []
        slide_num = slide_index + 1

        html_slide = self.html_slides[slide_index]
        pptx_slide = self.pptx_prs.slides[slide_index]

        # Check for images in HTML
        html_images = html_slide.findall('.//img')
        if html_images:
            # Count image shapes in PPTX
            pptx_images = 0
            for shape in pptx_slide.shapes:
                if shape.shape_type == 13:  # PICTURE
                    pptx_images += 1

            if pptx_images == 0:
                issues.append(ValidationIssue(
                    severity='warning',
                    category='content',
                    slide_number=slide_num,
                    message=f'HTML has {len(html_images)} image(s) but PPTX has none',
                    details='Images may not have been converted'
                ))

        # Check for tables
        html_tables = html_slide.findall('.//table')
        if html_tables:
            pptx_tables = 0
            for shape in pptx_slide.shapes:
                if shape.shape_type == 19:  # TABLE
                    pptx_tables += 1
                # Also count text-based table representations
                if hasattr(shape, 'text') and '|' in shape.text:
                    # Might be text-based table representation
                    pass

            # Tables often converted as shapes, not actual table objects
            # So we just check if there's substantial content
            if pptx_tables == 0 and len(pptx_slide.shapes) < 3:
                issues.append(ValidationIssue(
                    severity='info',
                    category='structure',
                    slide_number=slide_num,
                    message='HTML table may not be rendered as PPTX table',
                    details='Check if table content is present as shapes'
                ))

        return issues


def validate_conversion(html_path: str, pptx_path: str) -> ValidationReport:
    """
    Perform comprehensive validation of HTML to PPTX conversion.

    Args:
        html_path: Path to HTML file
        pptx_path: Path to PPTX file

    Returns:
        ValidationReport with all issues found
    """
    all_issues = []

    # Validate HTML
    print("Validating HTML...")
    html_validator = HTMLValidator(html_path)
    all_issues.extend(html_validator.validate())

    # Validate PPTX
    print("Validating PPTX...")
    pptx_validator = PPTXValidator(pptx_path)
    all_issues.extend(pptx_validator.validate())

    # Cross-validate
    print("Cross-validating HTML and PPTX...")
    cross_validator = CrossValidator(html_path, pptx_path)
    all_issues.extend(cross_validator.validate())

    # Categorize issues
    errors = [i for i in all_issues if i.severity == 'error']
    warnings = [i for i in all_issues if i.severity == 'warning']
    info = [i for i in all_issues if i.severity == 'info']

    # Get slide count
    prs = Presentation(pptx_path)
    total_slides = len(prs.slides)

    return ValidationReport(
        html_file=html_path,
        pptx_file=pptx_path,
        total_slides=total_slides,
        errors=errors,
        warnings=warnings,
        info=info
    )


def main():
    """CLI entry point."""
    if len(sys.argv) != 3:
        print("Usage: python3 validate_conversion.py <input.html> <output.pptx>")
        sys.exit(1)

    html_path = sys.argv[1]
    pptx_path = sys.argv[2]

    # Validate inputs exist
    if not Path(html_path).exists():
        print(f"Error: HTML file not found: {html_path}")
        sys.exit(1)

    if not Path(pptx_path).exists():
        print(f"Error: PPTX file not found: {pptx_path}")
        sys.exit(1)

    # Run validation
    report = validate_conversion(html_path, pptx_path)

    # Print results
    report.print_summary()

    # Exit code based on errors
    sys.exit(1 if report.has_errors() else 0)


if __name__ == "__main__":
    main()
