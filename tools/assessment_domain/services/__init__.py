"""
Service layer for assessment domain.

Provides business logic for quiz consolidation and other assessment operations.
"""

from .quiz_consolidation_service import QuizConsolidationService
from .question_ambiguity_analyzer import (
    QuestionAmbiguityAnalyzer,
    AmbiguityReport,
    OptionAnalysis,
    PlausibilityLevel
)

__all__ = [
    'QuizConsolidationService',
    'QuestionAmbiguityAnalyzer',
    'AmbiguityReport',
    'OptionAnalysis',
    'PlausibilityLevel',
]
