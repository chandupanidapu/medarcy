"""
Medarcy Enterprise Clinical Intelligence Platform

Base LLM Client

Defines the common interface and shared functionality for
all LLM clients.

Concrete clients should only implement vendor-specific
communication logic.
"""

from __future__ import annotations

from abc import ABC
from backend.infrastructure.llm.client_protocol import LLMClient, abstractmethod
from time import perf_counter

from backend.infrastructure.llm.models import (
    LLMRequest,
    LLMResponse,
)


class BaseClient(LLMClient, ABC):
    """
    Base class for all LLM clients.
    """

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Human-readable provider name.
        """

    @abstractmethod
    def execute(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Execute a request against the provider.

        Concrete implementations perform the actual API call.
        """

    def measure_latency(
        self,
        operation,
        *args,
        **kwargs,
    ):
        """
        Execute an operation while measuring latency.
        """

        start = perf_counter()

        response = operation(*args, **kwargs)

        elapsed = int(
            (perf_counter() - start) * 1000
        )

        return response, elapsed
