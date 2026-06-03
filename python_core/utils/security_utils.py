"""Security utility functions based on standard-library primitives.

These helpers cover tokens, hashing, HMAC signatures, constant-time comparison,
and redaction. Use the auth password hashers for passwords and
``encryption_utils`` for reversible encryption.
"""

from __future__ import annotations

from collections.abc import Mapping
import hashlib
import hmac
import secrets

DEFAULT_SECRET_BYTES = 32
SENSITIVE_KEY_PARTS = ("authorization", "cookie", "key", "password", "secret", "token")


def generate_token_bytes(length_bytes: int = DEFAULT_SECRET_BYTES) -> bytes:
    """Generate cryptographically strong random bytes."""

    return secrets.token_bytes(length_bytes)


def generate_hex_token(length_bytes: int = DEFAULT_SECRET_BYTES) -> str:
    """Generate a cryptographically strong hex token for IDs or secrets."""

    return secrets.token_hex(length_bytes)


def generate_urlsafe_token(length_bytes: int = DEFAULT_SECRET_BYTES) -> str:
    """Generate a cryptographically strong URL-safe token."""

    return secrets.token_urlsafe(length_bytes)


def generate_numeric_code(length: int = 6) -> str:
    """Generate a numeric one-time code.

    Pair this with short expiration and attempt limits in real auth flows.
    """

    if length <= 0:
        raise ValueError("length must be positive")
    return "".join(str(secrets.randbelow(10)) for _ in range(length))


def constant_time_equals(left: str | bytes, right: str | bytes) -> bool:
    """Compare strings or bytes without content-based short-circuiting.

    Use this when checking signatures, API keys, or tokens so timing does not
    reveal where two values differ.
    """

    if type(left) is not type(right):
        return False
    return hmac.compare_digest(left, right)


def hash_bytes_sha256(value: bytes) -> str:
    """Return SHA-256 hex digest for bytes.

    This is for integrity checks, not password storage.
    """

    return hashlib.sha256(value).hexdigest()


def hash_text_sha256(value: str, *, encoding: str = "utf-8") -> str:
    """Return SHA-256 hex digest for text."""

    return hash_bytes_sha256(value.encode(encoding))


def hmac_sha256(secret: bytes, message: bytes) -> str:
    """Return HMAC-SHA256 hex digest for a message and shared secret."""

    return hmac.new(secret, message, hashlib.sha256).hexdigest()


def verify_hmac_sha256(secret: bytes, message: bytes, expected_hexdigest: str) -> bool:
    """Verify an HMAC-SHA256 digest using constant-time comparison."""

    actual = hmac_sha256(secret, message)
    return constant_time_equals(actual, expected_hexdigest)


def mask_token(value: str, *, visible_prefix: int = 4, visible_suffix: int = 4) -> str:
    """Mask a token while leaving small stable hints for debugging."""

    if len(value) <= visible_prefix + visible_suffix:
        return "*" * len(value)
    return f"{value[:visible_prefix]}...{value[-visible_suffix:]}"


def redact_secret(value: object, *, replacement: str = "[REDACTED]") -> str:
    """Return a redacted placeholder for a sensitive value."""

    if value is None:
        return ""
    return replacement


def redact_mapping(
    values: Mapping[str, object],
    *,
    sensitive_parts: tuple[str, ...] = SENSITIVE_KEY_PARTS,
    replacement: str = "[REDACTED]",
) -> dict[str, object]:
    """Return a copy of a mapping with sensitive-looking keys redacted."""

    redacted: dict[str, object] = {}
    for key, value in values.items():
        lowered = key.lower()
        if any(part in lowered for part in sensitive_parts):
            redacted[key] = replacement
        else:
            redacted[key] = value
    return redacted
