"""Ownership policy."""

from __future__ import annotations

from python_core.auth.identity import Identity
from python_core.auth.resource_owner import ResourceOwner


class OwnershipPolicy:
    """Checks direct ownership or admin role."""

    def __init__(self, *, admin_role: str = "admin") -> None:
        self.admin_role = admin_role

    def can_access(self, identity: Identity, owner: ResourceOwner) -> bool:
        """Return True when identity can access the owned resource."""
        return identity.has_role(self.admin_role) or owner.is_owned_by(identity.subject)
