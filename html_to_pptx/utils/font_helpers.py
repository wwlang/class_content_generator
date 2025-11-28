"""Font styling and color application utilities.

This module provides helper functions for applying consistent font styling,
colors, and formatting to PowerPoint text runs and paragraphs.
"""

from typing import List, Optional
from pptx.text.text import _Run
from pptx.util import Pt
from ..config import FontConfig, ColorConfig


class FontStyler:
    """Utilities for applying font styles, sizes, and colors to text runs."""

    @staticmethod
    def apply_body_font_styling(
        runs: List[_Run],
        font_name: str = FontConfig.BODY_FONT,
        font_size: Pt = Pt(16),
        is_dark_bg: bool = False
    ) -> None:
        """Apply consistent body font styling to all runs.

        Args:
            runs: List of text runs to style
            font_name: Font family to apply
            font_size: Font size in points
            is_dark_bg: Whether background is dark (affects text color)
        """
        for run in runs:
            # Apply font name if not already set
            if not run.font.name:
                run.font.name = font_name

            # Apply font size if not already set
            if not run.font.size:
                run.font.size = font_size

            # Apply appropriate color based on bold status and background
            FontStyler.apply_text_color(run, is_dark_bg)

    @staticmethod
    def apply_text_color(run: _Run, is_dark_bg: bool = False) -> None:
        """Apply appropriate text color based on bold status and background.

        Args:
            run: Text run to color
            is_dark_bg: Whether background is dark
        """
        # Check if color is already set (safely)
        try:
            if run.font.color.rgb:
                return  # Color already set, don't override
        except AttributeError:
            pass  # Color not set, continue to set it

        # Bold text is always orange (accent color)
        if run.font.bold:
            run.font.color.rgb = ColorConfig.ORANGE
        else:
            # Regular text color depends on background
            if is_dark_bg:
                run.font.color.rgb = ColorConfig.CREAM
            else:
                run.font.color.rgb = ColorConfig.DARK_GRAY

    @staticmethod
    def apply_bold_orange_color(runs: List[_Run]) -> None:
        """Apply orange accent color to all bold text runs.

        Args:
            runs: List of text runs to process
        """
        for run in runs:
            if run.font.bold and not run.font.color.rgb:
                run.font.color.rgb = ColorConfig.ORANGE

    @staticmethod
    def apply_header_font_styling(
        runs: List[_Run],
        font_size: Pt = FontConfig.HEADING_MEDIUM,
        is_dark_bg: bool = False
    ) -> None:
        """Apply header font styling to all runs.

        Args:
            runs: List of text runs to style
            font_size: Font size for header
            is_dark_bg: Whether background is dark
        """
        for run in runs:
            run.font.name = FontConfig.HEADER_FONT
            run.font.size = font_size
            run.font.bold = True

            # Apply color based on background
            if is_dark_bg:
                run.font.color.rgb = ColorConfig.CREAM
            else:
                run.font.color.rgb = ColorConfig.DARK_GRAY

    @staticmethod
    def apply_conditional_styling(
        runs: List[_Run],
        font_name: Optional[str] = None,
        font_size: Optional[Pt] = None,
        bold: Optional[bool] = None,
        color_rgb: Optional[tuple] = None
    ) -> None:
        """Apply selective styling properties to runs.

        Only applies properties that are not None.

        Args:
            runs: List of text runs to style
            font_name: Optional font family
            font_size: Optional font size
            bold: Optional bold setting
            color_rgb: Optional RGB color tuple
        """
        for run in runs:
            if font_name is not None:
                run.font.name = font_name

            if font_size is not None:
                run.font.size = font_size

            if bold is not None:
                run.font.bold = bold

            if color_rgb is not None:
                run.font.color.rgb = color_rgb

    @staticmethod
    def ensure_minimum_styling(
        runs: List[_Run],
        default_font: str = FontConfig.BODY_FONT,
        default_size: Pt = Pt(16)
    ) -> None:
        """Ensure all runs have at least basic font and size set.

        Args:
            runs: List of text runs to check
            default_font: Default font if none set
            default_size: Default size if none set
        """
        for run in runs:
            if not run.font.name:
                run.font.name = default_font

            if not run.font.size:
                run.font.size = default_size

    @staticmethod
    def apply_footer_styling(
        run: _Run,
        is_dark_bg: bool = False,
        is_slide_number: bool = False
    ) -> None:
        """Apply footer text styling (small, bottom of slide).

        Args:
            run: Text run to style
            is_dark_bg: Whether slide has dark background
            is_slide_number: Whether this is slide number (orange) vs course name
        """
        run.font.name = FontConfig.BODY_FONT
        run.font.size = FontConfig.FOOTER_SIZE

        if is_slide_number:
            run.font.color.rgb = ColorConfig.ORANGE
        else:
            run.font.color.rgb = ColorConfig.CREAM if is_dark_bg else ColorConfig.DARK_GRAY

    @staticmethod
    def apply_muted_text_styling(
        run: _Run,
        font_size: Pt = Pt(16),
        bold: bool = False
    ) -> None:
        """Apply muted gray text styling (secondary text).

        Args:
            run: Text run to style
            font_size: Font size (default 16pt)
            bold: Whether text should be bold
        """
        run.font.name = FontConfig.BODY_FONT
        run.font.size = font_size
        run.font.bold = bold
        run.font.color.rgb = ColorConfig.MUTED_GRAY

    @staticmethod
    def apply_standard_body_styling(
        run: _Run,
        font_size: Pt = Pt(16),
        is_dark_bg: bool = False,
        bold: bool = False
    ) -> None:
        """Apply standard body text styling.

        Args:
            run: Text run to style
            font_size: Font size (default 16pt)
            is_dark_bg: Whether background is dark
            bold: Whether text should be bold
        """
        run.font.name = FontConfig.BODY_FONT
        run.font.size = font_size
        run.font.bold = bold

        if bold:
            run.font.color.rgb = ColorConfig.ORANGE
        elif is_dark_bg:
            run.font.color.rgb = ColorConfig.CREAM
        else:
            run.font.color.rgb = ColorConfig.DARK_GRAY

    @staticmethod
    def apply_heading_styling(
        run: _Run,
        font_size: Pt = FontConfig.HEADING_MEDIUM,
        is_dark_bg: bool = False
    ) -> None:
        """Apply heading text styling (header font, larger size).

        Args:
            run: Text run to style
            font_size: Font size for heading
            is_dark_bg: Whether background is dark
        """
        run.font.name = FontConfig.HEADER_FONT
        run.font.size = font_size
        run.font.bold = True

        if is_dark_bg:
            run.font.color.rgb = ColorConfig.CREAM
        else:
            run.font.color.rgb = ColorConfig.DARK_GRAY
