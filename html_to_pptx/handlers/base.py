"""
Base abstract class for slide handlers.

All slide type handlers inherit from SlideHandler and implement
the handle() method for their specific slide type.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from lxml import etree


class SlideHandler(ABC):
    """
    Abstract base class for slide handlers.

    Each slide type (title, content, stats, etc.) has a concrete handler
    that knows how to convert that HTML slide type to PowerPoint format.
    """

    def __init__(self, converter: Any):
        """
        Initialize handler with reference to main converter.

        Args:
            converter: HTMLToPPTXConverter instance that provides
                      helper methods and configuration access
        """
        self.converter = converter

    @abstractmethod
    def can_handle(self, html_slide: etree.Element) -> bool:
        """
        Determine if this handler can process the given HTML slide.

        Args:
            html_slide: lxml HTML element representing the slide

        Returns:
            True if this handler should process this slide type
        """
        pass

    @abstractmethod
    def handle(self, slide: Any, html_slide: etree.Element) -> None:
        """
        Process the HTML slide and populate the PowerPoint slide.

        Args:
            slide: python-pptx slide object to populate
            html_slide: lxml HTML element with slide content
        """
        pass

    @property
    def priority(self) -> int:
        """
        Handler priority for registration order.

        Lower numbers = higher priority. Handlers are tried in priority order.
        Most specific handlers should have lower numbers.

        Returns:
            Priority value (default: 100)
        """
        return 100

    def _has_class(self, element: etree.Element, class_name: str) -> bool:
        """
        Helper: Check if element has specific CSS class.

        Args:
            element: lxml element to check
            class_name: CSS class name to look for

        Returns:
            True if element has the class
        """
        classes = element.get('class', '').split()
        return class_name in classes

    def _is_dark_background(self, html_slide: etree.Element) -> bool:
        """
        Helper: Determine if slide should have dark background.

        Args:
            html_slide: lxml HTML slide element

        Returns:
            True if slide has dark-bg class
        """
        return self._has_class(html_slide, 'dark-bg')


class HandlerRegistry:
    """
    Registry for slide handlers.

    Maintains ordered list of handlers and finds appropriate handler
    for each slide based on can_handle() checks.
    """

    def __init__(self):
        """Initialize empty handler registry."""
        self.handlers = []

    def register(self, handler_class: type, converter: Any) -> None:
        """
        Register a handler class.

        Args:
            handler_class: SlideHandler subclass to register
            converter: Converter instance to pass to handler
        """
        handler = handler_class(converter)
        self.handlers.append(handler)
        # Sort by priority (lower numbers first)
        self.handlers.sort(key=lambda h: h.priority)

    def get_handler(self, html_slide: etree.Element) -> Optional[SlideHandler]:
        """
        Find appropriate handler for HTML slide.

        Tries handlers in priority order, returns first that can handle.

        Args:
            html_slide: lxml HTML element representing slide

        Returns:
            SlideHandler instance that can process this slide, or None
        """
        for handler in self.handlers:
            if handler.can_handle(html_slide):
                return handler
        return None

    def handle_slide(self, slide: Any, html_slide: etree.Element) -> bool:
        """
        Process slide using appropriate handler.

        Args:
            slide: python-pptx slide object
            html_slide: lxml HTML element

        Returns:
            True if slide was handled, False if no handler found
        """
        handler = self.get_handler(html_slide)
        if handler:
            handler.handle(slide, html_slide)
            return True
        return False
