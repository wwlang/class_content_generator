"""
Layout configuration for HTML to PPTX converter.

This module provides metadata about all supported slide layouts,
including their purpose, detection patterns, and visual characteristics.
"""

from dataclasses import dataclass
from typing import List, Callable, Optional
from enum import IntEnum


class LayoutPriority(IntEnum):
    """Priority levels for layout detection (higher = checked first)."""
    HIGHEST = 10
    VERY_HIGH = 9
    HIGH = 8
    MEDIUM_HIGH = 7
    MEDIUM = 6
    LOW = 3
    DEFAULT = 1


@dataclass
class LayoutConfig:
    """Configuration for a slide layout."""

    # Identification
    layout_id: str
    layout_name: str
    css_classes: List[str]
    priority: LayoutPriority

    # Description
    title: str
    purpose: str
    best_for: List[str]

    # Detection patterns
    content_indicators: List[str]
    required_elements: List[str]
    optional_elements: List[str]

    # Handler
    handler_method: str  # Name of method in converter

    # Visual characteristics
    visual_notes: str = ""


# ============================================================================
# LAYOUT DEFINITIONS
# ============================================================================

LAYOUT_TITLE = LayoutConfig(
    layout_id="title",
    layout_name="Title Slide",
    css_classes=["title-slide"],
    priority=LayoutPriority.HIGHEST,
    title="Opening Slide - Presentation Title",
    purpose="Introduce the presentation topic with maximum visual impact. Sets tone for entire deck.",
    best_for=[
        "Course title and code",
        "Lecture/module title",
        "Presenter name and credentials",
        "Date/semester information",
        "First slide only"
    ],
    content_indicators=[
        "First slide in deck (position = 0)",
        "Has <h1> title element",
        "May have .subtitle div",
        "May have .author div",
        "Has .decorative-shapes container",
        "No bullet lists or paragraphs in content area"
    ],
    required_elements=[
        ".title-content wrapper with <h1>"
    ],
    optional_elements=[
        ".subtitle (course/module name)",
        ".author (presenter info)",
        ".decorative-shapes (visual accent)"
    ],
    handler_method="handle_title_slide",
    visual_notes="Large title (60px), orange subtitle, decorative shapes at bottom-left"
)

LAYOUT_SECTION_BREAK = LayoutConfig(
    layout_id="section-break",
    layout_name="Section Break Slide",
    css_classes=["section-break"],
    priority=LayoutPriority.VERY_HIGH,
    title="Major Topic Transition",
    purpose="Signal major transitions between presentation sections. Creates visual break and refocuses attention.",
    best_for=[
        "Start of new major topic",
        "Transition between lecture segments",
        "'Part 1', 'Part 2' divisions",
        "Before major conceptual shifts",
        "Single bold statement"
    ],
    content_indicators=[
        "Single <h2> heading only",
        "No <p>, <ul>, or <ol> elements",
        "Short text (2-6 words typical)",
        "Often includes section numbers or 'Part X'",
        "Background color applied to entire slide"
    ],
    required_elements=[
        "Single heading element (h2 or h3)",
        "Colored background"
    ],
    optional_elements=[
        "Section number",
        "Decorative line or shape"
    ],
    handler_method="handle_section_break_slide",
    visual_notes="Colored background (purple #7373b0), large centered white text, full-bleed"
)

LAYOUT_VOCAB_TABLE = LayoutConfig(
    layout_id="vocab-table",
    layout_name="Vocabulary Table",
    css_classes=["vocab-table-slide"],
    priority=LayoutPriority.VERY_HIGH,
    title="Bilingual Vocabulary or Definitions",
    purpose="Present key terms with translations or definitions in structured table format.",
    best_for=[
        "English ↔ Vietnamese vocabulary",
        "Technical term definitions",
        "Glossary items",
        "Concept definitions with examples",
        "4-8 terms per slide"
    ],
    content_indicators=[
        "Contains <table> element",
        "Title includes 'vocabulary', 'terms', 'definitions'",
        "3 columns typical (term, translation, context)",
        "Has <thead> with column headers",
        "4-8 rows of content",
        "Vietnamese characters present"
    ],
    required_elements=[
        "<table> with headers",
        "Title mentioning vocabulary/terms"
    ],
    optional_elements=[
        "Row striping (alternating colors)",
        "Speaker notes with pronunciation"
    ],
    handler_method="handle_vocab_table_slide",
    visual_notes="Clean table with 3 columns, alternating row colors, bilingual content"
)

LAYOUT_OBJECTIVES = LayoutConfig(
    layout_id="objectives",
    layout_name="Learning Objectives",
    css_classes=["objectives-slide"],
    priority=LayoutPriority.HIGH,
    title="Course/Lesson Learning Objectives",
    purpose="State explicit learning objectives using Bloom's taxonomy verbs. Sets expectations.",
    best_for=[
        "Course learning outcomes",
        "Lesson objectives",
        "Assessment criteria preview",
        "'By the end of this lesson...' statements",
        "Competency statements"
    ],
    content_indicators=[
        "Title contains 'objectives', 'outcomes', 'you will'",
        "Numbered list with 3-6 items",
        "Starts with action verbs (Bloom's taxonomy)",
        "Bold verbs at start of each item",
        "Phrase 'By the end...'"
    ],
    required_elements=[
        "Title with 'objectives' or 'outcomes'",
        "Ordered list (<ol>)"
    ],
    optional_elements=[
        ".objective-item wrappers with boxes",
        "Icons for each objective",
        "Assessment connection note"
    ],
    handler_method="handle_objectives_slide",
    visual_notes="Numbered list, bold Bloom's verbs, clean layout, early in deck"
)

LAYOUT_BIG_NUMBER = LayoutConfig(
    layout_id="big-number",
    layout_name="Big Number / Statistic",
    css_classes=["big-number-slide", "stat-slide"],
    priority=LayoutPriority.HIGH,
    title="Emphasize Key Statistics",
    purpose="Draw attention to important numbers or statistics. Creates visual impact through scale and contrast.",
    best_for=[
        "Single key statistic",
        "Percentage or metric",
        "Survey results",
        "Year/date callouts",
        "'X% of people...' statements",
        "Data that deserves emphasis"
    ],
    content_indicators=[
        "Contains large <span class='big-number'>",
        "Number followed by %, $, or unit",
        "Short descriptive text",
        "Centered alignment",
        "Often starts with number or statistic",
        "Source citation in small text"
    ],
    required_elements=[
        ".big-number element",
        "Supporting description text"
    ],
    optional_elements=[
        "Source citation",
        "Context paragraph",
        "Icon or visual accent"
    ],
    handler_method="handle_big_number_slide",
    visual_notes="Very large number (100-135px), orange accent, centered, minimal other content"
)

LAYOUT_ACTIVITY = LayoutConfig(
    layout_id="activity",
    layout_name="Activity Instructions",
    css_classes=["activity-slide"],
    priority=LayoutPriority.MEDIUM_HIGH,
    title="Interactive Activity Setup",
    purpose="Provide clear instructions for in-class activities, discussions, or exercises.",
    best_for=[
        "Think-Pair-Share instructions",
        "Group activity setup",
        "Discussion prompts",
        "Reflection exercises",
        "Timed activities",
        "Step-by-step instructions"
    ],
    content_indicators=[
        "Contains .activity-header element",
        "Title mentions 'Activity', 'Exercise', 'Discussion'",
        "Numbered or bulleted steps",
        "Timing indicated (e.g., '5 minutes')",
        "Imperative verbs (Discuss, Write, Share, etc.)",
        "Often includes 'Instructions:' or 'Steps:'"
    ],
    required_elements=[
        ".activity-header with colored background",
        "Instructions or steps"
    ],
    optional_elements=[
        "Timer icon",
        "Grouping information (pairs, groups of 4, etc.)",
        "Materials needed"
    ],
    handler_method="handle_activity_slide",
    visual_notes="Colored header box (purple/blue), white title, numbered steps, timing info"
)

LAYOUT_COMPARISON = LayoutConfig(
    layout_id="comparison",
    layout_name="Two-Column Comparison",
    css_classes=["comparison-slide"],
    priority=LayoutPriority.MEDIUM_HIGH,
    title="Side-by-Side Comparisons",
    purpose="Compare and contrast two concepts, approaches, or options side-by-side.",
    best_for=[
        "Before/After scenarios",
        "Old vs. New approaches",
        "Option A vs. Option B",
        "Pros and Cons",
        "Two competing theories",
        "Contrasting examples"
    ],
    content_indicators=[
        "Contains 2 .comparison-box elements",
        "Side-by-side divs",
        "Contrasting headings (vs., compared to, etc.)",
        "Equal or balanced content length",
        "May use 'vs' or '→' in title"
    ],
    required_elements=[
        "2 content boxes",
        "Title for each comparison item"
    ],
    optional_elements=[
        "Different background colors",
        "Icons or visual dividers",
        "Connecting arrows"
    ],
    handler_method="handle_comparison_slide",
    visual_notes="Split screen (50/50 or 40/60), two distinct boxes, symmetrical layout"
)

LAYOUT_CARD = LayoutConfig(
    layout_id="card",
    layout_name="Multi-Card Layout",
    css_classes=["card-layout"],
    priority=LayoutPriority.MEDIUM_HIGH,
    title="Multiple Concepts in Visual Cards",
    purpose="Present 2-4 related concepts as distinct visual cards with consistent formatting.",
    best_for=[
        "Feature highlights",
        "Key design elements",
        "Component overview",
        "3-4 parallel concepts",
        "Framework dimensions",
        "Category summaries"
    ],
    content_indicators=[
        "Contains 2-4 .card elements",
        "Each card has .card-header and .card-body",
        "Parallel structure (similar content length)",
        "Often title mentions 'Key', 'Elements', 'Components'",
        "Cards have background styling",
        "Border or shadow on cards"
    ],
    required_elements=[
        "Multiple .card divs",
        "Structured content in each card"
    ],
    optional_elements=[
        "Colored borders",
        "Icons in headers",
        "Numbered cards"
    ],
    handler_method="handle_card_layout",
    visual_notes="White cards with rounded corners, optional colored left border (orange), 2-4 cards per slide"
)

LAYOUT_STATS_BANNER = LayoutConfig(
    layout_id="stats-banner",
    layout_name="Stats Banner",
    css_classes=["stats-banner", "stats-slide"],
    priority=LayoutPriority.MEDIUM_HIGH,
    title="Multiple Statistics in Horizontal Banner",
    purpose="Display 2-4 key metrics or statistics side-by-side for quick comparison.",
    best_for=[
        "Multiple related statistics",
        "Key performance indicators",
        "Survey results (multiple data points)",
        "Deadline information",
        "Metrics dashboard",
        "Quick facts"
    ],
    content_indicators=[
        "Contains .stats-container with 2-4 .stat-item elements",
        "Each has .stat-value (number/date) and .stat-label",
        "Horizontal layout",
        "Numbers, dates, or short values prominent",
        "Supporting text smaller below"
    ],
    required_elements=[
        ".stats-container wrapper",
        "2-4 stat items with value and label"
    ],
    optional_elements=[
        "Icons above stats",
        "Colored backgrounds for each stat",
        "Dividers between stats"
    ],
    handler_method="handle_stats_banner",
    visual_notes="Horizontal row of stat boxes, large numbers/dates, equal width sections, centered"
)

LAYOUT_CHECKLIST = LayoutConfig(
    layout_id="checklist",
    layout_name="Checklist / Success Criteria",
    css_classes=["checklist-slide"],
    priority=LayoutPriority.MEDIUM,
    title="Assessment Checklists or Success Criteria",
    purpose="Present assessment rubrics, checklists, or success criteria in scannable format.",
    best_for=[
        "Assignment checklist",
        "Assessment rubric preview",
        "Quality criteria",
        "'What to include' lists",
        "Requirements overview",
        "Success indicators"
    ],
    content_indicators=[
        "Contains .checklist-category elements",
        "Has .category-header with colored background",
        "Checkbox markers (✓, ☐, or similar)",
        "Title mentions 'checklist', 'requirements', 'criteria'",
        "Grouped structure",
        "Assessment or rubric context"
    ],
    required_elements=[
        "Categorized structure",
        "List items with criteria"
    ],
    optional_elements=[
        "Checkbox symbols",
        "Colored category headers",
        "Point values or weights"
    ],
    handler_method="handle_checklist_slide",
    visual_notes="Checkboxes, colored category headers (purple/orange), 3-5 categories, 2-4 items per category"
)

LAYOUT_DARK = LayoutConfig(
    layout_id="dark",
    layout_name="Dark Background Slide",
    css_classes=["dark-slide", "dark-background"],
    priority=LayoutPriority.MEDIUM,
    title="Emphasis or Case Studies",
    purpose="Create visual contrast and emphasis. Often used for examples, case studies, or quotes.",
    best_for=[
        "Case studies",
        "Real-world examples",
        "Quotations",
        "Vietnamese context examples",
        "Emphasis moments",
        "Storytelling sections"
    ],
    content_indicators=[
        "Background color: dark gray, dark purple, or navy",
        "Text color: cream, white, or light gray",
        "Often has 'Example:', 'Case Study:', or 'Vietnamese Context:'",
        "May have decorative elements",
        "Contrasts with surrounding slides"
    ],
    required_elements=[
        "Dark background styling",
        "Light colored text"
    ],
    optional_elements=[
        "Icon or image",
        "Accent color elements",
        "Quote formatting"
    ],
    handler_method="handle_content_slide",  # Uses standard handler with dark background
    visual_notes="Dark background (#131313 or dark purple), light text (cream/white), dramatic contrast"
)

LAYOUT_QUOTE = LayoutConfig(
    layout_id="quote",
    layout_name="Quote Slide",
    css_classes=["quote-slide"],
    priority=LayoutPriority.HIGH,
    title="Emphasize Important Quotes",
    purpose="Display impactful quotes with visual prominence and proper attribution. Used for opening questions, thought leadership, or supporting evidence.",
    best_for=[
        "Opening questions or statements",
        "Thought-provoking quotes",
        "Expert opinions and thought leadership",
        "Supporting evidence from authorities",
        "Closing inspiration or wisdom",
        "Cultural or philosophical statements"
    ],
    content_indicators=[
        "Contains <blockquote> element",
        "Has quotation marks in text",
        "Includes attribution (author, source, year)",
        "Short text (1-3 sentences typical)",
        "May use .quote-slide class",
        "Often positioned early or late in deck"
    ],
    required_elements=[
        "Quote text (in blockquote or with quote marks)",
        "Attribution information"
    ],
    optional_elements=[
        "Author photo or icon",
        "Quotation mark visual elements",
        "Colored or image background",
        "Source citation details"
    ],
    handler_method="handle_quote_slide",
    visual_notes="Large quotation marks (visual), centered or left-aligned text (32-40px), attribution below (18px muted)"
)

LAYOUT_REFERENCES = LayoutConfig(
    layout_id="references",
    layout_name="References / Citations",
    css_classes=["references-slide", "citations-slide"],
    priority=LayoutPriority.MEDIUM,
    title="Academic References and Citations",
    purpose="Present academic references in proper APA format with professional styling. Provides credibility and allows audience to explore sources.",
    best_for=[
        "End-of-presentation references",
        "Bibliography or works cited",
        "APA/MLA formatted citations",
        "Academic source attribution",
        "Research paper citations",
        "Further reading lists"
    ],
    content_indicators=[
        "Title contains 'references', 'citations', 'bibliography', 'works cited'",
        "Multiple citation paragraphs",
        "APA format: Author. (Year). Title. Source.",
        "Alphabetically ordered list",
        "Hanging indent formatting",
        "URLs or DOIs present"
    ],
    required_elements=[
        "Title indicating references",
        "Multiple formatted citations"
    ],
    optional_elements=[
        "Multiple columns for long lists",
        "Grouped by source type",
        "QR codes for digital access"
    ],
    handler_method="handle_references_slide",
    visual_notes="Clean minimal design, small font (11-12px), hanging indents, 1.5 line spacing, optional multi-column"
)

LAYOUT_FRAMEWORK = LayoutConfig(
    layout_id="framework",
    layout_name="Framework / Diagram",
    css_classes=["framework-slide", "diagram-slide", "model-slide"],
    priority=LayoutPriority.MEDIUM_HIGH,
    title="Visual Models and Process Diagrams",
    purpose="Present conceptual frameworks, process models, or theoretical diagrams with visual clarity. Shows relationships and structure.",
    best_for=[
        "Theoretical frameworks",
        "Process models (linear or cyclical)",
        "System diagrams",
        "Relationship visualizations",
        "Step-by-step processes with connections",
        "Conceptual models (e.g., Creative Tension, Gibbs' Cycle)"
    ],
    content_indicators=[
        "Has .framework-slide or .diagram-slide class",
        "Title mentions 'model', 'framework', 'process', 'cycle'",
        "Content describes visual relationships",
        "Arrows, connections, or flow indicated in text",
        "Numbered or labeled components",
        "Circular, linear, or hierarchical structure described"
    ],
    required_elements=[
        "Framework title",
        "Multiple connected components"
    ],
    optional_elements=[
        "Arrows between elements",
        "Numbered steps",
        "Color-coded categories",
        "Legend or key"
    ],
    handler_method="handle_framework_slide",
    visual_notes="Boxes with arrows, circular layouts for cycles, color-coded elements, clear visual hierarchy"
)

LAYOUT_REFLECTION = LayoutConfig(
    layout_id="reflection",
    layout_name="Reflection / Thinking Prompt",
    css_classes=["reflection-slide", "thinking-prompt"],
    priority=LayoutPriority.MEDIUM_HIGH,
    title="Contemplative Questions and Reflection",
    purpose="Provide space for contemplation and self-reflection. Signals pause for thinking, not immediate answers.",
    best_for=[
        "Reflection questions",
        "Self-assessment prompts",
        "Critical thinking questions",
        "Personal connection exercises",
        "Values exploration",
        "Journaling prompts"
    ],
    content_indicators=[
        "Title contains 'reflection', 'think', 'consider', 'question'",
        "Question format (ends with ?)",
        "Phrase 'think quietly', 'pause', 'reflect on'",
        "Personal pronouns (you, your)",
        "Multiple introspective questions",
        "Has .reflection-slide class"
    ],
    required_elements=[
        "Question or prompt text",
        "Contemplative framing"
    ],
    optional_elements=[
        "Thinking time indicator (e.g., '1 minute')",
        "Thought bubble or question mark icon",
        "Note-taking space indication",
        "Follow-up discussion cue"
    ],
    handler_method="handle_reflection_slide",
    visual_notes="Clean spacious layout, soft background (light blue/cream), large question text (20-24px), thought icon optional"
)

LAYOUT_COMPARISON_TABLE = LayoutConfig(
    layout_id="comparison-table",
    layout_name="Comparison Table (2-Column)",
    css_classes=["comparison-table-slide"],
    priority=LayoutPriority.HIGH,
    title="Two-Column Concept Comparison",
    purpose="Compare and contrast two concepts in detailed table format. Emphasizes differences and similarities across multiple dimensions.",
    best_for=[
        "Detailed concept comparisons",
        "Before/After states with multiple aspects",
        "Theory A vs. Theory B",
        "Traditional vs. Modern approaches",
        "Personal Vision vs. Goals (multiple rows)",
        "Comparing frameworks or methodologies"
    ],
    content_indicators=[
        "Has 2-column table structure",
        "Title contains 'vs', 'versus', 'compared to', 'comparison'",
        "Multiple rows (4-8 typical)",
        "Contrasting concepts in columns",
        "Row headers describing comparison dimensions",
        "Has .comparison-table-slide class"
    ],
    required_elements=[
        "2-column table",
        "Multiple comparison rows (3+)"
    ],
    optional_elements=[
        "Contrasting column colors",
        "'VS' symbol or arrow between columns",
        "Row striping for readability",
        "Summary row at bottom"
    ],
    handler_method="handle_comparison_table_slide",
    visual_notes="2 columns with contrasting colors, VS symbol, multiple rows, clear headers, emphasis on differences"
)

LAYOUT_STANDARD = LayoutConfig(
    layout_id="standard",
    layout_name="Standard Content Slide",
    css_classes=["content-slide"],
    priority=LayoutPriority.LOW,
    title="Main Lecture Content (Default)",
    purpose="Present standard lecture content with title and supporting information. Most common layout.",
    best_for=[
        "Bullet-point lists (2-6 items)",
        "Paragraph text with headings",
        "Mixed content (text + small lists)",
        "Concept explanations",
        "Process steps",
        "Key takeaways"
    ],
    content_indicators=[
        "Has <h2> or <h3> title",
        "Contains <ul>, <ol>, or <p> elements",
        "Content is not primarily tabular",
        "No special layout classes",
        "2-6 bullet points typical",
        "May have multiple paragraphs"
    ],
    required_elements=[
        "Slide title (h2 or h3)",
        "Content container with text"
    ],
    optional_elements=[
        "Bullet/numbered lists",
        "Paragraphs",
        "Bold/italic formatting",
        "Footer citations"
    ],
    handler_method="handle_content_slide",
    visual_notes="Title at top (28px), content area with padding, bullet points, slide number bottom-right"
)


# ============================================================================
# LAYOUT REGISTRY
# ============================================================================

# All layouts in priority order (highest to lowest)
ALL_LAYOUTS = [
    LAYOUT_TITLE,
    LAYOUT_SECTION_BREAK,
    LAYOUT_VOCAB_TABLE,
    LAYOUT_OBJECTIVES,
    LAYOUT_BIG_NUMBER,
    LAYOUT_QUOTE,                # Priority 8 (HIGH)
    LAYOUT_COMPARISON_TABLE,     # Priority 8 (HIGH)
    LAYOUT_ACTIVITY,
    LAYOUT_COMPARISON,
    LAYOUT_CARD,
    LAYOUT_STATS_BANNER,
    LAYOUT_FRAMEWORK,            # Priority 7 (MEDIUM_HIGH)
    LAYOUT_REFLECTION,           # Priority 7 (MEDIUM_HIGH)
    LAYOUT_CHECKLIST,
    LAYOUT_REFERENCES,           # Priority 5 (MEDIUM)
    LAYOUT_DARK,
    LAYOUT_STANDARD,  # Default fallback
]

# Map layout IDs to configs
LAYOUTS_BY_ID = {layout.layout_id: layout for layout in ALL_LAYOUTS}

# Map CSS classes to configs
LAYOUTS_BY_CLASS = {}
for layout in ALL_LAYOUTS:
    for css_class in layout.css_classes:
        LAYOUTS_BY_CLASS[css_class] = layout

# Map handler method names to configs
LAYOUTS_BY_HANDLER = {layout.handler_method: layout for layout in ALL_LAYOUTS}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_layout_by_id(layout_id: str) -> Optional[LayoutConfig]:
    """Get layout configuration by ID."""
    return LAYOUTS_BY_ID.get(layout_id)


def get_layout_by_class(css_class: str) -> Optional[LayoutConfig]:
    """Get layout configuration by CSS class name."""
    return LAYOUTS_BY_CLASS.get(css_class)


def get_layout_by_handler(handler_method: str) -> Optional[LayoutConfig]:
    """Get layout configuration by handler method name."""
    return LAYOUTS_BY_HANDLER.get(handler_method)


def get_layouts_by_priority() -> List[LayoutConfig]:
    """Get all layouts sorted by priority (highest first)."""
    return sorted(ALL_LAYOUTS, key=lambda x: x.priority, reverse=True)


def print_layout_summary():
    """Print a summary of all available layouts."""
    print("HTML to PPTX Converter - Available Layouts")
    print("=" * 80)
    print(f"Total layouts: {len(ALL_LAYOUTS)}\n")

    for layout in get_layouts_by_priority():
        print(f"{layout.layout_name} (Priority: {layout.priority})")
        print(f"  ID: {layout.layout_id}")
        print(f"  Classes: {', '.join(layout.css_classes)}")
        print(f"  Handler: {layout.handler_method}")
        print(f"  Purpose: {layout.purpose}")
        print()


if __name__ == "__main__":
    # Print layout summary when run directly
    print_layout_summary()
