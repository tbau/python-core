"""OAuth state store."""

from __future__ import annotations

import secrets
from dataclasses import dataclass, field


@dataclass
class OAuthStateStore:
    """Small one-time OAuth state store for examples and tests."""

    values: set[str] = field(default_factory=set)

    def create(self) -> str:
        """Create and remember a new state value."""
        value = secrets.token_urlsafe(32)
        self.values.add(value)
        return value

    def consume(self, value: str) -> bool:
        """Return True only once for a known state value."""
        if value not in self.values:
            return False
        self.values.remove(value)
        return True
