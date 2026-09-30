"""
Medarcy Enterprise Clinical Intelligence Platform

Domain Enumerations

This module contains all domain-level enumerations used throughout
the Medarcy platform. Domain enums are framework-independent and
represent core business concepts.

Do NOT import FastAPI, Pydantic, SQLAlchemy, or any infrastructure
dependencies into this module.
"""

from enum import Enum


class StringEnum(str, Enum):
    """
    Base class for string-based enumerations.

    Ensures enum values serialize naturally while retaining Enum
    semantics.
    """

    def __str__(self) -> str:
        return self.value


# ============================================================
# PATIENT
# ============================================================

class Sex(StringEnum):
    """Biological sex."""

    MALE = "male"
    FEMALE = "female"
    INTERSEX = "intersex"
    UNKNOWN = "unknown"


# ============================================================
# CASE
# ============================================================

class CaseStatus(StringEnum):
    """Lifecycle status of a patient case."""

    DRAFT = "draft"
    OPEN = "open"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Priority(StringEnum):
    """Clinical priority."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


# ============================================================
# ENCOUNTER
# ============================================================

class EncounterType(StringEnum):
    """Clinical encounter type."""

    OUTPATIENT = "outpatient"
    INPATIENT = "inpatient"
    EMERGENCY = "emergency"
    ICU = "icu"
    TELEMEDICINE = "telemedicine"
    HOME_CARE = "home_care"


# ============================================================
# REVIEW
# ============================================================

class ReviewStatus(StringEnum):
    """Execution status of a clinical review."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# ============================================================
# EVIDENCE
# ============================================================

class EvidenceLevel(StringEnum):
    """Strength of supporting evidence."""

    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    INSUFFICIENT = "insufficient"