"""
Medarcy Enterprise Clinical Intelligence Platform

Patient Case Aggregate Root

The PatientCase is the Aggregate Root for the Patient Domain.

All patient-related information is composed through this object.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.domain.common.base import AggregateRoot

from .attachments import Attachments
from .audit import Audit
from .encounter import Encounter
from .examination import Examination
from .investigations import Investigations
from .medical_history import MedicalHistory
from .metadata import Metadata
from .notes import Notes
from .patient import Patient
from .presentation import ClinicalPresentation


@dataclass(slots=True)
class PatientCase(AggregateRoot):
    """
    Aggregate Root representing a complete patient case.
    """

    metadata: Metadata

    patient: Patient

    encounter: Encounter

    presentation: ClinicalPresentation

    medical_history: MedicalHistory

    examination: Examination

    investigations: Investigations

    attachments: Attachments = field(
        default_factory=Attachments
    )

    notes: Notes = field(
        default_factory=Notes
    )

    audit: Audit | None = None

    @property
    def case_id(self) -> str:
        """
        Returns the unique case identifier.
        """
        return self.metadata.id

    @property
    def is_complete(self) -> bool:
        """
        Determines whether the minimum required
        information exists for clinical review.
        """

        return (
            self.patient is not None
            and self.encounter is not None
            and self.presentation is not None
        )

    def add_note(
        self,
        content: str,
        author: str,
    ) -> None:
        """
        Add a clinician note.
        """

        self.notes.add_note(
            content=content,
            author=author,
        )

    def add_attachment(
        self,
        document: str,
    ) -> None:
        """
        Add a supporting document.
        """

        self.attachments.add_document(
            document
        )

    def ready_for_review(self) -> bool:
        """
        Determines whether the case is ready
        for AI clinical review.
        """

        return self.is_complete