"""JWT authenticator."""

from __future__ import annotations

from python_core.auth.bearer_token_credentials import BearerTokenCredentials
from python_core.auth.identity import Identity
from python_core.auth.jwt_token_service import JwtTokenService


class JwtAuthenticator:
    """Authenticates bearer tokens with a JwtTokenService."""

    def __init__(self, token_service: JwtTokenService) -> None:
        self._token_service = token_service

    def authenticate(self, credentials: BearerTokenCredentials | str) -> Identity:
        """Authenticate bearer credentials."""
        token = credentials.token if isinstance(credentials, BearerTokenCredentials) else credentials
        return self._token_service.verify(token)
