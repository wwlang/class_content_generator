"""
Section break slide handler.

Handles section divider slides with large title on colored background.
"""

from typing import Any
from lxml import etree
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor

from .base import SlideHandler
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
        Process section break slide.

        Args:
            slide: PowerPoint slide to populate
            html_slide: HTML slide element with content
        """
        # Add colored background
        background = slide.shapes.add_shape(
            1,  # Rectangle shape
            0, 0,
            self.converter.prs.slide_width,
            self.converter.prs.slide_height
        )
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = ColorConfig.ORANGE  # Brand accent color

        # Move background to back
        slide.shapes._spTree.remove(background._element)
        slide.shapes._spTree.insert(2, background._element)

        # Extract title
        title_elem = html_slide.find('.//*[@class="section-title"]')
        if title_elem is not None:
            title_box = self.converter.add_textbox(
                slide,
                LayoutConfig.PADDING,
                LayoutConfig.SECTION_BREAK_Y,
                self.converter.SLIDE_WIDTH - 2 * LayoutConfig.PADDING,
                LayoutConfig.SECTION_BREAK_HEIGHT
            )
            tf = title_box.text_frame
            tf.word_wrap = True

            # Handle <br> tags by splitting into paragraphs
            # Get text before first <br>
            first_p = tf.paragraphs[0]
            first_p.alignment = PP_ALIGN.LEFT

            if title_elem.text:
                run = first_p.add_run()
                run.text = title_elem.text
                run.font.name = FontConfig.HEADER_FONT
                run.font.size = FontConfig.SECTION_TITLE_SIZE
                run.font.bold = True
                run.font.color.rgb = RGBColor(255, 255, 255)  # White text on colored bg
                run.font.spacing = FontConfig.TITLE_LETTER_SPACING  # Condensed

            # Process <br> elements and text after them
            for br in title_elem:
                if br.tag == 'br':
                    # Add a new paragraph for text after <br>
                    if br.tail:
                        p = tf.add_paragraph()
                        p.alignment = PP_ALIGN.LEFT
                        run = p.add_run()
                        run.text = br.tail
                        run.font.name = FontConfig.HEADER_FONT
                        run.font.size = FontConfig.SECTION_TITLE_SIZE
                        run.font.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)
                        run.font.spacing = FontConfig.TITLE_LETTER_SPACING  # Condensed
