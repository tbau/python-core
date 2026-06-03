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
        if ":" not in value:
            raise ValueError("permission must use resource:action format")
        resource, action = value.split(":", maxsplit=1)
        if not resource or not action:
            raise ValueError("permission resource and action cannot be blank")
        return cls(action=action, resource=resource)
