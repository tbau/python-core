"""API key authenticator."""

from __future__ import annotations

from python_core.auth.api_key_credentials import ApiKeyCredentials
from python_core.auth.identity import Identity


class ApiKeyAuthenticator:
    """Authenticates API keys from an in-memory mapping."""

    def __init__(self, identities_by_key: dict[str, Identity]) -> None:
        self._identities_by_key = identities_by_key

    def authenticate(self, credentials: ApiKeyCredentials | str) -> Identity | None:
        """Return the identity for an API key, or None."""
        key = credentials.key if isinstance(credentials, ApiKeyCredentials) else credentials
        return self._identities_by_key.get(key)
