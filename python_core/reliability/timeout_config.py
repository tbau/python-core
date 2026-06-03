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

    def __post_init__(self) -> None:
        if self.connect < 0 or self.read < 0 or self.write < 0 or self.pool < 0:
            raise ValueError("timeout values must be non-negative")

    def total(self) -> float:
        """Return the total configured timeout budget."""
        return self.connect + self.read + self.write + self.pool
