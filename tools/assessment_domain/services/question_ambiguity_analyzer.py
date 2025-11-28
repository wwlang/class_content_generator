"""
Question Ambiguity Analyzer

Detects multiple plausible answers in multiple-choice questions and suggests rewording.
Uses LLM-based semantic analysis to identify ambiguous questions.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from enum import Enum
import anthropic
import os

from tools.assessment_domain.models import Question, BloomLevel


class PlausibilityLevel(Enum):
    """How plausible an answer option is."""
    CLEARLY_CORRECT = "clearly_correct"
    PLAUSIBLE = "plausible"
    DEBATABLE = "debatable"
    CLEARLY_WRONG = "clearly_wrong"


@dataclass
class OptionAnalysis:
    """Analysis of a single answer option."""
    option_key: str
    option_text: str
    plausibility: PlausibilityLevel
    reasoning: str
    is_marked_correct: bool


@dataclass
class AmbiguityReport:
    """Report on question ambiguity."""
    question_id: str
    is_ambiguous: bool
    plausible_options: List[str]  # Options that are plausible (not clearly wrong)
    correct_answer: str
    analyses: List[OptionAnalysis]
    recommendation: str
    reworded_question: Optional[Question] = None


class QuestionAmbiguityAnalyzer:
    """
    Analyzes multiple-choice questions for answer ambiguity.

    Uses Claude to evaluate whether multiple answers could be considered correct,
    then suggests rewording to ensure only one clearly correct answer.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize analyzer with Anthropic API.

        Args:
            api_key: Anthropic API key (uses ANTHROPIC_API_KEY env var if not provided)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")

        self.client = anthropic.Anthropic(api_key=self.api_key)

    def analyze_question(self, question: Question, context: str = "") -> AmbiguityReport:
        """
        Analyze a question for answer plausibility.

        Args:
            question: Question to analyze
            context: Optional course context or topic area

        Returns:
            AmbiguityReport with plausibility analysis and recommendations
        """
        # Build analysis prompt
        prompt = self._build_analysis_prompt(question, context)

        # Call Claude for analysis
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse response
        analysis_text = response.content[0].text

        # Extract structured analysis
        analyses = self._parse_analysis(question, analysis_text)

        # Determine if ambiguous
        plausible_count = sum(
            1 for a in analyses
            if a.plausibility in [PlausibilityLevel.CLEARLY_CORRECT, PlausibilityLevel.PLAUSIBLE]
        )

        is_ambiguous = plausible_count > 1

        plausible_options = [
            a.option_key for a in analyses
            if a.plausibility in [PlausibilityLevel.CLEARLY_CORRECT, PlausibilityLevel.PLAUSIBLE]
        ]

        # Generate recommendation
        if is_ambiguous:
            recommendation = (
                f"Question has {plausible_count} plausible answers ({', '.join(plausible_options)}). "
                f"Reword to make only option {question.correct_answer} clearly correct."
            )
        else:
            recommendation = "Question has one clearly correct answer. No rewording needed."

        return AmbiguityReport(
            question_id=question.id,
            is_ambiguous=is_ambiguous,
            plausible_options=plausible_options,
            correct_answer=question.correct_answer,
            analyses=analyses,
            recommendation=recommendation
        )

    def analyze_and_reword(self, question: Question, context: str = "") -> AmbiguityReport:
        """
        Analyze question and automatically reword if ambiguous.

        Args:
            question: Question to analyze and potentially reword
            context: Optional course context

        Returns:
            AmbiguityReport with reworded question if ambiguous
        """
        # First analyze
        report = self.analyze_question(question, context)

        # If ambiguous, reword
        if report.is_ambiguous:
            reworded = self._reword_question(question, report, context)
            report.reworded_question = reworded

        return report

    def _build_analysis_prompt(self, question: Question, context: str) -> str:
        """Build prompt for question analysis."""
        context_str = f"\n\nCourse Context: {context}" if context else ""

        options_text = "\n".join([
            f"{key}. {text}" for key, text in question.options.items()
        ])

        return f"""Analyze this multiple-choice question for answer plausibility.

Question: {question.question_text}

Options:
{options_text}

Marked Correct Answer: {question.correct_answer}
{context_str}

For EACH option (A, B, C, D), determine:
1. Plausibility level: CLEARLY_CORRECT, PLAUSIBLE, DEBATABLE, or CLEARLY_WRONG
2. Reasoning: Why this option is/isn't plausible

IMPORTANT: An option is PLAUSIBLE if it could reasonably be considered correct by someone with domain knowledge, even if it's not the "best" answer. An option is DEBATABLE if reasonable people could disagree.

Format your response EXACTLY like this:

OPTION A:
Plausibility: [LEVEL]
Reasoning: [Your reasoning]

OPTION B:
Plausibility: [LEVEL]
Reasoning: [Your reasoning]

OPTION C:
Plausibility: [LEVEL]
Reasoning: [Your reasoning]

OPTION D:
Plausibility: [LEVEL]
Reasoning: [Your reasoning]

SUMMARY:
[Overall assessment of whether multiple answers are plausible]"""

    def _parse_analysis(self, question: Question, analysis_text: str) -> List[OptionAnalysis]:
        """Parse Claude's analysis into structured format."""
        analyses = []

        # Split into option blocks
        lines = analysis_text.split('\n')
        current_option = None
        current_plausibility = None
        current_reasoning = []

        for line in lines:
            line = line.strip()

            # Check for option header
            if line.startswith('OPTION '):
                # Save previous option if exists
                if current_option and current_plausibility:
                    analyses.append(OptionAnalysis(
                        option_key=current_option,
                        option_text=question.options[current_option],
                        plausibility=current_plausibility,
                        reasoning=' '.join(current_reasoning).strip(),
                        is_marked_correct=(current_option == question.correct_answer)
                    ))

                # Start new option
                current_option = line.split()[1].rstrip(':')
                current_plausibility = None
                current_reasoning = []

            elif line.startswith('Plausibility:'):
                plausibility_str = line.split(':', 1)[1].strip().upper()
                current_plausibility = self._parse_plausibility(plausibility_str)

            elif line.startswith('Reasoning:'):
                current_reasoning = [line.split(':', 1)[1].strip()]

            elif line.startswith('SUMMARY'):
                # Save last option
                if current_option and current_plausibility:
                    analyses.append(OptionAnalysis(
                        option_key=current_option,
                        option_text=question.options[current_option],
                        plausibility=current_plausibility,
                        reasoning=' '.join(current_reasoning).strip(),
                        is_marked_correct=(current_option == question.correct_answer)
                    ))
                break

            elif current_reasoning is not None and line:
                current_reasoning.append(line)

        return analyses

    def _parse_plausibility(self, plausibility_str: str) -> PlausibilityLevel:
        """Parse plausibility level from string."""
        if "CLEARLY_CORRECT" in plausibility_str or "CLEARLY CORRECT" in plausibility_str:
            return PlausibilityLevel.CLEARLY_CORRECT
        elif "PLAUSIBLE" in plausibility_str:
            return PlausibilityLevel.PLAUSIBLE
        elif "DEBATABLE" in plausibility_str:
            return PlausibilityLevel.DEBATABLE
        else:
            return PlausibilityLevel.CLEARLY_WRONG

    def _reword_question(
        self,
        question: Question,
        report: AmbiguityReport,
        context: str
    ) -> Question:
        """
        Reword question to make only one answer clearly correct.

        Args:
            question: Original question
            report: Ambiguity analysis report
            context: Course context

        Returns:
            Reworded Question object
        """
        # Build rewording prompt
        prompt = self._build_rewording_prompt(question, report, context)

        # Call Claude for rewording
        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse reworded question
        reworded_text = response.content[0].text
        return self._parse_reworded_question(question, reworded_text)

    def _build_rewording_prompt(
        self,
        question: Question,
        report: AmbiguityReport,
        context: str
    ) -> str:
        """Build prompt for question rewording."""
        context_str = f"\n\nCourse Context: {context}" if context else ""

        options_text = "\n".join([
            f"{key}. {text}" for key, text in question.options.items()
        ])

        # Include plausibility analysis
        analysis_text = "\n\n".join([
            f"Option {a.option_key}: {a.plausibility.value}\n  Reasoning: {a.reasoning}"
            for a in report.analyses
        ])

        return f"""This multiple-choice question has multiple plausible answers. Reword it so that ONLY option {question.correct_answer} is clearly correct.

ORIGINAL QUESTION:
{question.question_text}

ORIGINAL OPTIONS:
{options_text}

CORRECT ANSWER: {question.correct_answer}

PLAUSIBILITY ANALYSIS:
{analysis_text}
{context_str}

REWORDING STRATEGIES:
1. Make the question more SPECIFIC to eliminate ambiguity
2. Add qualifying details that make wrong options clearly incorrect
3. Reword distractors to be less plausible (but still realistic)
4. Ensure the correct answer is the ONLY defensible choice

Provide your reworded question in this EXACT format:

REWORDED QUESTION:
[Your reworded question text]

REWORDED OPTIONS:
A. [Option A text]
B. [Option B text]
C. [Option C text]
D. [Option D text]

FEEDBACK A:
[Updated feedback for option A]

FEEDBACK B:
[Updated feedback for option B]

FEEDBACK C:
[Updated feedback for option C]

FEEDBACK D:
[Updated feedback for option D]

CHANGES MADE:
[Brief explanation of what you changed and why]"""

    def _parse_reworded_question(self, original: Question, reworded_text: str) -> Question:
        """Parse reworded question from Claude's response."""
        lines = reworded_text.split('\n')

        question_text = None
        options = {}
        feedback = {}

        current_section = None
        current_text = []

        for line in lines:
            line = line.strip()

            if line.startswith('REWORDED QUESTION:'):
                current_section = 'question'
                current_text = []
            elif line.startswith('REWORDED OPTIONS:'):
                if current_text:
                    question_text = ' '.join(current_text).strip()
                current_section = 'options'
                current_text = []
            elif line.startswith('FEEDBACK A:'):
                current_section = 'feedback_a'
                current_text = []
            elif line.startswith('FEEDBACK B:'):
                if current_text:
                    feedback['A'] = ' '.join(current_text).strip()
                current_section = 'feedback_b'
                current_text = []
            elif line.startswith('FEEDBACK C:'):
                if current_text:
                    feedback['B'] = ' '.join(current_text).strip()
                current_section = 'feedback_c'
                current_text = []
            elif line.startswith('FEEDBACK D:'):
                if current_text:
                    feedback['C'] = ' '.join(current_text).strip()
                current_section = 'feedback_d'
                current_text = []
            elif line.startswith('CHANGES MADE:'):
                if current_text:
                    feedback['D'] = ' '.join(current_text).strip()
                break
            elif current_section == 'options' and line and line[0] in 'ABCD' and '. ' in line:
                # Parse option
                key = line[0]
                text = line.split('. ', 1)[1].strip()
                options[key] = text
            elif current_section and current_section.startswith('feedback_'):
                current_text.append(line)
            elif current_section == 'question' and line:
                current_text.append(line)

        # Create reworded question
        return Question(
            id=f"{original.id}-reworded",
            week=original.week,
            topic=original.topic,
            question_text=question_text or original.question_text,
            options=options if options else original.options,
            correct_answer=original.correct_answer,
            feedback=feedback if feedback else original.feedback,
            bloom_level=original.bloom_level,
            question_type=original.question_type
        )

    def batch_analyze(
        self,
        questions: List[Question],
        context: str = "",
        reword_ambiguous: bool = True
    ) -> List[AmbiguityReport]:
        """
        Analyze multiple questions in batch.

        Args:
            questions: List of questions to analyze
            context: Course context
            reword_ambiguous: Whether to automatically reword ambiguous questions

        Returns:
            List of AmbiguityReports
        """
        reports = []

        for question in questions:
            if reword_ambiguous:
                report = self.analyze_and_reword(question, context)
            else:
                report = self.analyze_question(question, context)

            reports.append(report)

        return reports

    def generate_report_summary(self, reports: List[AmbiguityReport]) -> str:
        """
        Generate human-readable summary of batch analysis.

        Args:
            reports: List of ambiguity reports

        Returns:
            Formatted summary text
        """
        total = len(reports)
        ambiguous = sum(1 for r in reports if r.is_ambiguous)
        reworded = sum(1 for r in reports if r.reworded_question is not None)

        summary = f"""Question Ambiguity Analysis Summary
{'=' * 50}

Total questions analyzed: {total}
Ambiguous questions found: {ambiguous} ({ambiguous/total*100:.1f}%)
Questions reworded: {reworded}

"""

        if ambiguous > 0:
            summary += "Ambiguous Questions:\n"
            summary += "-" * 50 + "\n"

            for report in reports:
                if report.is_ambiguous:
                    summary += f"\nQuestion ID: {report.question_id}\n"
                    summary += f"  Plausible options: {', '.join(report.plausible_options)}\n"
                    summary += f"  Correct answer: {report.correct_answer}\n"
                    summary += f"  Recommendation: {report.recommendation}\n"

                    if report.reworded_question:
                        summary += f"  ✓ Reworded version available\n"

        return summary
