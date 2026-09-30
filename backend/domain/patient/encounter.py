"""
Medarcy Enterprise Clinical Intelligence Platform

Encounter Domain Entity

Represents a single clinical encounter between a patient
and a healthcare provider.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

from backend.domain.common.base import Entity
from backend.domain.common.enums import EncounterType


@dataclass(slots=True)
class Encounter(Entity):
    """
    Represents a clinical encounter.
    """

    encounter_id: str

    encounter_type: EncounterType

    encounter_datetime: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    department: Optional[str] = None

    facility: Optional[str] = None

    clinician_id: Optional[str] = None

    encounter_reason: Optional[str] = None

    def reschedule(
        self,
        encounter_datetime: datetime,
    ) -> None:
        """
        Update the encounter date and time.
        """
        self.encounter_datetime = encounter_datetime

    def assign_clinician(
        self,
        clinician_id: str,
    ) -> None:
        """
        Assign a clinician to this encounter.
        """
        self.clinician_id = clinician_id

    def update_department(
        self,
        department: str,
    ) -> None:
        """
        Update department.
        """
        self.department = department

    def update_facility(
        self,
        facility: str,
    ) -> None:
        """
        Update facility.
        """
        self.facility = facility

    @property
    def is_emergency(self) -> bool:
        return (
            self.encounter_type
            == EncounterType.EMERGENCY
        )

    @property
    def is_inpatient(self) -> bool:
        return (
            self.encounter_type
            == EncounterType.INPATIENT
        )

    @property
    def is_outpatient(self) -> bool:
        return (
            self.encounter_type
            == EncounterType.OUTPATIENT
        )