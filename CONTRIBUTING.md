# Contributing to Class Content Generator

Thank you for your interest in contributing! This guide will help you understand the project structure and how to add new features.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Adding New Features](#adding-new-features)
5. [Code Standards](#code-standards)
6. [Testing Guidelines](#testing-guidelines)
7. [Documentation Requirements](#documentation-requirements)

---

## Quick Reference: File Organization

**Before creating any new file, check this list:**

| What You're Creating | Where It Goes | Examples |
|---------------------|---------------|----------|
| **Technical documentation** | `docs/` | ARCHITECTURE.md, design guides, reference docs |
| **Development tools/scripts** | `tools/` | analyze_pptx_design.py, utilities |
| **Slide type handlers** | `html_to_pptx/handlers/` | timeline.py, chart.py |
| **Configuration constants** | `html_to_pptx/config.py` | Add to existing classes |
| **Helper utilities** | `html_to_pptx/utils/` | text.py, images.py (future) |
| **Test files** | `html_to_pptx/tests/` | test_*.py (future) |
| **Sample HTML/PPTX** | `samples/` | showcase-*.html, demo.pptx |
| **Root-level files** | Root | README.md, CONTRIBUTING.md, main scripts ONLY |

**Key Rule:** If it's not README, CONTRIBUTING, or a main executable script → it belongs in a subdirectory.

---

## Project Overview

This project has two main components:

1. **Course Content Generator** - Generates world-class course materials (syllabus, lectures, tutorials)
2. **HTML to PPTX Converter** - Converts HTML slides to PowerPoint presentations

---

## Getting Started

### Prerequisites

```bash
# Python 3.8+
python3 --version

# Required packages
pip install python-pptx lxml pillow requests
```

### Project Structure

```
class_content_generator/
├── .archive/              # Historical documents (don't modify)
├── .claude/               # Claude Code workflows and commands
├── docs/                  # Documentation and guides
├── tools/                 # Development utilities
├── html_to_pptx/          # Converter package (main development area)
│   ├── config.py          # Configuration constants
│   ├── css_parser.py      # CSS parsing logic
│   ├── handlers/          # Slide type handlers
│   │   ├── base.py        # Abstract base class
│   │   ├── title.py       # Title slide handler
│   │   ├── section.py     # Section break handler
│   │   ├── big_number.py  # Big number handler
│   │   └── content.py     # Content slide handler
│   ├── utils/             # Helper utilities (future)
│   └── tests/             # Unit tests (future)
│
├── courses/               # Generated course content
├── templates/             # Course templates
├── samples/               # Sample files and outputs
├── shared/                # Shared resources
│
├── html_to_pptx_converter.py  # Main converter CLI
├── README.md              # Quick start guide
├── ARCHITECTURE.md        # Technical deep dive
└── CONTRIBUTING.md        # This file
```

---

## Development Workflow

### 1. Branch Strategy

```bash
# For new features
git checkout -b feature/handler-for-xyz

# For bug fixes
git checkout -b fix/border-rendering

# For refactoring
git checkout -b refactor/extract-utilities
```

### 2. Before Making Changes

```bash
# Test current functionality
python3 html_to_pptx_converter.py samples/showcase-enhancements.html test-output.pptx

# Verify output is correct (open test-output.pptx)
```

### 3. Making Changes

Follow the [Code Standards](#code-standards) below.

### 4. Testing Changes

```bash
# Run converter with test files
python3 html_to_pptx_converter.py samples/showcase-enhancements.html test-output.pptx

# Visual inspection (compare to previous version)
# Unit tests (when test suite exists)
```

### 5. Committing

```bash
git add [files]
git commit -m "Clear description of changes"
```

---

## Adding New Features

### Adding a New Slide Type Handler

**Example: Adding a "Timeline Slide" handler**

#### Step 1: Create Handler File

Create `html_to_pptx/handlers/timeline.py`:

```python
"""
Timeline slide handler.

Handles timeline slides with chronological events.
"""

from typing import Any
from lxml import etree

from .base import SlideHandler
from ..config import LayoutConfig, FontConfig, ColorConfig


class TimelineSlideHandler(SlideHandler):
    """Handler for timeline slides."""

    @property
    def priority(self) -> int:
        """Timeline slides have high priority."""
        return 25

    def can_handle(self, html_slide: etree.Element) -> bool:
        """Check if this is a timeline slide."""
        return self._has_class(html_slide, 'timeline-slide')

    def handle(self, slide: Any, html_slide: etree.Element) -> None:
        """Process timeline slide."""
        # Implementation here
        # Use self.converter for helper methods
        # Use LayoutConfig, FontConfig, ColorConfig for constants
        pass
```

#### Step 2: Register Handler

Edit `html_to_pptx/handlers/__init__.py`:

```python
# Add import
from .timeline import TimelineSlideHandler

# Add to create_handler_registry() function
def create_handler_registry(converter):
    registry = HandlerRegistry()

    # ... existing handlers ...
    registry.register(TimelineSlideHandler, converter)  # ADD THIS

    return registry

# Add to __all__
__all__ = [
    # ... existing exports ...
    'TimelineSlideHandler',  # ADD THIS
]
```

#### Step 3: Test

```python
# Create test HTML with class="timeline-slide"
# Run converter
# Verify handler is called
```

**That's it!** No changes to main converter needed.

---

### Adding Configuration Constants

**Example: Adding timeline-specific layout constants**

Edit `html_to_pptx/config.py`:

```python
class LayoutConfig:
    # ... existing constants ...

    # Timeline slide
    TIMELINE_EVENT_HEIGHT = 0.6
    TIMELINE_EVENT_GAP = 0.3
    TIMELINE_LINE_Y = 3.0
```

Use in your handler:
```python
event_height = LayoutConfig.TIMELINE_EVENT_HEIGHT
```

---

### Adding Helper Methods to Base Handler

If multiple handlers need the same functionality:

Edit `html_to_pptx/handlers/base.py`:

```python
class SlideHandler(ABC):
    # ... existing methods ...

    def _extract_list_items(self, element: etree.Element) -> list:
        """Helper: Extract all <li> items from element."""
        return element.xpath('.//li')
```

Use in any handler:
```python
items = self._extract_list_items(container_elem)
```

---

## Code Standards

### File Organization

**STRICT LIMITS:**
- ✅ **Maximum 500 lines per file**
- ✅ **Maximum 50 lines per function**
- ✅ **One class per file** (with exceptions for small helper classes)

**If you exceed these limits, refactor into smaller modules.**

---

### Configuration Over Code

**❌ BAD:**
```python
title_box = self.add_textbox(slide, 0.625, 0.7, 9.42, 0.7)
run.font.size = Pt(36)
run.font.color.rgb = RGBColor(237, 94, 41)
```

**✅ GOOD:**
```python
title_box = self.add_textbox(
    slide,
    LayoutConfig.PADDING,
    LayoutConfig.TITLE_Y,
    self.SLIDE_WIDTH - 2 * LayoutConfig.PADDING,
    LayoutConfig.TITLE_HEIGHT
)
run.font.size = FontConfig.HEADING_MEDIUM
run.font.color.rgb = ColorConfig.ORANGE
```

**Why:** Easy to change styling in one place, semantic names, no magic numbers.

---

### Type Hints Required

**❌ BAD:**
```python
def create_box(slide, x, y):
    return slide.shapes.add_shape(1, x, y, 2, 1)
```

**✅ GOOD:**
```python
from typing import Any
from pptx.shapes.base import BaseShape

def create_box(slide: Any, x: float, y: float) -> BaseShape:
    """Create a rectangular shape at specified position."""
    return slide.shapes.add_shape(1, x, y, 2, 1)
```

---

### Docstrings Required

**All public methods must have docstrings:**

```python
def parse_grid_layout(self, html_element: etree.Element) -> list[float]:
    """
    Parse CSS grid layout and return column widths.

    Args:
        html_element: HTML element with grid layout

    Returns:
        List of column width fractions that sum to 1.0

    Example:
        >>> widths = parser.parse_grid_layout(grid_elem)
        >>> widths
        [0.33, 0.33, 0.34]  # Three equal columns
    """
```

**Style:** Google-style docstrings

---

### Descriptive Names

**❌ BAD:**
```python
x = 1.9
y_start = x + 0.6
tb = slide.add_textbox(x, y_start, w, h)
```

**✅ GOOD:**
```python
title_bottom_y = LayoutConfig.TITLE_Y + LayoutConfig.TITLE_HEIGHT
content_start_y = title_bottom_y + LayoutConfig.TITLE_CONTENT_GAP
title_box = slide.add_textbox(
    LayoutConfig.PADDING,
    content_start_y,
    content_width,
    content_height
)
```

---

### Import Organization

```python
# Standard library imports
import re
from typing import Any, Optional

# Third-party imports
from lxml import etree
from pptx.util import Pt

# Local application imports
from .base import SlideHandler
from ..config import LayoutConfig, FontConfig, ColorConfig
```

**Order:** Standard library → Third-party → Local

---

### Error Handling

**Create specific exceptions:**

```python
class SlideHandlerError(Exception):
    """Base exception for slide handler errors."""
    pass

class UnsupportedLayoutError(SlideHandlerError):
    """Raised when slide layout is not supported."""
    pass
```

**Use with context:**

```python
if not self.can_handle(html_slide):
    raise UnsupportedLayoutError(
        f"Handler {self.__class__.__name__} cannot process "
        f"slide with classes: {html_slide.get('class', 'none')}"
    )
```

---

## Testing Guidelines

### Manual Testing (Current)

**Test with both sample files:**

```bash
# Test 1: Showcase enhancements
python3 html_to_pptx_converter.py \
    samples/showcase-enhancements.html \
    test-output-1.pptx

# Test 2: Enhanced samples (from archive)
python3 html_to_pptx_converter.py \
    docs/.archive/slide-technical/skill-backup/resources/examples/enhanced-sample-slides.html \
    test-output-2.pptx

# Visual inspection
# - Open both PPTX files
# - Check all 12 slides render correctly
# - Compare to previous version (if available)
```

### Unit Testing (Future)

**When writing unit tests:**

```python
# html_to_pptx/tests/test_timeline_handler.py
import pytest
from html_to_pptx.handlers.timeline import TimelineSlideHandler
from tests.mocks import MockConverter, MockSlide

def test_timeline_handler_can_handle():
    """Test that handler identifies timeline slides correctly."""
    converter = MockConverter()
    handler = TimelineSlideHandler(converter)

    # Positive test
    timeline_slide = create_html_element('div', classes=['slide', 'timeline-slide'])
    assert handler.can_handle(timeline_slide) == True

    # Negative test
    regular_slide = create_html_element('div', classes=['slide'])
    assert handler.can_handle(regular_slide) == False

def test_timeline_handler_renders_events():
    """Test that handler renders timeline events correctly."""
    converter = MockConverter()
    handler = TimelineSlideHandler(converter)
    slide = MockSlide()
    html = create_timeline_html(['2020: Event 1', '2021: Event 2'])

    handler.handle(slide, html)

    assert len(slide.shapes) == 2  # Two timeline events
    # More assertions...
```

**Run tests:**
```bash
pytest html_to_pptx/tests/
```

---

## Documentation Requirements

### When to Update Documentation

**You must update documentation when:**

1. **Adding new handler** → Update ARCHITECTURE.md "Handler Catalog"
2. **Adding config constants** → Update ARCHITECTURE.md "Configuration Reference"
3. **Changing directory structure** → Update README.md "Project Structure"
4. **Adding new feature** → Update README.md feature list
5. **Breaking changes** → Update CHANGELOG.md
6. **New dependencies** → Update README.md prerequisites

### Documentation Files

| File | Purpose | Update When |
|------|---------|-------------|
| `README.md` | Quick start, features overview | New features, structure changes |
| `docs/ARCHITECTURE.md` | Technical deep dive | New handlers, major refactoring |
| `CONTRIBUTING.md` | This file | New development processes |
| `CHANGELOG.md` | Version history | Each release |
| `.claude/CLAUDE.md` | Workflow documentation | New slash commands, workflows |

### Example Documentation Update

**After adding TimelineSlideHandler:**

Edit `docs/ARCHITECTURE.md`:

```markdown
## Handler Catalog

### TimelineSlideHandler

**File:** `html_to_pptx/handlers/timeline.py`
**Priority:** 25
**Detects:** `<div class="slide timeline-slide">`

**Purpose:** Renders chronological timeline with events.

**HTML Structure:**
\`\`\`html
<div class="slide timeline-slide">
  <h2>Project Timeline</h2>
  <div class="timeline-events">
    <div class="event" data-year="2020">Event 1</div>
    <div class="event" data-year="2021">Event 2</div>
  </div>
</div>
\`\`\`

**Output:** Timeline with horizontal line and event markers.
```

---

## Code Review Checklist

Before submitting changes, verify:

**Structure:**
- [ ] No file over 500 lines
- [ ] No function over 50 lines
- [ ] No code duplication (DRY)
- [ ] Proper module organization

**Quality:**
- [ ] All functions have type hints
- [ ] All public methods have docstrings
- [ ] No magic numbers (all in config)
- [ ] Descriptive variable names
- [ ] PEP 8 compliant

**Testing:**
- [ ] Manual testing with both sample files
- [ ] All slides render correctly
- [ ] No visual regressions

**Documentation:**
- [ ] README updated if needed
- [ ] ARCHITECTURE.md updated if new handler
- [ ] Code comments for complex logic
- [ ] CHANGELOG.md updated

---

## Questions?

- **Architecture questions:** See `docs/ARCHITECTURE.md`
- **Workflow questions:** See `.claude/CLAUDE.md`
- **Project questions:** See `README.md`

---

## Commit Message Guidelines

**Format:**
```
<type>: <short summary>

<optional detailed description>

<optional footer>
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code restructuring
- `docs:` Documentation changes
- `test:` Adding tests
- `chore:` Maintenance tasks

**Examples:**

```
feat: add timeline slide handler

- Created TimelineSlideHandler class
- Added timeline layout constants
- Registered in handler factory
```

```
fix: correct grid item spacing calculation

Grid items were overlapping due to incorrect gap calculation.
Changed from pixels to inches conversion.

Fixes visual regression in 3-column layouts.
```

---

**Thank you for contributing to making this project better!**
