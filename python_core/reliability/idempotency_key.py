"""Idempotency key value object."""

from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class IdempotencyKey:
    """Value object for duplicate-safe operation keys."""

    value: str

    @classmethod
    def generate(cls, prefix: str | None = None) -> "IdempotencyKey":
        """Create a new unique idempotency key."""
        value = uuid.uuid4().hex
        return cls(f"{prefix}-{value}" if prefix else value)

    @classmethod
    def new(cls, prefix: str | None = None) -> "IdempotencyKey":
        """Backward-compatible alias for generate."""
        return cls.generate(prefix=prefix)

    def as_header(self) -> dict[str, str]:
        """Return this key as an HTTP header."""
        return {"Idempotency-Key": self.value}
