"""
Section break slide handler.

Handles section divider slides with large title on colored background.
"""

from typing import Any
from lxml import etree
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

from .base import SlideHandler
from ..renderers import BaseRenderer, TextRenderer
from ..config import LayoutConfig, FontConfig, ColorConfig


class SectionBreakHandler(SlideHandler):
    """
    Handler for section break slides.

    Section breaks contain:
    - Colored background (orange accent)
    - Large title text (white, bold)
    - Support for <br> tags in title (multi-line)
    """

    @property
    def priority(self) -> int:
        """Section breaks have high priority (checked early)."""
        return 15

    def can_handle(self, html_slide: etree.Element) -> bool:
        """
        Check if this is a section break slide.

        Args:
            html_slide: HTML slide element

        Returns:
            True if slide has 'section-break-slide' class
        """
        return self._has_class(html_slide, 'section-break-slide')

    def handle(self, slide: Any, html_slide: etree.Element) -> None:
        """
        Process section break slide using renderers.

        Args:
            slide: PowerPoint slide to populate
            html_slide: HTML slide element with content
        """
        # Initialize renderers
        base_renderer = BaseRenderer(slide)
        text_renderer = TextRenderer(slide)

        # Apply orange background
        base_renderer.apply_background(ColorConfig.ORANGE)

        # Extract and render section title
        title_elem = html_slide.find('.//*[@class="section-title"]')
        if title_elem is not None:
            # Extract title text (handles <br> tags naturally)
            title_text = self.converter.extract_text_content(title_elem)

            # Use standard title position for visual consistency
            text_renderer.render_section_title(title_text, y=LayoutConfig.TITLE_Y)

        # Extract and render section subtitle if present
        subtitle_elem = html_slide.find('.//*[@class="section-subtitle"]')
        if subtitle_elem is not None:
            from pptx.util import Pt
            from pptx.enum.text import PP_ALIGN

            subtitle_text = self.converter.extract_text_content(subtitle_elem)

            # Position subtitle below title
            subtitle_y = LayoutConfig.TITLE_Y + 0.9  # Below title
            subtitle_box = text_renderer.add_textbox(
                LayoutConfig.PADDING,
                subtitle_y,
                text_renderer.config.SLIDE_WIDTH - 2 * LayoutConfig.PADDING,
                0.5
            )

            p = subtitle_box.text_frame.paragraphs[0]
            p.text = subtitle_text
            p.alignment = PP_ALIGN.LEFT
            p.font.name = FontConfig.BODY_FONT
            p.font.size = Pt(18)
            p.font.color.rgb = ColorConfig.WHITE
