"""Role to permission map."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class RolePermissionMap:
    """Maps roles to canonical permission strings."""

    permissions_by_role: dict[str, set[str]] = field(default_factory=dict)

    def permissions_for(self, roles: set[str]) -> set[str]:
        """Return permissions granted to a set of roles."""
        granted: set[str] = set()
        for role in roles:
            granted.update(self.permissions_by_role.get(role, set()))
        return granted
