"""
Medarcy Enterprise Clinical Intelligence Platform

Clinical Review Evidence

Evidence supporting clinical recommendations.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from backend.domain.common.base import ValueObject
from backend.domain.common.enums import EvidenceLevel


# ============================================================
# REFERENCE
# ============================================================

@dataclass(frozen=True, slots=True)
class Reference(ValueObject):
    """
    Scientific or clinical reference.
    """

    title: str

    source: str

    year: int | None = None

    doi: str | None = None

    url: str | None = None


# ============================================================
# EVIDENCE
# ============================================================

@dataclass(frozen=True, slots=True)
class Evidence(ValueObject):
    """
    Supporting evidence for a recommendation.
    """

    summary: str

    level: EvidenceLevel

    references: List[Reference] = field(default_factory=list)


# ============================================================
# CONFIDENCE
# ============================================================

@dataclass(frozen=True, slots=True)
class Confidence(ValueObject):
    """
    Confidence associated with the review.
    """

    score: float

    rationale: str

    def __post_init__(self) -> None:
        if not 0.0 <= self.score <= 1.0:
            raise ValueError(
                "Confidence score must be between 0.0 and 1.0."
            )


# ============================================================
# LIMITATION
# ============================================================

@dataclass(frozen=True, slots=True)
class Limitation(ValueObject):
    """
    Limitation affecting the review.
    """

    description: str