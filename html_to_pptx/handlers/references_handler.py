"""References slide handler.

Handles academic references/citations slides with proper formatting.
"""

from typing import Any
from lxml import etree
from pptx.util import Pt, Inches
from pptx.enum.text import MSO_VERTICAL_ANCHOR

from .base import SlideHandler
from ..renderers import TextRenderer, BaseRenderer
from ..config import LayoutConfig, ColorConfig, FontConfig, SpacingConfig


class ReferencesSlideHandler(SlideHandler):
    """Handler for references/citations slides."""

    def __init__(self, converter: Any):
        """Initialize with converter reference.

        Args:
            converter: HTMLToPPTXConverter instance
        """
        super().__init__(converter)

    @property
    def priority(self) -> int:
        """References slides have medium-high priority."""
        return 25

    def can_handle(self, html_slide: etree.Element) -> bool:
        """Check if this is a references slide.

        Args:
            html_slide: HTML slide element

        Returns:
            True if slide has 'references-slide' class or contains references list
        """
        # Check for explicit references-slide class
        if self._has_class(html_slide, 'references-slide'):
            return True

        # Check for references container
        refs_container = html_slide.find('.//*[@class="references"]')
        if refs_container is not None:
            return True

        return False

    def handle(self, slide: Any, html_slide: etree.Element) -> None:
        """Process references slide.

        Args:
            slide: PowerPoint slide to populate
            html_slide: HTML slide element with content
        """
        # Initialize renderers
        base_renderer = BaseRenderer(slide)
        text_renderer = TextRenderer(slide)

        # Apply cream background
        base_renderer.apply_background(ColorConfig.CREAM)

        # Find references list FIRST (before adding title)
        refs_list = self._find_references_list(html_slide)

        if not refs_list:
            # No references found, fall back to content slide handling
            self.converter.handle_content_slide(slide, html_slide)
            return

        # Add title using TextRenderer
        title_elem = html_slide.find('.//*[@class="slide-title"]')
        if title_elem is None:
            title_elem = html_slide.find('.//h2')

        if title_elem is not None:
            title_text = self.converter.extract_text_content(title_elem)
            text_renderer.render_slide_title(title_text, is_dark_bg=False)

        # Create references text box
        refs_box = base_renderer.add_textbox(
            LayoutConfig.PADDING,
            LayoutConfig.CONTENT_START_Y,
            LayoutConfig.SLIDE_WIDTH - 2 * LayoutConfig.PADDING,
            LayoutConfig.SLIDE_HEIGHT - LayoutConfig.CONTENT_START_Y - 0.8
        )
        refs_frame = refs_box.text_frame
        refs_frame.word_wrap = True
        refs_frame.vertical_anchor = MSO_VERTICAL_ANCHOR.TOP

        # Add each reference
        for i, ref_item in enumerate(refs_list):
            ref_text = ''.join(ref_item.itertext()).strip()

            if not ref_text:
                continue

            # Add paragraph for this reference
            if i == 0:
                p = refs_frame.paragraphs[0]
            else:
                p = refs_frame.add_paragraph()

            p.text = ref_text
            p.font.name = FontConfig.BODY_FONT
            p.font.size = Pt(14)
            p.font.color.rgb = ColorConfig.DARK_GRAY
            p.line_spacing = SpacingConfig.LINE_SPACING
            p.space_before = SpacingConfig.REFERENCE_SPACE_BEFORE
            p.space_after = SpacingConfig.REFERENCE_SPACE_AFTER
            p.level = 0

        # Add footer if present
        footer_elem = html_slide.find('.//*[@class="slide-footer"]')
        if footer_elem is not None:
            footer_text = self.converter.extract_text_content(footer_elem)
            text_renderer.render_footer(footer_text)

    def _find_references_list(self, html_slide: etree.Element) -> list:
        """Find references list in HTML slide.

        Args:
            html_slide: HTML slide element

        Returns:
            List of reference items or empty list if none found
        """
        # Try references container first
        refs_container = html_slide.find('.//*[@class="references"]')
        if refs_container is not None:
            refs_list = refs_container.findall('.//li')
            if refs_list:
                return refs_list
            # Try paragraphs instead
            refs_list = refs_container.findall('.//p')
            if refs_list:
                return refs_list

        # Look for ordered/unordered list that might contain references
        for list_elem in html_slide.findall('.//ol') + html_slide.findall('.//ul'):
            items = list_elem.findall('.//li')
            if items and len(items) >= 2:  # At least 2 references
                # Check if they look like citations (contain year in parens)
                first_item_text = ''.join(items[0].itertext())
                if '(' in first_item_text and ')' in first_item_text:
                    return items

        return []
