"""
Medarcy Enterprise Clinical Intelligence Platform

Clinical Presentation Domain Entity

Represents the patient's presenting clinical problem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from backend.domain.common.base import Entity


@dataclass(slots=True)
class ClinicalPresentation(Entity):
    """
    Represents the patient's presenting complaint
    and current clinical presentation.
    """

    chief_complaint: str

    history_of_present_illness: str

    symptoms: List[str] = field(default_factory=list)

    duration: Optional[str] = None

    onset: Optional[str] = None

    severity: Optional[str] = None

    clinical_context: Optional[str] = None

    def add_symptom(self, symptom: str) -> None:
        """
        Add a symptom if it is not already present.
        """

        symptom = symptom.strip()

        if symptom and symptom not in self.symptoms:
            self.symptoms.append(symptom)

    def remove_symptom(self, symptom: str) -> None:
        """
        Remove a symptom.
        """

        if symptom in self.symptoms:
            self.symptoms.remove(symptom)

    def update_chief_complaint(
        self,
        complaint: str,
    ) -> None:
        """
        Update chief complaint.
        """

        self.chief_complaint = complaint

    def update_history(
        self,
        history: str,
    ) -> None:
        """
        Update history of present illness.
        """

        self.history_of_present_illness = history

    @property
    def symptom_count(self) -> int:
        """
        Total number of symptoms.
        """

        return len(self.symptoms)