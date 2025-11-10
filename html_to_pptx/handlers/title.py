"""
Title slide handler.

Handles title slides with main title, subtitle, and author information,
along with decorative shapes.
"""

from typing import Any
from lxml import etree
from pptx.enum.text import PP_ALIGN, MSO_VERTICAL_ANCHOR

from .base import SlideHandler
from ..config import LayoutConfig, FontConfig, ColorConfig


class TitleSlideHandler(SlideHandler):
    """
    Handler for title slides.

    Title slides contain:
    - Main title (large, centered-ish)
    - Subtitle (medium size)
    - Author/description (smaller)
    - Decorative shapes at bottom-left
    """

    @property
    def priority(self) -> int:
        """Title slides have high priority (checked early)."""
        return 10

    def can_handle(self, html_slide: etree.Element) -> bool:
        """
        Check if this is a title slide.

        Args:
            html_slide: HTML slide element

        Returns:
            True if slide has 'title-slide' class
        """
        return self._has_class(html_slide, 'title-slide')

    def handle(self, slide: Any, html_slide: etree.Element) -> None:
        """
        Process title slide.

        Args:
            slide: PowerPoint slide to populate
            html_slide: HTML slide element with content
        """
        # Extract elements
        title_elem = html_slide.find('.//*[@class="title-content"]/h1')
        subtitle_elem = html_slide.find('.//*[@class="subtitle"]')
        author_elem = html_slide.find('.//*[@class="author"]')

        # Add title
        if title_elem is not None:
            title_box = self.converter.add_textbox(
                slide,
                LayoutConfig.PADDING,
                2.8,  # Vertically centered
                self.converter.SLIDE_WIDTH - 2 * LayoutConfig.PADDING,
                1.5
            )
            title_box.text_frame.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE
            self.converter.add_text(
                title_box.text_frame,
                self.converter.extract_text_content(title_elem),
                font_name=FontConfig.HEADER_FONT,
                font_size=FontConfig.TITLE_SIZE,
                bold=True,
                color=ColorConfig.DARK_GRAY,  # HTML: var(--color-primary) = #131313
                alignment=PP_ALIGN.LEFT,
                spacing=FontConfig.TITLE_LETTER_SPACING
            )

        # Add subtitle
        if subtitle_elem is not None:
            subtitle_box = self.converter.add_textbox(
                slide,
                LayoutConfig.PADDING,
                4.6,  # Below title (with proper gap)
                self.converter.SLIDE_WIDTH - 2 * LayoutConfig.PADDING,
                0.5
            )
            subtitle_box.text_frame.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP
            self.converter.add_text(
                subtitle_box.text_frame,
                self.converter.extract_text_content(subtitle_elem),
                font_name=FontConfig.BODY_FONT,
                font_size=FontConfig.HEADING_SMALL,
                color=ColorConfig.ORANGE,  # HTML: var(--color-accent) = #ed5e29
                alignment=PP_ALIGN.LEFT
            )

        # Add author
        if author_elem is not None:
            author_box = self.converter.add_textbox(
                slide,
                LayoutConfig.PADDING,
                5.4,  # Below subtitle (with proper gap)
                self.converter.SLIDE_WIDTH - 2 * LayoutConfig.PADDING,
                0.5
            )
            author_box.text_frame.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP
            self.converter.add_text(
                author_box.text_frame,
                self.converter.extract_text_content(author_elem),
                font_name=FontConfig.BODY_FONT,
                font_size=FontConfig.BODY_LARGE,
                color=ColorConfig.MUTED_GRAY,  # HTML: var(--color-muted) = #64748b
                alignment=PP_ALIGN.LEFT
            )

        # Add decorative shapes at bottom-left
        self.converter.add_decorative_shapes(slide, 'bottom-left')
