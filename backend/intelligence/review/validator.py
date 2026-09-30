"""
Medarcy Enterprise Clinical Intelligence Platform

Clinical Review Validator

Validates ClinicalReview aggregates produced by the
Review Intelligence Engine.
"""

from __future__ import annotations

from backend.domain.review.clinical_review import ClinicalReview
from backend.intelligence.shared.exceptions import (
    ResponseValidationError,
)


class ReviewValidator:
    """
    Validates ClinicalReview objects before they leave
    the Intelligence Layer.

    This validator is responsible only for ensuring the
    review satisfies Intelligence Layer requirements.
    """

    def validate(
        self,
        review: ClinicalReview,
    ) -> None:
        """
        Validate a ClinicalReview.

        Raises
        ------
        ResponseValidationError
            If validation fails.
        """

        if not review.is_complete():
            raise ResponseValidationError(
                "ClinicalReview is incomplete."
            )

        if review.metadata is None:
            raise ResponseValidationError(
                "Review metadata is missing."
            )

        if review.executive_summary is None:
            raise ResponseValidationError(
                "Executive summary is missing."
            )

        if review.assessment is None:
            raise ResponseValidationError(
                "Assessment is missing."
            )

        if review.clinical_reasoning is None:
            raise ResponseValidationError(
                "Clinical reasoning is missing."
            )

        if review.confidence is None:
            raise ResponseValidationError(
                "Confidence information is missing."
            )

        if not (
            0.0
            <= review.confidence.score
            <= 1.0
        ):
            raise ResponseValidationError(
                "Confidence score must be between 0.0 and 1.0."
            )

        if (
            review.executive_summary.content.strip()
            == ""
        ):
            raise ResponseValidationError(
                "Executive summary cannot be empty."
            )

        if (
            review.assessment.content.strip()
            == ""
        ):
            raise ResponseValidationError(
                "Assessment cannot be empty."
            )

        if (
            review.clinical_reasoning.content.strip()
            == ""
        ):
            raise ResponseValidationError(
                "Clinical reasoning cannot be empty."
            )