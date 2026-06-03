"""Role and permission based authorizer."""

from __future__ import annotations

from python_core.auth.identity import Identity
from python_core.auth.permission import Permission
from python_core.auth.role_permission_map import RolePermissionMap


class RoleBasedAuthorizer:
    """Authorizes using identity permissions and role permission mappings."""

    def __init__(self, role_permissions: RolePermissionMap | None = None) -> None:
        self._role_permissions = role_permissions or RolePermissionMap()

    def can(self, identity: Identity, action: str, resource: str) -> bool:
        """Return True when access is allowed."""
        required = f"{resource}:{action}"
        wildcard = f"{resource}:*"
        permissions = identity.permissions | self._role_permissions.permissions_for(identity.roles)
        return required in permissions or wildcard in permissions

    def allows(self, identity: Identity, permission: Permission) -> bool:
        """Return True when access is allowed for a permission."""
        return self.can(identity, permission.action, permission.resource)
