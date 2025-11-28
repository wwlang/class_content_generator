"""XML manipulation utilities for PowerPoint formatting.

This module provides helper functions for XML-level manipulation of PowerPoint
elements, particularly for bullets, numbering, and indentation which require
direct XML access.
"""

from typing import Optional
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls


class XMLHelper:
    """Utilities for XML-level PowerPoint formatting."""

    @staticmethod
    def add_bullet(paragraph, marker: str = '•', font_name: str = 'Plus Jakarta Sans') -> None:
        """Add bullet formatting to paragraph via XML.

        Args:
            paragraph: PowerPoint paragraph object
            marker: Bullet character to use
            font_name: Font for bullet character
        """
        pPr = paragraph._element.get_or_add_pPr()

        # Add bullet character XML element
        buChar_xml = f'<a:buChar {nsdecls("a")} char="{marker}"/>'
        buChar = parse_xml(buChar_xml)
        pPr.append(buChar)

        # Add bullet font XML element
        buFont_xml = f'<a:buFont {nsdecls("a")} typeface="{font_name}"/>'
        buFont = parse_xml(buFont_xml)
        pPr.append(buFont)

    @staticmethod
    def add_numbering(paragraph, style: str = 'arabicPeriod') -> None:
        """Add auto-numbering to paragraph via XML.

        Args:
            paragraph: PowerPoint paragraph object
            style: Numbering style (arabicPeriod, arabicParenR, etc.)
        """
        pPr = paragraph._element.get_or_add_pPr()

        # Add autonumbering XML element
        buAutoNum_xml = f'<a:buAutoNum {nsdecls("a")} type="{style}"/>'
        buAutoNum = parse_xml(buAutoNum_xml)
        pPr.append(buAutoNum)

    @staticmethod
    def set_indentation(
        paragraph,
        left_margin: int,
        hanging_indent: int,
        level: int = 0
    ) -> None:
        """Set paragraph indentation via XML.

        Args:
            paragraph: PowerPoint paragraph object
            left_margin: Left margin in EMUs (914400 EMUs = 1 inch)
            hanging_indent: Hanging indent in EMUs (negative for hanging)
            level: Indentation level (0-8)
        """
        pPr = paragraph._element.get_or_add_pPr()
        pPr.set('marL', str(left_margin))
        pPr.set('indent', str(hanging_indent))
        pPr.set('lvl', str(level))

    @staticmethod
    def add_bullet_with_indent(
        paragraph,
        marker: str = '•',
        font_name: str = 'Plus Jakarta Sans',
        left_margin_inches: float = 0.38,
        hanging_indent_inches: float = -0.25
    ) -> None:
        """Add bullet with proper indentation (convenience method).

        Args:
            paragraph: PowerPoint paragraph object
            marker: Bullet character
            font_name: Font for bullet
            left_margin_inches: Left margin in inches
            hanging_indent_inches: Hanging indent in inches (negative)
        """
        # Convert inches to EMUs (914400 EMUs = 1 inch)
        left_margin_emus = int(left_margin_inches * 914400)
        hanging_indent_emus = int(hanging_indent_inches * 914400)

        # Set indentation
        XMLHelper.set_indentation(paragraph, left_margin_emus, hanging_indent_emus)

        # Add bullet
        XMLHelper.add_bullet(paragraph, marker, font_name)

    @staticmethod
    def add_numbering_with_indent(
        paragraph,
        style: str = 'arabicPeriod',
        left_margin_inches: float = 0.38,
        hanging_indent_inches: float = -0.25
    ) -> None:
        """Add numbering with proper indentation (convenience method).

        Args:
            paragraph: PowerPoint paragraph object
            style: Numbering style
            left_margin_inches: Left margin in inches
            hanging_indent_inches: Hanging indent in inches (negative)
        """
        # Convert inches to EMUs
        left_margin_emus = int(left_margin_inches * 914400)
        hanging_indent_emus = int(hanging_indent_inches * 914400)

        # Set indentation
        XMLHelper.set_indentation(paragraph, left_margin_emus, hanging_indent_emus)

        # Add numbering
        XMLHelper.add_numbering(paragraph, style)

    @staticmethod
    def inches_to_emus(inches: float) -> int:
        """Convert inches to EMUs (English Metric Units).

        Args:
            inches: Measurement in inches

        Returns:
            Measurement in EMUs (914400 EMUs = 1 inch)
        """
        return int(inches * 914400)

    @staticmethod
    def emus_to_inches(emus: int) -> float:
        """Convert EMUs to inches.

        Args:
            emus: Measurement in EMUs

        Returns:
            Measurement in inches
        """
        return emus / 914400


# Standard indentation presets
class IndentationPresets:
    """Standard indentation values for common list types."""

    # Standard bullets (level 0)
    BULLET_L0_MARGIN = XMLHelper.inches_to_emus(0.38)
    BULLET_L0_INDENT = XMLHelper.inches_to_emus(-0.25)

    # Nested bullets (level 1) - under numbered items
    BULLET_L1_MARGIN = XMLHelper.inches_to_emus(0.75)
    BULLET_L1_INDENT = XMLHelper.inches_to_emus(-0.25)

    # Numbered lists (level 0)
    NUMBER_L0_MARGIN = XMLHelper.inches_to_emus(0.38)
    NUMBER_L0_INDENT = XMLHelper.inches_to_emus(-0.25)

    # Numbered paragraphs with lists
    NUMBER_WITH_LIST_MARGIN = XMLHelper.inches_to_emus(0.5)
    NUMBER_WITH_LIST_INDENT = XMLHelper.inches_to_emus(-0.25)
