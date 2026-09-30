"""
Medarcy Enterprise Clinical Intelligence Platform

Clinical Review Aggregate Root

The ClinicalReview aggregate is the single source of truth for one
complete clinical review. It composes domain value objects only and
intentionally does not store raw LLM responses or infrastructure data.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import ClassVar, Iterable

from backend.domain.common.base import AggregateRoot
from backend.domain.common.enums import EvidenceLevel, Priority, ReviewStatus
from backend.shared.exceptions.domain import (
    BusinessRuleViolation,
    InvalidStateTransition,
    ValidationError,
)

from .evidence import Confidence, Evidence, Limitation
from .metadata import ReviewMetadata
from .recommendations import (
    DifferentialDiagnosis,
    FollowUp,
    InvestigationPlan,
    ManagementPlan,
    MedicationPlan,
    PatientEducation,
    Procedures,
    Recommendation,
)
from .sections import (
    Assessment,
    ClinicalReasoning,
    ExecutiveSummary,
    ReviewSection,
)


@dataclass(slots=True, kw_only=True)
class ClinicalReview(AggregateRoot):
    """
    Aggregate Root representing a complete clinical review.

    The aggregate owns review lifecycle decisions and protects the
    consistency of review sections, recommendations, evidence,
    confidence, and limitations.
    """

    HIGH_CONFIDENCE_THRESHOLD: ClassVar[float] = 0.8
    metadata: ReviewMetadata

    executive_summary: ExecutiveSummary | None = None

    assessment: Assessment | None = None

    clinical_reasoning: ClinicalReasoning | None = None

    differential_diagnosis: DifferentialDiagnosis | None = None

    investigation_plan: InvestigationPlan | None = None

    management_plan: ManagementPlan | None = None

    medication_plan: MedicationPlan | None = None

    procedures: Procedures | None = None

    follow_up: FollowUp | None = None

    patient_education: PatientEducation | None = None

    evidence: list[Evidence] = field(default_factory=list)

    confidence: Confidence | None = None

    limitations: list[Limitation] = field(default_factory=list)

    def __post_init__(self) -> None:
        """
        Validate aggregate composition after dataclass construction.
        """

        if not isinstance(self.metadata, ReviewMetadata):
            raise ValidationError(
                "ClinicalReview requires ReviewMetadata."
            )

        self._validate_optional_components()
        self.evidence = self._validated_evidence_list(self.evidence)
        self.limitations = self._validated_limitation_list(
            self.limitations
        )

        if (
            self.metadata.status == ReviewStatus.COMPLETED
            and not self.is_complete()
        ):
            raise BusinessRuleViolation(
                "Completed clinical reviews must contain all required "
                "clinical content."
            )

    def is_complete(self) -> bool:
        """
        Return True when all required clinical review content is present.

        Completeness is based on clinical content rather than export or
        approval workflow state. A complete review may still require
        human review when confidence or evidence quality is insufficient.
        """

        return (
            self._section_is_complete(self.executive_summary)
            and self._section_is_complete(self.assessment)
            and self._section_is_complete(self.clinical_reasoning)
            and self._recommendation_is_complete(
                self.differential_diagnosis
            )
            and self._recommendation_is_complete(
                self.investigation_plan
            )
            and self._recommendation_is_complete(self.management_plan)
            and self._recommendation_is_complete(self.medication_plan)
            and self._recommendation_is_complete(self.procedures)
            and self._recommendation_is_complete(self.follow_up)
            and self._recommendation_is_complete(
                self.patient_education
            )
            and self._has_valid_evidence()
            and self._confidence_is_complete()
        )

    def can_be_exported(self) -> bool:
        """
        Return True when the review is ready for downstream export.

        Exportability means the generated review is completed and
        structurally complete. It does not imply that a clinician has
        accepted the recommendations.
        """

        return (
            self.metadata.status == ReviewStatus.COMPLETED
            and self.is_complete()
        )

    def is_high_confidence(self) -> bool:
        """
        Return True when the review confidence meets the high threshold.
        """

        return (
            self.confidence is not None
            and self.confidence.score >= self.HIGH_CONFIDENCE_THRESHOLD
        )

    def requires_human_review(self) -> bool:
        """
        Return True when clinical oversight should be required.

        A review is flagged when it is incomplete, failed, cancelled,
        not high-confidence, limited by known gaps, based on weak
        evidence, or attached to urgent/critical clinical priority.
        """

        if self.metadata.status in {
            ReviewStatus.FAILED,
            ReviewStatus.CANCELLED,
        }:
            return True

        if not self.is_complete():
            return True

        if not self.is_high_confidence():
            return True

        if self.limitations:
            return True

        if self.metadata.priority in {
            Priority.URGENT,
            Priority.CRITICAL,
        }:
            return True

        return any(
            item.level
            in {EvidenceLevel.LOW, EvidenceLevel.INSUFFICIENT}
            for item in self.evidence
        )

    def add_evidence(
        self,
        evidence: Evidence,
    ) -> None:
        """
        Add supporting evidence to an editable review version.

        Duplicate evidence value objects are ignored so the operation is
        idempotent for callers that retry the same domain command.
        """

        self._ensure_editable()
        self._validate_evidence(evidence)

        if evidence in self.evidence:
            return

        self.evidence.append(evidence)
        self._touch_metadata()

    def add_limitation(
        self,
        limitation: Limitation,
    ) -> None:
        """
        Add a known limitation to an editable review version.

        Duplicate limitations are ignored so callers can safely retry
        without creating repeated clinical warnings.
        """

        self._ensure_editable()
        self._validate_limitation(limitation)

        if limitation in self.limitations:
            return

        self.limitations.append(limitation)
        self._touch_metadata()

    def create_new_version(
        self,
        *,
        status: ReviewStatus = ReviewStatus.COMPLETED,
        model_name: str | None = None,
        model_version: str | None = None,
        generation_time_ms: int | None = None,
        executive_summary: ExecutiveSummary | None = None,
        assessment: Assessment | None = None,
        clinical_reasoning: ClinicalReasoning | None = None,
        differential_diagnosis: DifferentialDiagnosis | None = None,
        investigation_plan: InvestigationPlan | None = None,
        management_plan: ManagementPlan | None = None,
        medication_plan: MedicationPlan | None = None,
        procedures: Procedures | None = None,
        follow_up: FollowUp | None = None,
        patient_education: PatientEducation | None = None,
        evidence: Iterable[Evidence] | None = None,
        confidence: Confidence | None = None,
        limitations: Iterable[Limitation] | None = None,
    ) -> "ClinicalReview":
        """
        Create a new review version with updated metadata and content.

        The aggregate identity and metadata review_id are preserved while
        ReviewMetadata.version is advanced. Callers pass only the domain
        objects that changed; omitted components are copied from the
        current version.
        """

        if self.metadata.status == ReviewStatus.RUNNING:
            raise InvalidStateTransition(
                "Cannot create a new version while the current review "
                "version is running."
            )

        self._validate_version_metadata(
            status=status,
            model_name=model_name,
            model_version=model_version,
            generation_time_ms=generation_time_ms,
        )

        next_metadata = self.metadata.next_version(
            status=status,
            model_name=self._resolved_model_name(model_name),
            model_version=self._resolved_model_version(model_version),
            generation_time_ms=generation_time_ms,
        )

        next_review = ClinicalReview(
            id=self.id,
            metadata=next_metadata,
            executive_summary=(
                executive_summary
                if executive_summary is not None
                else self.executive_summary
            ),
            assessment=(
                assessment
                if assessment is not None
                else self.assessment
            ),
            clinical_reasoning=(
                clinical_reasoning
                if clinical_reasoning is not None
                else self.clinical_reasoning
            ),
            differential_diagnosis=(
                differential_diagnosis
                if differential_diagnosis is not None
                else self.differential_diagnosis
            ),
            investigation_plan=(
                investigation_plan
                if investigation_plan is not None
                else self.investigation_plan
            ),
            management_plan=(
                management_plan
                if management_plan is not None
                else self.management_plan
            ),
            medication_plan=(
                medication_plan
                if medication_plan is not None
                else self.medication_plan
            ),
            procedures=(
                procedures
                if procedures is not None
                else self.procedures
            ),
            follow_up=(
                follow_up
                if follow_up is not None
                else self.follow_up
            ),
            patient_education=(
                patient_education
                if patient_education is not None
                else self.patient_education
            ),
            evidence=(
                list(evidence)
                if evidence is not None
                else list(self.evidence)
            ),
            confidence=(
                confidence
                if confidence is not None
                else self.confidence
            ),
            limitations=(
                list(limitations)
                if limitations is not None
                else list(self.limitations)
            ),
        )

        if (
            next_review.metadata.status == ReviewStatus.COMPLETED
            and not next_review.is_complete()
        ):
            raise BusinessRuleViolation(
                "New completed review versions must contain all "
                "required clinical content."
            )

        return next_review

    def _validate_optional_components(self) -> None:
        """
        Validate optional single-value components when present.
        """

        self._validate_component(
            self.executive_summary,
            ExecutiveSummary,
            "executive_summary",
        )
        self._validate_component(
            self.assessment,
            Assessment,
            "assessment",
        )
        self._validate_component(
            self.clinical_reasoning,
            ClinicalReasoning,
            "clinical_reasoning",
        )
        self._validate_component(
            self.differential_diagnosis,
            DifferentialDiagnosis,
            "differential_diagnosis",
        )
        self._validate_component(
            self.investigation_plan,
            InvestigationPlan,
            "investigation_plan",
        )
        self._validate_component(
            self.management_plan,
            ManagementPlan,
            "management_plan",
        )
        self._validate_component(
            self.medication_plan,
            MedicationPlan,
            "medication_plan",
        )
        self._validate_component(
            self.procedures,
            Procedures,
            "procedures",
        )
        self._validate_component(
            self.follow_up,
            FollowUp,
            "follow_up",
        )
        self._validate_component(
            self.patient_education,
            PatientEducation,
            "patient_education",
        )
        self._validate_component(
            self.confidence,
            Confidence,
            "confidence",
        )

    def _validate_component(
        self,
        value: object | None,
        expected_type: type[object],
        field_name: str,
    ) -> None:
        """
        Validate an optional component's runtime type.
        """

        if value is not None and not isinstance(value, expected_type):
            raise ValidationError(
                f"ClinicalReview.{field_name} must be "
                f"{expected_type.__name__}."
            )

    def _validated_evidence_list(
        self,
        evidence_items: Iterable[Evidence],
    ) -> list[Evidence]:
        """
        Return a validated, duplicate-free evidence list.
        """

        if evidence_items is None:
            raise ValidationError(
                "ClinicalReview evidence collection cannot be None."
            )

        validated: list[Evidence] = []

        for item in evidence_items:
            self._validate_evidence(item)

            if item not in validated:
                validated.append(item)

        return validated

    def _validated_limitation_list(
        self,
        limitations: Iterable[Limitation],
    ) -> list[Limitation]:
        """
        Return a validated, duplicate-free limitation list.
        """

        if limitations is None:
            raise ValidationError(
                "ClinicalReview limitations collection cannot be None."
            )

        validated: list[Limitation] = []

        for item in limitations:
            self._validate_limitation(item)

            if item not in validated:
                validated.append(item)

        return validated

    def _validate_evidence(
        self,
        evidence: Evidence,
    ) -> None:
        """
        Validate a supporting evidence value object.
        """

        if not isinstance(evidence, Evidence):
            raise ValidationError(
                "ClinicalReview evidence must be Evidence."
            )

        if not evidence.summary.strip():
            raise ValidationError(
                "ClinicalReview evidence requires a summary."
            )

    def _validate_limitation(
        self,
        limitation: Limitation,
    ) -> None:
        """
        Validate a limitation value object.
        """

        if not isinstance(limitation, Limitation):
            raise ValidationError(
                "ClinicalReview limitation must be Limitation."
            )

        if not limitation.description.strip():
            raise ValidationError(
                "ClinicalReview limitation requires a description."
            )

    def _validate_version_metadata(
        self,
        *,
        status: ReviewStatus,
        model_name: str | None,
        model_version: str | None,
        generation_time_ms: int | None,
    ) -> None:
        """
        Validate metadata inputs for creating a review version.
        """

        if not isinstance(status, ReviewStatus):
            raise ValidationError(
                "ClinicalReview version status must be ReviewStatus."
            )

        if model_name is not None and not model_name.strip():
            raise ValidationError(
                "ClinicalReview model_name cannot be blank."
            )

        if model_version is not None and not model_version.strip():
            raise ValidationError(
                "ClinicalReview model_version cannot be blank."
            )

        if (
            generation_time_ms is not None
            and generation_time_ms < 0
        ):
            raise ValidationError(
                "ClinicalReview generation_time_ms cannot be negative."
            )

    def _ensure_editable(self) -> None:
        """
        Ensure this review version can be modified in place.
        """

        if self.metadata.status in {
            ReviewStatus.COMPLETED,
            ReviewStatus.FAILED,
            ReviewStatus.CANCELLED,
        }:
            raise InvalidStateTransition(
                "Cannot modify a terminal clinical review version. "
                "Create a new version instead."
            )

    def _touch_metadata(self) -> None:
        """
        Update metadata timestamp after aggregate mutation.
        """

        self.metadata = replace(
            self.metadata,
            updated_at=datetime.now(timezone.utc),
        )

    def _section_is_complete(
        self,
        section: ReviewSection | None,
    ) -> bool:
        """
        Return True when a review section has required text.
        """

        return (
            section is not None
            and bool(section.title.strip())
            and bool(section.content.strip())
        )

    def _recommendation_is_complete(
        self,
        recommendation: Recommendation | None,
    ) -> bool:
        """
        Return True when a recommendation has required text.
        """

        return (
            recommendation is not None
            and bool(recommendation.title.strip())
            and bool(recommendation.summary.strip())
        )

    def _has_valid_evidence(self) -> bool:
        """
        Return True when at least one valid evidence item exists.
        """

        return any(
            isinstance(item, Evidence)
            and bool(item.summary.strip())
            for item in self.evidence
        )

    def _confidence_is_complete(self) -> bool:
        """
        Return True when confidence has both score and rationale.
        """

        return (
            self.confidence is not None
            and bool(self.confidence.rationale.strip())
        )

    def _resolved_model_name(
        self,
        model_name: str | None,
    ) -> str:
        """
        Return the model name for the next version.
        """

        return (
            model_name.strip()
            if model_name is not None
            else self.metadata.model_name
        )

    def _resolved_model_version(
        self,
        model_version: str | None,
    ) -> str:
        """
        Return the model version for the next version.
        """

        return (
            model_version.strip()
            if model_version is not None
            else self.metadata.model_version
        )
