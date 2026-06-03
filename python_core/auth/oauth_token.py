"""OAuth token model."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta


@dataclass(frozen=True)
class OAuthToken:
    """OAuth access token response."""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int | None = None
    refresh_token: str | None = None
    scopes: tuple[str, ...] = ()
    issued_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def is_expired(self, *, leeway_seconds: int = 30) -> bool:
        """Return True when the token is expired or near expiry."""
        if self.expires_in is None:
            return False
        expires_at = self.issued_at + timedelta(seconds=self.expires_in)
        return datetime.now(UTC) >= expires_at - timedelta(seconds=leeway_seconds)

    def authorization_header(self) -> dict[str, str]:
        """Return an Authorization header."""
        return {"Authorization": f"{self.token_type} {self.access_token}"}
