"""Permission set model."""

from __future__ import annotations

from dataclasses import dataclass, field

from python_core.auth.permission import Permission


@dataclass(frozen=True)
class PermissionSet:
    """Named collection of permissions."""

    permissions: set[str] = field(default_factory=set)

    @classmethod
    def from_permissions(cls, permissions: set[Permission]) -> "PermissionSet":
        """Create a set from Permission objects."""
        return cls({permission.name for permission in permissions})

    def allows(self, action: str, resource: str) -> bool:
        """Return True when the set allows an action on a resource."""
        return f"{resource}:{action}" in self.permissions or f"{resource}:*" in self.permissions
