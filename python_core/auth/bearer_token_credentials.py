"""Bearer token credentials."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BearerTokenCredentials:
    """Bearer token extracted from a request."""

    token: str

    @classmethod
    def from_authorization_header(cls, value: str) -> "BearerTokenCredentials":
        """Create credentials from an Authorization header."""
        parts = value.strip().split(None, maxsplit=1)
        if len(parts) != 2:
            raise ValueError("authorization header must be '<scheme> <credentials>'")
        scheme, token = parts
        if scheme.lower() != "bearer":
            raise ValueError("authorization header must use Bearer scheme")
        if not token.strip():
            raise ValueError("bearer token cannot be blank")
        return cls(token=token)
