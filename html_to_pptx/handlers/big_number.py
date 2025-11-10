"""
Big number slide handler.

Handles slides with large centered statistic/number and explanation text.
"""

from typing import Any
from lxml import etree
from pptx.enum.text import PP_ALIGN, MSO_VERTICAL_ANCHOR

from .base import SlideHandler
from ..config import LayoutConfig, FontConfig, ColorConfig


class BigNumberSlideHandler(SlideHandler):
    """
    Handler for big number slides.

    Big number slides contain:
    - Large centered number (135pt, orange)
    - Explanation text below (medium size, muted gray)
    - Cream background
    """

    @property
    def priority(self) -> int:
        """Big number slides have high priority (checked early)."""
        return 20

    def can_handle(self, html_slide: etree.Element) -> bool:
        """
        Check if this is a big number slide.

        Args:
            html_slide: HTML slide element

        Returns:
            True if slide has 'big-number-slide' class
        """
        return self._has_class(html_slide, 'big-number-slide')

    def handle(self, slide: Any, html_slide: etree.Element) -> None:
        """
        Process big number slide.

        Args:
            slide: PowerPoint slide to populate
            html_slide: HTML slide element with content
        """
        # Apply cream background
        self.converter.apply_slide_background(slide, ColorConfig.CREAM)

        # Find number content container
        number_content = html_slide.find('.//*[@class="number-content"]')
        if number_content is None:
            return

        # Extract and render big number
        big_number_elem = number_content.find('.//*[@class="big-number"]')
        if big_number_elem is not None:
            number_text = self.converter.extract_text_content(big_number_elem).strip()

            # Create centered text box for big number
            number_box = self.converter.add_textbox(
                slide,
                1.0,  # Centered horizontally with padding
                LayoutConfig.BIG_NUMBER_Y,
                self.converter.SLIDE_WIDTH - 2.0,
                LayoutConfig.BIG_NUMBER_HEIGHT
            )
            tf = number_box.text_frame
            tf.word_wrap = False
            tf.vertical_anchor = MSO_VERTICAL_ANCHOR.MIDDLE

            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER

            run = p.add_run()
            run.text = number_text
            run.font.name = FontConfig.HEADER_FONT
            run.font.size = FontConfig.BIG_NUMBER_SIZE
            run.font.bold = True
            run.font.color.rgb = ColorConfig.ORANGE

        # Extract and render explanation text
        explanation_elem = number_content.find('.//*[@class="number-explanation"]')
        if explanation_elem is not None:
            explanation_text = self.converter.extract_text_content(explanation_elem).strip()

            # Create text box for explanation below number
            explanation_box = self.converter.add_textbox(
                slide,
                1.0,
                LayoutConfig.BIG_NUMBER_Y + LayoutConfig.BIG_NUMBER_EXPLANATION_Y_OFFSET,
                self.converter.SLIDE_WIDTH - 2.0,
                LayoutConfig.BIG_NUMBER_EXPLANATION_HEIGHT
            )
            tf = explanation_box.text_frame
            tf.word_wrap = True

            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER

            run = p.add_run()
            run.text = explanation_text
            run.font.name = FontConfig.BODY_FONT
            run.font.size = FontConfig.BODY_MEDIUM
            run.font.color.rgb = ColorConfig.MUTED_GRAY
