"""OAuth token request model."""

from __future__ import annotations

from dataclasses import dataclass

from python_core.auth.oauth_client_config import OAuthClientConfig


@dataclass(frozen=True)
class OAuthTokenRequest:
    """OAuth authorization-code token request."""

    code: str
    code_verifier: str | None = None

    def form_data(self, config: OAuthClientConfig) -> dict[str, str]:
        """Return form data for a token endpoint request."""
        data = {
            "grant_type": "authorization_code",
            "code": self.code,
            "client_id": config.client_id,
            "redirect_uri": config.redirect_uri,
        }
        if config.client_secret:
            data["client_secret"] = config.client_secret
        if self.code_verifier:
            data["code_verifier"] = self.code_verifier
        return data
