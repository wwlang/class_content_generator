"""
HTML to PPTX Converter Package

Converts HTML presentation slides to PowerPoint format with professional styling.
"""

from .config import (
    LayoutConfig,
    FontConfig,
    ColorConfig,
    SpacingConfig,
    COLORS,
    SLIDE_WIDTH,
    SLIDE_HEIGHT,
    PADDING,
    HEADER_FONT,
    BODY_FONT,
)

__version__ = '2.0.0'
__all__ = [
    'LayoutConfig',
    'FontConfig',
    'ColorConfig',
    'SpacingConfig',
    'COLORS',
    'SLIDE_WIDTH',
    'SLIDE_HEIGHT',
    'PADDING',
    'HEADER_FONT',
    'BODY_FONT',
]
