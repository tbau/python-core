"""PKCE helpers."""

from __future__ import annotations

import base64
import hashlib
import secrets


def create_code_verifier(length: int = 64) -> str:
    """Create a PKCE code verifier."""
    return secrets.token_urlsafe(length)[:128]


def create_code_challenge(verifier: str) -> str:
    """Create a S256 PKCE code challenge."""
    digest = hashlib.sha256(verifier.encode("ascii")).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode("ascii")
