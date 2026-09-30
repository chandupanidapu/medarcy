"""
Medarcy Enterprise Clinical Intelligence Platform

Patient Domain Entity

Represents the patient information required for clinical reasoning.

This entity intentionally does NOT represent a complete Electronic
Medical Record (EMR) patient.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from backend.domain.common.base import Entity
from backend.domain.common.enums import Sex
from backend.domain.common.value_objects import (
    Age,
    Height,
    Weight,
)


@dataclass(slots=True)
class Patient(Entity):
    """
    Clinical patient entity.
    """

    patient_id: str

    age: Age

    sex: Sex

    weight: Optional[Weight] = None

    height: Optional[Height] = None

    def update_age(self, age: Age) -> None:
        """
        Update patient age.
        """
        self.age = age

    def update_weight(self, weight: Weight) -> None:
        """
        Update patient weight.
        """
        self.weight = weight

    def update_height(self, height: Height) -> None:
        """
        Update patient height.
        """
        self.height = height

    @property
    def has_complete_anthropometry(self) -> bool:
        """
        Returns True when both height and weight are available.
        """
        return (
            self.height is not None
            and self.weight is not None
        )