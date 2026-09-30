"""
Medarcy Enterprise Clinical Intelligence Platform

Clinical Review Parser

Transforms a normalized ProviderResponse into a
ClinicalReview aggregate.

This parser is provider-independent.
"""

from __future__ import annotations

from backend.domain.review.clinical_review import ClinicalReview
from backend.domain.review.evidence import (
    Confidence,
    Evidence,
)
from backend.domain.review.metadata import ReviewMetadata
from backend.domain.review.recommendations import (
    DifferentialDiagnosis,
    FollowUp,
    InvestigationPlan,
    ManagementPlan,
    MedicationPlan,
    PatientEducation,
    Procedures,
)
from backend.domain.review.sections import (
    Assessment,
    ClinicalReasoning,
    ExecutiveSummary,
)
from backend.intelligence.shared.exceptions import (
    ResponseParsingError,
)
from backend.intelligence.shared.models import ProviderResponse
from backend.intelligence.shared.utils import parse_json


class ReviewResponseParser:
    """
    Converts ProviderResponse into ClinicalReview.
    """

    def parse(
        self,
        response: ProviderResponse,
    ) -> ClinicalReview:
        """
        Parse a provider response into a ClinicalReview.
        """

        data = parse_json(response.content)

        try:
            metadata = ReviewMetadata(
                review_id=data["review_id"],
                model_name=response.config.model_name,
                model_version=response.config.model_version,
            )

            review = ClinicalReview(
                metadata=metadata,
                executive_summary=ExecutiveSummary(
                    title="Executive Summary",
                    content=data["executive_summary"],
                ),
                assessment=Assessment(
                    title="Assessment",
                    content=data["assessment"],
                ),
                clinical_reasoning=ClinicalReasoning(
                    title="Clinical Reasoning",
                    content=data["clinical_reasoning"],
                ),
                differential_diagnosis=DifferentialDiagnosis(
                    title="Differential Diagnosis",
                    summary="Differential diagnoses",
                    recommendations=data.get(
                        "differential_diagnosis",
                        [],
                    ),
                ),
                investigation_plan=InvestigationPlan(
                    title="Investigation Plan",
                    summary="Recommended investigations",
                    recommendations=data.get(
                        "investigation_plan",
                        [],
                    ),
                ),
                management_plan=ManagementPlan(
                    title="Management Plan",
                    summary="Recommended management",
                    recommendations=data.get(
                        "management_plan",
                        [],
                    ),
                ),
                medication_plan=MedicationPlan(
                    title="Medication Plan",
                    summary="Medication recommendations",
                    recommendations=data.get(
                        "medication_plan",
                        [],
                    ),
                ),
                procedures=Procedures(
                    title="Procedures",
                    summary="Recommended procedures",
                    recommendations=data.get(
                        "procedures",
                        [],
                    ),
                ),
                follow_up=FollowUp(
                    title="Follow-up",
                    summary="Follow-up recommendations",
                    recommendations=data.get(
                        "follow_up",
                        [],
                    ),
                ),
                patient_education=PatientEducation(
                    title="Patient Education",
                    summary="Patient counselling",
                    recommendations=data.get(
                        "patient_education",
                        [],
                    ),
                ),
                evidence=[
                    Evidence(
                        summary=item["summary"],
                        level=item["level"],
                    )
                    for item in data.get("evidence", [])
                ],
                confidence=Confidence(
                    score=data["confidence"]["score"],
                    rationale=data["confidence"]["rationale"],
                ),
                limitations=data.get(
                    "limitations",
                    [],
                ),
            )

        except KeyError as exc:
            raise ResponseParsingError(
                f"Missing required field: {exc.args[0]}"
            ) from exc

        return review