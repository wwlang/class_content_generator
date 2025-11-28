#!/usr/bin/env python3
"""
Convert lecture content markdown to HTML presentation slides.
Follows the enhanced design system from reference examples.
"""

import re
from typing import List, Dict, Tuple

class SlideConverter:
    """Converts markdown lecture content to HTML slides."""

    # Semantic keyword lists for framework slide parsing
    SUBTITLE_INDICATORS = [
        'according to', 'based on', 'research shows',
        'in three questions', 'in four steps', 'in five steps',
        'has three dimensions', 'has four components',
        'framework', 'model', 'as ongoing exchange',
        'strategic message planning', 'communication as'
    ]

    AUXILIARY_INDICATORS = [
        'key insight', 'business application', 'why this matters',
        'application', 'limitation', 'example', 'note',
        'remember', 'important', 'context', 'what this adds',
        'all three required', 'all four required'
    ]

    # Keywords that indicate this is a component, not auxiliary
    COMPONENT_KEYWORDS = [
        'sender', 'receiver', 'encoder', 'decoder', 'channel', 'noise',
        'feedback', 'person', 'competence', 'character', 'connection',
        'care', 'logic', 'empathy', 'authenticity',
        'know', 'feel', 'do'
    ]

    def __init__(self, lecture_md_path: str, output_html_path: str):
        self.lecture_md_path = lecture_md_path
        self.output_html_path = output_html_path
        self.slides = []
        self.instructor_names = self.extract_instructor_names()

    def read_markdown(self) -> str:
        """Read the markdown file."""
        with open(self.lecture_md_path, 'r', encoding='utf-8') as f:
            return f.read()

    def extract_instructor_names(self) -> str:
        """Extract instructor names from syllabus."""
        try:
            # Determine syllabus path from lecture path
            # Path structure: courses/COURSE-CODE/weeks/week-N/lecture-content.md
            # Syllabus is at: courses/COURSE-CODE/syllabus.md
            import os
            lecture_dir = os.path.dirname(self.lecture_md_path)

            # Navigate up from week-N directory to course root
            if 'weeks' in lecture_dir:
                # Go up two levels: week-N -> weeks -> course-root
                course_dir = os.path.dirname(os.path.dirname(lecture_dir))
                syllabus_path = os.path.join(course_dir, 'syllabus.md')

                if os.path.exists(syllabus_path):
                    with open(syllabus_path, 'r', encoding='utf-8') as f:
                        syllabus_content = f.read()

                    # Extract instructor names from syllabus
                    # Look for pattern: **Instructors:** followed by names with dashes or bullets
                    instructor_match = re.search(r'\*\*Instructors?:\*\*\s*\n((?:[-•]\s*.+\n?)+)', syllabus_content)
                    if instructor_match:
                        # Extract names and clean them
                        names_text = instructor_match.group(1)
                        names = re.findall(r'[-•]\s*(.+)', names_text)
                        # Join with comma and "and" for last name
                        if len(names) > 1:
                            return ', '.join(names[:-1]) + ' and ' + names[-1]
                        elif names:
                            return names[0]
        except Exception as e:
            # If anything fails, silently continue without instructor names
            pass

        return ''

    def parse_slides(self, content: str) -> List[Dict]:
        """Parse markdown content into slide data structures."""
        slides = []

        # Split content into slide blocks
        # Pattern: Find SLIDE markers and capture everything until the next SLIDE or end
        slide_pattern = r'\*\*SLIDE (\d+):\s*(.+?)\*\*.*?(?=\*\*SLIDE \d+:|$)'
        slide_matches = re.finditer(slide_pattern, content, re.DOTALL)

        for match in slide_matches:
            slide_num = match.group(1)
            slide_title = match.group(2).strip()
            full_section = match.group(0)

            # Check if there's an explicit TITLE: line (overrides the slide label)
            title_match = re.search(r'^TITLE:\s*(.+?)$', full_section, re.MULTILINE)
            if title_match:
                slide_title = title_match.group(1).strip()

            # Extract SUBTITLE if present
            subtitle_match = re.search(r'^SUBTITLE:\s*(.+?)$', full_section, re.MULTILINE)
            slide_subtitle = subtitle_match.group(1).strip() if subtitle_match else ""

            # Extract CONTENT section
            # Try with explicit CONTENT: marker first (old format)
            content_match = re.search(r'CONTENT:(.*?)(?:\[PURPOSE:|\n---)', full_section, re.DOTALL)
            if content_match:
                slide_content = content_match.group(1).strip()
            else:
                # New format: content is between slide title and [PURPOSE:] or ## Speaker Notes
                # Skip the slide title line but KEEP layout comments for layout detection
                after_title = re.split(r'\*\*SLIDE \d+:.*?\*\*\s*\n', full_section, maxsplit=1)
                if len(after_title) > 1:
                    remaining = after_title[1]
                    # DON'T remove layout comments yet - detect_layout() needs them
                    # Extract content up to [PURPOSE:], [TIMING:], ---, or ## Speaker Notes
                    content_match2 = re.search(r'^(.*?)(?:\[PURPOSE:|\[TIMING:|\n---|\n## Speaker Notes)', remaining, re.DOTALL)
                    slide_content = content_match2.group(1).strip() if content_match2 else remaining.strip()
                else:
                    slide_content = ""

            # Extract speaker notes (comes after the first --- separator after CONTENT)
            notes_match = re.search(r'## Speaker Notes(.*?)(?=\n\*\*SLIDE|\Z)', full_section, re.DOTALL)
            speaker_notes = notes_match.group(1).strip() if notes_match else ""

            # Extract full references from content
            slide_content, references = self.extract_references(slide_content)

            # Also extract legacy citation format (with URLs/DOIs)
            legacy_citations = re.findall(r'\*[^*]+\*\s*\([^)]+\)\.\s*(?:https?://[^\s]+|DOI:[^\s]+)', slide_content)

            # Combine references
            all_citations = references + legacy_citations

            slides.append({
                'number': int(slide_num),
                'title': slide_title,
                'subtitle': slide_subtitle,
                'content': slide_content,
                'notes': speaker_notes,
                'citations': all_citations
            })

        return slides

    def detect_layout(self, slide: Dict) -> str:
        """
        Detect the appropriate layout for a slide based on content.

        Priority order:
        1. Explicit layout hints (HTML comments, markers)
        2. Content-based pattern matching
        3. Default to standard content
        """
        content = slide['content']
        title = slide['title']

        # EXPLICIT LAYOUT HINTS (Highest Priority)
        # Look for layout markers like <!-- LAYOUT: quote --> in content
        # Find ALL layout hints (supports multiple hints like big-number + dark-bg)
        layout_hints = re.findall(r'<!--\s*LAYOUT:\s*([\w-]+)\s*-->', content, re.IGNORECASE)
        layout_hints = [hint.lower() for hint in layout_hints]

        valid_layouts = ['quote', 'references', 'framework', 'diagram', 'reflection',
                       'thinking-prompt', 'comparison-table', 'vocab-table', 'section-break', 'dark-bg',
                       'stats-banner', 'big-number', 'big-number-slide']

        # Filter to valid layout hints
        valid_hints = [hint for hint in layout_hints if hint in valid_layouts]

        if valid_hints:
            # Remove ALL layout hints from content so they don't appear in HTML
            slide['content'] = re.sub(r'<!--\s*LAYOUT:\s*[\w-]+\s*-->', '', slide['content']).strip()

            # Normalize layout names (big-number-slide → big-number)
            valid_hints = ['big-number' if hint == 'big-number-slide' else hint for hint in valid_hints]

            # Primary layout is the first non-dark-bg hint (dark-bg is a modifier, not primary layout)
            primary_layout = None
            for hint in valid_hints:
                if hint != 'dark-bg':
                    primary_layout = hint
                    break

            # If only dark-bg hint, use 'content' as primary layout
            if primary_layout is None:
                primary_layout = 'content'

            # Store dark-bg flag in slide metadata for later use
            slide['is_dark'] = 'dark-bg' in valid_hints

            # VALIDATE reflection hint against content structure
            # Reflection slides should be simple prompts, not complex structured content
            if primary_layout == 'reflection':
                # Check for indicators of structured content (not reflection)
                has_numbered_list = bool(re.search(r'^\d+\.\s+', content, re.MULTILINE))
                has_bullet_list = bool(re.search(r'^[-•]\s+', content, re.MULTILINE))
                bold_count = content.count('**')
                has_integration_summary = 'Integration' in title or 'Summary' in title

                # If structured content, override to 'content' layout
                if (has_numbered_list or has_bullet_list or bold_count >= 6 or has_integration_summary):
                    return 'content'

            # VALIDATE big-number hint against statistics count
            # Big number is for single statistic only; multiple stats should use stats-banner
            if primary_layout == 'big-number':
                # Count bold percentage patterns: **87%**, **73%**, etc.
                stat_pattern = r'\*\*\d+(?:\.\d+)?%\*\*'
                stat_matches = re.findall(stat_pattern, content)
                stat_count = len(stat_matches)

                # If multiple statistics, override to stats-banner
                if stat_count >= 2:
                    return 'stats-banner'
                # Single stat or no stats: keep big-number
                elif stat_count == 1:
                    return 'big-number'
                # No percentage stats found - check for other number patterns
                else:
                    # Look for other bold number patterns: **1,234**, **$5.6M**, etc.
                    number_pattern = r'\*\*[\d,\.$€£¥]+[KMB]?\*\*'
                    number_matches = re.findall(number_pattern, content)
                    if len(number_matches) >= 2:
                        return 'stats-banner'
                    elif len(number_matches) == 1:
                        return 'big-number'
                    # No stats found, but hint provided - respect hint
                    return 'big-number'

            return primary_layout

        # Title slide (slide 1)
        if slide['number'] == 1:
            return 'title'

        # CONTENT-BASED DETECTION (By priority)

        # Section break detection
        if ('Section Break' in title or 'SECTION BREAK' in title or
            re.search(r'^(Part \d+|SEGMENT \d+|Synthesis)', title)):
            return 'section-break'

        # Quote detection (HIGH PRIORITY)
        # True quote slides have a single quote with attribution (— Author)
        has_quote_marks = bool(re.search(r'^\s*["\'""]|^>\s+', content, re.MULTILINE)) or 'Quote:' in content
        has_attribution = bool(re.search(r'—\s*\w+', content))  # Em dash followed by name
        quote_count = content.count('"') + content.count('"') + content.count('"')

        # Single quote with attribution → quote slide
        if has_quote_marks and has_attribution and quote_count <= 4:  # Max 2 quote pairs
            return 'quote'

        # Multiple quotes without attribution → content (examples, not quote slide)
        # Let this fall through to other detection

        # References detection (HIGH PRIORITY)
        if 'References' in title or 'Citations' in title or 'Sources' in title:
            return 'references'
        # Also detect by content pattern (multiple citations)
        citation_pattern = r'\([12]\d{3}\)'  # Year in parentheses like (2023)
        if content.count('(') >= 3 and len(re.findall(citation_pattern, content)) >= 2:
            return 'references'

        # Framework/Diagram detection (HIGH PRIORITY - before reflection)
        if any(keyword in title for keyword in ['Framework', 'Model', 'Diagram', 'Process']):
            return 'framework'

        # Detect numbered rules/principles pattern (e.g., "Rule 1:", "Principle 2:", "Step 3:")
        # Common in design guidelines, best practices, procedural frameworks
        rule_pattern = r'\*\*(?:Rule|Principle|Step|Guideline)\s+\d+:'
        rule_matches = re.findall(rule_pattern, content)
        if len(rule_matches) >= 3:  # At least 3 numbered components
            return 'framework'

        # Detect structured multi-component content (Assessment, Evaluation, Integration)
        # These have 3-4 bold headings with descriptions - framework format
        bold_count = content.count('**')
        has_check_pattern = 'Check:' in content or 'Assessment:' in content or 'Evaluate' in title
        has_component_words = any(word in content for word in ['Component', 'Step', 'Element'])
        has_integration = 'Integration' in title or 'Summary' in title

        # Multi-component structured content = framework
        if bold_count >= 6:
            if has_component_words or has_check_pattern or has_integration:
                return 'framework'

        # Reflection prompt detection (MEDIUM-HIGH PRIORITY)
        # Single reflective question or open-ended prompt
        if any(keyword in content for keyword in ['Reflect on these', 'Think about:', 'Consider:']):
            # But not if it's structured evaluation (that's framework)
            if not has_check_pattern:
                return 'reflection'
        # Questions with reflective indicators
        if '?' in content and any(word in content.lower() for word in ['how might you', 'what would you', 'why do you']):
            if not has_check_pattern:
                return 'reflection'

        # Comparison table detection (HIGH PRIORITY)
        if 'vs' in title.lower() or 'versus' in title.lower() or 'comparison' in title.lower():
            if '|' in content and '---' in content:
                return 'comparison-table'

        # Big number / Stats banner detection
        # Count bold percentage patterns to distinguish single vs multiple stats
        stat_pattern = r'\*\*\d+(?:\.\d+)?%\*\*'
        stat_matches = re.findall(stat_pattern, content)
        stat_count = len(stat_matches)

        if stat_count >= 2:
            # Multiple statistics → stats-banner layout
            return 'stats-banner'
        elif stat_count == 1 and len(content) < 300:
            # Single statistic → big-number layout
            return 'big-number'

        # Table detection (vocabulary slides)
        if '|' in content and '---' in content:
            return 'table'

        # Stats/metrics detection (multiple statistics)
        # IMPORTANT: Exclude assessment-related slides from stats detection
        assessment_keywords = ['assessment', 'checklist', 'exam', 'quiz', 'assignment', 'presentation', 'rubric', 'grading']
        if not any(keyword in title.lower() for keyword in assessment_keywords):
            if content.count('%') >= 3 or content.count('📌') >= 2:
                return 'stats'

        # Dark background detection for contextual/example slides
        # Check both title and content for Vietnamese, case study, or example indicators
        dark_keywords = ['Vietnamese', 'Case study', 'Case:', 'Example:']
        title_lower = title.lower()
        content_lower = content.lower()

        if any(keyword.lower() in title_lower or keyword.lower() in content_lower
               for keyword in dark_keywords):
            # Set dark flag for content slide
            slide['is_dark'] = True
            return 'content'

        # Default: standard content with bullets
        return 'content'

    def extract_references(self, content: str) -> Tuple[str, List[str]]:
        """
        Extract full APA-style references from content and return cleaned content + references.

        Distinguishes between:
        - Full references (italicized, with Author, Year, Title, Source) → extract to footer
        - Inline citations (parenthetical like "(Author, Year)") → keep in content

        Args:
            content: Slide content text

        Returns:
            Tuple of (cleaned_content, list_of_references)
        """
        references = []

        # Pattern for full APA-style references:
        # - Italicized with *...*
        # - Starts with capital letter (Author name)
        # - Contains (YYYY) year format
        # - Has period after year: (YYYY).
        # - Followed by title and source information
        # - May include volume/issue/page numbers after closing asterisk
        #
        # Examples:
        # *Senge, P. M. (2006). The fifth discipline. Currency/Doubleday.*
        # *Pink, D. H. (2009). Drive: The surprising truth about what motivates us. Riverhead Books.*
        # *Ericsson, K. A., Krampe, R. T., & Tesch-Römer, C. (1993). The role of deliberate practice in the acquisition of expert performance. Psychological Review, 100*(3), 363-406.
        # *Doran, G. T. (1981). There's a S.M.A.R.T. way to write management's goals and objectives. Management Review, 70*(11), 35-36.
        #
        # Pattern explanation:
        # \*[A-Z][^*]+?\([12][0-9]{3}\)\.[^*]+\*  - Main reference in italics
        # (?:\([0-9]+\),?\s*)?                    - Optional (Issue) number
        # (?:\d+[-–]\d+)?                         - Optional page range (e.g., 35-36)
        # \.?                                     - Optional ending period

        # Main reference pattern with optional volume/issue/page extensions
        reference_pattern = r'\*[A-Z][^*]+?\([12][0-9]{3}\)\.[^*]+\*(?:\([0-9]+\),?\s*)?(?:\d+[-–]\d+)?\.?'

        # Find all full references
        matches = re.finditer(reference_pattern, content)

        for match in matches:
            ref_text = match.group(0)
            # Remove ALL asterisks (italics markers) from reference
            clean_ref = ref_text.replace('*', '').strip()
            references.append(clean_ref)

            # Remove from content
            content = content.replace(ref_text, '')

        # Clean up any resulting empty lines or extra whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # Max 2 newlines
        content = content.strip()

        return content, references

    def convert_inline_markdown(self, text: str) -> str:
        """Convert only inline markdown formatting (bold, italic, code) to HTML.

        Does NOT convert block elements like lists, tables, or paragraphs.
        Used for framework card descriptions where we want plain text with formatting.
        """
        # Remove layout hints
        text = re.sub(r'<!--\s*LAYOUT:\s*[\w-]+\s*-->', '', text)

        # Bold (double asterisks)
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

        # Italics (single asterisks) - do after bold to avoid interference
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

        # Inline code (backticks)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

        # Links [text](url)
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

        return text.strip()

    def convert_markdown_to_html(self, text: str) -> str:
        """Convert markdown formatting to HTML."""
        # First, remove ALL layout hints from the entire text
        text = re.sub(r'<!--\s*LAYOUT:\s*[\w-]+\s*-->', '', text)

        # Extract and preserve code blocks before other processing
        code_blocks = []
        def save_code_block(match):
            code_blocks.append(match.group(1))
            return f'__CODE_BLOCK_{len(code_blocks)-1}__'

        # Find code blocks (``` ... ```)
        text = re.sub(r'```\n?(.*?)\n?```', save_code_block, text, flags=re.DOTALL)

        # Bold (double asterisks)
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

        # Italics (single asterisks) - do after bold to avoid interference
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

        # Lists and tables
        lines = text.split('\n')
        html_lines = []
        in_ul = False
        in_ol = False
        in_nested_ul = False
        in_table = False
        table_rows = []

        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue

            # Check if this line contains a code block placeholder
            if '__CODE_BLOCK_' in line:
                # Close any open lists or tables
                if in_nested_ul:
                    html_lines.append('</ul>')
                    in_nested_ul = False
                if in_ul:
                    html_lines.append('</ul>')
                    in_ul = False
                if in_ol:
                    html_lines.append('</ol>')
                    in_ol = False
                if in_table:
                    html_lines.append(self._convert_table_to_html(table_rows))
                    in_table = False
                    table_rows = []

                # Extract code block index and restore content
                match = re.search(r'__CODE_BLOCK_(\d+)__', line)
                if match:
                    idx = int(match.group(1))
                    code_content = code_blocks[idx]
                    html_lines.append(f'<pre><code>{code_content}</code></pre>')
                continue

            # Check if line is a table row (starts and ends with |)
            if line.strip().startswith('|') and line.strip().endswith('|'):
                # Close any open lists
                if in_nested_ul:
                    html_lines.append('</ul>')
                    in_nested_ul = False
                if in_ul:
                    html_lines.append('</ul>')
                    in_ul = False
                if in_ol:
                    html_lines.append('</ol>')
                    in_ol = False

                if not in_table:
                    in_table = True
                    table_rows = []

                # Skip separator rows (|---|---|)
                if re.match(r'^\|\s*[-:]+\s*\|', line):
                    continue

                table_rows.append(line)
            else:
                # If we were in a table, close it and convert to HTML
                if in_table:
                    html_lines.append(self._convert_table_to_html(table_rows))
                    in_table = False
                    table_rows = []

                # Check for numbered list items (1., 2., 3., etc.)
                numbered_match = re.match(r'^(\d+)\.\s+(.+)$', line)
                if numbered_match:
                    # Close nested list if open
                    if in_nested_ul:
                        html_lines.append('</ul>')
                        in_nested_ul = False
                    # Close unordered list if open
                    if in_ul:
                        html_lines.append('</ul>')
                        in_ul = False
                    # Open ordered list if needed
                    if not in_ol:
                        html_lines.append('<ol>')
                        in_ol = True
                    item_content = numbered_match.group(2)
                    html_lines.append(f'<li>{item_content}</li>')
                # Check for nested bullet points (indented with spaces/tabs)
                elif re.match(r'^\s+[-•✓✗📌]\s+', line):
                    # This is a nested bullet under a numbered item
                    if not in_nested_ul:
                        html_lines.append('<ul class="nested-list">')
                        in_nested_ul = True
                    item = re.sub(r'^\s+[-•✓✗📌]\s+', '', line)
                    html_lines.append(f'<li>{item}</li>')
                # Check for regular bullet points
                elif re.match(r'^[-•✓✗📌]\s+', line):
                    # Close nested list if open
                    if in_nested_ul:
                        html_lines.append('</ul>')
                        in_nested_ul = False
                    # Close ordered list if open
                    if in_ol:
                        html_lines.append('</ol>')
                        in_ol = False
                    # Open unordered list if needed
                    if not in_ul:
                        html_lines.append('<ul>')
                        in_ul = True
                    item = re.sub(r'^[-•✓✗📌]\s+', '', line)
                    html_lines.append(f'<li>{item}</li>')
                else:
                    # Close all lists if we hit non-list content
                    if in_nested_ul:
                        html_lines.append('</ul>')
                        in_nested_ul = False
                    if in_ul:
                        html_lines.append('</ul>')
                        in_ul = False
                    if in_ol:
                        html_lines.append('</ol>')
                        in_ol = False

                    if line.strip():
                        html_lines.append(f'<p>{line}</p>')

        # Close any open table
        if in_table:
            html_lines.append(self._convert_table_to_html(table_rows))

        # Close any open lists
        if in_nested_ul:
            html_lines.append('</ul>')
        if in_ul:
            html_lines.append('</ul>')
        if in_ol:
            html_lines.append('</ol>')

        return '\n'.join(html_lines)

    def _convert_inline_markdown(self, text: str) -> str:
        """Convert inline markdown formatting (bold, italic) to HTML."""
        # Bold (double asterisks)
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        # Italics (single asterisks) - do after bold to avoid interference
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        # Inline code (backticks)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        return text

    def _convert_table_to_html(self, rows: list) -> str:
        """Convert markdown table rows to HTML table."""
        if not rows:
            return ''

        html = '<table>\n'

        # First row is header
        if len(rows) > 0:
            html += '  <thead>\n    <tr>\n'
            header_cells = [cell.strip() for cell in rows[0].split('|')[1:-1]]
            for cell in header_cells:
                # Convert markdown formatting in header cells
                formatted_cell = self._convert_inline_markdown(cell)
                html += f'      <th>{formatted_cell}</th>\n'
            html += '    </tr>\n  </thead>\n'

        # Remaining rows are body
        if len(rows) > 1:
            html += '  <tbody>\n'
            for row in rows[1:]:
                html += '    <tr>\n'
                body_cells = [cell.strip() for cell in row.split('|')[1:-1]]
                for cell in body_cells:
                    # Convert markdown formatting in body cells
                    formatted_cell = self._convert_inline_markdown(cell)
                    html += f'      <td>{formatted_cell}</td>\n'
                html += '    </tr>\n'
            html += '  </tbody>\n'

        html += '</table>'
        return html

    def generate_speaker_notes_html(self, notes: str) -> str:
        """
        Generate HTML for speaker notes section.

        Args:
            notes: Speaker notes text (markdown format)

        Returns:
            HTML string for speaker notes aside element
        """
        if not notes or not notes.strip():
            return ''

        # Convert markdown to HTML for notes
        notes_html = self.convert_markdown_to_html(notes)

        return f'''
      <aside class="speaker-notes">
        <h4>Speaker Notes</h4>
        <div class="notes-content">
          {notes_html}
        </div>
      </aside>'''

    def generate_slide_html(self, slide: Dict, layout: str) -> str:
        """Generate HTML for a single slide based on layout.

        Returns a string containing one or more slides (references may be paginated).
        """
        content_html = self.convert_markdown_to_html(slide['content'])

        if layout == 'title':
            return self.generate_title_slide(slide)
        elif layout == 'section-break':
            return self.generate_section_break(slide)
        elif layout == 'table':
            return self.generate_table_slide(slide)
        elif layout == 'stats' or layout == 'stats-banner':
            return self.generate_stats_slide(slide)
        elif layout == 'big-number':
            return self.generate_big_number_slide(slide)
        elif layout == 'framework':
            return self.generate_framework_slide(slide)
        elif layout == 'quote':
            return self.generate_quote_slide(slide)
        elif layout == 'dark-bg':
            return self.generate_dark_slide(slide)
        elif layout == 'comparison-table':
            return self.generate_comparison_table_slide(slide)
        elif layout == 'reflection':
            return self.generate_reflection_slide(slide)
        elif layout == 'references':
            return self.generate_references_slide(slide)
        else:
            return self.generate_content_slide(slide, layout)

    def generate_title_slide(self, slide: Dict) -> str:
        """Generate title slide HTML."""
        notes_html = self.generate_speaker_notes_html(slide['notes'])

        # Use subtitle if provided, otherwise use default
        subtitle = slide.get('subtitle', 'Personal and Professional Development')

        # Parse content for course info (usually contains course name, university, week)
        # Filter out layout hints and duplicate title
        content_lines = []
        for line in slide['content'].split('\n'):
            line = line.strip()
            if not line:
                continue
            # Skip layout hints
            if re.match(r'^\s*<!--\s*LAYOUT:\s*[\w-]+\s*-->\s*$', line):
                continue
            # Skip if line matches the slide title (to avoid duplication)
            if line == slide['title']:
                continue
            content_lines.append(line)

        # Convert markdown bold in content lines
        content_lines = [re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', line) for line in content_lines]

        # Build author info with instructor names if available
        author_parts = []
        if self.instructor_names:
            author_parts.append(self.instructor_names)
        if content_lines:
            author_parts.extend(content_lines)

        author_info = '<br>'.join(author_parts) if author_parts else 'Week 12'

        return f'''
    <div class="slide title-slide" data-slide="{slide['number']}">
      <div class="title-content">
        <h1>{slide['title']}</h1>
        <p class="subtitle">{subtitle}</p>
        <p class="author">{author_info}</p>
      </div>
      <div class="decorative-shapes">
        <div class="shape orange"></div>
        <div class="shape tan"></div>
        <div class="shape small"></div>
      </div>
      {notes_html}
    </div>'''

    def generate_section_break(self, slide: Dict) -> str:
        """Generate section break slide HTML."""
        notes_html = self.generate_speaker_notes_html(slide['notes'])

        # Include subtitle if provided
        subtitle_html = f'<p class="section-subtitle">{slide["subtitle"]}</p>' if slide.get('subtitle') else ''

        return f'''
    <div class="slide section-break-slide" data-slide="{slide['number']}">
      <h2 class="section-title">{slide['title']}</h2>
      {subtitle_html}
      {notes_html}
    </div>'''

    def generate_table_slide(self, slide: Dict) -> str:
        """Generate table slide HTML (for vocabulary, etc.)."""
        # Extract table from markdown
        table_match = re.search(r'\|.*?\|.*?\n\|[-:| ]+\n((?:\|.*?\|.*?\n)+)', slide['content'], re.DOTALL)

        if table_match:
            table_html = '<table class="vocab-table">'
            rows = table_match.group(0).strip().split('\n')

            # Header row
            headers = [cell.strip() for cell in rows[0].split('|')[1:-1]]
            table_html += '<thead><tr>'
            for header in headers:
                # Convert markdown formatting in header cells
                header = self._convert_inline_markdown(header)
                table_html += f'<th>{header}</th>'
            table_html += '</tr></thead><tbody>'

            # Data rows (skip separator row)
            for row in rows[2:]:
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                table_html += '<tr>'
                for cell in cells:
                    # Convert markdown formatting in body cells
                    cell = self._convert_inline_markdown(cell)
                    table_html += f'<td>{cell}</td>'
                table_html += '</tr>'

            table_html += '</tbody></table>'
        else:
            table_html = ''

        notes_html = self.generate_speaker_notes_html(slide['notes'])
        return f'''
    <div class="slide vocab-table-slide" data-slide="{slide['number']}">
      <h2 class="slide-title">{slide['title']}</h2>
      {table_html}
      {notes_html}
    </div>'''

    def generate_stats_slide(self, slide: Dict) -> str:
        """Generate stats banner slide - horizontal metrics display."""
        content = slide['content']

        # Try to extract from table format first (| number | number | ... |)
        # Match entire table rows with all columns
        table_match = re.search(r'\|(.+)\|\s*\n\|[-:| ]+\|\s*\n\|(.+)\|', content, re.MULTILINE)

        if table_match:
            # Parse table format - split by | and clean
            numbers_row = [cell.strip() for cell in table_match.group(1).split('|') if cell.strip()]
            labels_row = [cell.strip() for cell in table_match.group(2).split('|') if cell.strip()]

            stats_html = '<div class="stats-banner">'
            for i, (number, label) in enumerate(zip(numbers_row[:4], labels_row[:4])):  # Max 4 stats
                stats_html += f'''
        <div class="stat-item">
          <div class="stat-number">{number}</div>
          <div class="stat-description">{label}</div>
        </div>'''
            stats_html += '</div>'
        else:
            # Try emoji-based format first
            stats = re.findall(r'📌\s*\*\*([^*]+)\*\*.*?[-–]\s*\*\*([^:]+):\*\*([^📌\n]+)', content, re.DOTALL)

            if stats:
                # Emoji format found
                stats_html = '<div class="stats-banner">'
                for label, title, description in stats[:4]:  # Max 4 stats
                    stats_html += f'''
        <div class="stat-item">
          <div class="stat-number">{label}</div>
          <div class="stat-label">{title.strip()}</div>
          <div class="stat-description">{description.strip()[:100]}</div>
        </div>'''
                stats_html += '</div>'
            else:
                # Fallback: simple bold number + description format
                # Match: **87%** followed by description text, then **73%** followed by description, etc.
                # Pattern: **NUMBER** \n description text (until next ** or end of logical section)
                stat_pattern = r'\*\*([^*]+?)\*\*\s*\n\s*([^*\n][^\n]*(?:\n(?!\*\*)[^\n]*)*)'
                stat_matches = re.findall(stat_pattern, content)

                if stat_matches:
                    stats_html = '<div class="stats-banner">'
                    for number, description in stat_matches[:4]:  # Max 4 stats
                        # Clean up description (remove extra whitespace, truncate)
                        clean_desc = ' '.join(description.split()).strip()
                        stats_html += f'''
        <div class="stat-item">
          <div class="stat-number">{number.strip()}</div>
          <div class="stat-description">{clean_desc}</div>
        </div>'''
                    stats_html += '</div>'
                else:
                    # No stats found - return empty banner
                    stats_html = '<div class="stats-banner"></div>'

        notes_html = self.generate_speaker_notes_html(slide['notes'])

        # Extract citation if present (usually after table)
        citation_match = re.search(r'\(([^)]+)\)\s*$', content, re.MULTILINE)
        citation_html = f'<p class="citation">{citation_match.group(1)}</p>' if citation_match else ''

        # Stats slides are always dark background
        dark_class = 'dark-bg '

        return f'''
    <div class="slide {dark_class}content-slide" data-slide="{slide['number']}">
      <h2 class="slide-title">{slide['title']}</h2>
      {stats_html}
      {citation_html}
      {notes_html}
    </div>'''

    def generate_big_number_slide(self, slide: Dict) -> str:
        """Generate big number slide."""
        # Extract number - match various formats:
        # **30%**, **$1.82 Billion**, **5,000**, etc.
        number_match = re.search(r'\*\*([^\*]+?)\*\*', slide['content'])
        number = number_match.group(1).strip() if number_match else "?"

        # Extract explanation (everything after the number)
        explanation = re.sub(r'\*\*[^\*]+?\*\*', '', slide['content'], count=1).strip()

        # Convert markdown formatting in explanation (bold text → orange styling)
        # Keep bold markers for now, convert to HTML
        explanation_html = self.convert_markdown_to_html(explanation)

        # Check for dark background flag
        dark_class = ' dark-bg' if slide.get('is_dark', False) else ''

        notes_html = self.generate_speaker_notes_html(slide['notes'])
        return f'''
    <div class="slide big-number-slide{dark_class}" data-slide="{slide['number']}">
      <div class="number-content">
        <div class="big-number">{number}</div>
        <div class="number-explanation">{explanation_html}</div>
      </div>
      {notes_html}
    </div>'''

    def _is_subtitle_not_component(self, text: str) -> bool:
        """
        Determine if bold text ending with : is a subtitle vs component heading.

        Subtitle patterns (NOT components):
        - Long descriptive phrases (>4 words before colon)
        - Contains "According to", "Based on" (citations)
        - Contains "in three questions", "model", "framework" (descriptive)

        Component patterns (ARE components):
        - Short labels: "Sender:", "Competence:", "Step 1:"
        - Numbered: "1. Know:", "Component 1:"
        - Flow diagrams: Contains → arrows
        """
        # Remove markdown formatting
        clean_text = text.replace('**', '').replace(':', '').strip()

        # Check for citation patterns (always subtitles)
        if any(phrase in clean_text for phrase in ['According to', 'Based on', 'Research shows']):
            return True

        # Check for descriptive intro patterns (always subtitles)
        if any(phrase in clean_text.lower() for phrase in ['in three questions', 'in four steps', 'communication model', 'has three dimensions']):
            return True

        # Check for flow diagrams (components, not subtitles)
        if '→' in text or '⇒' in text or '⟶' in text:
            return False

        # Check for numbered components (components, not subtitles)
        if re.match(r'^\*\*\d+\.', text) or re.match(r'^\*\*(Step|Component|Rule|Phase) \d+', text):
            return False

        # Word count heuristic: >4 words = likely subtitle, ≤2 words = likely component
        word_count = len(clean_text.split())
        if word_count > 4:
            return True  # Long phrase = subtitle
        elif word_count <= 2:
            return False  # Short label = component

        # 3-4 words: ambiguous, check if it's descriptive
        # Common component words: Sender, Receiver, Channel, Competence, Character, Connection
        component_words = ['sender', 'receiver', 'channel', 'encoder', 'decoder', 'noise',
                          'competence', 'character', 'connection', 'care', 'logic', 'empathy']
        if any(word in clean_text.lower() for word in component_words):
            return False  # Component term

        # Default: if 3-4 words and not clearly a component, treat as subtitle
        return word_count >= 3

    def detect_and_parse_flow_diagram(self, text: str) -> Tuple[bool, List[str]]:
        """
        Detect if text contains a flow diagram and extract elements.

        Returns:
            Tuple of (is_flow_diagram, elements_list)
            - is_flow_diagram: True if contains → ↔ ⇒ arrows
            - elements_list: List of flow elements (empty if not flow diagram)
        """
        arrows = ['→', '↔', '⇒', '⟶', '⇔']
        is_flow = any(arrow in text for arrow in arrows)

        if not is_flow:
            return False, []

        # Remove bold markers for parsing
        clean_text = text.replace('**', '').strip()

        # Split on any arrow type
        elements = re.split(r'\s*[→↔⇒⟶⇔]\s*', clean_text)

        # Clean up elements
        elements = [elem.strip() for elem in elements if elem.strip()]

        return True, elements

    def parse_multiline_component(self, lines: List[str], start_idx: int) -> Tuple[Dict, int]:
        """
        Parse a component that may span multiple lines with different formatting.

        Structure handled:
        **1. Heading (Label)**           <- Line 1: Component heading
        "Question or statement?"         <- Line 2: Optional question
        - Bullet 1                       <- Lines 3+: Bullets or description
        - Bullet 2

        Args:
            lines: All content lines
            start_idx: Index of component heading line

        Returns:
            Tuple of (component_dict, next_line_index)
            component_dict contains:
                - heading: Component label (e.g., "1. Competence (Logic)")
                - question: Optional question text (if quoted line follows)
                - bullets: List of bullet points
                - description: Remaining description text
        """
        component = {
            'heading': '',
            'question': '',
            'bullets': [],
            'description': ''
        }

        # Line 1: Extract heading (remove bold markers and colon)
        heading_line = lines[start_idx].strip()
        component['heading'] = heading_line.replace('**', '').replace(':', '').strip()

        # Parse subsequent lines until next component or auxiliary section
        idx = start_idx + 1
        while idx < len(lines):
            line = lines[idx].strip()

            # Stop if we hit next numbered component (**N. ...)
            if re.match(r'\*\*\d+\.', line):
                break

            # Stop if we hit next component (starts with ** and has : or ends with **)
            if line.startswith('**') and (':' in line or line.endswith('**')):
                # Check if this is a new component or auxiliary heading
                break

            # Quoted text → question
            if line.startswith('"') and line.endswith('"'):
                component['question'] = line.strip('"')

            # Bullet point
            elif line.startswith('- ') or line.startswith('• '):
                component['bullets'].append(line[2:].strip())

            # Empty line → might be component separator
            elif not line:
                # Peek ahead - if next line is component start, stop
                if idx + 1 < len(lines) and lines[idx + 1].strip().startswith('**'):
                    break

            # Regular text → description
            elif line:
                component['description'] += line + ' '

            idx += 1

        # Clean up description
        component['description'] = component['description'].strip()

        return component, idx

    def generate_framework_slide(self, slide: Dict) -> str:
        """
        Generate framework slide using four-stage semantic parsing.

        Stages:
        1. Extract subtitle (descriptive intro with citation/context)
        2. Extract components (numbered items, flow diagrams, framework labels)
        3. Extract auxiliary content (insights, applications, limitations)
        4. Extract references (italic citations at end)
        """
        content = slide['content'].strip()
        content_lines = [line.strip() for line in content.split('\n') if line.strip() and not line.strip().startswith('<!--')]

        # Initialize containers
        subtitle = None
        components = []
        auxiliary_lines = []

        # ===== STAGE 1: EXTRACT SUBTITLE =====
        # First bold text with citation patterns or descriptive phrases
        if content_lines:
            first_line = content_lines[0]
            if first_line.startswith('**') and first_line.endswith(':**'):
                # Check if this looks like a subtitle using semantic indicators
                clean_text = first_line.replace('**', '').replace(':', '').strip().lower()
                is_subtitle = any(indicator in clean_text for indicator in self.SUBTITLE_INDICATORS)

                if is_subtitle:
                    subtitle = first_line.replace('**', '').replace(':', '').strip()
                    content_lines = content_lines[1:]  # Remove from further processing

        # ===== STAGE 2: EXTRACT COMPONENTS =====
        idx = 0
        while idx < len(content_lines):
            line = content_lines[idx]

            # Pattern A: Flow Diagram (contains arrows)
            is_flow, flow_elements = self.detect_and_parse_flow_diagram(line)
            if is_flow and line.startswith('**'):
                # Each flow element becomes a component
                for element in flow_elements:
                    components.append({
                        'heading': element,
                        'question': '',
                        'bullets': [],
                        'description': ''
                    })
                idx += 1
                continue

            # Pattern B: Numbered component **N. Label** or **N. Label (Qualifier):**
            if re.match(r'\*\*\d+\.', line):
                # Multi-line component - use parser
                component, next_idx = self.parse_multiline_component(content_lines, idx)
                components.append(component)
                idx = next_idx
                continue

            # Pattern C: Simple component label **Label:**
            if line.startswith('**') and line.endswith(':**'):
                # Check if this is a component or auxiliary heading
                clean_text = line.replace('**', '').replace(':', '').strip().lower()

                # Auxiliary indicators
                is_auxiliary = any(indicator in clean_text for indicator in self.AUXILIARY_INDICATORS)

                # Component indicators
                has_component_keyword = any(keyword in clean_text for keyword in self.COMPONENT_KEYWORDS)

                if is_auxiliary:
                    # This is auxiliary content, not a component
                    # Collect this line and subsequent non-component lines
                    auxiliary_lines.append(line)
                    idx += 1
                    # Collect following lines until next component/subtitle
                    while idx < len(content_lines):
                        next_line = content_lines[idx]
                        if next_line.startswith('**') and next_line.endswith(':**'):
                            break  # Next component/section
                        if re.match(r'\*\*\d+\.', next_line):
                            break  # Numbered component
                        auxiliary_lines.append(next_line)
                        idx += 1
                    continue
                elif has_component_keyword:
                    # This is a component
                    component, next_idx = self.parse_multiline_component(content_lines, idx)
                    components.append(component)
                    idx = next_idx
                    continue
                else:
                    # Ambiguous - default to component if we don't have many yet
                    if len(components) < 3:
                        component, next_idx = self.parse_multiline_component(content_lines, idx)
                        components.append(component)
                        idx = next_idx
                    else:
                        # Likely auxiliary
                        auxiliary_lines.append(line)
                        idx += 1
                    continue

            # Pattern D: Bold statement without colon (commentary)
            if line.startswith('**') and ':' not in line and line.endswith('**'):
                auxiliary_lines.append(line)
                idx += 1
                continue

            # Pattern E: With: label pattern (Slide 7 example)
            if line.startswith('**With:**') or line.startswith('**With:'):
                auxiliary_lines.append(line)
                idx += 1
                continue

            # Default: If we have components already, this is probably auxiliary
            if components:
                auxiliary_lines.append(line)

            idx += 1

        # ===== STAGE 3: AUXILIARY CONTENT (already collected above) =====
        # Additional pass: filter out references from auxiliary
        final_auxiliary = []
        for line in auxiliary_lines:
            # Skip italic citations (Stage 4 handles these)
            if line.startswith('*') and line.endswith('*') and '(' in line and ')' in line:
                continue  # This is a reference
            final_auxiliary.append(line)

        # ===== STAGE 4: REFERENCES (use existing citations from slide) =====
        citations_html = ''
        if slide['citations']:
            citations_html = '<div class="slide-footer">'
            for citation in slide['citations']:
                citations_html += f'<p class="citation">{citation}</p>'
            citations_html += '</div>'

        # ===== GENERATE HTML =====
        notes_html = self.generate_speaker_notes_html(slide['notes'])

        # Subtitle HTML
        subtitle_html = ''
        if subtitle:
            subtitle_html = f'<p class="framework-subtitle">{subtitle}</p>'

        # Components HTML (with enhanced structure for questions and bullets)
        components_html = ''
        for comp in components:
            heading_html = f'<h3>{comp["heading"]}</h3>'

            question_html = ''
            if comp['question']:
                question_html = f'<p class="component-question">"{comp["question"]}"</p>'

            bullets_html = ''
            if comp['bullets']:
                bullets_html = '<ul class="component-bullets">'
                for bullet in comp['bullets']:
                    bullets_html += f'<li>{bullet}</li>'
                bullets_html += '</ul>'

            description_html = ''
            if comp['description']:
                description_html = f'<p>{comp["description"]}</p>'

            components_html += f'''
        <div class="component">
          {heading_html}
          {question_html}
          {bullets_html}
          {description_html}
        </div>'''

        # Auxiliary content HTML
        auxiliary_html = ''
        if final_auxiliary:
            auxiliary_text = '\n'.join(final_auxiliary)
            auxiliary_html = f'<div class="framework-auxiliary">{self.convert_markdown_to_html(auxiliary_text)}</div>'

        # Fallback if no components found
        if not components:
            content_html = self.convert_markdown_to_html(slide['content'])
            return f'''
    <div class="slide framework-slide" data-slide="{slide['number']}">
      <h2 class="slide-title">{slide['title']}</h2>
      <div class="slide-content">
        {content_html}
      </div>
      {citations_html}
      {notes_html}
    </div>'''

        return f'''
    <div class="slide framework-slide" data-slide="{slide['number']}">
      <h2 class="framework-title">{slide['title']}</h2>
      {subtitle_html}
      <div class="framework-components">{components_html}
      </div>
      {auxiliary_html}
      {citations_html}
      {notes_html}
    </div>'''

    def generate_references_slide(self, slide: Dict) -> str:
        """Generate references slide(s) with automatic pagination (max 7 per page)."""
        # Parse references from content
        content = slide['content']

        # Check if content contains lists (numbered or bulleted)
        # If so, treat as content slide instead of references
        has_lists = (bool(re.search(r'^\d+\.\s+', content, re.MULTILINE)) or
                    bool(re.search(r'^[-•]\s+', content, re.MULTILINE)) or
                    bool(re.search(r'^\s+[-•]\s+', content, re.MULTILINE)))

        if has_lists:
            # Content has lists, use content slide renderer
            return self.generate_content_slide(slide, 'content')

        # References are typically in paragraph format, one per line
        # Pattern: Author(s). (Year). Title. Source.
        lines = content.strip().split('\n')
        references = []

        for line in lines:
            line = line.strip()
            # Skip empty lines and layout hints
            if not line or line.startswith('[') or line.startswith('**[') or line.startswith('<!--'):
                continue
            references.append(line)

        if not references:
            # No references found, fall back to content slide
            return self.generate_content_slide(slide, 'content')

        # Split references into chunks of 7
        MAX_REFS_PER_PAGE = 7
        ref_chunks = [references[i:i + MAX_REFS_PER_PAGE]
                      for i in range(0, len(references), MAX_REFS_PER_PAGE)]

        # Generate HTML for each page
        slides_html = []
        notes_html = self.generate_speaker_notes_html(slide['notes'])
        base_slide_num = int(slide['number'])

        for page_idx, ref_chunk in enumerate(ref_chunks):
            # Determine title
            if len(ref_chunks) == 1:
                title = slide['title']
                speaker_notes = notes_html
            else:
                if page_idx == 0:
                    title = slide['title']
                    # Update speaker notes for Part 1
                    notes_text = f"Complete reference list for all sources cited (Part 1 of {len(ref_chunks)}). " + slide['notes'].split('.', 1)[-1] if '.' in slide['notes'] else slide['notes']
                    speaker_notes = self.generate_speaker_notes_html(notes_text)
                else:
                    title = f"{slide['title']} (continued)"
                    # Speaker notes for continuation pages
                    notes_text = f"Complete reference list for all sources cited (Part {page_idx + 1} of {len(ref_chunks)}). Continued from previous slide."
                    speaker_notes = self.generate_speaker_notes_html(notes_text)

            # Convert references to HTML
            # Note: convert_markdown_to_html may already wrap in <p> tags
            refs_html_list = []
            for ref in ref_chunk:
                ref_html = self.convert_markdown_to_html(ref)
                # If already wrapped in <p>, use as-is; otherwise wrap it
                if ref_html.strip().startswith('<p>'):
                    refs_html_list.append(ref_html)
                else:
                    refs_html_list.append(f'<p>{ref_html}</p>')
            refs_html = '\n'.join(refs_html_list)

            # Calculate slide number
            slide_num = base_slide_num + page_idx

            slide_html = f'''
    <div class="slide references-slide" data-slide="{slide_num}">
      <h2 class="slide-title">{title}</h2>
      <div class="slide-content">
        {refs_html}
      </div>

      {speaker_notes}
    </div>'''

            slides_html.append(slide_html)

        # Return all slides concatenated
        return '\n'.join(slides_html)

    def generate_quote_slide(self, slide: Dict) -> str:
        """Generate quote slide with large text and attribution."""
        notes_html = self.generate_speaker_notes_html(slide['notes'])

        # Parse quote and attribution
        # Expected format: "Quote text" — Attribution (Source, Year)
        content = slide['content'].strip()

        # Try to split into quote and attribution
        if '—' in content:
            parts = content.split('—', 1)
            quote_text = parts[0].strip().strip('"').strip('"').strip('"')  # Remove quotes
            attribution = parts[1].strip()
        elif '\n\n' in content:
            # Alternative: quote and attribution separated by blank line
            parts = content.split('\n\n', 1)
            quote_text = parts[0].strip().strip('"').strip('"').strip('"')
            attribution = parts[1].strip()
        else:
            # No clear attribution, use whole content as quote
            quote_text = content.strip().strip('"').strip('"').strip('"')
            attribution = ''

        attribution_html = f'<p class="quote-attribution">{attribution}</p>' if attribution else ''

        # Include slide title
        title = slide['title']
        subtitle = f'<p class="slide-subtitle">{slide["subtitle"]}</p>' if slide.get('subtitle') else ''

        return f'''
    <div class="slide quote-slide" data-slide="{slide['number']}">
      <h2 class="slide-title">{title}</h2>
      {subtitle}
      <div class="quote-content">
        <blockquote class="large-quote">"{quote_text}"</blockquote>
        {attribution_html}
      </div>
      {notes_html}
    </div>'''

    def generate_dark_slide(self, slide: Dict) -> str:
        """Generate dark background slide for case studies, examples, warnings."""
        notes_html = self.generate_speaker_notes_html(slide['notes'])
        content_html = self.convert_markdown_to_html(slide['content'])

        # Add citations if present
        citations_html = ''
        if slide['citations']:
            citations_html = '<div class="slide-footer">'
            for citation in slide['citations']:
                citations_html += f'<p class="citation">{citation}</p>'
            citations_html += '</div>'

        return f'''
    <div class="slide content-slide dark-bg" data-slide="{slide['number']}">
      <h2 class="slide-title">{slide['title']}</h2>
      <div class="slide-content">
        {content_html}
      </div>
      {citations_html}
      {notes_html}
    </div>'''

    def generate_comparison_table_slide(self, slide: Dict) -> str:
        """Generate comparison table slide (2-column comparison)."""
        notes_html = self.generate_speaker_notes_html(slide['notes'])

        # Extract table from markdown
        table_match = re.search(r'\|.*?\|.*?\n\|[-:| ]+\n((?:\|.*?\|.*?\n)+)', slide['content'], re.DOTALL)

        if table_match:
            table_html = '<table>'  # No class needed - CSS uses .comparison-table-slide table selector
            rows = table_match.group(0).strip().split('\n')

            # Header row
            headers = [cell.strip() for cell in rows[0].split('|')[1:-1]]
            table_html += '<thead><tr>'
            for header in headers:
                # Remove markdown bold from headers
                header_clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', header)
                table_html += f'<th>{header_clean}</th>'
            table_html += '</tr></thead>'

            # Data rows (skip separator row)
            table_html += '<tbody>'
            for row in rows[2:]:
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                table_html += '<tr>'
                for cell in cells:
                    # Convert markdown in cells
                    cell_html = self.convert_markdown_to_html(cell)
                    # Remove wrapper <p> tags
                    cell_html = re.sub(r'^<p>(.*)</p>$', r'\1', cell_html.strip())
                    table_html += f'<td>{cell_html}</td>'
                table_html += '</tr>'
            table_html += '</tbody></table>'
        else:
            # No table found, use content
            table_html = self.convert_markdown_to_html(slide['content'])

        return f'''
    <div class="slide comparison-table-slide" data-slide="{slide['number']}">
      <h2 class="slide-title">{slide['title']}</h2>
      {table_html}
      {notes_html}
    </div>'''

    def generate_reflection_slide(self, slide: Dict) -> str:
        """Generate reflection/thinking prompt slide."""
        notes_html = self.generate_speaker_notes_html(slide['notes'])
        content_html = self.convert_markdown_to_html(slide['content'])

        return f'''
    <div class="slide reflection-slide" data-slide="{slide['number']}">
      <h2 class="slide-title">{slide['title']}</h2>
      <div class="reflection-content">
        {content_html}
      </div>
      {notes_html}
    </div>'''

    def generate_content_slide(self, slide: Dict, layout: str) -> str:
        """Generate standard content slide."""
        # Determine background class
        # Check layout parameter, slide['is_dark'] flag, or auto-dark for stats
        is_dark = (layout == 'dark-content' or
                  layout == 'dark-bg' or
                  slide.get('is_dark', False) or
                  layout == 'stats-banner')  # Stats slides are always dark
        bg_class = 'dark-bg ' if is_dark else ''

        # Determine layout-specific class
        if layout in ['content', 'dark-content']:
            layout_class = 'content-slide'
        else:
            # Use layout-specific class for special layouts (quote, framework, reflection, etc.)
            layout_class = f'{layout}-slide'

        # Convert content to HTML
        content_html = self.convert_markdown_to_html(slide['content'])

        # Add citations if present
        citations_html = ''
        if slide['citations']:
            citations_html = '<div class="slide-footer">'
            for citation in slide['citations']:
                citations_html += f'<p class="citation">{citation}</p>'
            citations_html += '</div>'

        notes_html = self.generate_speaker_notes_html(slide['notes'])
        return f'''
    <div class="slide {bg_class}{layout_class}" data-slide="{slide['number']}">
      <h2 class="slide-title">{slide['title']}</h2>
      <div class="slide-content">
        {content_html}
      </div>
      {citations_html}
      {notes_html}
    </div>'''

    def generate_html_document(self, slides_html: str, total_slides: int) -> str:
        """Generate complete HTML document with navigation and styling."""

        # Read the CSS and JavaScript from reference template
        css = '''
    /* CSS VARIABLES */
    :root {
      --color-primary: #131313;
      --color-accent: #ed5e29;
      --color-cream: #f4f3f1;
      --color-tan: #cac3b7;
      --color-white: #ffffff;
      --color-muted: #64748b;
      --color-light-gray: #f4f3f1;
      --color-border: #cac3b7;

      --font-header: 'Cal Sans', 'Arial Black', sans-serif;
      --font-body: 'Plus Jakarta Sans', sans-serif;

      --slide-padding: 60px;
      --slide-width: 1024px;
      --slide-height: 768px;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    html, body {
      width: 100%;
      height: 100%;
      font-family: var(--font-body);
      color: var(--color-primary);
      overflow: hidden;
      background: #e5e5e5;
    }

    .presentation-container {
      width: 100vw;
      height: 100vh;
      background: #e5e5e5;
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
      padding: 40px;
    }

    /* ========================================
       SLIDE BACKGROUND POLICY
       ======================================== */
    /* RULE: All slides have beige background by default.
       ONLY these slide types override the background:
       1. .title-slide (beige with decorative shapes)
       2. .section-break-slide (orange)
       3. .dark-bg (dark gray)

       All other slide types (.content-slide, .framework-slide, .quote-slide,
       .reflection-slide, .comparison-table-slide, .vocab-table-slide, etc.)
       MUST use the default beige background. */

    .slide {
      width: var(--slide-width);
      height: var(--slide-height);
      background: var(--color-cream);  /* Default beige for ALL slides */
      box-shadow: 0 10px 24px rgba(0, 0, 0, 0.15);
      border-radius: 8px;
      position: absolute;
      opacity: 0;
      transition: opacity 0.3s ease-in-out;
      display: none;
      overflow: hidden;
      padding: var(--slide-padding);
    }

    .slide.active { opacity: 1; display: block; }
    .slide.dark-bg { background: var(--color-primary); }  /* Override for dark slides */

    h1, h2, h3, h4 {
      font-family: var(--font-header);
      font-weight: 700;
      line-height: 1.2;
      letter-spacing: -0.05em;
    }

    .slide-title {
      font-size: 48px;
      color: var(--color-primary);
      margin-bottom: 30px;
    }

    .dark-bg .slide-title { color: var(--color-cream); }

    p, li {
      font-family: var(--font-body);
      font-size: 18px;
      line-height: 1.6;
      color: var(--color-primary);
    }

    /* Dark background text colors */
    .dark-bg p,
    .dark-bg li {
      color: var(--color-cream);
    }

    strong { font-weight: 600; color: var(--color-accent); }

    ul {
      list-style-type: disc;  /* Use native disc bullets */
      padding-left: 28px;
      margin: 0;
    }

    li {
      padding: 0;  /* No padding needed with native bullets */
    }

    /* Style native bullet markers orange */
    ul li::marker {
      color: var(--color-accent);
      font-size: 1.2em;
    }

    /* Ordered lists (numbered) */
    ol {
      padding-left: 28px;
      margin: 0;
    }

    ol li {
      padding: 0;  /* No padding for ordered lists */
    }

    /* Style native number markers orange */
    ol li::marker {
      color: var(--color-accent);
      font-weight: 600;
    }

    /* Nested unordered lists under ordered lists */
    ol ul.nested-list {
      margin: 0;
      padding-left: 20px;
      list-style-type: disc;  /* Use native disc bullets */
    }

    ol ul.nested-list li {
      padding: 0;  /* No padding needed with native bullets */
      font-size: 0.95em;  /* Slightly smaller text */
    }

    ol ul.nested-list li::marker {
      color: var(--color-accent);
      font-size: 1em;
    }

    /* Title Slide */
    .title-slide {
      display: flex;
      justify-content: flex-start;
      align-items: center;
    }

    .title-content h1 {
      font-size: 60px;
      margin-bottom: 20px;
    }

    .subtitle {
      font-size: 24px;
      color: var(--color-accent);
      margin-top: 20px;
      font-weight: 600;
    }

    .author {
      font-size: 18px;
      color: var(--color-muted);
      margin-top: 40px;
    }

    .decorative-shapes {
      position: absolute;
      bottom: 40px;
      left: 40px;
      display: flex;
      gap: 12px;
    }

    .shape {
      border-radius: 50%;
    }

    .shape.orange {
      width: 20px;
      height: 20px;
      background: var(--color-accent);
    }

    .shape.tan {
      width: 16px;
      height: 16px;
      background: var(--color-tan);
    }

    .shape.small {
      width: 12px;
      height: 12px;
      background: var(--color-accent);
      opacity: 0.5;
    }

    /* Section Break - Orange background (override) */
    .section-break-slide {
      background: var(--color-accent);  /* Override: orange for section breaks */
      display: flex;
      justify-content: flex-start;
      align-items: center;
    }

    .section-title {
      font-size: 54px;
      color: #ffffff;
    }

    .section-subtitle {
      font-size: 24px;
      color: #ffffff;
      font-weight: 700;
      margin-top: 20px;
    }

    /* Big Number */
    .big-number-slide {
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .number-content {
      text-align: center;
    }

    .big-number {
      font-family: var(--font-header);
      font-size: 180px;
      font-weight: 700;
      color: var(--color-accent);
      line-height: 1;
      margin-bottom: 30px;
    }

    .number-explanation {
      font-size: 28px;
      max-width: 700px;
      margin: 30px auto 0;
    }

    /* Tables */
    .vocab-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }

    .vocab-table-slide table th,
    .vocab-table-slide table td,
    .vocab-table th,
    .vocab-table td {
      padding: 8px 12px;
      text-align: left;
      border-bottom: 1px solid #e0e0e0;
    }

    .vocab-table-slide table th,
    .vocab-table th {
      background: var(--color-accent);
      color: white;
      font-weight: 700;
    }

    .vocab-table-slide table th strong,
    .vocab-table th strong {
      color: white !important;  /* Override global strong color for table headers */
    }

    .vocab-table-slide table td,
    .vocab-table td {
      font-size: 16px;
    }

    /* Stats */
    .stats-banner {
      display: flex;
      justify-content: space-between;
      gap: 24px;
      margin-top: 40px;
    }

    .stat-item {
      flex: 1;
      text-align: center;
    }

    .stat-number {
      font-family: var(--font-header);
      font-size: 56px;
      font-weight: 700;
      color: var(--color-accent);
      line-height: 1;
      margin-bottom: 12px;
    }

    .stat-label {
      font-size: 16px;
      font-weight: 700;
      color: var(--color-cream);
      margin-bottom: 8px;
    }

    .stat-description {
      font-size: 14px;
      color: var(--color-cream);
      opacity: 0.8;
    }

    /* Navigation */
    .nav-controls {
      position: fixed;
      bottom: 30px;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      align-items: center;
      gap: 20px;
      background: rgba(19, 19, 19, 0.9);
      padding: 12px 24px;
      border-radius: 30px;
      z-index: 1000;
    }

    .nav-controls button {
      background: transparent;
      border: none;
      color: #ffffff;
      font-size: 24px;
      font-weight: 700;
      cursor: pointer;
      padding: 8px 16px;
      border-radius: 8px;
    }

    .nav-controls button:hover {
      background: rgba(237, 94, 41, 0.3);
    }

    #slide-counter {
      color: #ffffff;
      font-family: var(--font-body);
      font-size: 16px;
      font-weight: 500;
      min-width: 80px;
      text-align: center;
    }

    .progress-bar {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 4px;
      background: rgba(19, 19, 19, 0.1);
      z-index: 1000;
    }

    .progress-fill {
      height: 100%;
      background: var(--color-accent);
      width: 0%;
      transition: width 0.3s ease;
    }

    .slide-footer {
      position: absolute;
      bottom: 20px;
      left: 60px;
      right: 60px;
    }

    .citation {
      font-size: 14px;
      color: var(--color-muted);
      font-style: italic;
      line-height: 1.4;
    }

    /* Speaker Notes */
    .speaker-notes {
      display: none;  /* Hidden by default in browser view */
      position: absolute;
      bottom: 80px;
      left: 60px;
      right: 60px;
      padding: 20px;
      background: rgba(244, 243, 241, 0.95);
      border-left: 4px solid var(--color-accent);
      border-radius: 8px;
      font-size: 14px;
      line-height: 1.5;
      max-height: 200px;
      overflow-y: auto;
      z-index: 100;
      box-shadow: 0 -4px 12px rgba(0, 0, 0, 0.1);
    }

    .speaker-notes h4 {
      font-family: var(--font-body);
      font-size: 12px;
      font-weight: 700;
      color: var(--color-accent);
      letter-spacing: 0.1em;
      margin-bottom: 12px;
    }

    .speaker-notes .notes-content {
      color: var(--color-primary);
    }

    .speaker-notes .notes-content p {
      font-size: 13px;
      margin-bottom: 8px;
    }

    .speaker-notes .notes-content ul {
      margin-left: 20px;
    }

    .speaker-notes .notes-content li {
      font-size: 13px;
      padding: 4px 0;
    }

    /* Show speaker notes on dark slides with white background */
    .dark-bg .speaker-notes {
      background: rgba(255, 255, 255, 0.95);
    }

    /* Print styles - show speaker notes when printing */
    @media print {
      .speaker-notes {
        display: block !important;
        page-break-inside: avoid;
        margin-top: 40px;
        position: static;
        background: #f8fafc;
        border: 1px solid #cbd5e1;
        max-height: none;
      }

      .nav-controls,
      .progress-bar {
        display: none;
      }

      .slide {
        page-break-after: always;
        box-shadow: none;
        position: relative !important;
        opacity: 1 !important;
        display: block !important;
      }
    }

    /* Quote Slide - DISABLED (conflicts with .slide-content structure)
    .quote-slide {
      display: flex;
      justify-content: center;
      align-items: center;
      position: relative;
    }

    .quote-slide .quote-mark {
      font-family: var(--font-header);
      font-size: 120px;
      color: #e2e8f0;
      position: absolute;
      top: 60px;
      left: 60px;
      line-height: 1;
      opacity: 0.5;
    }

    .quote-slide .quote-content {
      max-width: 800px;
      padding: 0 80px;
      text-align: left;
    }

    .quote-slide .quote-text {
      font-family: var(--font-body);
      font-size: 36px;
      line-height: 1.4;
      color: var(--color-primary);
      margin-bottom: 30px;
    }

    .quote-slide .quote-attribution {
      font-family: var(--font-body);
      font-size: 18px;
      color: var(--color-muted);
      text-align: right;
    }
    */

    /* References Slide */
    .references-slide .references {
      padding-top: 20px;
    }

    .references-slide .references li {
      padding-left: 40px;
      text-indent: -40px;
      margin-bottom: 16px;
      font-size: 14px;
      line-height: 1.3;
    }

    .references-slide .references li::before {
      content: none;
    }

    /* Framework Slide */
    .framework-slide {
      flex-direction: column;
    }

    .framework-title {
      font-size: 48px;
      color: var(--color-primary);
      text-align: center;
      margin-bottom: 40px;
    }

    .framework-subtitle {
      font-family: var(--font-header);
      font-size: 32px;
      font-weight: 700;
      color: var(--color-text);
      text-align: center;
      margin-bottom: 40px;
      line-height: 1.3;
    }

    .framework-components {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 20px;
    }

    .component {
      background: var(--color-white);
      border: 1px solid var(--color-border);
      border-radius: 8px;
      padding: 20px;
      text-align: center;
    }

    .component h3 {
      font-family: var(--font-header);
      font-size: 27px;
      color: var(--color-primary);
      margin-bottom: 12px;
    }

    .component p {
      font-size: 17px;
      color: var(--color-muted);
    }

    /* Framework commentary (content below component grid) */
    .framework-commentary {
      margin-top: 30px;
      text-align: center;
      max-width: 80%;
      margin-left: auto;
      margin-right: auto;
    }

    .framework-commentary p {
      font-size: 24px;
      line-height: 1.6;
      margin: 0.5em 0;
    }

    .framework-commentary strong {
      color: var(--color-accent);
      font-weight: 600;
    }

    .framework-commentary em {
      font-style: italic;
      color: var(--color-muted);
      font-size: 21px;
    }

    /* Framework slide fallback (for non-component content like ASCII art) */
    .framework-slide .slide-content {
      font-family: monospace;
      font-size: 14px;
      line-height: 1.8;
      white-space: pre;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 2em;
    }

    .framework-slide .slide-content p {
      font-family: var(--font-body);
      font-size: 16px;
      line-height: 1.6;
      white-space: normal;
      max-width: 90%;
      margin: 0.5em 0;
    }

    /* Reflection/Thinking Prompt Slide */
    .reflection-slide,
    .thinking-prompt {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: flex-start;
      text-align: left;
    }

    .reflection-slide .reflection-icon,
    .thinking-prompt .reflection-icon {
      font-size: 72px;
      margin-bottom: 30px;
    }

    .reflection-slide .reflection-question,
    .thinking-prompt .reflection-question {
      font-family: var(--font-body);
      font-size: 32px;
      line-height: 1.4;
      color: var(--color-primary);
      max-width: 800px;
      margin-bottom: 40px;
    }

    .reflection-slide .reflection-instruction,
    .thinking-prompt .reflection-instruction {
      font-size: 16px;
      font-style: italic;
      color: var(--color-muted);
    }

    /* Comparison Table Slide (2-Column boxes - NOT for HTML tables) */
    .comparison-table-slide .comparison-boxes {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 30px;
      margin-top: 40px;
    }

    /* Ensure HTML tables inside comparison-table-slide are NOT affected by grid */
    .comparison-table-slide table {
      display: table !important;
    }

    .comparison-table-slide .comparison-column {
      background: #ffffff;
      border-radius: 8px;
      overflow: hidden;
    }

    .comparison-table-slide .column-header {
      background: var(--color-accent);
      color: #ffffff;
      font-family: var(--font-header);
      font-size: 20px;
      font-weight: 700;
      padding: 16px;
      text-align: center;
    }

    .comparison-table-slide .column-content {
      padding: 20px;
    }

    .comparison-table-slide .column-content ul {
      list-style: none;
      padding: 0;
    }

    .comparison-table-slide .column-content li {
      padding: 8px 0;
      font-size: 14px;
      border-bottom: 1px solid #e2e8f0;
    }

    .comparison-table-slide .column-content li:last-child {
      border-bottom: none;
    }

    /* QUOTE SLIDE STYLING */
    .quote-slide .slide-content {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
      padding: 3em 4em;
      min-height: 400px;
    }

    .quote-slide .slide-content p {
      font-size: 1.8em;
      line-height: 1.2;
      font-style: italic;
      color: var(--color-text-primary);
      margin: 0;
    }

    .quote-slide .slide-content p:first-of-type {
      font-size: 2em;
      margin-bottom: 0.8em;
      font-weight: 500;
    }

    .quote-slide .slide-content p:last-of-type {
      font-size: 1.2em;
      font-style: normal;
      color: var(--color-text-secondary);
      margin-top: 1.5em;
    }


    /* REFLECTION SLIDE STYLING */
    /* BACKGROUND RULE: Only title-slide, section-break-slide, and .dark-bg have non-beige backgrounds.
       All other slides inherit the default beige background from .slide {} */
    .reflection-slide {
      /* No background override - uses default beige from .slide */
    }

    .reflection-slide .slide-content {
      font-size: 1.15em;
      line-height: 1.9;
      padding: 2em 3em;
      text-align: left;
      width: 100%;
    }

    .reflection-slide .slide-content p {
      margin: 1.2em 0;
      color: var(--color-text-primary);
    }

    .reflection-slide .slide-content p strong {
      color: var(--color-accent);
      font-size: 1.1em;
      display: block;
      margin-bottom: 0.5em;
    }

    .reflection-slide .slide-content ul {
      margin-left: 2em;
    }

    .reflection-slide .slide-content li {
      margin: 0.8em 0;
      padding-left: 0.5em;
    }

    /* MULTI-HEADING FORMATTING - Inline bold orange emphasis */
    .slide-content p > strong:only-child {
      font-weight: 700;
      color: var(--color-accent);
    }

    /* COMPARISON TABLE WITH MARKDOWN TABLE */
    .comparison-table-slide table {
      width: 100%;
      border-collapse: collapse;
      margin: 1em auto 0.5em;
      max-width: 95%;
    }

    .comparison-table-slide th {
      background: var(--color-accent);
      color: white;
      font-weight: 700;
      font-size: 1.2em;
      padding: 8px 12px;
      text-align: left;
      border-right: 2px solid white;
    }

    .comparison-table-slide th:last-child {
      border-right: none;
    }

    .comparison-table-slide td {
      padding: 8px 12px;
      border: 1px solid #e2e8f0;
      border-top: none;
      vertical-align: top;
      font-size: 1em;
      line-height: 1.5;
      background: white;
    }

    .comparison-table-slide td:first-child {
      border-right: 2px solid #e2e8f0;
    }

    .comparison-table-slide tbody tr:last-child td {
      border-bottom: 2px solid var(--color-accent);
    }

    /* THINKING PROMPT / REFLECTION PROMPT */
    .thinking-prompt .slide-content {
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding: 3em;
      background: linear-gradient(135deg, rgba(237, 94, 41, 0.05) 0%, rgba(237, 94, 41, 0.02) 100%);
      border-radius: 12px;
      margin: 2em;
    }

    .thinking-prompt .slide-content p {
      font-size: 1.3em;
      line-height: 1.8;
      margin: 1em 0;
      color: var(--color-text-primary);
    }
'''

        js = '''
    (function() {
      let currentSlide = 1;
      const slides = document.querySelectorAll('.slide');
      const totalSlides = slides.length;
      const prevBtn = document.getElementById('prev-btn');
      const nextBtn = document.getElementById('next-btn');
      const counter = document.getElementById('slide-counter');
      const progressFill = document.getElementById('progress-fill');

      function showSlide(n) {
        if (n < 1) n = 1;
        if (n > totalSlides) n = totalSlides;

        slides.forEach(slide => slide.classList.remove('active'));
        slides[n - 1].classList.add('active');

        currentSlide = n;
        counter.textContent = `${n} / ${totalSlides}`;
        progressFill.style.width = `${(n / totalSlides) * 100}%`;
      }

      function nextSlide() { showSlide(currentSlide + 1); }
      function prevSlide() { showSlide(currentSlide - 1); }

      prevBtn.addEventListener('click', prevSlide);
      nextBtn.addEventListener('click', nextSlide);

      document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === ' ') {
          e.preventDefault();
          nextSlide();
        }
        if (e.key === 'ArrowLeft') {
          e.preventDefault();
          prevSlide();
        }
        if (e.key === 'Home') {
          e.preventDefault();
          showSlide(1);
        }
        if (e.key === 'End') {
          e.preventDefault();
          showSlide(totalSlides);
        }
      });

      showSlide(1);
    })();
'''

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Week 12: Integrating Growth - BBAE-PPD</title>

  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

  <style>
    @font-face {{
      font-family: 'Cal Sans';
      src: local('Arial Black'), local('Impact');
      font-weight: 700;
    }}

{css}
  </style>
</head>
<body>
  <div class="presentation-container">

    <!-- Navigation Controls -->
    <div class="nav-controls">
      <button id="prev-btn">‹</button>
      <span id="slide-counter">1 / {total_slides}</span>
      <button id="next-btn">›</button>
    </div>

    <!-- Progress Bar -->
    <div class="progress-bar">
      <div class="progress-fill" id="progress-fill"></div>
    </div>

{slides_html}

  </div>

  <script>
{js}
  </script>
</body>
</html>'''

    def convert(self):
        """Main conversion process."""
        print(f"Reading lecture content from: {self.lecture_md_path}")
        content = self.read_markdown()

        print("Parsing slides...")
        self.slides = self.parse_slides(content)
        print(f"Found {len(self.slides)} slides")

        print("Generating HTML for each slide...")
        slides_html_parts = []
        for i, slide in enumerate(self.slides, 1):
            layout = self.detect_layout(slide)
            slide_html = self.generate_slide_html(slide, layout)
            slides_html_parts.append(slide_html)

            # Count actual slides generated (may be >1 for paginated references)
            actual_count = slide_html.count('data-slide=')
            if actual_count > 1:
                print(f"  Slide {i}: {slide['title'][:50]}... [{layout}] (paginated into {actual_count} slides)")
            else:
                print(f"  Slide {i}: {slide['title'][:50]}... [{layout}]")

        slides_html = '\n'.join(slides_html_parts)

        # Count total actual slides in the generated HTML
        total_slides = slides_html.count('data-slide=')

        print("Generating complete HTML document...")
        html_doc = self.generate_html_document(slides_html, total_slides)

        print(f"Writing output to: {self.output_html_path}")
        with open(self.output_html_path, 'w', encoding='utf-8') as f:
            f.write(html_doc)

        print(f"\n✓ Conversion complete!")
        print(f"  Markdown slides: {len(self.slides)}")
        print(f"  HTML slides: {total_slides}")
        if total_slides > len(self.slides):
            print(f"  (References paginated: +{total_slides - len(self.slides)} slides)")
        print(f"  Output file: {self.output_html_path}")
        print(f"  File size: {len(html_doc):,} bytes")


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print("Usage: python convert_lecture_to_slides.py <input.md> <output.html>")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    converter = SlideConverter(input_path, output_path)
    converter.convert()
