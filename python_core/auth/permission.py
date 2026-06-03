"""Permission model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Permission:
    """Named action on a resource."""

    action: str
    resource: str

    @property
    def name(self) -> str:
        """Return canonical permission name."""
        return f"{self.resource}:{self.action}"

    @classmethod
    def parse(cls, value: str) -> "Permission":
        """Parse a resource:action permission string."""
        resource, action = value.split(":", maxsplit=1)
        return cls(action=action, resource=resource)
