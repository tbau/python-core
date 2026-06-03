"""Prototype pattern.

Use this when new objects should start from a configured template instead of
being rebuilt from scratch.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field


@dataclass
class ReportTemplate:
    """Cloneable report template with mutable section configuration."""

    title: str
    sections: list[str] = field(default_factory=list)

    def clone(self) -> "ReportTemplate":
        """Return a deep copy so cloned sections can be edited independently."""

        return deepcopy(self)
