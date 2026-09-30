"""
Medarcy Enterprise Clinical Intelligence Platform

Medical History Domain Entity

Represents the patient's relevant medical background.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from backend.domain.common.base import Entity


@dataclass(slots=True)
class MedicalHistory(Entity):
    """
    Represents clinically relevant medical history.
    """

    past_medical_history: List[str] = field(default_factory=list)

    surgical_history: List[str] = field(default_factory=list)

    family_history: List[str] = field(default_factory=list)

    social_history: List[str] = field(default_factory=list)

    allergies: List[str] = field(default_factory=list)

    current_medications: List[str] = field(default_factory=list)

    def add_past_condition(self, condition: str) -> None:
        condition = condition.strip()

        if condition and condition not in self.past_medical_history:
            self.past_medical_history.append(condition)

    def add_surgery(self, surgery: str) -> None:
        surgery = surgery.strip()

        if surgery and surgery not in self.surgical_history:
            self.surgical_history.append(surgery)

    def add_family_history(self, condition: str) -> None:
        condition = condition.strip()

        if condition and condition not in self.family_history:
            self.family_history.append(condition)

    def add_social_history(self, item: str) -> None:
        item = item.strip()

        if item and item not in self.social_history:
            self.social_history.append(item)

    def add_allergy(self, allergy: str) -> None:
        allergy = allergy.strip()

        if allergy and allergy not in self.allergies:
            self.allergies.append(allergy)

    def add_medication(self, medication: str) -> None:
        medication = medication.strip()

        if medication and medication not in self.current_medications:
            self.current_medications.append(medication)

    @property
    def has_allergies(self) -> bool:
        return len(self.allergies) > 0

    @property
    def medication_count(self) -> int:
        return len(self.current_medications)