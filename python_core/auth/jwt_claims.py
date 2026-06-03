"""JWT claims."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import Any

from python_core.auth.identity import Identity


@dataclass(frozen=True)
class JwtClaims:
    """Claims used to create or verify a JWT."""

    subject: str
    issuer: str | None = None
    audience: str | None = None
    expires_at: datetime | None = None
    issued_at: datetime | None = None
    not_before: datetime | None = None
    roles: set[str] = field(default_factory=set)
    permissions: set[str] = field(default_factory=set)
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def for_identity(
        cls,
        identity: Identity,
        *,
        issuer: str | None = None,
        audience: str | None = None,
        expires_in: timedelta,
    ) -> "JwtClaims":
        """Create claims for an identity."""
        now = datetime.now(UTC)
        return cls(
            subject=identity.subject,
            issuer=issuer,
            audience=audience,
            issued_at=now,
            not_before=now,
            expires_at=now + expires_in,
            roles=set(identity.roles),
            permissions=set(identity.permissions),
            extra=dict(identity.claims),
        )

    def to_identity(self) -> Identity:
        """Convert claims to an identity."""
        return Identity(
            subject=self.subject,
            roles=set(self.roles),
            permissions=set(self.permissions),
            claims=dict(self.extra),
        )
