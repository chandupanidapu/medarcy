"""
Medarcy Enterprise Clinical Intelligence Platform

Shared Intelligence Protocols

Defines the contracts implemented by all intelligence
components.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from backend.domain.patient.patient_case import PatientCase
from backend.domain.review.clinical_review import ClinicalReview

from .models import (
    Prompt,
    ProviderConfig,
    ProviderResponse,
)


# ============================================================
# PROVIDER
# ============================================================

@runtime_checkable
class Provider(Protocol):
    """
    Contract implemented by every AI provider.

    Examples
    --------
    - ClaudeProvider
    - OpenAIProvider
    - GeminiProvider
    - LocalProvider
    """

    @property
    def name(self) -> str:
        """
        Human-readable provider name.
        """
        ...

    def generate(
        self,
        prompt: Prompt,
        config: ProviderConfig,
    ) -> ProviderResponse:
        """
        Generate a response from the AI model.
        """
        ...


# ============================================================
# PROMPT BUILDER
# ============================================================

@runtime_checkable
class PromptBuilder(Protocol):
    """
    Converts a PatientCase into a provider-ready prompt.
    """

    def build(
        self,
        patient_case: PatientCase,
    ) -> Prompt:
        """
        Build the complete prompt.
        """
        ...


# ============================================================
# RESPONSE PARSER
# ============================================================

@runtime_checkable
class ResponseParser(Protocol):
    """
    Converts a provider response into a domain object.
    """

    def parse(
        self,
        response: ProviderResponse,
    ) -> ClinicalReview:
        """
        Parse the provider response.
        """
        ...


# ============================================================
# RESPONSE VALIDATOR
# ============================================================

@runtime_checkable
class ResponseValidator(Protocol):
    """
    Validates generated Clinical Reviews.
    """

    def validate(
        self,
        review: ClinicalReview,
    ) -> None:
        """
        Raise an exception if validation fails.
        """
        ...