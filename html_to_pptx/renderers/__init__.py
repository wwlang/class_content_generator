"""Renderer modules for PowerPoint slide generation.

This package contains renderer classes that handle the actual creation
of PowerPoint shapes, text, tables, and layouts.

Renderers:
- BaseRenderer: Abstract base class with common operations
- TextRenderer: Text, titles, paragraphs, lists, quotes
- ShapeRenderer: Cards, grids, stats banners, decorative shapes
- TableRenderer: Tables with styling and formatting
"""

from .base_renderer import BaseRenderer
from .text_renderer import TextRenderer
from .shape_renderer import ShapeRenderer
from .table_renderer import TableRenderer

__all__ = [
    'BaseRenderer',
    'TextRenderer',
    'ShapeRenderer',
    'TableRenderer'
]
