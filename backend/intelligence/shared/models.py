"""
Medarcy Enterprise Clinical Intelligence Platform

Shared Intelligence Models

Shared immutable models used across all intelligence engines.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True, slots=True)
class Prompt:
    """
    Prompt sent to an AI provider.
    """

    system_prompt: str

    user_prompt: str

    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ProviderConfig:
    """
    Runtime configuration for an AI provider.
    """

    provider_name: str

    model_name: str

    model_version: str

    temperature: float = 0.2

    max_tokens: int = 4096

    timeout_seconds: int = 120

    stream: bool = False


@dataclass(frozen=True, slots=True)
class TokenUsage:
    """
    Token accounting information.
    """

    prompt_tokens: int

    completion_tokens: int

    total_tokens: int


@dataclass(frozen=True, slots=True)
class ProviderResponse:
    """
    Raw response returned from an AI provider.
    """

    content: str

    config: ProviderConfig

    token_usage: TokenUsage | None = None

    latency_ms: int | None = None

    finish_reason: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass(frozen=True, slots=True)
class ModelMetadata:
    """
    Metadata describing the executing AI model.
    """

    provider: str

    model_name: str

    model_version: str