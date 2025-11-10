"""
Content slide handler.

Handles standard content slides with titles, bullets, cards, stats, grids, etc.
This is the default/fallback handler for most slide types.
"""

from typing import Any
from lxml import etree

from .base import SlideHandler


class ContentSlideHandler(SlideHandler):
    """
    Handler for content slides.

    Content slides are the most complex and include:
    - Title + body text
    - Bullet lists
    - Card layouts
    - Stats banners
    - Grid layouts
    - Objectives

    This handler delegates to the main converter's handle_content_slide()
    method which contains all the complex logic for these various layouts.

    Future refactoring can break this into sub-handlers for each layout type.
    """

    @property
    def priority(self) -> int:
        """
        Content slides have low priority (fallback/default).

        They are tried last since they handle everything that doesn't
        match a more specific handler.
        """
        return 100

    def can_handle(self, html_slide: etree.Element) -> bool:
        """
        Check if this is a content slide.

        Content slides are identified by the 'content-slide' class,
        but this handler also serves as fallback for unmatched slides.

        Args:
            html_slide: HTML slide element

        Returns:
            True if slide has 'content-slide' class or 'objectives-slide'
        """
        return (
            self._has_class(html_slide, 'content-slide') or
            self._has_class(html_slide, 'objectives-slide')
        )

    def handle(self, slide: Any, html_slide: etree.Element) -> None:
        """
        Process content slide.

        Delegates to the main converter's handle_content_slide() method
        which contains all the complex layout logic.

        Args:
            slide: PowerPoint slide to populate
            html_slide: HTML slide element with content
        """
        # Delegate to existing method in main converter
        # This method handles:
        # - Dark/light backgrounds
        # - Title rendering
        # - Card layouts
        # - Stats banners
        # - Grid layouts
        # - Bullet lists
        # - Objectives
        self.converter.handle_content_slide(slide, html_slide)
