"""
CSS Style Parser for HTML to PPTX conversion.

Parses inline CSS styles, CSS classes from <style> tags, and CSS variables.
Supports conversion of CSS units to PowerPoint equivalents.
"""

import re
from pptx.util import Pt
from pptx.dml.color import RGBColor


class CSSStyleParser:
    """Parse inline CSS styles and CSS variables to extract styling properties."""

    def __init__(self, css_variables=None):
        """
        Initialize CSS parser with optional CSS custom properties.

        Args:
            css_variables: Dict of CSS custom properties (e.g., {'--color-primary': '#131313'})
        """
        self.css_vars = css_variables or {}
        self.css_rules = {}  # Class name -> CSS properties mapping

    def parse_inline_style(self, style_string):
        """
        Parse inline style attribute into dict.

        Args:
            style_string: String like "color: #131313; font-size: 18px; padding: 24px;"

        Returns:
            Dict like {'color': '#131313', 'font-size': '18px', 'padding': '24px'}
        """
        if not style_string:
            return {}

        styles = {}
        # Split by semicolon, then by colon
        declarations = style_string.split(';')
        for decl in declarations:
            if ':' in decl:
                prop, value = decl.split(':', 1)
                prop = prop.strip().lower()
                value = value.strip()
                styles[prop] = value

        return styles

    def resolve_css_var(self, value):
        """
        Resolve CSS variable references.

        Args:
            value: String like "var(--color-primary)" or "#131313"

        Returns:
            Resolved value or original if not a var()
        """
        if not value or not isinstance(value, str):
            return value

        # Check for var() syntax
        var_match = re.match(r'var\((--[\w-]+)\)', value.strip())
        if var_match:
            var_name = var_match.group(1)
            return self.css_vars.get(var_name, value)

        return value

    def parse_color(self, color_value):
        """
        Parse any CSS color format to RGBColor.

        Supports:
        - Hex: #131313, #fff
        - RGB: rgb(19, 19, 19)
        - RGBA: rgba(19, 19, 19, 0.9) - ignores alpha
        - CSS vars: var(--color-primary)

        Returns:
            RGBColor object or None if parsing fails
        """
        if not color_value:
            return None

        # Resolve CSS variables
        color_value = self.resolve_css_var(color_value)
        color_value = color_value.strip()

        # Hex color (#131313 or #fff)
        if color_value.startswith('#'):
            hex_color = color_value[1:]
            # Handle shorthand (#fff -> #ffffff)
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])

            if len(hex_color) == 6:
                try:
                    r = int(hex_color[0:2], 16)
                    g = int(hex_color[2:4], 16)
                    b = int(hex_color[4:6], 16)
                    return RGBColor(r, g, b)
                except ValueError:
                    return None

        # RGB/RGBA color
        rgb_match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', color_value)
        if rgb_match:
            r, g, b = rgb_match.groups()
            return RGBColor(int(r), int(g), int(b))

        return None

    def parse_size(self, size_value, context='font', base_size=16):
        """
        Convert CSS size to Pt (for fonts) or inches (for dimensions).

        Supports:
        - px: 24px → Pt or inches
        - pt: 18pt → Pt
        - em: 1.5em → relative to base
        - %: 150% → relative to base

        Args:
            size_value: CSS size string
            context: 'font' returns Pt, 'spacing' returns inches (float)
            base_size: Base size for relative units (default 16px)

        Returns:
            Pt object (if context='font') or float inches (if context='spacing')
        """
        if not size_value:
            return None

        # Resolve CSS variables
        size_value = self.resolve_css_var(size_value)
        size_value = size_value.strip()

        # Extract number and unit
        match = re.match(r'([\d.]+)(px|pt|em|rem|%)?', size_value)
        if not match:
            return None

        num = float(match.group(1))
        unit = match.group(2) or 'px'

        # Convert to base unit (pixels)
        if unit == 'px':
            pixels = num
        elif unit == 'pt':
            pixels = num * 96 / 72  # 1pt = 1/72 inch, 96 DPI
        elif unit in ['em', 'rem']:
            pixels = num * base_size
        elif unit == '%':
            pixels = (num / 100) * base_size
        else:
            pixels = num

        # Convert based on context
        if context == 'font':
            # Convert pixels to points (72 DPI for fonts)
            points = pixels * 72 / 96
            return Pt(points)
        else:  # spacing, dimensions
            # Convert pixels to inches (96 DPI)
            inches = pixels / 96
            return inches

    def parse_spacing(self, spacing_value):
        """
        Parse CSS spacing (padding, margin, gap) values.

        Supports:
        - Single: "24px" → all sides
        - Two: "16px 24px" → top/bottom, left/right
        - Four: "10px 20px 15px 25px" → top, right, bottom, left

        Args:
            spacing_value: CSS spacing string

        Returns:
            Dict with {'top': float, 'right': float, 'bottom': float, 'left': float} in inches
            Or single float if uniform spacing
        """
        if not spacing_value:
            return None

        # Resolve CSS variables
        spacing_value = self.resolve_css_var(spacing_value)
        parts = spacing_value.strip().split()

        if len(parts) == 1:
            # Uniform spacing
            size = self.parse_size(parts[0], context='spacing')
            return size if size else 0

        # Parse each value
        sizes = [self.parse_size(p, context='spacing') or 0 for p in parts]

        if len(sizes) == 2:
            # top/bottom, left/right
            return {
                'top': sizes[0],
                'right': sizes[1],
                'bottom': sizes[0],
                'left': sizes[1]
            }
        elif len(sizes) == 4:
            # top, right, bottom, left
            return {
                'top': sizes[0],
                'right': sizes[1],
                'bottom': sizes[2],
                'left': sizes[3]
            }

        return None

    def parse_grid(self, grid_template_columns):
        """
        Parse CSS grid-template-columns.

        Supports:
        - "1fr 1fr" → 2 equal columns [0.5, 0.5]
        - "repeat(3, 1fr)" → 3 equal columns [0.333, 0.333, 0.333]
        - "200px 1fr 2fr" → mixed units (converts to fractions based on available space)

        Args:
            grid_template_columns: CSS grid-template-columns value

        Returns:
            List of column width fractions (sum = 1.0)
        """
        if not grid_template_columns:
            return [1.0]  # Single column

        # Resolve CSS variables
        grid_template_columns = self.resolve_css_var(grid_template_columns)

        # Handle repeat() syntax
        repeat_match = re.match(r'repeat\((\d+),\s*(.+)\)', grid_template_columns.strip())
        if repeat_match:
            count = int(repeat_match.group(1))
            pattern = repeat_match.group(2)
            grid_template_columns = ' '.join([pattern] * count)

        # Split into column definitions
        columns = grid_template_columns.split()

        # Parse each column
        fr_total = 0
        px_total = 0
        col_data = []

        for col in columns:
            if col.endswith('fr'):
                # Fractional unit
                fr_value = float(col[:-2])
                col_data.append(('fr', fr_value))
                fr_total += fr_value
            elif col.endswith('px'):
                # Pixel unit
                px_value = float(col[:-2])
                col_data.append(('px', px_value))
                px_total += px_value
            elif col == 'auto':
                # Auto sizing (treat as 1fr)
                col_data.append(('fr', 1))
                fr_total += 1
            else:
                # Unknown, treat as 1fr
                col_data.append(('fr', 1))
                fr_total += 1

        # Convert to fractions
        # For now, simplified: assume px columns take their space, fr columns share remaining
        # In real implementation, would need available width
        if fr_total > 0 and px_total == 0:
            # All fractional
            fractions = [(data[1] / fr_total) if data[0] == 'fr' else 0 for data in col_data]
        else:
            # Mixed or all px - for now, distribute evenly
            count = len(col_data)
            fractions = [1.0 / count] * count

        return fractions

    def parse_border(self, border_value):
        """
        Parse CSS border property.

        Supports:
        - "2px solid #cac3b7"
        - "1px solid var(--color-accent)"
        - "none"

        Args:
            border_value: CSS border string

        Returns:
            Dict with {'width': Pt, 'color': RGBColor, 'style': str} or None if "none"
        """
        if not border_value or border_value.strip().lower() == 'none':
            return None

        # Resolve CSS variables
        border_value = self.resolve_css_var(border_value)

        # Parse border: "2px solid #cac3b7"
        parts = border_value.split()
        if len(parts) < 2:
            return None

        result = {
            'width': None,
            'color': None,
            'style': 'solid'
        }

        for part in parts:
            # Width (px, pt)
            if re.match(r'\d+px', part) or re.match(r'\d+pt', part):
                size = self.parse_size(part, context='spacing')
                # Convert inches to Pt for line width
                result['width'] = Pt(size * 72) if size else None
            # Style
            elif part in ['solid', 'dashed', 'dotted', 'double']:
                result['style'] = part
            # Color
            elif part.startswith('#') or part.startswith('rgb'):
                result['color'] = self.parse_color(part)

        return result

    def parse_box_shadow(self, shadow_value):
        """
        Parse CSS box-shadow property.

        Supports:
        - "0 4px 6px rgba(0, 0, 0, 0.1)"
        - "2px 2px 8px #131313"
        - "none"

        Args:
            shadow_value: CSS box-shadow string

        Returns:
            Dict with {'offset_x': inches, 'offset_y': inches, 'blur': inches,
                      'color': RGBColor, 'transparency': int (0-100)} or None
        """
        if not shadow_value or shadow_value.strip().lower() == 'none':
            return None

        # Resolve CSS variables
        shadow_value = self.resolve_css_var(shadow_value)

        # Parse: "0 4px 6px rgba(0, 0, 0, 0.1)"
        # Format: offset-x offset-y blur-radius color
        parts = shadow_value.strip().split()

        if len(parts) < 3:
            return None

        result = {
            'offset_x': 0,
            'offset_y': 0,
            'blur': 0,
            'color': RGBColor(0, 0, 0),
            'transparency': 90  # Default 90% opaque
        }

        # Parse offsets and blur
        offset_x = self.parse_size(parts[0], context='spacing') if len(parts) > 0 else 0
        offset_y = self.parse_size(parts[1], context='spacing') if len(parts) > 1 else 0
        blur = self.parse_size(parts[2], context='spacing') if len(parts) > 2 else 0

        result['offset_x'] = offset_x or 0
        result['offset_y'] = offset_y or 0
        result['blur'] = blur or 0

        # Parse color (could be hex or rgba)
        color_part = ' '.join(parts[3:]) if len(parts) > 3 else None
        if color_part:
            # Check for rgba with alpha
            rgba_match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)', color_part)
            if rgba_match:
                r, g, b, a = rgba_match.groups()
                result['color'] = RGBColor(int(r), int(g), int(b))
                if a:
                    # Convert alpha (0.0-1.0) to transparency percentage (0-100)
                    alpha = float(a)
                    result['transparency'] = int(alpha * 100)
            else:
                # Try parsing as regular color
                color = self.parse_color(color_part)
                if color:
                    result['color'] = color

        return result

    def extract_css_from_style_tag(self, style_tag_content):
        """
        Extract CSS rules from <style> tag content.

        Args:
            style_tag_content: String content of <style> tag

        Returns:
            Dict mapping class names to CSS properties
            Example: {'card': {'background': '#ffffff', 'box-shadow': '0 4px 6px...'}}
        """
        rules = {}

        # Remove CSS comments
        style_tag_content = re.sub(r'/\*.*?\*/', '', style_tag_content, flags=re.DOTALL)

        # Match CSS rules: .class-name { properties }
        # This regex matches: .selector { ... }
        rule_pattern = r'\.([a-zA-Z0-9_-]+)\s*\{([^}]+)\}'
        matches = re.findall(rule_pattern, style_tag_content)

        for class_name, properties in matches:
            # Parse the properties block
            parsed_props = self.parse_inline_style(properties)
            rules[class_name] = parsed_props

        return rules

    def load_css_rules_from_html(self, html_tree):
        """
        Extract and load all CSS rules from <style> tags in HTML document.

        Args:
            html_tree: lxml HTML tree

        Updates:
            self.css_rules with all extracted rules
        """
        # Find all <style> tags
        style_tags = html_tree.xpath('//style')

        for style_tag in style_tags:
            style_content = style_tag.text
            if style_content:
                # Extract rules from this style tag
                rules = self.extract_css_from_style_tag(style_content)

                # Merge into existing rules (later rules override earlier ones)
                self.css_rules.update(rules)

        # Also extract CSS variables from :root
        root_pattern = r':root\s*\{([^}]+)\}'
        for style_tag in style_tags:
            if style_tag.text:
                root_match = re.search(root_pattern, style_tag.text)
                if root_match:
                    root_props = root_match.group(1)
                    # Parse CSS variables
                    var_pattern = r'(--[a-zA-Z0-9_-]+):\s*([^;]+);'
                    var_matches = re.findall(var_pattern, root_props)
                    for var_name, var_value in var_matches:
                        self.css_vars[var_name] = var_value.strip()

    def get_computed_style(self, element):
        """
        Get computed styles for an element (CSS rules + inline styles).

        CSS specificity: inline styles > class rules

        Args:
            element: lxml HTML element

        Returns:
            Dict of CSS properties (merged class rules + inline styles)
        """
        computed = {}

        # 1. Apply CSS rules from classes
        element_classes = element.get('class', '').split()
        for class_name in element_classes:
            if class_name in self.css_rules:
                # Merge class rules
                computed.update(self.css_rules[class_name])

        # 2. Apply inline styles (highest priority)
        inline_style = element.get('style', '')
        if inline_style:
            inline_props = self.parse_inline_style(inline_style)
            computed.update(inline_props)

        return computed
