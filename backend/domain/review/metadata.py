"""
Medarcy Enterprise Clinical Intelligence Platform

Clinical Review Metadata

Defines metadata associated with a clinical review.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from backend.domain.common.base import ValueObject
from backend.domain.common.enums import Priority, ReviewStatus


@dataclass(frozen=True, slots=True)
class ReviewMetadata(ValueObject):
    """
    Immutable metadata describing a ClinicalReview.
    """

    review_id: str

    status: ReviewStatus = ReviewStatus.PENDING

    priority: Priority = Priority.NORMAL

    version: int = 1

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    generated_by: str = "Medarcy Clinical Intelligence Engine"

    model_name: str = "Unknown"

    model_version: str = "Unknown"

    generation_time_ms: int | None = None

    language: str = "en"

    def next_version(
        self,
        *,
        status: ReviewStatus,
        model_name: str,
        model_version: str,
        generation_time_ms: int | None = None,
    ) -> "ReviewMetadata":
        """
        Create a new metadata instance representing
        the next review version.
        """

        return ReviewMetadata(
            review_id=self.review_id,
            status=status,
            priority=self.priority,
            version=self.version + 1,
            created_at=self.created_at,
            updated_at=datetime.now(timezone.utc),
            generated_by=self.generated_by,
            model_name=model_name,
            model_version=model_version,
            generation_time_ms=generation_time_ms,
            language=self.language,
        )