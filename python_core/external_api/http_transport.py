"""HTTP transport interface for external API requests."""

from __future__ import annotations

from typing import Protocol

from python_core.external_api.api_request import ApiRequest
from python_core.external_api.api_response import ApiResponse


class HttpTransport(Protocol):
    """Sends prepared external API requests over an HTTP implementation."""

    def send(self, request: ApiRequest, *, timeout_seconds: float) -> ApiResponse:
        """Send one request and return the raw HTTP response."""
