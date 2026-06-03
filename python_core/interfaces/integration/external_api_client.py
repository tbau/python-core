"""External API client interface."""

from __future__ import annotations

from typing import Protocol

from python_core.external_api.api_request import ApiRequest
from python_core.external_api.api_response import ApiResponse


class ExternalApiClient(Protocol):
    """Transport boundary for third-party API calls."""

    def send(self, request: ApiRequest) -> ApiResponse:
        """Send one request and return a response."""
