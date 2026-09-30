"""
Medarcy Enterprise Clinical Intelligence Platform

Shared Intelligence Utilities

Pure utility functions used throughout the Intelligence Layer.

Utilities in this module must:

- Be deterministic.
- Have no side effects.
- Be framework independent.
- Contain no provider-specific logic.
"""

from __future__ import annotations

import json
import time
import uuid
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from .exceptions import InvalidResponseFormatError

F = TypeVar("F", bound=Callable[..., Any])


# ============================================================
# IDENTIFIERS
# ============================================================

def generate_id(prefix: str) -> str:
    """
    Generate a readable unique identifier.

    Example
    -------
    review_3b8b0d7e5c1e4d8c
    """

    return f"{prefix}_{uuid.uuid4().hex}"


# ============================================================
# JSON
# ============================================================

def parse_json(content: str) -> dict[str, Any]:
    """
    Parse a JSON string.

    Raises
    ------
    InvalidResponseFormatError
        If the content is not valid JSON.
    """

    try:
        data = json.loads(content)

    except json.JSONDecodeError as exc:
        raise InvalidResponseFormatError(
            "Provider returned invalid JSON."
        ) from exc

    if not isinstance(data, dict):
        raise InvalidResponseFormatError(
            "Expected a JSON object."
        )

    return data


# ============================================================
# STRINGS
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize whitespace.

    Removes duplicate whitespace while preserving
    paragraph boundaries.
    """

    return "\n".join(
        " ".join(line.split())
        for line in text.strip().splitlines()
    )


# ============================================================
# TIMING
# ============================================================

def timed(func: F) -> F:
    """
    Decorator that measures execution time.

    The wrapped function returns:

    (
        original_result,
        elapsed_time_ms,
    )
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed = int(
            (time.perf_counter() - start) * 1000
        )

        return result, elapsed

    return wrapper  # type: ignore[return-value]


# ============================================================
# COLLECTIONS
# ============================================================

def remove_duplicates(values: list[str]) -> list[str]:
    """
    Remove duplicates while preserving order.
    """

    return list(dict.fromkeys(values))