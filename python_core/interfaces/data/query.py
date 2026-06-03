"""Query interface."""

from __future__ import annotations

from typing import Protocol


class Query(Protocol):
    """Marker interface for read-only requests."""
