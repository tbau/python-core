"""Ownership checker interface."""

from __future__ import annotations

from typing import Protocol

from python_core.auth.identity import Identity
from python_core.auth.resource_owner import ResourceOwner


class OwnershipChecker(Protocol):
    """Checks whether an identity can access an owned resource."""

    def can_access(self, identity: Identity, owner: ResourceOwner) -> bool:
        """Return True when access is allowed."""
