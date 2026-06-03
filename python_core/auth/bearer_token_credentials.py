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
        scheme, token = value.split(" ", maxsplit=1)
        if scheme.lower() != "bearer":
            raise ValueError("authorization header must use Bearer scheme")
        return cls(token=token)
