"""
Content Validators Package

AI-powered validation for university teaching content quality.
"""

from .base import (
    BaseValidator,
    ValidationResult,
    ValidationIssue,
    IssueSeverity,
    ValidationReport
)

from .bloom_level_validator import BloomLevelValidator
from .tutorial_assessment_validator import TutorialAssessmentValidator
from .lecture_quiz_validator import LectureQuizValidator
from .framework_scaffolding_validator import FrameworkScaffoldingValidator
from .learning_objective_validator import LearningObjectiveValidator
from .rubric_validator import RubricValidator
from .terminology_validator import TerminologyValidator
from .cultural_sensitivity_validator import CulturalSensitivityValidator

__all__ = [
    # Base classes
    'BaseValidator',
    'ValidationResult',
    'ValidationIssue',
    'IssueSeverity',
    'ValidationReport',

    # Phase 1 Validators
    'BloomLevelValidator',
    'TutorialAssessmentValidator',
    'LectureQuizValidator',
    'FrameworkScaffoldingValidator',

    # Phase 2 Validators
    'LearningObjectiveValidator',
    'RubricValidator',
    'TerminologyValidator',
    'CulturalSensitivityValidator',
]
