"""
Medarcy Enterprise Clinical Intelligence Platform

Clinical Review Orchestrator

Coordinates the complete Clinical Review generation workflow.

Responsibilities
----------------
- Build prompt
- Execute provider
- Parse response
- Validate review
- Return ClinicalReview

The orchestrator contains orchestration only.
It never performs prompt engineering,
provider-specific logic,
response parsing,
or validation itself.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.domain.patient.patient_case import PatientCase
from backend.domain.review.clinical_review import ClinicalReview
from backend.intelligence.shared.models import ProviderConfig

from .parser import ReviewResponseParser
from .prompt_builder import ReviewPromptBuilder
from .providers import ReviewProviderRegistry
from .validator import ReviewValidator


@dataclass(slots=True)
class ReviewOrchestrator:
    """
    Coordinates Clinical Review generation.
    """

    prompt_builder: ReviewPromptBuilder

    provider_registry: ReviewProviderRegistry

    parser: ReviewResponseParser

    validator: ReviewValidator

    def generate_review(
        self,
        patient_case: PatientCase,
        config: ProviderConfig,
    ) -> ClinicalReview:
        """
        Generate a validated ClinicalReview.
        """

        prompt = self.prompt_builder.build(
            patient_case
        )

        response = self.provider_registry.generate(
            prompt=prompt,
            config=config,
        )

        review = self.parser.parse(
            response
        )

        self.validator.validate(
            review
        )

        return review