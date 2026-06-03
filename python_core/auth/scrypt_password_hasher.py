"""Scrypt password hasher."""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets


class ScryptPasswordHasher:
    """Hashes and verifies passwords with scrypt."""

    algorithm = "scrypt"

    def __init__(
        self,
        *,
        n: int = 2**17,
        r: int = 8,
        p: int = 1,
        salt_bytes: int = 16,
        dklen: int = 64,
        maxmem: int = 256 * 1024 * 1024,
    ) -> None:
        self.n = n
        self.r = r
        self.p = p
        self.salt_bytes = salt_bytes
        self.dklen = dklen
        self.maxmem = maxmem

    def hash(self, password: str) -> str:
        """Hash a password for storage."""
        salt = secrets.token_bytes(self.salt_bytes)
        digest = self._digest(password, salt, self.n, self.r, self.p)
        return "$".join(
            [
                self.algorithm,
                str(self.n),
                str(self.r),
                str(self.p),
                self._b64(salt),
                self._b64(digest),
            ]
        )

    def verify(self, password: str, encoded: str) -> bool:
        """Return True when password matches an encoded hash."""
        algorithm, n, r, p, salt, expected = encoded.split("$", maxsplit=5)
        if algorithm != self.algorithm:
            return False
        expected_bytes = self._unb64(expected)
        actual = self._digest(password, self._unb64(salt), int(n), int(r), int(p))
        return hmac.compare_digest(actual, expected_bytes)

    def _digest(self, password: str, salt: bytes, n: int, r: int, p: int) -> bytes:
        return hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=n,
            r=r,
            p=p,
            maxmem=self.maxmem,
            dklen=self.dklen,
        )

    def _b64(self, value: bytes) -> str:
        return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")

    def _unb64(self, value: str) -> bytes:
        padding = "=" * (-len(value) % 4)
        return base64.urlsafe_b64decode(value + padding)
