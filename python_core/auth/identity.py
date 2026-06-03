"""Identity model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Identity:
    """Authenticated caller identity."""

    subject: str
    roles: set[str] = field(default_factory=set)
    permissions: set[str] = field(default_factory=set)
    claims: dict[str, object] = field(default_factory=dict)

    def has_role(self, role: str) -> bool:
        """Return True when the identity has a role."""
        return role in self.roles

    def has_permission(self, permission: str) -> bool:
        """Return True when the identity has a permission."""
        return permission in self.permissions

    def claim(self, name: str, default: object | None = None) -> object | None:
        """Return a claim by name."""
        return self.claims.get(name, default)
