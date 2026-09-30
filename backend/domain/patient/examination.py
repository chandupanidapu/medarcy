"""
Medarcy Enterprise Clinical Intelligence Platform

Examination Domain Entity

Represents findings from the patient's physical examination.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from backend.domain.common.base import Entity


@dataclass(slots=True)
class Examination(Entity):
    """
    Represents the patient's physical examination.
    """

    general_appearance: Optional[str] = None

    vital_signs: Dict[str, str] = field(default_factory=dict)

    systemic_examination: Dict[str, str] = field(default_factory=dict)

    def update_general_appearance(
        self,
        appearance: str,
    ) -> None:
        """
        Update general appearance.
        """

        self.general_appearance = appearance.strip()

    def record_vital(
        self,
        name: str,
        value: str,
    ) -> None:
        """
        Record or update a vital sign.
        """

        self.vital_signs[name.strip()] = value.strip()

    def record_system(
        self,
        system: str,
        finding: str,
    ) -> None:
        """
        Record a systemic examination finding.
        """

        self.systemic_examination[
            system.strip()
        ] = finding.strip()

    @property
    def has_vitals(self) -> bool:
        return bool(self.vital_signs)

    @property
    def has_systemic_findings(self) -> bool:
        return bool(self.systemic_examination)