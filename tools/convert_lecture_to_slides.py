#!/usr/bin/env python3
"""
Convert lecture content markdown to HTML presentation slides.
Follows the enhanced design system from reference examples.
"""

import re
from typing import List, Dict, Tuple

class SlideConverter:
    """Converts markdown lecture content to HTML slides."""

    def __init__(self, lecture_md_path: str, output_html_path: str):
        self.lecture_md_path = lecture_md_path
        self.output_html_path = output_html_path
        self.slides = []

    def read_markdown(self) -> str:
        """Read the markdown file."""
        with open(self.lecture_md_path, 'r', encoding='utf-8') as f:
            return f.read()

    def parse_slides(self, content: str) -> List[Dict]:
        """Parse markdown content into slide data structures."""
        slides = []

        # Split by slide separators (---)
        sections = content.split('\n---\n')

        for section in sections:
            if not section.strip():
                continue

            # Skip header sections and meta info
            if section.startswith('#') and 'SLIDE' not in section:
                continue

            # Extract slide number and title
            slide_match = re.search(r'\*\*SLIDE (\d+):\s*(.+?)\*\*', section)
            if not slide_match:
                continue

            slide_num = slide_match.group(1)
            slide_title = slide_match.group(2).strip()

            # Extract CONTENT section
            content_match = re.search(r'CONTENT:(.*?)(?:\[PURPOSE:|## Speaker Notes|$)', section, re.DOTALL)
            slide_content = content_match.group(1).strip() if content_match else ""

            # Extract speaker notes
            notes_match = re.search(r'## Speaker Notes(.*?)(?:\n---|\Z)', section, re.DOTALL)
            speaker_notes = notes_match.group(1).strip() if notes_match else ""

            # Extract citations
            citations = re.findall(r'\*[^*]+\*\s*\([^)]+\)\.\s*(?:https?://[^\s]+|DOI:[^\s]+)', slide_content)

            slides.append({
                'number': int(slide_num),
                'title': slide_title,
                'content': slide_content,
                'notes': speaker_notes,
                'citations': citations
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
        layout_hint_match = re.search(r'<!--\s*LAYOUT:\s*(\w+)\s*-->', content, re.IGNORECASE)
        if layout_hint_match:
            layout_hint = layout_hint_match.group(1).lower()
            valid_layouts = ['quote', 'references', 'framework', 'diagram', 'reflection',
                           'thinking-prompt', 'comparison-table', 'vocab-table']
            if layout_hint in valid_layouts:
                return layout_hint

        # Title slide (slide 1)
        if slide['number'] == 1:
            return 'title'

        # CONTENT-BASED DETECTION (By priority)

        # Section break detection
        if 'Section Break' in title or re.search(r'^(Part \d+|SEGMENT \d+)', title):
            return 'section-break'

        # Quote detection (HIGH PRIORITY)
        if re.search(r'^\s*["\'""]|^>\s+', content, re.MULTILINE) or 'Quote:' in content:
            return 'quote'

        # References detection (HIGH PRIORITY)
        if 'References' in title or 'Citations' in title or 'Sources' in title:
            return 'references'
        # Also detect by content pattern (multiple citations)
        citation_pattern = r'\([12]\d{3}\)'  # Year in parentheses like (2023)
        if content.count('(') >= 3 and len(re.findall(citation_pattern, content)) >= 2:
            return 'references'

        # Framework/Diagram detection (HIGH PRIORITY)
        if any(keyword in title for keyword in ['Framework', 'Model', 'Diagram', 'Process']):
            return 'framework'
        # Detect by content structure (multiple components/steps)
        if content.count('**') >= 6 and ('Component' in content or 'Step' in content or 'Element' in content):
            return 'framework'

        # Reflection prompt detection (MEDIUM-HIGH PRIORITY)
        if any(keyword in content for keyword in ['Reflect:', 'Think about:', 'Consider:', 'Reflection:']):
            return 'reflection'
        # Questions with reflective indicators
        if '?' in content and any(word in content.lower() for word in ['how might you', 'what would you', 'why do you']):
            return 'reflection'

        # Comparison table detection (HIGH PRIORITY)
        if 'vs' in title.lower() or 'versus' in title.lower() or 'comparison' in title.lower():
            if '|' in content and '---' in content:
                return 'comparison-table'

        # Big number detection
        if re.search(r'\*\*\d+%\*\*', content) and len(content) < 300:
            return 'big-number'

        # Table detection (vocabulary slides)
        if '|' in content and '---' in content:
            return 'table'

        # Stats/metrics detection (multiple statistics)
        if content.count('%') >= 3 or content.count('📌') >= 2:
            return 'stats'

        # Dark background detection
        if 'Vietnamese example' in content or 'Case study' in title:
            return 'dark-content'

        # Default: standard content with bullets
        return 'content'

    def convert_markdown_to_html(self, text: str) -> str:
        """Convert markdown formatting to HTML."""
        # Bold
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

        # Lists
        lines = text.split('\n')
        html_lines = []
        in_list = False

        for line in lines:
            # Bullet points
            if re.match(r'^[-•✓✗📌]\s+', line):
                if not in_list:
                    html_lines.append('<ul>')
                    in_list = True
                item = re.sub(r'^[-•✓✗📌]\s+', '', line)
                html_lines.append(f'<li>{item}</li>')
            else:
                if in_list:
                    html_lines.append('</ul>')
                    in_list = False
                if line.strip():
                    html_lines.append(f'<p>{line}</p>')

        if in_list:
            html_lines.append('</ul>')

        return '\n'.join(html_lines)

    def generate_slide_html(self, slide: Dict, layout: str) -> str:
        """Generate HTML for a single slide based on layout."""
        content_html = self.convert_markdown_to_html(slide['content'])

        if layout == 'title':
            return self.generate_title_slide(slide)
        elif layout == 'section-break':
            return self.generate_section_break(slide)
        elif layout == 'table':
            return self.generate_table_slide(slide)
        elif layout == 'stats':
            return self.generate_stats_slide(slide)
        elif layout == 'big-number':
            return self.generate_big_number_slide(slide)
        else:
            return self.generate_content_slide(slide, layout)

    def generate_title_slide(self, slide: Dict) -> str:
        """Generate title slide HTML."""
        return f'''
    <div class="slide title-slide" data-slide="{slide['number']}">
      <div class="title-content">
        <h1>{slide['title']}</h1>
        <p class="subtitle">Personal and Professional Development (BBAE-PPD)</p>
        <p class="author">Week 12 - Integrating Growth</p>
      </div>
      <div class="decorative-shapes">
        <div class="shape orange"></div>
        <div class="shape tan"></div>
        <div class="shape small"></div>
      </div>
      <!-- Speaker Notes: {slide['notes'][:200]}... -->
    </div>'''

    def generate_section_break(self, slide: Dict) -> str:
        """Generate section break slide HTML."""
        return f'''
    <div class="slide section-break-slide" data-slide="{slide['number']}">
      <h2 class="section-title">{slide['title']}</h2>
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
                table_html += f'<th>{header}</th>'
            table_html += '</tr></thead><tbody>'

            # Data rows (skip separator row)
            for row in rows[2:]:
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                table_html += '<tr>'
                for cell in cells:
                    # Convert markdown bold to HTML
                    cell = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', cell)
                    table_html += f'<td>{cell}</td>'
                table_html += '</tr>'

            table_html += '</tbody></table>'
        else:
            table_html = ''

        return f'''
    <div class="slide content-slide" data-slide="{slide['number']}">
      <h2 class="slide-title">{slide['title']}</h2>
      {table_html}
    </div>'''

    def generate_stats_slide(self, slide: Dict) -> str:
        """Generate stats slide with dark background."""
        # Extract statistics from content
        stats = re.findall(r'📌\s*\*\*([^*]+)\*\*.*?[-–]\s*\*\*([^:]+):\*\*([^📌\n]+)', slide['content'], re.DOTALL)

        stats_html = '<div class="stats-banner">'
        for label, title, description in stats[:4]:  # Max 4 stats
            stats_html += f'''
        <div class="stat-item">
          <div class="stat-number">{label}</div>
          <div class="stat-label">{title.strip()}</div>
          <div class="stat-description">{description.strip()[:100]}</div>
        </div>'''
        stats_html += '</div>'

        return f'''
    <div class="slide dark-bg content-slide" data-slide="{slide['number']}">
      <h2 class="slide-title">{slide['title']}</h2>
      {stats_html}
    </div>'''

    def generate_big_number_slide(self, slide: Dict) -> str:
        """Generate big number slide."""
        # Extract number
        number_match = re.search(r'\*\*(\d+%?)\*\*', slide['content'])
        number = number_match.group(1) if number_match else "?"

        # Extract explanation
        explanation = re.sub(r'\*\*\d+%?\*\*', '', slide['content']).strip()[:200]

        return f'''
    <div class="slide big-number-slide" data-slide="{slide['number']}">
      <div class="number-content">
        <div class="big-number">{number}</div>
        <p class="number-explanation">{explanation}</p>
      </div>
    </div>'''

    def generate_content_slide(self, slide: Dict, layout: str) -> str:
        """Generate standard content slide."""
        bg_class = 'dark-bg ' if layout == 'dark-content' else ''

        # Convert content to HTML
        content_html = self.convert_markdown_to_html(slide['content'])

        # Add citations if present
        citations_html = ''
        if slide['citations']:
            citations_html = '<div class="slide-footer">'
            for citation in slide['citations']:
                citations_html += f'<p class="citation">{citation}</p>'
            citations_html += '</div>'

        return f'''
    <div class="slide {bg_class}content-slide" data-slide="{slide['number']}">
      <h2 class="slide-title">{slide['title']}</h2>
      <div class="slide-content">
        {content_html}
      </div>
      {citations_html}
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

    .slide {
      width: var(--slide-width);
      height: var(--slide-height);
      background: var(--color-cream);
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
    .slide.dark-bg { background: var(--color-primary); }

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

    strong { font-weight: 600; color: var(--color-accent); }

    ul {
      list-style: none;
      padding: 0;
    }

    li {
      padding: 8px 0 8px 28px;
      position: relative;
    }

    li::before {
      content: "•";
      position: absolute;
      left: 0;
      color: var(--color-accent);
      font-size: 24px;
      font-weight: 700;
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

    /* Section Break */
    .section-break-slide {
      background: var(--color-accent);
      display: flex;
      justify-content: flex-start;
      align-items: center;
    }

    .section-title {
      font-size: 54px;
      color: #ffffff;
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

    .vocab-table th, .vocab-table td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid var(--color-tan);
    }

    .vocab-table th {
      background: var(--color-accent);
      color: white;
      font-weight: 600;
    }

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

    /* Quote Slide */
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

    /* Framework/Diagram Slide */
    .framework-slide .framework,
    .diagram-slide .diagram,
    .model-slide .model {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      gap: 20px;
      margin-top: 40px;
    }

    .framework-slide .framework-box,
    .diagram-slide .diagram-box,
    .model-slide .model-box {
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      padding: 20px;
      text-align: center;
    }

    .framework-slide .framework-box strong,
    .diagram-slide .diagram-box strong,
    .model-slide .model-box strong {
      display: block;
      font-family: var(--font-header);
      font-size: 18px;
      color: var(--color-primary);
      margin-bottom: 12px;
    }

    .framework-slide .framework-box p,
    .diagram-slide .diagram-box p,
    .model-slide .model-box p {
      font-size: 14px;
      color: var(--color-muted);
    }

    /* Reflection/Thinking Prompt Slide */
    .reflection-slide,
    .thinking-prompt {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      text-align: center;
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

    /* Comparison Table Slide (2-Column) */
    .comparison-table-slide .comparison-table {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 30px;
      margin-top: 40px;
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
            print(f"  Slide {i}: {slide['title'][:50]}... [{layout}]")

        slides_html = '\n'.join(slides_html_parts)

        print("Generating complete HTML document...")
        html_doc = self.generate_html_document(slides_html, len(self.slides))

        print(f"Writing output to: {self.output_html_path}")
        with open(self.output_html_path, 'w', encoding='utf-8') as f:
            f.write(html_doc)

        print(f"\n✓ Conversion complete!")
        print(f"  Total slides: {len(self.slides)}")
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
