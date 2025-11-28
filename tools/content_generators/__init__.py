"""
Content generators package for course generation.

Provides classes for generating lecture content, tutorials, and tutor notes.
"""

from .base_generator import BaseGenerator
from .lecture_generator import LectureGenerator
from .tutorial_generator import TutorialGenerator
from .tutor_notes_generator import TutorNotesGenerator

__all__ = [
    'BaseGenerator',
    'LectureGenerator',
    'TutorialGenerator',
    'TutorNotesGenerator'
]

__version__ = '1.0.0'
