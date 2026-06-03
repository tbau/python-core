"""Composite pattern.

Use this when individual objects and groups of objects should be treated with
the same interface, such as menus, trees, and nested categories.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class MenuItem:
    """Tree node that can contain child menu items."""

    label: str
    children: list["MenuItem"] = field(default_factory=list)

    def add(self, child: "MenuItem") -> None:
        """Attach a child menu item."""

        self.children.append(child)

    def labels(self) -> list[str]:
        """Return this node and every descendant label in traversal order."""

        labels = [self.label]
        for child in self.children:
            labels.extend(child.labels())
        return labels
