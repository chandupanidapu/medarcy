"""
Medarcy Enterprise Clinical Intelligence Platform

Clinical Review Sections

Core reasoning sections used in a Clinical Review.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from backend.domain.common.base import ValueObject


# ============================================================
# BASE SECTION
# ============================================================

@dataclass(frozen=True, slots=True)
class ReviewSection(ValueObject):
    """
    Base class for all review sections.
    """

    title: str

    content: str

    key_findings: List[str] = field(default_factory=list)


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================

@dataclass(frozen=True, slots=True)
class ExecutiveSummary(ReviewSection):
    """
    High-level overview of the clinical case.
    """


# ============================================================
# ASSESSMENT
# ============================================================

@dataclass(frozen=True, slots=True)
class Assessment(ReviewSection):
    """
    Primary clinical assessment.
    """


# ============================================================
# CLINICAL REASONING
# ============================================================

@dataclass(frozen=True, slots=True)
class ClinicalReasoning(ReviewSection):
    """
    Explains why the assessment was reached.
    """