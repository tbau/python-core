"""Timeout configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeoutConfig:
    """Timeout settings for external work."""

    connect: float = 5.0
    read: float = 30.0
    write: float = 30.0
    pool: float = 5.0

    def total(self) -> float:
        """Return the total configured timeout budget."""
        return self.connect + self.read + self.write + self.pool
