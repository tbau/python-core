"""API key credentials."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ApiKeyCredentials:
    """API key credentials."""

    key: str
    key_id: str | None = None
