"""
Medarcy Enterprise Clinical Intelligence Platform

LLM Infrastructure Models

Infrastructure-only models used by LLM clients.

These models must never be used directly by the
Domain or Application layers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ============================================================
# REQUEST
# ============================================================

@dataclass(frozen=True, slots=True)
class LLMRequest:
    """
    Infrastructure request sent to an external provider.
    """

    system_prompt: str

    user_prompt: str

    model: str

    temperature: float

    max_tokens: int

    stream: bool = False

    metadata: dict[str, Any] = field(default_factory=dict)


# ============================================================
# RESPONSE
# ============================================================

@dataclass(frozen=True, slots=True)
class LLMResponse:
    """
    Raw infrastructure response returned by an LLM.
    """

    content: str

    prompt_tokens: int

    completion_tokens: int

    finish_reason: str | None = None

    latency_ms: int | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def total_tokens(self) -> int:
        """
        Total token consumption.
        """

        return (
            self.prompt_tokens
            + self.completion_tokens
        )