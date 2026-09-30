"""
Medarcy Enterprise Clinical Intelligence Platform

Shared Intelligence Serializers

Responsible for converting Domain objects into stable,
provider-independent representations suitable for AI
processing.

The serialization layer isolates prompt generation from
the internal structure of domain models.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any

from backend.domain.patient.patient_case import PatientCase


class DomainSerializer:
    """
    Base serializer for Domain objects.
    """

    def to_dict(self, obj: Any) -> dict[str, Any]:
        """
        Convert a dataclass-based domain object into a dictionary.
        """

        return asdict(obj)

    def to_json(
        self,
        obj: Any,
        *,
        indent: int = 2,
    ) -> str:
        """
        Convert a domain object into formatted JSON.
        """

        return json.dumps(
            self.to_dict(obj),
            indent=indent,
            ensure_ascii=False,
            default=str,
        )


class PatientCaseSerializer(DomainSerializer):
    """
    Serializes PatientCase objects for Clinical Intelligence.

    Future responsibilities include:

    - PHI masking
    - Field filtering
    - Prompt versioning
    - Specialty-specific serialization
    - Localization
    """

    def to_dict(
        self,
        patient_case: PatientCase,
    ) -> dict[str, Any]:
        """
        Serialize a PatientCase into a stable dictionary.
        """

        return super().to_dict(patient_case)