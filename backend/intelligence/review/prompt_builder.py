"""
Medarcy Enterprise Clinical Intelligence Platform

Clinical Review Prompt Builder

Transforms a PatientCase domain object into a provider-independent
Prompt used by the Intelligence Layer.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from backend.domain.patient.patient_case import PatientCase
from backend.intelligence.shared.models import Prompt
from backend.intelligence.shared.serializers import PatientCaseSerializer

from .templates import (
    OUTPUT_REQUIREMENTS,
    REVIEW_INSTRUCTIONS,
    SYSTEM_PROMPT,
)


class ReviewPromptBuilder:
    _serializer = PatientCaseSerializer()
    """
    Builds prompts for Clinical Review generation.

    This class is responsible only for assembling prompts.
    It does not communicate with AI providers.
    """

    def build(
        self,
        patient_case: PatientCase,
    ) -> Prompt:
        """
        Build a provider-independent prompt.

        Parameters
        ----------
        patient_case:
            Patient case to be reviewed.

        Returns
        -------
        Prompt
            Structured prompt ready for any AI provider.
        """

        case_json = self._serializer.to_json(
    patient_case
)

        user_prompt = (
            f"{REVIEW_INSTRUCTIONS}\n\n"
            "Patient Case\n"
            "============\n\n"
            f"{case_json}\n\n"
            f"{OUTPUT_REQUIREMENTS}"
        )

        return Prompt(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
            metadata={
                "case_id": patient_case.case_id,
                "review_type": "clinical_review",
            },
        )
