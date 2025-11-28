"""
PDF exporter for assessment briefs.

Exports Assessment objects to professional PDF documents using WeasyPrint.
"""

from pathlib import Path
from typing import Optional
from ..models import Assessment


class PDFExporter:
    """
    Export assessments to PDF format.

    Uses WeasyPrint to convert HTML assessment briefs to PDF documents
    with professional styling and layout.

    Features:
    - Professional styling with headers/footers
    - Scenario options formatting
    - Rubric table rendering
    - Requirements checklist
    - Page breaks where appropriate

    Usage:
        exporter = PDFExporter()
        pdf_path = exporter.export_to_pdf(
            assessment,
            "output/persuasive-proposal.pdf",
            course_code="BCI2AU"
        )
    """

    def __init__(self):
        """Initialize PDF exporter."""
        pass

    def export_to_pdf(
        self,
        assessment: Assessment,
        output_path: str,
        course_code: Optional[str] = None,
        base_url: Optional[str] = None
    ) -> Path:
        """
        Export assessment to PDF file.

        Args:
            assessment: Assessment to export
            output_path: Path to output PDF file
            course_code: Optional course code for header
            base_url: Optional base URL for resolving relative paths

        Returns:
            Path to generated PDF file

        Raises:
            ImportError: If WeasyPrint is not installed
            ValueError: If HTML generation fails

        Example:
            path = exporter.export_to_pdf(
                assessment,
                "output/proposal.pdf",
                course_code="BCI2AU"
            )
        """
        try:
            from weasyprint import HTML, CSS
        except ImportError:
            raise ImportError(
                "WeasyPrint is required for PDF export. "
                "Install with: pip install weasyprint>=60.0"
            )

        # Generate HTML content
        html_content = assessment.to_html_brief(course_code)

        # Add enhanced CSS for PDF rendering
        css_content = self._get_pdf_css()

        # Prepare output path
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        # Convert to PDF
        html = HTML(string=html_content, base_url=base_url)
        css = CSS(string=css_content)

        html.write_pdf(
            output,
            stylesheets=[css]
        )

        return output

    def _get_pdf_css(self) -> str:
        """
        Get enhanced CSS for PDF rendering.

        Returns:
            CSS string optimized for PDF output
        """
        return """
            @page {
                size: A4;
                margin: 2.5cm 2cm;
                @top-center {
                    content: "Assessment Brief";
                    font-size: 10pt;
                    color: #666;
                }
                @bottom-right {
                    content: "Page " counter(page) " of " counter(pages);
                    font-size: 9pt;
                    color: #666;
                }
            }

            body {
                font-family: 'Georgia', 'Times New Roman', serif;
                font-size: 11pt;
                line-height: 1.6;
                color: #333;
            }

            h1 {
                font-size: 24pt;
                font-weight: bold;
                color: #1a1a1a;
                margin-top: 0;
                margin-bottom: 0.5em;
                page-break-after: avoid;
            }

            h2 {
                font-size: 18pt;
                font-weight: bold;
                color: #2c2c2c;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
                page-break-after: avoid;
                border-bottom: 2px solid #ddd;
                padding-bottom: 0.3em;
            }

            h3 {
                font-size: 14pt;
                font-weight: bold;
                color: #444;
                margin-top: 1.2em;
                margin-bottom: 0.4em;
                page-break-after: avoid;
            }

            p {
                margin: 0.5em 0;
                text-align: justify;
            }

            .metadata {
                background: #f5f5f5;
                padding: 1em;
                margin: 1em 0;
                border-radius: 4px;
                border-left: 4px solid #0066cc;
                page-break-inside: avoid;
            }

            .metadata p {
                margin: 0.3em 0;
                text-align: left;
            }

            ul, ol {
                margin: 0.5em 0;
                padding-left: 2em;
            }

            li {
                margin: 0.3em 0;
            }

            .scenario {
                background: #fafafa;
                padding: 1em;
                margin: 1em 0;
                border: 1px solid #ddd;
                border-radius: 4px;
                page-break-inside: avoid;
            }

            .scenario h4 {
                margin-top: 0;
                color: #0066cc;
            }

            .requirements {
                margin: 1em 0;
            }

            .requirements input[type="checkbox"] {
                margin-right: 0.5em;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin: 1em 0;
                page-break-inside: avoid;
            }

            table th {
                background: #0066cc;
                color: white;
                padding: 0.6em;
                text-align: left;
                font-weight: bold;
                font-size: 10pt;
            }

            table td {
                padding: 0.6em;
                border: 1px solid #ddd;
                font-size: 10pt;
                vertical-align: top;
            }

            table tr:nth-child(even) {
                background: #f9f9f9;
            }

            .rubric-table {
                font-size: 9pt;
            }

            .rubric-table th {
                font-size: 9pt;
            }

            .rubric-table td {
                font-size: 8.5pt;
                line-height: 1.4;
            }

            .page-break {
                page-break-before: always;
            }

            .no-break {
                page-break-inside: avoid;
            }

            strong {
                font-weight: bold;
                color: #1a1a1a;
            }

            em {
                font-style: italic;
            }

            code {
                font-family: 'Courier New', monospace;
                background: #f5f5f5;
                padding: 0.2em 0.4em;
                border-radius: 3px;
                font-size: 10pt;
            }

            a {
                color: #0066cc;
                text-decoration: none;
            }

            a:hover {
                text-decoration: underline;
            }
        """

    def export_html_to_file(
        self,
        assessment: Assessment,
        output_path: str,
        course_code: Optional[str] = None
    ) -> Path:
        """
        Export assessment to HTML file (for preview).

        Useful for debugging or generating HTML versions alongside PDFs.

        Args:
            assessment: Assessment to export
            output_path: Path to output HTML file
            course_code: Optional course code for header

        Returns:
            Path to generated HTML file

        Example:
            path = exporter.export_html_to_file(
                assessment,
                "output/proposal.html",
                course_code="BCI2AU"
            )
        """
        html_content = assessment.to_html_brief(course_code)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return output
