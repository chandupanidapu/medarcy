"""
Medarcy Enterprise Clinical Intelligence Platform

Notes Domain Entity

Represents clinician-authored notes associated
with a patient case.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List

from backend.domain.common.base import Entity


@dataclass(slots=True)
class ClinicalNote(Entity):
    """
    Represents a single clinical note.
    """

    content: str

    author: str

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass(slots=True)
class Notes(Entity):
    """
    Collection of clinician-authored notes.
    """

    notes: List[ClinicalNote] = field(default_factory=list)

    def add_note(
        self,
        content: str,
        author: str,
    ) -> None:
        """
        Add a new clinical note.
        """

        content = content.strip()

        if not content:
            return

        self.notes.append(
            ClinicalNote(
                content=content,
                author=author,
            )
        )

    @property
    def total_notes(self) -> int:
        """
        Total number of notes.
        """

        return len(self.notes)

    @property
    def is_empty(self) -> bool:
        """
        Returns True when no notes exist.
        """

        return len(self.notes) == 0