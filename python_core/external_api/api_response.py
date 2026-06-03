"""External API response model."""

from __future__ import annotations

import json as jsonlib
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ApiResponse:
    """Response description for external APIs."""

    status_code: int
    headers: dict[str, str]
    text: str
    json_data: Any | None = None

    @property
    def ok(self) -> bool:
        """Return True for 2xx responses."""
        return 200 <= self.status_code < 300

    def json(self) -> Any:
        """Return parsed JSON data."""
        if self.json_data is not None:
            return self.json_data
        return jsonlib.loads(self.text)
