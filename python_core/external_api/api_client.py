"""Simple external API client."""

from __future__ import annotations

import json as jsonlib
from collections.abc import Mapping
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen

from python_core.exceptions import ExternalApiError, IdempotencyRequiredError
from python_core.external_api.api_request import ApiRequest
from python_core.external_api.api_response import ApiResponse
from python_core.reliability.idempotency_key import IdempotencyKey
from python_core.reliability.no_retry_policy import NoRetryPolicy
from python_core.reliability.retry import retry_sync
from python_core.reliability.retry_policy import RetryPolicy

RETRY_STATUS_CODES = {408, 409, 425, 429, 500, 502, 503, 504}
SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


class ApiClient:
    """Small synchronous client for JSON-style external APIs."""

    def __init__(
        self,
        *,
        base_url: str = "",
        headers: Mapping[str, str] | None = None,
        timeout_seconds: float = 30.0,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        self.base_url = base_url
        self.headers = dict(headers or {})
        self.timeout_seconds = timeout_seconds
        self.retry_policy = retry_policy or NoRetryPolicy()

    def get(self, path: str, *, headers: Mapping[str, str] | None = None) -> ApiResponse:
        """Send a GET request."""
        return self.request("GET", path, headers=headers)

    def post(
        self,
        path: str,
        *,
        json: Any | None = None,
        data: Any | None = None,
        headers: Mapping[str, str] | None = None,
        idempotency_key: IdempotencyKey | str | None = None,
    ) -> ApiResponse:
        """Send a POST request."""
        return self.request(
            "POST",
            path,
            json=json,
            data=data,
            headers=headers,
            idempotency_key=idempotency_key,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        json: Any | None = None,
        data: Any | None = None,
        headers: Mapping[str, str] | None = None,
        idempotency_key: IdempotencyKey | str | None = None,
    ) -> ApiResponse:
        """Send one external API request."""

        api_request = ApiRequest(
            method=method.upper(),
            url=self._url(path),
            headers=self._headers(headers),
            json=json,
            data=data,
            idempotency_key=idempotency_key,
        )
        return self.send(api_request)

    def send(self, request: ApiRequest) -> ApiResponse:
        """Send an ApiRequest instance."""
        if self._needs_idempotency(request) and request.idempotency_key is None:
            raise IdempotencyRequiredError("retryable writes require an idempotency key")

        return retry_sync(
            lambda: self._send_once(request),
            policy=self.retry_policy,
            retry_on=(ExternalApiError,),
        )

    def _send_once(self, request: ApiRequest) -> ApiResponse:
        body, headers = self._body_and_headers(request)
        urllib_request = Request(request.url, data=body, headers=headers, method=request.method)
        try:
            with urlopen(urllib_request, timeout=self.timeout_seconds) as response:
                text = response.read().decode("utf-8")
                return ApiResponse(
                    status_code=response.status,
                    headers=dict(response.headers.items()),
                    text=text,
                    json_data=self._json_or_none(text),
                )
        except HTTPError as exc:
            return self._handle_http_error(exc)
        except URLError as exc:
            raise ExternalApiError("external api request failed") from exc

    def _handle_http_error(self, exc: HTTPError) -> ApiResponse:
        text = exc.read().decode("utf-8")
        response = ApiResponse(
            status_code=exc.code,
            headers=dict(exc.headers.items()),
            text=text,
            json_data=self._json_or_none(text),
        )
        if exc.code in RETRY_STATUS_CODES:
            raise ExternalApiError(f"retryable status code: {exc.code}")
        return response

    def _body_and_headers(self, request: ApiRequest) -> tuple[bytes | None, dict[str, str]]:
        headers = dict(request.headers)
        if request.idempotency_key is not None:
            key = request.idempotency_key
            headers["Idempotency-Key"] = (
                key.value if isinstance(key, IdempotencyKey) else key
            )
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

    def _headers(self, headers: Mapping[str, str] | None) -> dict[str, str]:
        merged = dict(self.headers)
        merged.update(headers or {})
        return merged

    def _url(self, path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        return urljoin(f"{self.base_url.rstrip('/')}/", path.lstrip("/"))

    def _needs_idempotency(self, request: ApiRequest) -> bool:
        return request.method not in SAFE_METHODS and self.retry_policy.attempts > 1

    def _json_or_none(self, text: str) -> Any:
        try:
            return jsonlib.loads(text)
        except ValueError:
            return None
