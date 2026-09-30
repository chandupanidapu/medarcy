"""
Medarcy Enterprise Clinical Intelligence Platform

Audit Domain Entity

Represents audit information for domain entities.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from backend.domain.common.base import ValueObject


@dataclass(frozen=True, slots=True)
class Audit(ValueObject):
    """
    Immutable audit information associated with a domain entity.
    """

    created_by: str

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    last_modified_by: Optional[str] = None

    last_modified_at: Optional[datetime] = None

    version: int = 1

    def next_version(
        self,
        modified_by: str,
    ) -> "Audit":
        """
        Return a new Audit instance with an incremented version.
        """

        return Audit(
            created_by=self.created_by,
            created_at=self.created_at,
            last_modified_by=modified_by,
            last_modified_at=datetime.now(timezone.utc),
            version=self.version + 1,
        )