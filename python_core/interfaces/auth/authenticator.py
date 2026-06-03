"""Authenticator interface."""

from __future__ import annotations

from typing import Protocol

from python_core.auth.identity import Identity


class Authenticator(Protocol):
    """Turns credentials into an identity."""

    def authenticate(self, credentials: object) -> Identity | None:
        """Authenticate credentials and return an identity."""
