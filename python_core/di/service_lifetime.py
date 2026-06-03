"""Service lifetime enum."""

from __future__ import annotations

from enum import StrEnum


class ServiceLifetime(StrEnum):
    """Dependency lifetime."""

    SINGLETON = "singleton"
    TRANSIENT = "transient"
    SCOPED = "scoped"
