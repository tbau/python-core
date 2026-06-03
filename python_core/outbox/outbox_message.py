"""Outbox message model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True)
class OutboxMessage:
    """Message stored inside the transactional outbox."""

    name: str
    payload: dict[str, object]
    id: str = field(default_factory=lambda: uuid4().hex)
    headers: dict[str, str] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    sent_at: datetime | None = None
