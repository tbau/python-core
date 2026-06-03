"""JWT token service backed by PyJWT."""

from __future__ import annotations

from typing import Any

from python_core.auth.identity import Identity
from python_core.auth.jwt_claims import JwtClaims
from python_core.auth.jwt_settings import JwtSettings
from python_core.exceptions import AuthenticationError, ConfigurationError, ValidationError


class JwtTokenService:
    """Signs and verifies JSON Web Tokens using PyJWT."""

    algorithm = "HS256"

    def __init__(self, settings: JwtSettings) -> None:
        self.settings = settings

    def issue(self, identity: Identity, *, extra: dict[str, Any] | None = None) -> str:
        """Issue a token for an identity."""
        claims = JwtClaims.for_identity(
            identity,
            issuer=self.settings.issuer,
            audience=self.settings.audience,
            expires_in=self.settings.expires_in,
        )
        payload = self._claims_to_payload(claims)
        if extra:
            reserved = self._reserved_claims()
            overlap = reserved.intersection(extra)
            if overlap:
                raise ValidationError(
                    f"extra jwt claims cannot override reserved claims: {sorted(overlap)}"
                )
            payload.update(extra)
        return self._jwt().encode(payload, self.settings.secret, algorithm=self.algorithm)

    def verify(self, token: str) -> Identity:
        """Verify a token and return its identity."""
        jwt = self._jwt()
        try:
            payload = jwt.decode(
                token,
                self.settings.secret,
                algorithms=[self.algorithm],
                audience=self.settings.audience,
                issuer=self.settings.issuer,
                leeway=self.settings.leeway_seconds,
            )
        except Exception as exc:
            raise AuthenticationError("invalid jwt") from exc
        subject = payload.get("sub")
        if not subject:
            raise AuthenticationError("invalid jwt")
        return JwtClaims(
            subject=str(subject),
            issuer=payload.get("iss"),
            audience=payload.get("aud"),
            roles=set(payload.get("roles", [])),
            permissions=set(payload.get("permissions", [])),
            extra=self._extra_claims(payload),
        ).to_identity()

    def _jwt(self) -> Any:
        try:
            import jwt
        except ImportError as exc:
            raise ConfigurationError("Install python-core[auth] to use JWT") from exc
        return jwt

    def _claims_to_payload(self, claims: JwtClaims) -> dict[str, Any]:
        payload = dict(claims.extra)
        payload["sub"] = claims.subject
        if claims.issuer:
            payload["iss"] = claims.issuer
        if claims.audience:
            payload["aud"] = claims.audience
        if claims.issued_at:
            payload["iat"] = int(claims.issued_at.timestamp())
        if claims.not_before:
            payload["nbf"] = int(claims.not_before.timestamp())
        if claims.expires_at:
            payload["exp"] = int(claims.expires_at.timestamp())
        payload["roles"] = sorted(claims.roles)
        payload["permissions"] = sorted(claims.permissions)
        return payload

    def _extra_claims(self, payload: dict[str, Any]) -> dict[str, Any]:
        reserved = self._reserved_claims()
        return {key: value for key, value in payload.items() if key not in reserved}

    def _reserved_claims(self) -> set[str]:
        return {"sub", "iss", "aud", "iat", "nbf", "exp", "roles", "permissions"}
