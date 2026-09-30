"""
Medarcy Enterprise Clinical Intelligence Platform

Shared Intelligence Exceptions

Exception hierarchy for the Intelligence Layer.
"""

from __future__ import annotations


class IntelligenceError(Exception):
    """
    Base exception for all Intelligence Layer errors.
    """


# ============================================================
# PROVIDER
# ============================================================

class ProviderError(IntelligenceError):
    """
    Base class for provider-related failures.
    """


class ProviderUnavailableError(ProviderError):
    """
    Raised when the configured provider cannot be reached.
    """


class ProviderTimeoutError(ProviderError):
    """
    Raised when a provider request exceeds the configured timeout.
    """


class AuthenticationError(ProviderError):
    """
    Raised when provider authentication fails.
    """


class RateLimitError(ProviderError):
    """
    Raised when the provider enforces a rate limit.
    """


class ModelNotFoundError(ProviderError):
    """
    Raised when the requested model does not exist.
    """


# ============================================================
# PROMPT
# ============================================================

class PromptGenerationError(IntelligenceError):
    """
    Raised when prompt generation fails.
    """


# ============================================================
# PARSER
# ============================================================

class ResponseParsingError(IntelligenceError):
    """
    Raised when a provider response cannot be parsed.
    """


class InvalidResponseFormatError(ResponseParsingError):
    """
    Raised when the provider returns an invalid response format.
    """


# ============================================================
# VALIDATION
# ============================================================

class ResponseValidationError(IntelligenceError):
    """
    Raised when a parsed ClinicalReview fails validation.
    """


class ConfidenceThresholdError(ResponseValidationError):
    """
    Raised when the review confidence is below the accepted threshold.
    """


# ============================================================
# ORCHESTRATION
# ============================================================

class OrchestrationError(IntelligenceError):
    """
    Raised when orchestration of the intelligence workflow fails.
    """


class RetryLimitExceededError(OrchestrationError):
    """
    Raised when all retry attempts have been exhausted.
    """