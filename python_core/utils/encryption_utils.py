"""Optional authenticated symmetric encryption helpers.

This module wraps ``cryptography.fernet`` so callers get authenticated
encryption without this library inventing its own cryptography.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from python_core.exceptions import ConfigurationError


class FernetEncryption:
    """Encrypt and decrypt bytes or text with one Fernet key.

    Fernet provides symmetric authenticated encryption: the same key encrypts
    and decrypts, and tampered tokens fail to decrypt.
    """

    def __init__(self, key: str | bytes) -> None:
        fernet = _load_fernet()
        self._fernet = fernet(key)

    @staticmethod
    def generate_key() -> str:
        """Generate a URL-safe base64 Fernet key."""

        fernet = _load_fernet()
        return fernet.generate_key().decode("ascii")

    def encrypt_bytes(self, value: bytes) -> bytes:
        """Encrypt bytes and return a Fernet token."""

        return self._fernet.encrypt(value)

    def decrypt_bytes(self, token: bytes, *, ttl_seconds: int | None = None) -> bytes:
        """Decrypt a Fernet token, optionally requiring it to be fresh."""

        if ttl_seconds is None:
            return self._fernet.decrypt(token)
        return self._fernet.decrypt(token, ttl=ttl_seconds)

    def encrypt_text(self, value: str, *, encoding: str = "utf-8") -> str:
        """Encrypt text and return an ASCII token safe for storage."""

        return self.encrypt_bytes(value.encode(encoding)).decode("ascii")

    def decrypt_text(
        self,
        token: str,
        *,
        encoding: str = "utf-8",
        ttl_seconds: int | None = None,
    ) -> str:
        """Decrypt an ASCII token back into text."""

        return self.decrypt_bytes(token.encode("ascii"), ttl_seconds=ttl_seconds).decode(encoding)


class FernetKeyRing:
    """Fernet helper for key rotation using ``MultiFernet``.

    The first key encrypts new data. All keys are tried during decryption, which
    lets you rotate keys without immediately invalidating existing tokens.
    """

    def __init__(self, keys: Iterable[str | bytes]) -> None:
        fernet = _load_fernet()
        multi_fernet = _load_multi_fernet()
        instances = [fernet(key) for key in keys]
        if not instances:
            raise ValueError("at least one key is required")
        self._multi_fernet = multi_fernet(instances)

    def encrypt_bytes(self, value: bytes) -> bytes:
        """Encrypt with the primary key."""

        return self._multi_fernet.encrypt(value)

    def decrypt_bytes(self, token: bytes, *, ttl_seconds: int | None = None) -> bytes:
        """Decrypt with any configured key."""

        if ttl_seconds is None:
            return self._multi_fernet.decrypt(token)
        return self._multi_fernet.decrypt(token, ttl=ttl_seconds)

    def rotate_token(self, token: bytes) -> bytes:
        """Re-encrypt a token with the primary key."""

        return self._multi_fernet.rotate(token)


def _load_fernet() -> Any:
    try:
        from cryptography.fernet import Fernet
    except ImportError as exc:
        raise ConfigurationError('Install python-core with the "security" extra.') from exc
    return Fernet


def _load_multi_fernet() -> Any:
    try:
        from cryptography.fernet import MultiFernet
    except ImportError as exc:
        raise ConfigurationError('Install python-core with the "security" extra.') from exc
    return MultiFernet
