"""Argon2id password hasher."""

from __future__ import annotations

from typing import Any

from python_core.exceptions import ConfigurationError


class Argon2idPasswordHasher:
    """Hashes and verifies passwords with Argon2id."""

    def __init__(
        self,
        *,
        time_cost: int = 2,
        memory_cost: int = 19_456,
        parallelism: int = 1,
        hash_len: int = 32,
        salt_len: int = 16,
    ) -> None:
        self._settings = {
            "time_cost": time_cost,
            "memory_cost": memory_cost,
            "parallelism": parallelism,
            "hash_len": hash_len,
            "salt_len": salt_len,
        }

    def hash(self, password: str) -> str:
        """Hash a password for storage."""
        return self._hasher().hash(password)

    def verify(self, password: str, encoded: str) -> bool:
        """Return True when password matches an encoded hash."""
        hasher = self._hasher()
        try:
            return hasher.verify(encoded, password)
        except Exception:
            return False

    def needs_rehash(self, encoded: str) -> bool:
        """Return True when the encoded hash should be upgraded."""
        return self._hasher().check_needs_rehash(encoded)

    def _hasher(self) -> Any:
        try:
            from argon2 import PasswordHasher
            from argon2.low_level import Type
        except ImportError as exc:
            raise ConfigurationError("Install python-core[auth] to use Argon2id") from exc
        return PasswordHasher(type=Type.ID, **self._settings)
