"""Middleware context."""

from __future__ import annotations

from dataclasses import dataclass, field

from python_core.auth.identity import Identity


@dataclass
class MiddlewareContext:
    """Context passed through middleware."""

    request_id: str
    identity: Identity | None = None
    values: dict[str, object] = field(default_factory=dict)
