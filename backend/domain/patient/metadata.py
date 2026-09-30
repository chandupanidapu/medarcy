"""
Medarcy Enterprise Clinical Intelligence Platform

Patient Case Metadata

Defines framework-independent metadata for a PatientCase aggregate.
The value object carries case identity and high-level workflow
classification without depending on API schemas or persistence models.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from backend.domain.common.base import ValueObject
from backend.domain.common.enums import CaseStatus, Priority


@dataclass(frozen=True, slots=True)
class Metadata(ValueObject):
    """
    Immutable metadata associated with a patient case.

    PatientCase uses this object as the stable source of its case
    identifier and workflow attributes. The domain layer intentionally
    keeps this structure independent of database primary keys, API
    request models, and infrastructure audit records.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    status: CaseStatus = CaseStatus.DRAFT

    priority: Priority = Priority.NORMAL

    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    created_by: str | None = None

    source: str | None = None
