"""Token issuer interface."""

from __future__ import annotations

from typing import Protocol

from python_core.auth.identity import Identity


class TokenIssuer(Protocol):
    """Issues tokens for identities."""

    def issue(self, identity: Identity) -> str:
        """Issue a token."""
