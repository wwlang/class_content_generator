"""Utility modules for HTML to PPTX converter.

This package contains helper modules for common operations:
- font_helpers: Font and color styling utilities
- xml_helpers: XML manipulation for PowerPoint formatting
- layout_helpers: Layout calculation utilities
"""

from .font_helpers import FontStyler
from .xml_helpers import XMLHelper, IndentationPresets
from .layout_helpers import LayoutCalculator, LayoutBox, GridLayoutPresets

__all__ = [
    'FontStyler',
    'XMLHelper',
    'IndentationPresets',
    'LayoutCalculator',
    'LayoutBox',
    'GridLayoutPresets'
]
