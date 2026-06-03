"""Builder pattern.

Use this when constructing an object is clearer as a sequence of named steps
than one long constructor call.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BuiltRequest:
    """Immutable request value produced by ``RequestBuilder``."""

    path: str
    headers: dict[str, str] = field(default_factory=dict)
    query: dict[str, str] = field(default_factory=dict)


class RequestBuilder:
    """Builds a request through chainable, readable steps."""

    def __init__(self, path: str) -> None:
        self._path = path
        self._headers: dict[str, str] = {}
        self._query: dict[str, str] = {}

    def header(self, name: str, value: str) -> "RequestBuilder":
        """Add a header and return the builder for chaining."""

        self._headers[name] = value
        return self

    def query(self, name: str, value: str) -> "RequestBuilder":
        """Add a query parameter and return the builder for chaining."""

        self._query[name] = value
        return self

    def build(self) -> BuiltRequest:
        """Return the completed immutable request value."""

        return BuiltRequest(self._path, dict(self._headers), dict(self._query))
