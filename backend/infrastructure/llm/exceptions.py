"""
Medarcy Enterprise Clinical Intelligence Platform

LLM Infrastructure Exceptions

Exceptions raised by the Infrastructure Layer while
communicating with external AI providers.
"""

from __future__ import annotations


class LLMInfrastructureError(Exception):
    """
    Base exception for LLM infrastructure.
    """


class ProviderNotRegisteredError(LLMInfrastructureError):
    """
    Raised when a requested provider has not been registered.
    """


class APIConnectionError(LLMInfrastructureError):
    """
    Raised when a connection to an external provider fails.
    """


class AuthenticationError(LLMInfrastructureError):
    """
    Raised when provider authentication fails.
    """


class RequestTimeoutError(LLMInfrastructureError):
    """
    Raised when an API request exceeds the configured timeout.
    """


class RateLimitExceededError(LLMInfrastructureError):
    """
    Raised when a provider rate limit is exceeded.
    """


class InvalidAPIResponseError(LLMInfrastructureError):
    """
    Raised when an external provider returns an invalid response.
    """


class ConfigurationError(LLMInfrastructureError):
    """
    Raised when infrastructure configuration is invalid.
    """