"""Layout calculation utilities for PowerPoint slides.

This module provides helper functions for calculating positions and dimensions
for various layout patterns like grids, cards, and columns.
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class LayoutBox:
    """Represents a positioned box in a layout."""
    x: float  # X position in inches
    y: float  # Y position in inches
    width: float  # Width in inches
    height: float  # Height in inches


class LayoutCalculator:
    """Utilities for calculating layout positions and dimensions."""

    @staticmethod
    def calculate_grid_layout(
        num_items: int,
        container_x: float,
        container_y: float,
        container_width: float,
        container_height: float,
        columns: int = 2,
        gap: float = 0.4
    ) -> List[LayoutBox]:
        """Calculate grid item positions and sizes.

        Args:
            num_items: Number of items in grid
            container_x: Container X position (inches)
            container_y: Container Y position (inches)
            container_width: Container width (inches)
            container_height: Container height (inches)
            columns: Number of columns
            gap: Gap between items (inches)

        Returns:
            List of LayoutBox objects with positions and dimensions
        """
        # Calculate dimensions
        rows = (num_items + columns - 1) // columns  # Ceiling division

        # Account for gaps
        total_gap_width = gap * (columns - 1)
        total_gap_height = gap * (rows - 1)

        # Calculate item dimensions
        item_width = (container_width - total_gap_width) / columns
        item_height = (container_height - total_gap_height) / rows

        # Generate layout boxes
        boxes = []
        for i in range(num_items):
            row = i // columns
            col = i % columns

            x = container_x + col * (item_width + gap)
            y = container_y + row * (item_height + gap)

            boxes.append(LayoutBox(x, y, item_width, item_height))

        return boxes

    @staticmethod
    def calculate_card_layout(
        num_cards: int,
        container_x: float,
        container_y: float,
        container_width: float,
        card_height: float,
        columns: int = 2,
        gap: float = 0.4
    ) -> List[LayoutBox]:
        """Calculate card positions for card-based layouts.

        Args:
            num_cards: Number of cards
            container_x: Container X position (inches)
            container_y: Container Y position (inches)
            container_width: Container width (inches)
            card_height: Height of each card (inches)
            columns: Number of columns
            gap: Gap between cards (inches)

        Returns:
            List of LayoutBox objects for cards
        """
        # Calculate card width
        total_gap_width = gap * (columns - 1)
        card_width = (container_width - total_gap_width) / columns

        # Generate card boxes
        boxes = []
        for i in range(num_cards):
            row = i // columns
            col = i % columns

            x = container_x + col * (card_width + gap)
            y = container_y + row * (card_height + gap)

            boxes.append(LayoutBox(x, y, card_width, card_height))

        return boxes

    @staticmethod
    def calculate_two_column_layout(
        container_x: float,
        container_y: float,
        container_width: float,
        container_height: float,
        gap: float = 0.4
    ) -> Tuple[LayoutBox, LayoutBox]:
        """Calculate positions for two-column layout.

        Args:
            container_x: Container X position (inches)
            container_y: Container Y position (inches)
            container_width: Container width (inches)
            container_height: Container height (inches)
            gap: Gap between columns (inches)

        Returns:
            Tuple of (left_box, right_box)
        """
        column_width = (container_width - gap) / 2

        left_box = LayoutBox(container_x, container_y, column_width, container_height)
        right_box = LayoutBox(
            container_x + column_width + gap,
            container_y,
            column_width,
            container_height
        )

        return left_box, right_box

    @staticmethod
    def calculate_stats_banner_layout(
        num_stats: int,
        container_x: float,
        container_y: float,
        container_width: float,
        stat_height: float,
        gap: float = 0.4
    ) -> List[LayoutBox]:
        """Calculate positions for statistics banner.

        Args:
            num_stats: Number of stat items
            container_x: Container X position (inches)
            container_y: Container Y position (inches)
            container_width: Container width (inches)
            stat_height: Height of each stat (inches)
            gap: Gap between stats (inches)

        Returns:
            List of LayoutBox objects for stat items
        """
        # Calculate stat width
        total_gap_width = gap * (num_stats - 1)
        stat_width = (container_width - total_gap_width) / num_stats

        # Generate stat boxes
        boxes = []
        for i in range(num_stats):
            x = container_x + i * (stat_width + gap)
            boxes.append(LayoutBox(x, container_y, stat_width, stat_height))

        return boxes

    @staticmethod
    def calculate_vertical_stack(
        num_items: int,
        container_x: float,
        container_y: float,
        container_width: float,
        item_height: float,
        gap: float = 0.2
    ) -> List[LayoutBox]:
        """Calculate positions for vertically stacked items.

        Args:
            num_items: Number of items
            container_x: Container X position (inches)
            container_y: Container Y position (inches)
            container_width: Container width (inches)
            item_height: Height of each item (inches)
            gap: Gap between items (inches)

        Returns:
            List of LayoutBox objects
        """
        boxes = []
        current_y = container_y

        for i in range(num_items):
            boxes.append(LayoutBox(container_x, current_y, container_width, item_height))
            current_y += item_height + gap

        return boxes

    @staticmethod
    def fit_text_in_box(
        text_length: int,
        box_width: float,
        box_height: float,
        base_font_size: float = 16.0,
        chars_per_line_ratio: float = 10.0
    ) -> float:
        """Calculate appropriate font size to fit text in box.

        Args:
            text_length: Number of characters in text
            box_width: Available width (inches)
            box_height: Available height (inches)
            base_font_size: Starting font size (points)
            chars_per_line_ratio: Approximate characters per inch at base size

        Returns:
            Recommended font size in points
        """
        # Estimate lines needed
        chars_per_line = box_width * chars_per_line_ratio
        estimated_lines = text_length / chars_per_line if chars_per_line > 0 else 1

        # Calculate available space per line
        line_height_inches = box_height / estimated_lines if estimated_lines > 0 else box_height

        # Convert to points (72 points per inch)
        available_points = line_height_inches * 72

        # Return reasonable font size (between 8pt and base_font_size)
        return max(8.0, min(base_font_size, available_points * 0.6))


class GridLayoutPresets:
    """Common grid layout configurations."""

    @staticmethod
    def two_column_grid() -> Dict:
        """Standard 2-column grid configuration."""
        return {'columns': 2, 'gap': 0.4}

    @staticmethod
    def three_column_grid() -> Dict:
        """Standard 3-column grid configuration."""
        return {'columns': 3, 'gap': 0.3}

    @staticmethod
    def four_column_grid() -> Dict:
        """Standard 4-column grid configuration."""
        return {'columns': 4, 'gap': 0.25}
