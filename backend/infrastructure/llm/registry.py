"""
Medarcy Enterprise Clinical Intelligence Platform

LLM Provider Registry

Central registry responsible for managing AI provider
implementations.

This registry is the single entry point for resolving
providers throughout the application.
"""

from __future__ import annotations

from backend.infrastructure.llm.exceptions import ProviderNotRegisteredError

from typing import Dict

from backend.intelligence.shared.protocols import Provider


class ProviderRegistry:
    """
    Registry of available AI providers.
    """

    def __init__(self) -> None:
        self._providers: Dict[str, Provider] = {}

    def register(
        self,
        provider: Provider,
    ) -> None:
        """
        Register a provider instance.
        """

        self._providers[
            provider.name.lower()
        ] = provider

    def get(
        self,
        provider_name: str,
    ) -> Provider:
        """
        Resolve a provider.

        Raises
        ------
        KeyError
            If the provider has not been registered.
        """

        provider = self._providers.get(
            provider_name.lower()
        )

        if provider is None:
            raise ProviderNotRegisteredError(
                f"Unknown provider: {provider_name}"
            )

        return provider

    def has(
        self,
        provider_name: str,
    ) -> bool:
        """
        Determine whether a provider is registered.
        """

        return (
            provider_name.lower()
            in self._providers
        )

    def registered(self) -> list[str]:
        """
        Return registered provider names.
        """

        return sorted(
            self._providers.keys()
        )
