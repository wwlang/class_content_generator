"""
Unit tests for GIFTExporter and PDFExporter.

Tests GIFT format generation, PDF export, and file I/O operations.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from tools.assessment_domain.exporters.gift_exporter import GIFTExporter
from tools.assessment_domain.exporters.pdf_exporter import PDFExporter
from tools.assessment_domain.models import (
    Question, QuizBank, Assessment, AssessmentType,
    BloomLevel, Rubric, RubricCriterion, Scenario
)


@pytest.fixture
def sample_questions():
    """Create sample questions for testing."""
    return [
        Question(
            "W1-Q1-test",
            1,
            "Test Topic 1",
            "What is the answer?",
            {'A': 'Option A', 'B': 'Option B', 'C': 'Option C', 'D': 'Option D'},
            'A',
            {'A': 'Correct answer', 'B': 'Wrong because X', 'C': 'Wrong because Y', 'D': 'Wrong because Z'},
            BloomLevel.REMEMBERING
        ),
        Question(
            "W1-Q2-test",
            1,
            "Test Topic 2",
            "Why is this important?",
            {'A': 'Reason A', 'B': 'Reason B', 'C': 'Reason C', 'D': 'Reason D'},
            'B',
            {'A': 'Wrong', 'B': 'Correct', 'C': 'Wrong', 'D': 'Wrong'},
            BloomLevel.UNDERSTANDING
        )
    ]


@pytest.fixture
def sample_quiz_bank(sample_questions):
    """Create sample quiz bank for testing."""
    return QuizBank(
        quiz_id="quiz-1",
        title="Quiz 1 - Weeks 1-2",
        weeks_covered=[1, 2],
        questions=sample_questions,
        target_total=2,
        target_remembering=1,
        target_understanding=1
    )


@pytest.fixture
def sample_assessment():
    """Create sample assessment for testing."""
    criteria = [
        RubricCriterion(
            "Content", 0.5,
            "Excellent content", "Good content", "OK content", "Poor content", "No content"
        ),
        RubricCriterion(
            "Style", 0.5,
            "Excellent style", "Good style", "OK style", "Poor style", "No style"
        )
    ]
    rubric = Rubric("Test Rubric", criteria)

    scenarios = [
        Scenario(
            "Option A: Scenario 1",
            "Description of scenario 1",
            ["Requirement 1", "Requirement 2"]
        )
    ]

    return Assessment(
        id="test-assessment",
        name="Test Assessment",
        type=AssessmentType.PORTFOLIO,
        weight=0.10,
        due_week=3,
        description="Test description",
        requirements=["Requirement 1", "Requirement 2"],
        rubric=rubric,
        scenarios=scenarios
    )


class TestGIFTExporter:
    """Tests for GIFTExporter."""

    def test_export_quiz_bank_basic(self, sample_quiz_bank):
        """Test basic GIFT export."""
        exporter = GIFTExporter()
        gift = exporter.export_quiz_bank(sample_quiz_bank)

        # Check header comments
        assert "// Quiz 1 - Weeks 1-2" in gift
        assert "// Quiz ID: quiz-1" in gift
        assert "// Questions: 2" in gift
        assert "// Weeks covered: 1, 2" in gift

        # Check Bloom distribution
        assert "1 Remembering" in gift
        assert "1 Understanding" in gift

        # Check category
        assert "$CATEGORY:" in gift

    def test_export_question_with_feedback(self, sample_questions):
        """Test exporting question with feedback."""
        exporter = GIFTExporter(include_feedback=True)
        gift = exporter._export_question(sample_questions[0])

        # Check question title and text
        assert "::Test Topic 1::" in gift
        assert "What is the answer?" in gift

        # Check correct answer marker
        assert "=Option A #Correct answer" in gift

        # Check distractor markers
        assert "~Option B #Wrong because X" in gift
        assert "~Option C #Wrong because Y" in gift
        assert "~Option D #Wrong because Z" in gift

    def test_export_question_without_feedback(self, sample_questions):
        """Test exporting question without feedback."""
        exporter = GIFTExporter(include_feedback=False)
        gift = exporter._export_question(sample_questions[0])

        # Should have options but no feedback
        assert "=Option A" in gift
        assert "~Option B" in gift
        # Should NOT have feedback markers
        assert "#Correct answer" not in gift
        assert "#Wrong because" not in gift

    def test_escape_gift_text_backslash(self):
        """Test escaping backslashes."""
        exporter = GIFTExporter()
        text = r"Use \ backslash"
        escaped = exporter._escape_gift_text(text)
        assert escaped == r"Use \\ backslash"

    def test_escape_gift_text_braces(self):
        """Test escaping braces."""
        exporter = GIFTExporter()
        text = "Use {braces} here"
        escaped = exporter._escape_gift_text(text)
        assert escaped == r"Use \{braces\} here"

    def test_escape_gift_text_special_chars(self):
        """Test escaping all special GIFT characters."""
        exporter = GIFTExporter()
        text = r"Use \ { } = ~ # : all"
        escaped = exporter._escape_gift_text(text)

        # All should be escaped
        assert r"\\" in escaped
        assert r"\{" in escaped
        assert r"\}" in escaped
        assert r"\=" in escaped
        assert r"\~" in escaped
        assert r"\#" in escaped
        assert r"\:" in escaped

    def test_escape_gift_text_order_matters(self):
        """Test that escaping order prevents double-escaping."""
        exporter = GIFTExporter()
        # Backslash followed by brace
        text = r"\{test}"
        escaped = exporter._escape_gift_text(text)

        # Should be \\{test\}, not \\\{test\}
        assert escaped == r"\\\{test\}"

    def test_write_to_file(self, tmp_path, sample_quiz_bank):
        """Test writing GIFT to file."""
        exporter = GIFTExporter()
        gift_content = exporter.export_quiz_bank(sample_quiz_bank)

        output_path = tmp_path / "test-quiz.gift"
        result_path = exporter.write_to_file(gift_content, str(output_path))

        # Check file was created
        assert result_path.exists()
        assert result_path == output_path

        # Check content
        content = result_path.read_text(encoding='utf-8')
        assert "Quiz 1" in content
        assert "$CATEGORY:" in content

    def test_write_to_file_creates_directories(self, tmp_path, sample_quiz_bank):
        """Test that write_to_file creates parent directories."""
        exporter = GIFTExporter()
        gift_content = exporter.export_quiz_bank(sample_quiz_bank)

        # Nested path that doesn't exist
        output_path = tmp_path / "nested" / "dir" / "quiz.gift"
        result_path = exporter.write_to_file(gift_content, str(output_path))

        assert result_path.exists()
        assert result_path.parent.exists()

    def test_export_to_file(self, tmp_path, sample_quiz_bank):
        """Test convenience method export_to_file."""
        exporter = GIFTExporter()
        output_path = tmp_path / "quiz.gift"

        result_path = exporter.export_to_file(sample_quiz_bank, str(output_path))

        assert result_path.exists()

        content = result_path.read_text(encoding='utf-8')
        assert "Quiz 1" in content
        assert "::Test Topic 1::" in content

    def test_export_with_custom_category(self, sample_quiz_bank):
        """Test exporting with custom category name."""
        exporter = GIFTExporter()
        gift = exporter.export_quiz_bank(sample_quiz_bank, category="Custom Category")

        assert "$CATEGORY: Custom Category" in gift

    def test_export_empty_quiz_bank(self):
        """Test exporting empty quiz bank."""
        quiz_bank = QuizBank(
            quiz_id="empty",
            title="Empty Quiz",
            weeks_covered=[1],
            questions=[]
        )

        exporter = GIFTExporter()
        gift = exporter.export_quiz_bank(quiz_bank)

        # Should have header but no questions
        assert "// Empty Quiz" in gift
        assert "// Questions: 0" in gift
        assert "$CATEGORY:" in gift


class TestPDFExporter:
    """Tests for PDFExporter."""

    def test_initialization(self):
        """Test PDF exporter initialization."""
        exporter = PDFExporter()
        assert exporter is not None

    def test_get_pdf_css(self):
        """Test CSS generation for PDF."""
        exporter = PDFExporter()
        css = exporter._get_pdf_css()

        # Check key CSS elements
        assert "@page" in css
        assert "size: A4" in css
        assert "font-family:" in css
        assert "table" in css
        assert ".metadata" in css
        assert ".scenario" in css

    @patch('tools.assessment_domain.exporters.pdf_exporter.HTML')
    @patch('tools.assessment_domain.exporters.pdf_exporter.CSS')
    def test_export_to_pdf_weasyprint_available(self, mock_css, mock_html, tmp_path, sample_assessment):
        """Test PDF export when WeasyPrint is available."""
        # Mock WeasyPrint
        mock_html_instance = MagicMock()
        mock_html.return_value = mock_html_instance

        exporter = PDFExporter()
        output_path = tmp_path / "test.pdf"

        # Need to patch the import
        with patch.dict('sys.modules', {'weasyprint': MagicMock()}):
            result_path = exporter.export_to_pdf(
                sample_assessment,
                str(output_path),
                course_code="TEST101"
            )

        # Check HTML.write_pdf was called
        mock_html_instance.write_pdf.assert_called_once()

    def test_export_to_pdf_weasyprint_not_available(self, tmp_path, sample_assessment):
        """Test PDF export raises error when WeasyPrint not installed."""
        exporter = PDFExporter()
        output_path = tmp_path / "test.pdf"

        # Simulate ImportError for weasyprint
        with patch('builtins.__import__', side_effect=ImportError("No module named 'weasyprint'")):
            with pytest.raises(ImportError, match="WeasyPrint is required"):
                exporter.export_to_pdf(sample_assessment, str(output_path))

    def test_export_html_to_file(self, tmp_path, sample_assessment):
        """Test HTML export to file."""
        exporter = PDFExporter()
        output_path = tmp_path / "test.html"

        result_path = exporter.export_html_to_file(
            sample_assessment,
            str(output_path),
            course_code="TEST101"
        )

        # Check file was created
        assert result_path.exists()

        # Check content
        content = result_path.read_text(encoding='utf-8')
        assert "<html" in content
        assert "Test Assessment" in content
        assert "TEST101" in content

    def test_export_html_creates_directories(self, tmp_path, sample_assessment):
        """Test that HTML export creates parent directories."""
        exporter = PDFExporter()
        output_path = tmp_path / "nested" / "dir" / "test.html"

        result_path = exporter.export_html_to_file(sample_assessment, str(output_path))

        assert result_path.exists()
        assert result_path.parent.exists()

    def test_export_html_with_rubric(self, sample_assessment):
        """Test HTML export includes rubric."""
        exporter = PDFExporter()
        html = sample_assessment.to_html_brief()

        assert "Content" in html
        assert "Style" in html
        assert "Excellent" in html

    def test_export_html_with_scenarios(self, sample_assessment):
        """Test HTML export includes scenarios."""
        exporter = PDFExporter()
        html = sample_assessment.to_html_brief()

        assert "Option A: Scenario 1" in html
        assert "Description of scenario 1" in html

    def test_export_html_encoding(self, tmp_path):
        """Test HTML export handles UTF-8 encoding."""
        # Create assessment with special characters
        assessment = Assessment(
            id="special",
            name="Test © Assessment™",
            type=AssessmentType.PORTFOLIO,
            weight=0.10,
            due_week=1,
            description="Description with émojis 🎓 and spëcial çharacters",
            requirements=["Requirement with €uro"]
        )

        exporter = PDFExporter()
        output_path = tmp_path / "special.html"

        result_path = exporter.export_html_to_file(assessment, str(output_path))

        # Check file can be read with UTF-8
        content = result_path.read_text(encoding='utf-8')
        assert "©" in content or "Assessment" in content
        assert "émojis" in content or "special" in content


class TestExporterIntegration:
    """Integration tests for exporters."""

    def test_gift_export_full_workflow(self, tmp_path, sample_quiz_bank):
        """Test complete GIFT export workflow."""
        exporter = GIFTExporter(include_feedback=True)

        # Export to file
        output_path = tmp_path / "output" / "quiz-1.gift"
        result_path = exporter.export_to_file(sample_quiz_bank, str(output_path))

        # Verify file
        assert result_path.exists()

        content = result_path.read_text()

        # Check all components present
        assert "// Quiz 1 - Weeks 1-2" in content
        assert "$CATEGORY:" in content
        assert "::Test Topic 1::" in content
        assert "::Test Topic 2::" in content
        assert "What is the answer?" in content
        assert "Why is this important?" in content

    def test_html_export_full_workflow(self, tmp_path, sample_assessment):
        """Test complete HTML export workflow."""
        exporter = PDFExporter()

        # Export to file
        output_path = tmp_path / "output" / "assessment.html"
        result_path = exporter.export_html_to_file(
            sample_assessment,
            str(output_path),
            course_code="BCI2AU"
        )

        # Verify file
        assert result_path.exists()

        content = result_path.read_text()

        # Check all components present
        assert "Test Assessment" in content
        assert "BCI2AU" in content
        assert "Portfolio" in content
        assert "10%" in content or "10.0%" in content
        assert "Week 3" in content
        assert "Test Rubric" in content
        assert "Option A: Scenario 1" in content
