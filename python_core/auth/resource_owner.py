"""Resource ownership model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ResourceOwner:
    """Describes ownership of a resource."""

    resource_type: str
    resource_id: str
    owner_subject: str

    def is_owned_by(self, subject: str) -> bool:
        """Return True when the subject owns the resource."""
        return self.owner_subject == subject
