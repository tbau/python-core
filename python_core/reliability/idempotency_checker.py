"""Simple idempotency checker."""

from __future__ import annotations

from dataclasses import dataclass, field

from python_core.exceptions import IdempotencyError
from python_core.reliability.idempotency_key import IdempotencyKey

KeyLike = IdempotencyKey | str


@dataclass
class IdempotencyChecker:
    """Tracks idempotency keys and optional result tokens."""

    seen: dict[str, str | None] = field(default_factory=dict)

    def create_key(self, prefix: str | None = None) -> IdempotencyKey:
        """Create a new idempotency key."""
        return IdempotencyKey.generate(prefix=prefix)

    def has_seen(self, key: KeyLike) -> bool:
        """Return True when the key has already been added."""
        return self._value(key) in self.seen

    def check_and_add(self, key: KeyLike, *, result: str | None = None) -> bool:
        """Add a key if it is new.

        Returns True when the caller should do the work, and False when the key
        was already seen.
        """

        value = self._value(key)
        if value in self.seen:
            return False
        self.seen[value] = result
        return True

    def remember_result(self, key: KeyLike, result: str) -> None:
        """Store or replace the result token for a key."""
        self.seen[self._value(key)] = result

    def result_for(self, key: KeyLike) -> str | None:
        """Return a stored result token for a key."""
        return self.seen.get(self._value(key))

    def require_new(self, key: KeyLike) -> None:
        """Raise if the key was already used."""
        if self.has_seen(key):
            raise IdempotencyError("idempotency key has already been used")

    def _value(self, key: KeyLike) -> str:
        return key.value if isinstance(key, IdempotencyKey) else key
