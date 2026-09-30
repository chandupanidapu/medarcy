"""
Medarcy Enterprise Clinical Intelligence Platform

Case Review Queries

Queries are immutable application-layer messages that describe
read-only requests for clinical review data. They do not contain
business rules, persistence behavior, or framework concerns.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.domain.common.enums import ReviewStatus


@dataclass(frozen=True, slots=True)
class GetClinicalReviewQuery:
    """
    Request to retrieve one Clinical Review by its review identifier.
    """

    review_id: str


@dataclass(frozen=True, slots=True)
class GetLatestClinicalReviewQuery:
    """
    Request to retrieve the latest Clinical Review for a patient case.
    """

    patient_case_id: str


@dataclass(frozen=True, slots=True)
class ListClinicalReviewsQuery:
    """
    Request to list Clinical Reviews with optional application filters.
    """

    patient_case_id: str | None = None

    status: ReviewStatus | None = None

    limit: int | None = None

    offset: int = 0
