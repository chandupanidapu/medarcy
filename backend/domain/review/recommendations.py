"""
Medarcy Enterprise Clinical Intelligence Platform

Clinical Review Recommendations

Actionable recommendations generated during
clinical review.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from backend.domain.common.base import ValueObject


# ============================================================
# BASE RECOMMENDATION
# ============================================================

@dataclass(frozen=True, slots=True)
class Recommendation(ValueObject):
    """
    Base recommendation object.
    """

    title: str

    summary: str

    recommendations: List[str] = field(default_factory=list)


# ============================================================
# DIFFERENTIAL DIAGNOSIS
# ============================================================

@dataclass(frozen=True, slots=True)
class DifferentialDiagnosis(Recommendation):
    """
    Ranked differential diagnoses.
    """


# ============================================================
# INVESTIGATION PLAN
# ============================================================

@dataclass(frozen=True, slots=True)
class InvestigationPlan(Recommendation):
    """
    Recommended investigations.
    """


# ============================================================
# MANAGEMENT PLAN
# ============================================================

@dataclass(frozen=True, slots=True)
class ManagementPlan(Recommendation):
    """
    Recommended clinical management.
    """


# ============================================================
# MEDICATION PLAN
# ============================================================

@dataclass(frozen=True, slots=True)
class MedicationPlan(Recommendation):
    """
    Medication recommendations.
    """


# ============================================================
# PROCEDURES
# ============================================================

@dataclass(frozen=True, slots=True)
class Procedures(Recommendation):
    """
    Recommended procedures.
    """


# ============================================================
# FOLLOW-UP
# ============================================================

@dataclass(frozen=True, slots=True)
class FollowUp(Recommendation):
    """
    Follow-up recommendations.
    """


# ============================================================
# PATIENT EDUCATION
# ============================================================

@dataclass(frozen=True, slots=True)
class PatientEducation(Recommendation):
    """
    Patient counselling and education.
    """