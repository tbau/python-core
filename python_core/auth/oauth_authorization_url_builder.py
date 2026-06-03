"""OAuth authorization URL builder."""

from __future__ import annotations

from urllib.parse import urlencode

from python_core.auth.oauth_client_config import OAuthClientConfig


class OAuthAuthorizationUrlBuilder:
    """Builds OAuth authorization URLs."""

    def __init__(self, config: OAuthClientConfig) -> None:
        self.config = config

    def build(self, *, state: str, code_challenge: str | None = None) -> str:
        """Build an authorization URL."""
        params = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": self.config.redirect_uri,
            "scope": " ".join(self.config.scopes),
            "state": state,
        }
        if code_challenge:
            params["code_challenge"] = code_challenge
            params["code_challenge_method"] = "S256"
        return f"{self.config.authorization_url}?{urlencode(params)}"
