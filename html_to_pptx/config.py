"""
Configuration constants for HTML to PPTX converter.

This module contains all layout dimensions, font sizes, colors, and spacing
constants used throughout the converter. All values are extracted here to
eliminate magic numbers and enable easy customization.
"""

from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor


class LayoutConfig:
    """Layout dimensions and positioning constants (all in inches)."""

    # Slide dimensions
    SLIDE_WIDTH = 10.67   # 1024px / 96 DPI
    SLIDE_HEIGHT = 8.0    # 768px / 96 DPI

    # Padding and margins
    PADDING = 0.625       # 60px / 96 DPI - standard slide padding

    # Title positioning
    TITLE_Y = 0.42        # Title vertical position from top (raised by 0.5cm from 0.62)
    TITLE_HEIGHT = 0.7    # Title text box height
    TITLE_CONTENT_GAP = 0.58  # Gap between title and content (reduced by 1.25cm for tighter spacing)

    # Content positioning (calculated)
    CONTENT_START_Y = TITLE_Y + TITLE_HEIGHT + TITLE_CONTENT_GAP  # 1.7 inches (raised by 1.25cm for better content positioning)

    # Footer positioning
    FOOTER_HEIGHT = 0.25
    FOOTER_Y_OFFSET = 0.35  # Distance from bottom
    FOOTER_Y = SLIDE_HEIGHT - FOOTER_Y_OFFSET  # 7.65 inches
    FOOTER_NUMBER_WIDTH = 0.78
    FOOTER_NUMBER_X_OFFSET = 1.3

    # Decorative shapes (title slide)
    DECORATIVE_SHAPE_WIDTH = 0.35
    DECORATIVE_SHAPE_HEIGHT = 0.58
    DECORATIVE_SHAPE_SPACING = 0.25  # Gap between shapes
    DECORATIVE_SHAPE_Y = 7.1  # Position from top (moved to bottom of slide)
    DECORATIVE_SHAPE_X_START = 0.74  # First shape X position

    # Card layout
    CARD_PADDING = 0.3     # Internal card padding
    CARD_HEADER_HEIGHT = 0.5
    CARD_MIN_HEIGHT = 2.5
    CARD_GAP = 0.4         # Gap between cards

    # Grid layout
    GRID_GAP = 0.4         # Gap between grid items
    GRID_ITEM_PADDING = 0.25
    GRID_ITEM_ICON_SIZE = 0.45
    GRID_ITEM_ACCENT_HEIGHT = 0.04  # Orange bar at top

    # Stats banner
    STATS_ICON_SIZE = 0.7
    STATS_ICON_Y_OFFSET = 0.15  # Above stat number
    STATS_NUMBER_HEIGHT = 1.0
    STATS_LABEL_HEIGHT = 0.4
    STATS_DESCRIPTION_HEIGHT = 0.4

    # Big number slide
    BIG_NUMBER_Y = 2.5
    BIG_NUMBER_HEIGHT = 1.5
    BIG_NUMBER_EXPLANATION_Y_OFFSET = 2.0
    BIG_NUMBER_EXPLANATION_HEIGHT = 1.2

    # Objectives slide
    OBJECTIVE_NUMBER_SIZE = 0.6
    OBJECTIVE_GAP = 0.4
    OBJECTIVE_PADDING = 0.25

    # Section break
    SECTION_BREAK_Y = 1.3
    SECTION_BREAK_HEIGHT = 5.5


class FontConfig:
    """Font families and sizes used throughout presentations."""

    # Font families
    HEADER_FONT = "Cal Sans"
    BODY_FONT = "Plus Jakarta Sans"

    # Font sizes (in points)
    # Footer and small text
    FOOTER_SIZE = Pt(8)

    # Body text sizes
    BODY_TINY = Pt(12)
    BODY_SMALL = Pt(14)
    BODY_NORMAL = Pt(16)
    BODY_MEDIUM = Pt(18)
    BODY_LARGE = Pt(20)

    # Heading sizes
    HEADING_SMALL = Pt(27)
    HEADING_MEDIUM = Pt(36)
    HEADING_LARGE = Pt(38)

    # Title sizes
    TITLE_SIZE = Pt(52)
    SECTION_TITLE_SIZE = Pt(38)

    # Special sizes
    BIG_NUMBER_SIZE = Pt(135)  # For big number slides
    STAT_NUMBER_SIZE = Pt(36)  # For statistics

    # Line spacing
    LINE_SPACING_SINGLE = 1.0
    LINE_SPACING_NORMAL = 1.15
    LINE_SPACING_RELAXED = 1.5

    # Paragraph spacing
    SPACE_AFTER_SMALL = Pt(6)
    SPACE_AFTER_NORMAL = Pt(12)
    SPACE_AFTER_LARGE = Pt(18)

    # Character spacing (in EMUs: English Metric Units)
    # Negative values = condensed, positive = expanded
    # 1 point = 12700 EMUs
    # -0.05em condensing for titles (approx -0.65pt at 13pt base)
    TITLE_LETTER_SPACING = Pt(-0.65)  # Condensed by ~0.05em


class ColorConfig:
    """Color palette for presentations."""

    # Primary brand colors (reference design)
    DARK_GRAY = RGBColor(19, 19, 19)      # #131313 - Main text, dark backgrounds
    ORANGE = RGBColor(237, 94, 41)        # #ed5e29 - Accent, emphasis
    CREAM = RGBColor(244, 243, 241)       # #f4f3f1 - Backgrounds
    TAN = RGBColor(202, 195, 183)         # #cac3b7 - Decorative elements
    WHITE = RGBColor(255, 255, 255)       # #ffffff - Cards, contrast

    # Neutral colors
    MUTED_GRAY = RGBColor(100, 116, 139)  # #64748b - Secondary text
    LIGHT_GRAY = RGBColor(226, 232, 240)  # #e2e8f0 - Borders, dividers

    # Color mapping dictionary (for CSS color lookup)
    COLORS = {
        # Primary palette
        '#131313': DARK_GRAY,
        '#ed5e29': ORANGE,
        '#f4f3f1': CREAM,
        '#cac3b7': TAN,
        '#ffffff': WHITE,

        # Tailwind orange variant (also maps to our orange)
        '#f97316': ORANGE,      # Tailwind orange-500 → Our orange

        # Additional gray shades
        '#f1f5f9': RGBColor(241, 245, 249),  # slate-100
        '#94a3b8': RGBColor(148, 163, 184),  # slate-400
        '#cbd5e1': RGBColor(203, 213, 225),  # slate-300

        # Legacy color mappings (automatically converted to new palette)
        '#7373b0': ORANGE,      # Old purple → New orange
        '#475569': DARK_GRAY,   # Old body text → Dark gray
        '#1e293b': DARK_GRAY,   # Old dark → Dark gray
        '#64748b': MUTED_GRAY,  # Muted (keep as-is)
        '#f8fafc': CREAM,       # Old light bg → Cream
        '#e2e8f0': CREAM,       # Old border → Cream
        '#ef4444': ORANGE,      # Red → Orange
        '#10b981': ORANGE,      # Green → Orange
        '#f59e0b': ORANGE,      # Amber → Orange
    }

    # CSS variable mapping (for var(--color-name) resolution)
    CSS_VARIABLES = {
        '--color-dark': '#131313',
        '--color-primary': '#ed5e29',
        '--color-cream': '#f4f3f1',
        '--color-tan': '#cac3b7',
        '--color-white': '#ffffff',
        '--color-muted': '#64748b',

        # Semantic variables
        '--color-background': '#f4f3f1',
        '--color-text': '#131313',
        '--color-accent': '#ed5e29',
    }

    @classmethod
    def get_text_color_for_background(cls, bg_color):
        """
        Determine appropriate text color based on background.

        Args:
            bg_color: RGBColor of background

        Returns:
            RGBColor appropriate for text (dark or light)
        """
        # Check if background is dark (dark gray or similar)
        if bg_color == cls.DARK_GRAY or (
            hasattr(bg_color, 'rgb') and
            bg_color.rgb[0] < 50 and
            bg_color.rgb[1] < 50 and
            bg_color.rgb[2] < 50
        ):
            return cls.CREAM  # Light text on dark background
        else:
            return cls.DARK_GRAY  # Dark text on light background


class SpacingConfig:
    """Spacing and gap constants for consistent layout."""

    # Text line spacing (1.2 = 120% of font size)
    LINE_SPACING = 1.2  # Unified line spacing for all text
    TITLE_LINE_SPACING = 0.9  # Tighter line spacing for slide titles

    # Paragraph spacing (in Points)
    PARAGRAPH_SPACE_BEFORE = Pt(6)     # Space before paragraphs
    PARAGRAPH_SPACE_AFTER = Pt(6)      # Space after paragraphs

    # Subheading spacing (bold paragraphs acting as headings)
    SUBHEADING_SPACE_BEFORE = Pt(12)   # Larger space before subheadings
    SUBHEADING_SPACE_AFTER = Pt(3)     # Smaller space after subheadings

    # List item spacing
    LIST_ITEM_SPACE_BEFORE = Pt(0)     # No space before list items
    LIST_ITEM_SPACE_AFTER = Pt(0)      # No space after list items

    # Special context spacing
    REFERENCE_SPACE_BEFORE = Pt(6)     # Space before bibliography entries
    REFERENCE_SPACE_AFTER = Pt(0)      # No space after references
    CHECKLIST_SPACE_BEFORE = Pt(0)     # No space before checklist items
    CHECKLIST_SPACE_AFTER = Pt(0)      # No space after checklist items
    FRAMEWORK_TITLE_SPACE_BEFORE = Pt(0)  # No space before framework titles
    FRAMEWORK_TITLE_SPACE_AFTER = Pt(12)  # Space after framework card titles (keeps separation from content)

    # Vertical spacing
    TITLE_BOTTOM_MARGIN = 0.6
    SECTION_GAP = 0.4
    PARAGRAPH_GAP = 0.15
    LIST_ITEM_GAP = 0.1

    # Horizontal spacing
    BULLET_INDENT = 0.3
    TEXT_INDENT = 0.5

    # Content area calculations
    CONTENT_WIDTH = LayoutConfig.SLIDE_WIDTH - (2 * LayoutConfig.PADDING)
    CONTENT_HEIGHT = LayoutConfig.SLIDE_HEIGHT - LayoutConfig.CONTENT_START_Y - LayoutConfig.FOOTER_Y_OFFSET


# Convenience export for backward compatibility
SLIDE_WIDTH = LayoutConfig.SLIDE_WIDTH
SLIDE_HEIGHT = LayoutConfig.SLIDE_HEIGHT
PADDING = LayoutConfig.PADDING
HEADER_FONT = FontConfig.HEADER_FONT
BODY_FONT = FontConfig.BODY_FONT
COLORS = ColorConfig.COLORS
