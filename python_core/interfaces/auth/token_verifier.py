"""Token verifier interface."""

from __future__ import annotations

from typing import Protocol

from python_core.auth.identity import Identity


class TokenVerifier(Protocol):
    """Verifies tokens and returns identities."""

    def verify(self, token: str) -> Identity:
        """Verify a token."""
