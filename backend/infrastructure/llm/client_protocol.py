"""
Medarcy Enterprise Clinical Intelligence Platform

LLM Client Protocol

Defines the contract implemented by all infrastructure
LLM clients.

Concrete clients communicate with external AI providers.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from backend.infrastructure.llm.models import (
    LLMRequest,
    LLMResponse,
)


@runtime_checkable
class LLMClient(Protocol):
    """
    Contract implemented by all LLM clients.
    """

    @property
    def provider_name(self) -> str:
        """
        Human-readable provider name.
        """
        ...

    def execute(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Execute a request against the provider.
        """
        ...
        