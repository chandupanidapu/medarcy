"""
Medarcy Enterprise Clinical Intelligence Platform

LLM Infrastructure Configuration

Defines deployment configuration for LLM providers.

These settings are infrastructure concerns and must never
be exposed to the Domain or Intelligence layers.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LLMSettings:
    """
    Infrastructure configuration for an LLM provider.
    """

    provider_name: str

    api_key: str

    model: str

    base_url: str | None = None

    timeout_seconds: int = 120

    max_retries: int = 3

    organization: str | None = None

    stream: bool = False