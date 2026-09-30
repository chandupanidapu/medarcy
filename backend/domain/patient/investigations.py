"""
Medarcy Enterprise Clinical Intelligence Platform

Investigations Domain Entity

Represents diagnostic investigations performed during
the patient's clinical evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from backend.domain.common.base import Entity


@dataclass(slots=True)
class Investigations(Entity):
    """
    Represents investigations relevant to the patient case.
    """

    laboratory: List[str] = field(default_factory=list)

    imaging: List[str] = field(default_factory=list)

    ecg: List[str] = field(default_factory=list)

    microbiology: List[str] = field(default_factory=list)

    pathology: List[str] = field(default_factory=list)

    other: List[str] = field(default_factory=list)

    def add_laboratory(self, result: str) -> None:
        result = result.strip()
        if result and result not in self.laboratory:
            self.laboratory.append(result)

    def add_imaging(self, study: str) -> None:
        study = study.strip()
        if study and study not in self.imaging:
            self.imaging.append(study)

    def add_ecg(self, finding: str) -> None:
        finding = finding.strip()
        if finding and finding not in self.ecg:
            self.ecg.append(finding)

    def add_microbiology(self, result: str) -> None:
        result = result.strip()
        if result and result not in self.microbiology:
            self.microbiology.append(result)

    def add_pathology(self, result: str) -> None:
        result = result.strip()
        if result and result not in self.pathology:
            self.pathology.append(result)

    def add_other(self, investigation: str) -> None:
        investigation = investigation.strip()
        if investigation and investigation not in self.other:
            self.other.append(investigation)

    @property
    def has_investigations(self) -> bool:
        return any((
            self.laboratory,
            self.imaging,
            self.ecg,
            self.microbiology,
            self.pathology,
            self.other,
        ))