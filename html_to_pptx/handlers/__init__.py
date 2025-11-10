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
    registry.register(SectionBreakHandler, converter)
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
    'create_handler_registry',
]
