"""
Medarcy Enterprise Clinical Intelligence Platform

Case Review Application Service

This module contains the application-layer orchestration for the
Review Patient Case use case. The service coordinates domain objects
and application ports only: it does not import web frameworks,
database adapters, provider SDKs, prompt builders, or parsers.

The concrete infrastructure responsible for persistence, model
execution, prompt construction, and response parsing must live behind
the protocols declared here and be supplied by a composition root.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from backend.application.case_review.commands import (
    ApproveClinicalReviewCommand,
    CreateClinicalReviewCommand,
    RegenerateClinicalReviewCommand,
)
from backend.application.case_review.queries import (
    GetClinicalReviewQuery,
    GetLatestClinicalReviewQuery,
    ListClinicalReviewsQuery,
)
from backend.domain.common.enums import ReviewStatus
from backend.domain.patient.patient_case import PatientCase
from backend.domain.review.clinical_review import ClinicalReview
from backend.shared.exceptions.domain import (
    BusinessRuleViolation,
    EntityNotFound,
    InvalidStateTransition,
    ValidationError,
)


class ClinicalReviewRepository(Protocol):
    """
    Persistence port for Clinical Review aggregates.

    Implementations may use SQL databases, document stores, files, or
    remote services, but those details are hidden from the application
    layer. Every method accepts application/domain values and returns
    domain objects only.
    """

    def save(
        self,
        review: ClinicalReview,
    ) -> None:
        """
        Persist a ClinicalReview aggregate.
        """

    def get_by_id(
        self,
        review_id: str,
    ) -> ClinicalReview | None:
        """
        Return a ClinicalReview by review identifier, if one exists.
        """

    def get_latest_by_patient_case_id(
        self,
        patient_case_id: str,
    ) -> ClinicalReview | None:
        """
        Return the latest ClinicalReview for a patient case, if present.
        """

    def list_reviews(
        self,
        *,
        patient_case_id: str | None = None,
        status: ReviewStatus | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> Sequence[ClinicalReview]:
        """
        Return ClinicalReview aggregates matching the supplied filters.
        """


class ClinicalReviewGenerator(Protocol):
    """
    Generation port for Clinical Review aggregates.

    This is the application-layer boundary to any clinical intelligence
    implementation. A concrete adapter may call an LLM, a rules engine,
    or another clinical reasoning service, but it must return a fully
    formed ClinicalReview domain object rather than raw provider output,
    markdown, or dictionaries.
    """

    def create_review(
        self,
        patient_case: PatientCase,
        *,
        model_name: str,
        model_version: str,
    ) -> ClinicalReview:
        """
        Generate a new ClinicalReview for a patient case.
        """

    def regenerate_review(
        self,
        patient_case: PatientCase,
        current_review: ClinicalReview,
        *,
        model_name: str,
        model_version: str,
    ) -> ClinicalReview:
        """
        Generate a new version of an existing ClinicalReview.
        """


@runtime_checkable
class ClinicalReviewApprovalWorkflow(Protocol):
    """
    Approval port for completed Clinical Review aggregates.

    Approval may later become a richer domain workflow. Until then, the
    application service treats it as an injected policy/workflow port so
    approval audit, status mapping, and persistence behavior stay out of
    this orchestration module.
    """

    def approve_review(
        self,
        review: ClinicalReview,
        *,
        approved_by: str,
    ) -> ClinicalReview:
        """
        Approve and return a ClinicalReview domain object.
        """


class ReviewService:
    """
    Application service for the Review Patient Case use case.

    ReviewService is intentionally thin. It validates command/query
    messages, coordinates ports, enforces that collaborators return
    ClinicalReview domain objects, and raises domain/application
    exceptions when required data cannot be found or a workflow cannot
    proceed.

    The service does not know how reviews are persisted or generated.
    It depends only on protocols, which keeps FastAPI, SQLAlchemy, LLM
    SDKs, prompt construction, and output parsing outside the
    application layer.
    """

    def __init__(
        self,
        review_repository: ClinicalReviewRepository,
        review_generator: ClinicalReviewGenerator,
        review_approval_workflow: ClinicalReviewApprovalWorkflow | None = None,
    ) -> None:
        """
        Create a ReviewService with injected application ports.
        """

        self._review_repository = review_repository
        self._review_generator = review_generator
        self._review_approval_workflow = review_approval_workflow

    def create_review(
        self,
        command: CreateClinicalReviewCommand,
    ) -> ClinicalReview:
        """
        Generate and persist a new ClinicalReview for a patient case.

        The write operation accepts a command object and returns the
        generated ClinicalReview aggregate. Provider responses and
        serialization concerns remain behind the generator port.
        """

        if not isinstance(command, CreateClinicalReviewCommand):
            raise ValidationError("create_review requires CreateClinicalReviewCommand.")

        self._ensure_patient_case_ready(command.patient_case)
        self._ensure_not_blank(command.model_name, "model_name")
        self._ensure_not_blank(command.model_version, "model_version")

        review = self._review_generator.create_review(
            command.patient_case,
            model_name=command.model_name.strip(),
            model_version=command.model_version.strip(),
        )
        review = self._ensure_review(
            review,
            "ClinicalReviewGenerator.create_review",
        )

        self._review_repository.save(review)

        return review

    def regenerate_review(
        self,
        command: RegenerateClinicalReviewCommand,
    ) -> ClinicalReview:
        """
        Generate and persist a new version of an existing review.

        The existing ClinicalReview is loaded through the repository
        port and supplied to the generator port so implementation
        details for re-generation stay outside the application service.
        """

        if not isinstance(command, RegenerateClinicalReviewCommand):
            raise ValidationError(
                "regenerate_review requires " "RegenerateClinicalReviewCommand."
            )

        self._ensure_patient_case_ready(command.patient_case)
        self._ensure_not_blank(command.review_id, "review_id")
        self._ensure_not_blank(command.model_name, "model_name")
        self._ensure_not_blank(command.model_version, "model_version")

        current_review = self._get_existing_review(command.review_id)
        regenerated_review = self._review_generator.regenerate_review(
            command.patient_case,
            current_review,
            model_name=command.model_name.strip(),
            model_version=command.model_version.strip(),
        )
        regenerated_review = self._ensure_review(
            regenerated_review,
            "ClinicalReviewGenerator.regenerate_review",
        )

        self._ensure_same_review_identity(
            current_review,
            regenerated_review,
        )
        self._review_repository.save(regenerated_review)

        return regenerated_review

    def approve_review(
        self,
        command: ApproveClinicalReviewCommand,
    ) -> ClinicalReview:
        """
        Approve an existing completed ClinicalReview.

        Approval is delegated to an injected approval workflow when one
        is configured. If the repository itself also implements the
        approval workflow protocol, the service can use that adapter.
        Without an approval workflow, the service verifies that the
        review is exportable, persists it unchanged, and returns the
        domain object.
        """

        if not isinstance(command, ApproveClinicalReviewCommand):
            raise ValidationError(
                "approve_review requires ApproveClinicalReviewCommand."
            )

        self._ensure_not_blank(command.review_id, "review_id")
        self._ensure_not_blank(command.approved_by, "approved_by")

        review = self._get_existing_review(command.review_id)
        approval_workflow = self._resolve_approval_workflow()

        if approval_workflow is None:
            self._ensure_review_can_be_approved(review)
            self._review_repository.save(review)
            return review

        approved_review = approval_workflow.approve_review(
            review,
            approved_by=command.approved_by.strip(),
        )
        approved_review = self._ensure_review(
            approved_review,
            "ClinicalReviewApprovalWorkflow.approve_review",
        )
        self._ensure_same_review_identity(review, approved_review)

        return approved_review

    def get_review(
        self,
        query: GetClinicalReviewQuery,
    ) -> ClinicalReview:
        """
        Retrieve one ClinicalReview by review identifier.
        """

        if not isinstance(query, GetClinicalReviewQuery):
            raise ValidationError("get_review requires GetClinicalReviewQuery.")

        self._ensure_not_blank(query.review_id, "review_id")

        return self._get_existing_review(query.review_id)

    def get_latest_review(
        self,
        query: GetLatestClinicalReviewQuery,
    ) -> ClinicalReview:
        """
        Retrieve the latest ClinicalReview for a patient case.
        """

        if not isinstance(query, GetLatestClinicalReviewQuery):
            raise ValidationError(
                "get_latest_review requires " "GetLatestClinicalReviewQuery."
            )

        self._ensure_not_blank(query.patient_case_id, "patient_case_id")

        review = self._review_repository.get_latest_by_patient_case_id(
            query.patient_case_id.strip()
        )

        if review is None:
            raise EntityNotFound(
                "ClinicalReview was not found for patient case "
                f"{query.patient_case_id!r}."
            )

        return self._ensure_review(
            review,
            "ClinicalReviewRepository.get_latest_by_patient_case_id",
        )

    def list_reviews(
        self,
        query: ListClinicalReviewsQuery,
    ) -> list[ClinicalReview]:
        """
        List ClinicalReview aggregates matching a read query.
        """

        if not isinstance(query, ListClinicalReviewsQuery):
            raise ValidationError("list_reviews requires ListClinicalReviewsQuery.")

        self._ensure_valid_pagination(query)

        reviews = self._review_repository.list_reviews(
            patient_case_id=self._optional_stripped(query.patient_case_id),
            status=query.status,
            limit=query.limit,
            offset=query.offset,
        )

        if isinstance(reviews, str) or not isinstance(
            reviews,
            Sequence,
        ):
            raise ValidationError(
                "ClinicalReviewRepository.list_reviews must return a "
                "sequence of ClinicalReview domain objects."
            )

        return [
            self._ensure_review(
                review,
                "ClinicalReviewRepository.list_reviews",
            )
            for review in reviews
        ]

    def _get_existing_review(
        self,
        review_id: str,
    ) -> ClinicalReview:
        """
        Load a ClinicalReview or raise EntityNotFound.
        """

        review = self._review_repository.get_by_id(review_id.strip())

        if review is None:
            raise EntityNotFound(f"ClinicalReview {review_id!r} was not found.")

        return self._ensure_review(
            review,
            "ClinicalReviewRepository.get_by_id",
        )

    def _resolve_approval_workflow(
        self,
    ) -> ClinicalReviewApprovalWorkflow | None:
        """
        Return the configured approval workflow, if available.
        """

        if self._review_approval_workflow is not None:
            return self._review_approval_workflow

        if isinstance(
            self._review_repository,
            ClinicalReviewApprovalWorkflow,
        ):
            return self._review_repository

        return None

    def _ensure_patient_case_ready(
        self,
        patient_case: PatientCase,
    ) -> None:
        """
        Ensure a PatientCase can enter the review workflow.
        """

        if not isinstance(patient_case, PatientCase):
            raise ValidationError(
                "Review commands require a PatientCase domain object."
            )

        if not patient_case.ready_for_review():
            raise BusinessRuleViolation("PatientCase is not ready for clinical review.")

    def _ensure_review_can_be_approved(
        self,
        review: ClinicalReview,
    ) -> None:
        """
        Ensure the review is in a completed, exportable state.
        """

        if not review.can_be_exported():
            raise InvalidStateTransition(
                "Only completed clinical reviews can be approved."
            )

    def _ensure_same_review_identity(
        self,
        current_review: ClinicalReview,
        next_review: ClinicalReview,
    ) -> None:
        """
        Ensure workflow ports do not replace the aggregate identity.
        """

        if current_review.id != next_review.id:
            raise BusinessRuleViolation(
                "Review workflow returned a different aggregate id."
            )

        if current_review.metadata.review_id != next_review.metadata.review_id:
            raise BusinessRuleViolation(
                "Review workflow returned a different review id."
            )

    def _ensure_review(
        self,
        review: object,
        source: str,
    ) -> ClinicalReview:
        """
        Ensure a collaborator returned a ClinicalReview domain object.
        """

        if not isinstance(review, ClinicalReview):
            raise ValidationError(
                f"{source} must return a ClinicalReview domain object."
            )

        return review

    def _ensure_valid_pagination(
        self,
        query: ListClinicalReviewsQuery,
    ) -> None:
        """
        Validate pagination values before passing them to a repository.
        """

        if query.limit is not None and query.limit < 0:
            raise ValidationError("limit cannot be negative.")

        if query.offset < 0:
            raise ValidationError("offset cannot be negative.")

    def _ensure_not_blank(
        self,
        value: str,
        field_name: str,
    ) -> None:
        """
        Ensure a required string field contains non-whitespace text.
        """

        if not isinstance(value, str) or not value.strip():
            raise ValidationError(f"{field_name} cannot be blank.")

    def _optional_stripped(
        self,
        value: str | None,
    ) -> str | None:
        """
        Return a stripped optional string, preserving None.
        """

        if value is None:
            return None

        stripped = value.strip()

        return stripped or None
