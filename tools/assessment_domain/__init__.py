"""
Assessment Domain - Clean architecture domain layer for assessment automation.

This package provides domain models, repositories, services, parsers, and exporters
for automated quiz bank consolidation and assignment brief generation.
"""

from .models import (
    Question,
    QuestionType,
    BloomLevel,
    QuizBank,
    Rubric,
    RubricCriterion,
    Assessment,
    AssessmentType,
    Scenario,
)
from .repositories import (
    QuestionRepository,
    AssessmentRepository,
)
from .services import (
    QuizConsolidationService,
)
from .exporters import (
    GIFTExporter,
    PDFExporter,
)

__version__ = '1.0.0'

__all__ = [
    'Question',
    'QuestionType',
    'BloomLevel',
    'QuizBank',
    'Rubric',
    'RubricCriterion',
    'Assessment',
    'AssessmentType',
    'Scenario',
    'QuestionRepository',
    'AssessmentRepository',
    'QuizConsolidationService',
    'GIFTExporter',
    'PDFExporter',
]
