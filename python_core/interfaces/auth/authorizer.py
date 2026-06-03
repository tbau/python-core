"""Authorizer interface."""

from __future__ import annotations

from typing import Protocol

from python_core.auth.identity import Identity
from python_core.auth.permission import Permission


class Authorizer(Protocol):
    """Checks whether an identity may perform an action."""

    def can(self, identity: Identity, action: str, resource: str) -> bool:
        """Return True when access is allowed."""

    def allows(self, identity: Identity, permission: Permission) -> bool:
        """Return True when access is allowed for a permission."""
