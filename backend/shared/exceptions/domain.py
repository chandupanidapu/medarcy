"""
Medarcy Enterprise Clinical Intelligence Platform

Domain Exceptions

Defines the base exception hierarchy for the Domain Layer.

Only domain/business exceptions belong here.
Framework-specific exceptions must remain outside the domain.
"""


class DomainError(Exception):
    """
    Base exception for all domain-level errors.
    """

    default_message = "A domain error occurred."

    def __init__(self, message: str | None = None):
        super().__init__(message or self.default_message)


class ValidationError(DomainError):
    """
    Raised when domain validation fails.
    """

    default_message = "Domain validation failed."


class BusinessRuleViolation(DomainError):
    """
    Raised when a business rule is violated.
    """

    default_message = "Business rule violated."


class EntityNotFound(DomainError):
    """
    Raised when a required domain entity cannot be found.
    """

    default_message = "Requested entity was not found."


class InvalidStateTransition(DomainError):
    """
    Raised when an entity attempts an invalid state transition.
    """

    default_message = "Invalid state transition."


class DuplicateEntity(DomainError):
    """
    Raised when attempting to create a duplicate entity.
    """

    default_message = "Duplicate entity."