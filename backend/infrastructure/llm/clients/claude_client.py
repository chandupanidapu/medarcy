"""
Medarcy Enterprise Clinical Intelligence Platform

Claude Client

Infrastructure client responsible for communicating with
Anthropic Claude.

Only vendor-specific communication belongs here.
"""

from __future__ import annotations

from backend.infrastructure.llm.clients.base_client import BaseClient
from backend.infrastructure.llm.models import (
    LLMRequest,
    LLMResponse,
)


class ClaudeClient(BaseClient):
    """
    Claude client implementation.

    The actual Anthropic SDK integration will be added
    during provider integration.
    """

    @property
    def provider_name(self) -> str:
        return "claude"

    def execute(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        """
        Execute a request against Claude.

        This method will be implemented when integrating
        the Anthropic SDK.
        """

        raise NotImplementedError(
            "Claude client integration has not yet been implemented."
        )