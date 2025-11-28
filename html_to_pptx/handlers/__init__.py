"""
Slide handler modules for different slide types.

Each handler knows how to process a specific slide type (title, content, stats, etc.).
Handlers are registered with the converter and tried in priority order.
"""

from .base import SlideHandler, HandlerRegistry
from .title import TitleSlideHandler
from .section import SectionBreakHandler
from .big_number import BigNumberSlideHandler
from .content import ContentSlideHandler
from .quote_handler import QuoteSlideHandler
from .framework_handler import FrameworkSlideHandler
from .table_handler import VocabTableSlideHandler, ComparisonTableSlideHandler
from .references_handler import ReferencesSlideHandler
from .objectives_handler import ObjectivesSlideHandler
from .checklist_handler import ChecklistSlideHandler
from .reflection_handler import ReflectionSlideHandler


def create_handler_registry(converter):
    """
    Create and populate handler registry with all available handlers.

    Handlers are registered in priority order (lowest priority number first).

    Args:
        converter: HTMLToPPTXConverter instance

    Returns:
        HandlerRegistry with all handlers registered
    """
    registry = HandlerRegistry()

    # Register handlers (will be sorted by priority automatically)
    registry.register(TitleSlideHandler, converter)
    registry.register(QuoteSlideHandler, converter)
    registry.register(ReferencesSlideHandler, converter)
    registry.register(FrameworkSlideHandler, converter)
    registry.register(SectionBreakHandler, converter)
    registry.register(ObjectivesSlideHandler, converter)
    registry.register(ChecklistSlideHandler, converter)
    registry.register(ReflectionSlideHandler, converter)
    registry.register(VocabTableSlideHandler, converter)
    registry.register(ComparisonTableSlideHandler, converter)
    registry.register(BigNumberSlideHandler, converter)
    registry.register(ContentSlideHandler, converter)  # Fallback, lowest priority

    return registry


__all__ = [
    'SlideHandler',
    'HandlerRegistry',
    'TitleSlideHandler',
    'SectionBreakHandler',
    'BigNumberSlideHandler',
    'ContentSlideHandler',
    'QuoteSlideHandler',
    'FrameworkSlideHandler',
    'VocabTableSlideHandler',
    'ComparisonTableSlideHandler',
    'ReferencesSlideHandler',
    'ObjectivesSlideHandler',
    'ChecklistSlideHandler',
    'ReflectionSlideHandler',
    'create_handler_registry',
]
