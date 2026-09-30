"""
Medarcy Enterprise Clinical Intelligence Platform

Domain Value Objects

Immutable value objects shared across the clinical domain.

Value objects are compared by value rather than identity.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.shared.exceptions.domain import ValidationError
from .base import ValueObject


# ============================================================
# AGE
# ============================================================

@dataclass(frozen=True, slots=True)
class Age(ValueObject):
    """
    Patient age in completed years.
    """

    years: int

    def __post_init__(self) -> None:
        if self.years < 0:
            raise ValidationError(
                "Age cannot be negative."
            )

        if self.years > 130:
            raise ValidationError(
                "Age exceeds supported range."
            )


# ============================================================
# WEIGHT
# ============================================================

@dataclass(frozen=True, slots=True)
class Weight(ValueObject):
    """
    Body weight in kilograms.
    """

    kilograms: float

    def __post_init__(self) -> None:
        if self.kilograms <= 0:
            raise ValidationError(
                "Weight must be greater than zero."
            )

        if self.kilograms > 500:
            raise ValidationError(
                "Weight exceeds supported range."
            )


# ============================================================
# HEIGHT
# ============================================================

@dataclass(frozen=True, slots=True)
class Height(ValueObject):
    """
    Height in centimeters.
    """

    centimeters: float

    def __post_init__(self) -> None:
        if self.centimeters <= 0:
            raise ValidationError(
                "Height must be greater than zero."
            )

        if self.centimeters > 300:
            raise ValidationError(
                "Height exceeds supported range."
            )


# ============================================================
# BODY MASS INDEX
# ============================================================

@dataclass(frozen=True, slots=True)
class BodyMassIndex(ValueObject):
    """
    Body Mass Index (kg/m²).
    """

    value: float

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValidationError(
                "BMI must be greater than zero."
            )

        if self.value > 100:
            raise ValidationError(
                "BMI exceeds supported range."
            )