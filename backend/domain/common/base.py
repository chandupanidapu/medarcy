"""
Medarcy Enterprise Clinical Intelligence Platform

Domain Base Classes

Defines the foundational abstractions for all domain objects.

The domain layer must remain independent of FastAPI, Pydantic,
SQLAlchemy, databases, and LLM providers.
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

# ============================================================
# ENTITY
# ============================================================


@dataclass(slots=True)
class Entity(ABC):
    """
    Base class for all domain entities.

    Entities have identity and lifecycle.
    """

    id: str = field(
        default_factory=lambda: str(uuid4()),
        kw_only=True,
    )

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False

        return self.id == other.id


# ============================================================
# AGGREGATE ROOT
# ============================================================


@dataclass(slots=True)
class AggregateRoot(Entity):
    """
    Root entity of an aggregate.

    Example:
        PatientCase
        ClinicalReview
    """

    pass


# ============================================================
# VALUE OBJECT
# ============================================================


@dataclass(frozen=True, slots=True)
class ValueObject(ABC):
    """
    Base class for immutable value objects.

    Equality is determined by values rather than identity.
    """

    pass


# ============================================================
# AUDITABLE ENTITY
# ============================================================


@dataclass(slots=True)
class AuditableEntity(Entity):
    """
    Base entity with auditing information.
    """

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
        kw_only=True,
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
        kw_only=True,
    )

    def touch(self) -> None:
        """
        Update the modification timestamp.
        """

        self.updated_at = datetime.now(timezone.utc)
