"""Quote slide handler.

Handles quote slides with centered quotes and optional author attribution.
"""

from typing import Any
from lxml import etree

from .base import SlideHandler
from ..renderers import TextRenderer, BaseRenderer
from ..config import LayoutConfig, ColorConfig


class QuoteSlideHandler(SlideHandler):
    """Handler for quote slides with centered text."""

    def __init__(self, converter: Any):
        """Initialize with converter reference.

        Args:
            converter: HTMLToPPTXConverter instance
        """
        super().__init__(converter)
        self.text_renderer = None
        self.base_renderer = None

    @property
    def priority(self) -> int:
        """Quote slides have high priority (specific type)."""
        return 20

    def can_handle(self, html_slide: etree.Element) -> bool:
        """Check if this is a quote slide.

        Args:
            html_slide: HTML slide element

        Returns:
            True if slide has 'quote-slide' class
        """
        return self._has_class(html_slide, 'quote-slide')

    def handle(self, slide: Any, html_slide: etree.Element) -> None:
        """Process quote slide using renderers.

        Args:
            slide: PowerPoint slide to populate
            html_slide: HTML slide element with content
        """
        # Initialize renderers
        self.text_renderer = TextRenderer(slide)
        self.base_renderer = BaseRenderer(slide)

        # Detect dark background
        is_dark = self._has_class(html_slide, 'dark-bg')

        # Apply background
        if is_dark:
            self.base_renderer.apply_background(ColorConfig.DARK_GRAY)
        else:
            self.base_renderer.apply_background(ColorConfig.CREAM)

        # Extract title (optional)
        title_elem = html_slide.find('.//h2')
        if title_elem is not None:
            title_text = self.converter.extract_text_content(title_elem)
            self.text_renderer.render_slide_title(title_text, is_dark_bg=is_dark)

        # Extract quote content
        quote_elem = html_slide.find('.//blockquote')
        if quote_elem is None:
            quote_elem = html_slide.find('.//*[@class="quote-content"]')

        # Fallback: look for slide-content with paragraphs
        quote_text = None
        author = None

        if quote_elem is not None:
            quote_text = self.converter.extract_text_content(quote_elem).strip('"\'')

            # Extract author/citation if present
            cite_elem = html_slide.find('.//cite')
            if cite_elem is None:
                cite_elem = html_slide.find('.//*[@class="quote-author"]')
            if cite_elem is None:
                cite_elem = html_slide.find('.//*[@class="quote-attribution"]')

            if cite_elem is not None:
                author = self.converter.extract_text_content(cite_elem)
        else:
            # Try slide-content with paragraphs pattern
            content_elem = html_slide.find('.//*[@class="slide-content"]')
            if content_elem is not None:
                paragraphs = content_elem.findall('.//p')
                if len(paragraphs) >= 1:
                    # First paragraph is quote text
                    quote_text = self.converter.extract_text_content(paragraphs[0]).strip('"\'')

                    # Second paragraph (if exists) is author
                    if len(paragraphs) >= 2:
                        author_text = self.converter.extract_text_content(paragraphs[1]).strip()
                        # Remove leading em dash if present
                        author = author_text.lstrip('—').lstrip('-').strip()

        # Render quote if we found content
        if quote_text:
            self.text_renderer.render_quote(
                quote_text=quote_text,
                author=author
            )

        # Add footer
        footer_elem = html_slide.find('.//*[@class="slide-footer"]')
        if footer_elem is not None:
            footer_text = self.converter.extract_text_content(footer_elem)
            self.text_renderer.render_footer(footer_text)
