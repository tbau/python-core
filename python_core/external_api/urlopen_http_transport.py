"""urllib-based HTTP transport."""

from __future__ import annotations

import json as jsonlib
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from python_core.exceptions import ExternalApiError
from python_core.external_api.api_request import ApiRequest
from python_core.external_api.api_response import ApiResponse


class UrlopenHttpTransport:
    """HTTP transport implemented with the Python standard library."""

    def send(self, request: ApiRequest, *, timeout_seconds: float) -> ApiResponse:
        """Send one request with urllib."""
        body, headers = self._body_and_headers(request)
        urllib_request = Request(request.url, data=body, headers=headers, method=request.method)
        try:
            with urlopen(urllib_request, timeout=timeout_seconds) as response:
                text = response.read().decode("utf-8")
                return ApiResponse(
                    status_code=response.status,
                    headers=dict(response.headers.items()),
                    text=text,
                    json_data=self._json_or_none(text),
                )
        except HTTPError as exc:
            return self._response_from_http_error(exc)
        except URLError as exc:
            raise ExternalApiError("external api request failed") from exc

    def _response_from_http_error(self, exc: HTTPError) -> ApiResponse:
        text = exc.read().decode("utf-8")
        return ApiResponse(
            status_code=exc.code,
            headers=dict(exc.headers.items()),
            text=text,
            json_data=self._json_or_none(text),
        )

    def _body_and_headers(self, request: ApiRequest) -> tuple[bytes | None, dict[str, str]]:
        headers = dict(request.headers)
        if request.json is not None:
            headers.setdefault("Content-Type", "application/json")
            return jsonlib.dumps(request.json).encode("utf-8"), headers
        if request.data is None:
            return None, headers
        if isinstance(request.data, bytes):
            return request.data, headers
        if isinstance(request.data, str):
            return request.data.encode("utf-8"), headers
        headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
        return urlencode(request.data).encode("utf-8"), headers

    def _json_or_none(self, text: str) -> Any:
        try:
            return jsonlib.loads(text)
        except ValueError:
            return None
