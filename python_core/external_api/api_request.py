"""External API request model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from python_core.reliability.idempotency_key import IdempotencyKey


@dataclass(frozen=True)
class ApiRequest:
    """Request description for external APIs."""

    method: str
    url: str
    headers: dict[str, str] = field(default_factory=dict)
    json: Any | None = None
    data: Any | None = None
    idempotency_key: IdempotencyKey | str | None = None
