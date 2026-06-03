"""Message model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Message:
    """Small message envelope for queues and buses."""

    name: str
    payload: dict[str, object]
    headers: dict[str, str] = field(default_factory=dict)
