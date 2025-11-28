"""
Phase 3B: Coherence Analysis and Enhancement

This package provides comprehensive cross-week content analysis for professional
course quality enhancement.

Modules:
- analyzer: Content extraction and analysis
- terminology: Terminology consistency analysis
- scaffolding: Concept scaffolding and prerequisites
- examples: Example diversity and duplication
- cross_references: Cross-reference opportunities
- citations: Citation formatting consistency
- scorer: Quality impact scoring (1-10)
- enhancer: Enhancement application engine
- reporter: Report generation
"""

__version__ = '1.0.0'
__author__ = 'Class Content Generator'

from .analyzer import (
    WeekContent,
    Term,
    Concept,
    Example,
    Citation,
    Framework,
    ContentExtractor
)

from .terminology_analyzer import TerminologyAnalyzer
from .scaffolding_analyzer import ScaffoldingAnalyzer
from .examples_analyzer import ExamplesAnalyzer
from .cross_reference_analyzer import CrossReferenceAnalyzer
from .citation_analyzer import CitationAnalyzer
from .reporter import CoherenceReporter
from .enhancement_applicator import EnhancementApplicator, ApplicationReport

__all__ = [
    # Data structures
    'WeekContent',
    'Term',
    'Concept',
    'Example',
    'Citation',
    'Framework',
    # Content extraction
    'ContentExtractor',
    # Analyzers
    'TerminologyAnalyzer',
    'ScaffoldingAnalyzer',
    'ExamplesAnalyzer',
    'CrossReferenceAnalyzer',
    'CitationAnalyzer',
    # Reporting and application
    'CoherenceReporter',
    'EnhancementApplicator',
    'ApplicationReport'
]
