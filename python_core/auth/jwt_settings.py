"""JWT settings."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class JwtSettings:
    """Settings for signing and verifying HS256 JWTs."""

    secret: str
    issuer: str | None = None
    audience: str | None = None
    expires_in: timedelta = timedelta(minutes=15)
    leeway_seconds: int = 30
