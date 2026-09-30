"""
Medarcy Enterprise Clinical Intelligence Platform

Claude Provider

Infrastructure adapter connecting the Intelligence Layer
to Anthropic Claude.

Responsibilities
----------------
- Convert Prompt -> LLMRequest
- Invoke ClaudeClient
- Convert LLMResponse -> ProviderResponse

This class never performs HTTP requests directly.
"""

from __future__ import annotations

from dataclasses import dataclass

from backend.infrastructure.llm.client_protocol import LLMClient
from backend.infrastructure.llm.base import BaseProvider
from backend.infrastructure.llm.models import (
    LLMRequest,
)
from backend.intelligence.shared.models import (
    Prompt,
    ProviderConfig,
    ProviderResponse,
    TokenUsage,
)


@dataclass(slots=True)
class ClaudeProvider(BaseProvider):
    """
    Anthropic Claude implementation of the Provider protocol.
    """

    client: LLMClient

    @property
    def name(self) -> str:
        return "claude"

    def generate(
        self,
        prompt: Prompt,
        config: ProviderConfig,
    ) -> ProviderResponse:
        """
        Generate a ProviderResponse using Claude.
        """

        request = LLMRequest(
            system_prompt=prompt.system_prompt,
            user_prompt=prompt.user_prompt,
            model=config.model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            stream=config.stream,
            metadata=prompt.metadata,
        )

        llm_response = self.client.execute(request)

        return ProviderResponse(
            content=llm_response.content,
            config=config,
            token_usage=TokenUsage(
                prompt_tokens=llm_response.prompt_tokens,
                completion_tokens=llm_response.completion_tokens,
                total_tokens=llm_response.total_tokens,
            ),
            latency_ms=llm_response.latency_ms,
            finish_reason=llm_response.finish_reason,
            metadata=llm_response.metadata,
        )