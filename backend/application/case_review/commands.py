"""
Medarcy Enterprise Clinical Intelligence Platform

Case Review Commands

Commands represent intentions to perform state-changing
operations within the Case Review application layer.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.domain.patient.patient_case import PatientCase


@dataclass(frozen=True, slots=True)
class CreateClinicalReviewCommand:
    """
    Request to generate a new Clinical Review.
    """

    patient_case: PatientCase

    model_name: str

    model_version: str


@dataclass(frozen=True, slots=True)
class RegenerateClinicalReviewCommand:
    """
    Request to regenerate an existing Clinical Review.
    """

    patient_case: PatientCase

    review_id: str

    model_name: str

    model_version: str


@dataclass(frozen=True, slots=True)
class ApproveClinicalReviewCommand:
    """
    Request to approve a completed Clinical Review.
    """

    review_id: str

    approved_by: str
