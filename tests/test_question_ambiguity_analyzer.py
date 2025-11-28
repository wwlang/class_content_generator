"""
Unit tests for QuestionAmbiguityAnalyzer.

Tests ambiguity detection, question rewording, and batch analysis.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from tools.assessment_domain.models import Question, BloomLevel, QuestionType
from tools.assessment_domain.services import (
    QuestionAmbiguityAnalyzer,
    AmbiguityReport,
    OptionAnalysis,
    PlausibilityLevel
)


@pytest.fixture
def sample_question():
    """Create a sample question for testing."""
    return Question(
        id="W1-Q1-test",
        week=1,
        topic="Cloud Computing",
        question_text="What is a benefit of cloud computing?",
        options={
            'A': 'Scalability',
            'B': 'Cost reduction',
            'C': 'Flexibility',
            'D': 'Increased complexity'
        },
        correct_answer='A',
        feedback={
            'A': 'Correct! Scalability is a primary benefit.',
            'B': 'While possible, not the primary benefit.',
            'C': 'True, but scalability is more fundamental.',
            'D': 'This is actually a challenge, not a benefit.'
        },
        bloom_level=BloomLevel.REMEMBERING
    )


@pytest.fixture
def clear_question():
    """Create a question with one clearly correct answer."""
    return Question(
        id="W1-Q2-clear",
        week=1,
        topic="Networking",
        question_text="What protocol is used for secure web traffic?",
        options={
            'A': 'HTTPS',
            'B': 'FTP',
            'C': 'SMTP',
            'D': 'TCP'
        },
        correct_answer='A',
        feedback={
            'A': 'Correct! HTTPS encrypts web traffic.',
            'B': 'FTP is for file transfer, not secure by default.',
            'C': 'SMTP is for email, not web traffic.',
            'D': 'TCP is a transport protocol, not specific to security.'
        },
        bloom_level=BloomLevel.REMEMBERING
    )


@pytest.fixture
def mock_anthropic_client():
    """Create mock Anthropic client."""
    with patch('tools.assessment_domain.services.question_ambiguity_analyzer.anthropic.Anthropic') as mock:
        yield mock


@pytest.fixture
def analyzer_with_mock(mock_anthropic_client):
    """Create analyzer with mocked API."""
    with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
        analyzer = QuestionAmbiguityAnalyzer(api_key='test-key')
        return analyzer


def test_analyzer_initialization():
    """Test analyzer initialization with API key."""
    with patch.dict('os.environ', {'ANTHROPIC_API_KEY': 'test-key'}):
        analyzer = QuestionAmbiguityAnalyzer()
        assert analyzer.api_key == 'test-key'


def test_analyzer_initialization_no_key():
    """Test analyzer fails without API key."""
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError, match="ANTHROPIC_API_KEY not found"):
            QuestionAmbiguityAnalyzer()


def test_build_analysis_prompt(analyzer_with_mock, sample_question):
    """Test analysis prompt building."""
    prompt = analyzer_with_mock._build_analysis_prompt(sample_question, "")

    assert "What is a benefit of cloud computing?" in prompt
    assert "A. Scalability" in prompt
    assert "B. Cost reduction" in prompt
    assert "Marked Correct Answer: A" in prompt
    assert "PLAUSIBLE" in prompt


def test_build_analysis_prompt_with_context(analyzer_with_mock, sample_question):
    """Test analysis prompt with course context."""
    context = "Introduction to Cloud Services - Week 1"
    prompt = analyzer_with_mock._build_analysis_prompt(sample_question, context)

    assert "Course Context: Introduction to Cloud Services" in prompt


def test_parse_plausibility_levels(analyzer_with_mock):
    """Test parsing plausibility levels from strings."""
    assert analyzer_with_mock._parse_plausibility("CLEARLY_CORRECT") == PlausibilityLevel.CLEARLY_CORRECT
    assert analyzer_with_mock._parse_plausibility("PLAUSIBLE") == PlausibilityLevel.PLAUSIBLE
    assert analyzer_with_mock._parse_plausibility("DEBATABLE") == PlausibilityLevel.DEBATABLE
    assert analyzer_with_mock._parse_plausibility("CLEARLY_WRONG") == PlausibilityLevel.CLEARLY_WRONG


def test_parse_analysis_response(analyzer_with_mock, sample_question):
    """Test parsing Claude's analysis response."""
    mock_response = """OPTION A:
Plausibility: CLEARLY_CORRECT
Reasoning: Scalability is the primary benefit of cloud computing.

OPTION B:
Plausibility: PLAUSIBLE
Reasoning: Cost reduction is also a valid benefit of cloud computing.

OPTION C:
Plausibility: PLAUSIBLE
Reasoning: Flexibility is another key benefit.

OPTION D:
Plausibility: CLEARLY_WRONG
Reasoning: Complexity is a challenge, not a benefit.

SUMMARY:
Multiple plausible answers detected (A, B, C)."""

    analyses = analyzer_with_mock._parse_analysis(sample_question, mock_response)

    assert len(analyses) == 4
    assert analyses[0].option_key == 'A'
    assert analyses[0].plausibility == PlausibilityLevel.CLEARLY_CORRECT
    assert analyses[1].plausibility == PlausibilityLevel.PLAUSIBLE
    assert analyses[2].plausibility == PlausibilityLevel.PLAUSIBLE
    assert analyses[3].plausibility == PlausibilityLevel.CLEARLY_WRONG


def test_analyze_question_clear(analyzer_with_mock, clear_question):
    """Test analyzing a clear question (one correct answer)."""
    # Mock Claude response
    mock_message = MagicMock()
    mock_message.content = [MagicMock()]
    mock_message.content[0].text = """OPTION A:
Plausibility: CLEARLY_CORRECT
Reasoning: HTTPS is the standard protocol for secure web traffic.

OPTION B:
Plausibility: CLEARLY_WRONG
Reasoning: FTP is for file transfer, not web traffic.

OPTION C:
Plausibility: CLEARLY_WRONG
Reasoning: SMTP is for email, not web traffic.

OPTION D:
Plausibility: CLEARLY_WRONG
Reasoning: TCP is a transport layer protocol, not application layer.

SUMMARY:
Only option A is clearly correct."""

    analyzer_with_mock.client.messages.create = Mock(return_value=mock_message)

    report = analyzer_with_mock.analyze_question(clear_question)

    assert report.is_ambiguous is False
    assert report.correct_answer == 'A'
    assert len(report.plausible_options) == 1
    assert 'A' in report.plausible_options
    assert "No rewording needed" in report.recommendation


def test_analyze_question_ambiguous(analyzer_with_mock, sample_question):
    """Test analyzing an ambiguous question (multiple plausible answers)."""
    # Mock Claude response showing ambiguity
    mock_message = MagicMock()
    mock_message.content = [MagicMock()]
    mock_message.content[0].text = """OPTION A:
Plausibility: CLEARLY_CORRECT
Reasoning: Scalability is a primary benefit.

OPTION B:
Plausibility: PLAUSIBLE
Reasoning: Cost reduction is also a valid benefit.

OPTION C:
Plausibility: PLAUSIBLE
Reasoning: Flexibility is another key benefit.

OPTION D:
Plausibility: CLEARLY_WRONG
Reasoning: Complexity is a challenge.

SUMMARY:
Multiple plausible answers (A, B, C)."""

    analyzer_with_mock.client.messages.create = Mock(return_value=mock_message)

    report = analyzer_with_mock.analyze_question(sample_question)

    assert report.is_ambiguous is True
    assert len(report.plausible_options) == 3
    assert 'A' in report.plausible_options
    assert 'B' in report.plausible_options
    assert 'C' in report.plausible_options
    assert "Reword to make only option A clearly correct" in report.recommendation


def test_build_rewording_prompt(analyzer_with_mock, sample_question):
    """Test rewording prompt building."""
    # Create mock report
    report = AmbiguityReport(
        question_id=sample_question.id,
        is_ambiguous=True,
        plausible_options=['A', 'B', 'C'],
        correct_answer='A',
        analyses=[
            OptionAnalysis('A', 'Scalability', PlausibilityLevel.CLEARLY_CORRECT, 'Primary benefit', True),
            OptionAnalysis('B', 'Cost reduction', PlausibilityLevel.PLAUSIBLE, 'Also valid', False),
            OptionAnalysis('C', 'Flexibility', PlausibilityLevel.PLAUSIBLE, 'Key benefit', False),
            OptionAnalysis('D', 'Increased complexity', PlausibilityLevel.CLEARLY_WRONG, 'Not a benefit', False)
        ],
        recommendation="Reword"
    )

    prompt = analyzer_with_mock._build_rewording_prompt(sample_question, report, "")

    assert "What is a benefit of cloud computing?" in prompt
    assert "CORRECT ANSWER: A" in prompt
    assert "PLAUSIBILITY ANALYSIS:" in prompt
    assert "Scalability" in prompt
    assert "REWORDING STRATEGIES" in prompt


def test_parse_reworded_question(analyzer_with_mock, sample_question):
    """Test parsing reworded question from Claude response."""
    mock_response = """REWORDED QUESTION:
What is the PRIMARY architectural benefit of cloud computing that allows automatic resource adjustment?

REWORDED OPTIONS:
A. Scalability and elasticity
B. Lower fixed costs
C. Deployment flexibility
D. Vendor lock-in complexity

FEEDBACK A:
Correct! Scalability and elasticity are the defining architectural benefits that distinguish cloud from traditional infrastructure.

FEEDBACK B:
While cost can be lower, this is an economic benefit, not an architectural one. The question asks about architectural benefits.

FEEDBACK C:
Flexibility is a benefit but not the PRIMARY architectural feature that enables automatic resource adjustment.

FEEDBACK D:
Vendor lock-in is a risk/challenge of cloud computing, not a benefit.

CHANGES MADE:
Made question more specific by asking about the PRIMARY architectural benefit and added "automatic resource adjustment" to clarify what makes scalability the correct answer."""

    reworded = analyzer_with_mock._parse_reworded_question(sample_question, mock_response)

    assert "PRIMARY architectural benefit" in reworded.question_text
    assert "automatic resource adjustment" in reworded.question_text
    assert 'A' in reworded.options
    assert 'B' in reworded.options
    assert "Scalability and elasticity" in reworded.options['A']
    assert len(reworded.feedback) == 4
    assert "Correct!" in reworded.feedback['A']


def test_analyze_and_reword(analyzer_with_mock, sample_question):
    """Test full analyze and reword workflow."""
    # Mock analysis response
    analysis_message = MagicMock()
    analysis_message.content = [MagicMock()]
    analysis_message.content[0].text = """OPTION A:
Plausibility: CLEARLY_CORRECT
Reasoning: Primary benefit.

OPTION B:
Plausibility: PLAUSIBLE
Reasoning: Also valid.

OPTION C:
Plausibility: PLAUSIBLE
Reasoning: Key benefit.

OPTION D:
Plausibility: CLEARLY_WRONG
Reasoning: Not a benefit.

SUMMARY:
Ambiguous."""

    # Mock rewording response
    rewording_message = MagicMock()
    rewording_message.content = [MagicMock()]
    rewording_message.content[0].text = """REWORDED QUESTION:
What is the PRIMARY benefit that distinguishes cloud computing?

REWORDED OPTIONS:
A. Scalability
B. Reduced infrastructure costs
C. Flexible deployment
D. Complex management

FEEDBACK A:
Correct! Scalability is the defining benefit.

FEEDBACK B:
Cost reduction is secondary.

FEEDBACK C:
Flexibility is not the primary distinguisher.

FEEDBACK D:
Complexity is a challenge.

CHANGES MADE:
Made question more specific."""

    analyzer_with_mock.client.messages.create = Mock(
        side_effect=[analysis_message, rewording_message]
    )

    report = analyzer_with_mock.analyze_and_reword(sample_question)

    assert report.is_ambiguous is True
    assert report.reworded_question is not None
    assert "PRIMARY benefit" in report.reworded_question.question_text
    assert analyzer_with_mock.client.messages.create.call_count == 2


def test_batch_analyze(analyzer_with_mock, sample_question, clear_question):
    """Test batch analysis of multiple questions."""
    questions = [sample_question, clear_question]

    # Mock responses for both questions
    mock_message = MagicMock()
    mock_message.content = [MagicMock()]
    mock_message.content[0].text = """OPTION A:
Plausibility: CLEARLY_CORRECT
Reasoning: Correct answer.

OPTION B:
Plausibility: CLEARLY_WRONG
Reasoning: Wrong.

OPTION C:
Plausibility: CLEARLY_WRONG
Reasoning: Wrong.

OPTION D:
Plausibility: CLEARLY_WRONG
Reasoning: Wrong.

SUMMARY:
Clear."""

    analyzer_with_mock.client.messages.create = Mock(return_value=mock_message)

    reports = analyzer_with_mock.batch_analyze(questions, reword_ambiguous=False)

    assert len(reports) == 2
    assert all(isinstance(r, AmbiguityReport) for r in reports)


def test_generate_report_summary(analyzer_with_mock):
    """Test report summary generation."""
    reports = [
        AmbiguityReport(
            question_id="Q1",
            is_ambiguous=True,
            plausible_options=['A', 'B'],
            correct_answer='A',
            analyses=[],
            recommendation="Reword Q1"
        ),
        AmbiguityReport(
            question_id="Q2",
            is_ambiguous=False,
            plausible_options=['C'],
            correct_answer='C',
            analyses=[],
            recommendation="OK"
        )
    ]

    summary = analyzer_with_mock.generate_report_summary(reports)

    assert "Total questions analyzed: 2" in summary
    assert "Ambiguous questions found: 1 (50.0%)" in summary
    assert "Q1" in summary
    assert "Plausible options: A, B" in summary


def test_option_analysis_creation():
    """Test creating OptionAnalysis dataclass."""
    analysis = OptionAnalysis(
        option_key='A',
        option_text='Test option',
        plausibility=PlausibilityLevel.PLAUSIBLE,
        reasoning='This is plausible because...',
        is_marked_correct=True
    )

    assert analysis.option_key == 'A'
    assert analysis.plausibility == PlausibilityLevel.PLAUSIBLE
    assert analysis.is_marked_correct is True


def test_ambiguity_report_creation():
    """Test creating AmbiguityReport dataclass."""
    report = AmbiguityReport(
        question_id='W1-Q1',
        is_ambiguous=True,
        plausible_options=['A', 'B'],
        correct_answer='A',
        analyses=[],
        recommendation='Reword question'
    )

    assert report.question_id == 'W1-Q1'
    assert report.is_ambiguous is True
    assert len(report.plausible_options) == 2
    assert report.reworded_question is None


def test_plausibility_level_enum():
    """Test PlausibilityLevel enum values."""
    assert PlausibilityLevel.CLEARLY_CORRECT.value == "clearly_correct"
    assert PlausibilityLevel.PLAUSIBLE.value == "plausible"
    assert PlausibilityLevel.DEBATABLE.value == "debatable"
    assert PlausibilityLevel.CLEARLY_WRONG.value == "clearly_wrong"
