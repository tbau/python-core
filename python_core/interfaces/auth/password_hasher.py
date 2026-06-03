"""Password hasher interface."""

from __future__ import annotations

from typing import Protocol


class PasswordHasher(Protocol):
    """Hashes and verifies passwords."""

    def hash(self, password: str) -> str:
        """Hash a password for storage."""

    def verify(self, password: str, encoded: str) -> bool:
        """Return True when password matches an encoded hash."""
