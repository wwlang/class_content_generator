"""Table slide handlers for vocabulary and comparison tables."""

from typing import Any, List, Dict
from lxml import etree
from pptx.util import Pt

from .base import SlideHandler
from ..renderers import TextRenderer, TableRenderer, BaseRenderer
from ..config import LayoutConfig, ColorConfig, FontConfig


class VocabTableSlideHandler(SlideHandler):
    """Handler for vocabulary table slides."""

    def __init__(self, converter: Any):
        """Initialize with converter reference."""
        super().__init__(converter)
        self.text_renderer = None
        self.table_renderer = None
        self.base_renderer = None

    @property
    def priority(self) -> int:
        """Vocab tables have medium-high priority."""
        return 40

    def can_handle(self, html_slide: etree.Element) -> bool:
        """Check if this is a vocab table slide."""
        return self._has_class(html_slide, 'vocab-table-slide')

    def handle(self, slide: Any, html_slide: etree.Element) -> None:
        """Process vocab table slide using renderers."""
        # Initialize renderers
        self.text_renderer = TextRenderer(slide)
        self.table_renderer = TableRenderer(slide)
        self.base_renderer = BaseRenderer(slide)

        # Apply background
        self.base_renderer.apply_background(ColorConfig.CREAM)

        # Extract and render title
        title_elem = html_slide.find('.//h2')
        if title_elem is not None:
            title_text = self.converter.extract_text_content(title_elem)
            self.text_renderer.render_slide_title(title_text, is_dark_bg=False)

        # Extract table data
        table_elem = html_slide.find('.//table')
        if table_elem is None:
            return

        vocab_data = []
        rows = table_elem.findall('.//tr')

        # Extract headers to determine table structure
        headers = []
        if rows and rows[0].find('.//th') is not None:
            header_row = rows[0]
            for th in header_row.findall('.//th'):
                headers.append(self.converter.extract_text_content(th))
            start_idx = 1
        else:
            start_idx = 0

        # Extract data rows with flexible column support
        for row in rows[start_idx:]:
            cells = row.findall('.//td')
            if len(cells) >= 2:
                row_data = {}
                # Support both 2-column (term, definition) and 3-column (term, translation, definition)
                if len(cells) >= 3:
                    row_data['term'] = self.converter.extract_text_content(cells[0])
                    row_data['translation'] = self.converter.extract_text_content(cells[1])
                    row_data['definition'] = self.converter.extract_text_content(cells[2])
                else:
                    row_data['term'] = self.converter.extract_text_content(cells[0])
                    row_data['definition'] = self.converter.extract_text_content(cells[1])
                vocab_data.append(row_data)

        # Render table using table renderer
        if vocab_data:
            self.table_renderer.render_vocab_table(
                x=LayoutConfig.PADDING,
                y=LayoutConfig.CONTENT_START_Y,
                width=LayoutConfig.SLIDE_WIDTH - 2 * LayoutConfig.PADDING,
                vocab_data=vocab_data,
                headers=headers if headers else None
            )

        # Add footer
        footer_elem = html_slide.find('.//*[@class="slide-footer"]')
        if footer_elem is not None:
            footer_text = self.converter.extract_text_content(footer_elem)
            self.text_renderer.render_footer(footer_text)


class ComparisonTableSlideHandler(SlideHandler):
    """Handler for comparison table slides."""

    def __init__(self, converter: Any):
        """Initialize with converter reference."""
        super().__init__(converter)
        self.text_renderer = None
        self.table_renderer = None
        self.base_renderer = None

    @property
    def priority(self) -> int:
        """Comparison tables have medium-high priority."""
        return 45

    def can_handle(self, html_slide: etree.Element) -> bool:
        """Check if this is a comparison table slide."""
        return self._has_class(html_slide, 'comparison-table-slide')

    def handle(self, slide: Any, html_slide: etree.Element) -> None:
        """Process comparison table slide using renderers."""
        # Initialize renderers
        self.text_renderer = TextRenderer(slide)
        self.table_renderer = TableRenderer(slide)
        self.base_renderer = BaseRenderer(slide)

        # Apply background
        self.base_renderer.apply_background(ColorConfig.CREAM)

        # Extract and render title
        title_elem = html_slide.find('.//h2')
        if title_elem is not None:
            title_text = self.converter.extract_text_content(title_elem)
            self.text_renderer.render_slide_title(title_text, is_dark_bg=False)

        # Check for intro paragraph(s) before the table
        content_elem = html_slide.find('.//*[@class="slide-content"]')
        table_y = LayoutConfig.CONTENT_START_Y

        if content_elem is not None:
            # Find paragraphs before the table
            intro_paras = []
            for child in content_elem:
                if child.tag == 'p':
                    intro_paras.append(child)
                elif child.tag == 'table':
                    break  # Stop at table

            # Render intro paragraphs if present
            if intro_paras:
                intro_box = self.base_renderer.add_textbox(
                    LayoutConfig.PADDING,
                    LayoutConfig.CONTENT_START_Y,
                    LayoutConfig.SLIDE_WIDTH - 2 * LayoutConfig.PADDING,
                    0.6  # Height for intro text
                )
                tf = intro_box.text_frame
                tf.word_wrap = True

                for i, para_elem in enumerate(intro_paras):
                    para_text = self.converter.extract_text_content(para_elem)
                    if para_text:
                        if i == 0:
                            p = tf.paragraphs[0]
                        else:
                            p = tf.add_paragraph()
                        p.text = para_text
                        p.font.name = FontConfig.BODY_FONT
                        p.font.size = Pt(16)
                        p.font.color.rgb = ColorConfig.DARK_GRAY
                        p.line_spacing = 1.2

                # Adjust table Y position to start after intro
                table_y = LayoutConfig.CONTENT_START_Y + 0.7  # Intro height + gap

        # Extract table data
        table_elem = html_slide.find('.//table')
        if table_elem is None:
            return

        rows = table_elem.findall('.//tr')
        if not rows:
            return

        # Extract headers
        headers = []
        header_row = rows[0]
        for cell in header_row.findall('.//th'):
            headers.append(self.converter.extract_text_content(cell))

        # If no th elements, try td in first row
        if not headers:
            for cell in header_row.findall('.//td'):
                headers.append(self.converter.extract_text_content(cell))

        # Extract data rows
        comparison_data = []
        start_idx = 1 if headers else 0

        for row in rows[start_idx:]:
            cells = row.findall('.//td')
            row_data = {}
            for i, cell in enumerate(cells):
                key = headers[i] if i < len(headers) else f'col_{i}'
                row_data[key] = self.converter.extract_text_content(cell)
            if row_data:
                comparison_data.append(row_data)

        # Calculate table height to leave room for footer
        # Footer is at 7.65, we want 0.3 inches of space before it for the citation
        max_table_bottom = LayoutConfig.FOOTER_Y - 0.5  # Leave space for citation
        table_height = max_table_bottom - table_y

        # Render table using table renderer
        if comparison_data:
            self.table_renderer.render_comparison_table(
                x=LayoutConfig.PADDING,
                y=table_y,
                width=LayoutConfig.SLIDE_WIDTH - 2 * LayoutConfig.PADDING,
                height=table_height,
                comparison_data=comparison_data,
                headers=headers if headers else None
            )

        # Add footer
        footer_elem = html_slide.find('.//*[@class="slide-footer"]')
        if footer_elem is not None:
            footer_text = self.converter.extract_text_content(footer_elem)
            self.text_renderer.render_footer(footer_text)
