"""requests-based HTTP transport."""

from __future__ import annotations

from typing import Any

from python_core.exceptions import DependencyError, ExternalApiError
from python_core.external_api.api_request import ApiRequest
from python_core.external_api.api_response import ApiResponse


class RequestsHttpTransport:
    """HTTP transport implemented with the optional requests library."""

    def __init__(
        self,
        session: Any | None = None,
        *,
        request_error_types: tuple[type[BaseException], ...] | None = None,
    ) -> None:
        self._session = session
        self._request_error_types_override = request_error_types

    def send(self, request: ApiRequest, *, timeout_seconds: float) -> ApiResponse:
        """Send one request with requests."""
        session = self._session_or_default()
        data = None if request.json is not None else request.data
        try:
            response = session.request(
                method=request.method,
                url=request.url,
                headers=dict(request.headers),
                json=request.json,
                data=data,
                timeout=timeout_seconds,
            )
        except self._request_error_types() as exc:
            raise ExternalApiError("external api request failed") from exc

        return ApiResponse(
            status_code=response.status_code,
            headers=dict(response.headers),
            text=response.text,
            json_data=self._json_or_none(response),
        )

    def _session_or_default(self) -> Any:
        if self._session is not None:
            return self._session
        try:
            import requests
        except ImportError as exc:
            raise DependencyError(
                "requests is required for RequestsHttpTransport; install python-core[requests]"
            ) from exc
        self._session = requests.Session()
        return self._session

    def _request_error_types(self) -> tuple[type[BaseException], ...]:
        if self._request_error_types_override is not None:
            return self._request_error_types_override
        try:
            import requests
        except ImportError:
            return (OSError,)
        if self._session is not None:
            return (requests.RequestException, OSError)
        return (requests.RequestException,)

    def _json_or_none(self, response: Any) -> Any:
        try:
            return response.json()
        except ValueError:
            return None
