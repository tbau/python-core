"""OAuth client configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OAuthClientConfig:
    """OAuth/OIDC client settings."""

    client_id: str
    client_secret: str | None
    authorization_url: str
    token_url: str
    redirect_uri: str
    scopes: tuple[str, ...] = ()
