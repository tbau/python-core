"""Simple external API client."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import urljoin

from python_core.exceptions import ConfigurationError, ExternalApiError, IdempotencyRequiredError
from python_core.external_api.api_request import ApiRequest
from python_core.external_api.api_response import ApiResponse
from python_core.external_api.http_transport import HttpTransport
from python_core.external_api.urlopen_http_transport import UrlopenHttpTransport
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
        transport: HttpTransport | None = None,
    ) -> None:
        if timeout_seconds <= 0:
            raise ConfigurationError("timeout_seconds must be positive")

        self.base_url = base_url
        self.headers = dict(headers or {})
        self.timeout_seconds = timeout_seconds
        self.retry_policy = retry_policy or NoRetryPolicy()
        self.transport = transport or UrlopenHttpTransport()

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
        response = self.transport.send(
            self._prepare_request(request),
            timeout_seconds=self.timeout_seconds,
        )
        if response.status_code in RETRY_STATUS_CODES:
            raise ExternalApiError(f"retryable status code: {response.status_code}")
        return response

    def _prepare_request(self, request: ApiRequest) -> ApiRequest:
        headers = dict(request.headers)
        key = request.idempotency_key
        if key is not None:
            headers["Idempotency-Key"] = key.value if isinstance(key, IdempotencyKey) else key
        return ApiRequest(
            method=request.method.upper(),
            url=request.url,
            headers=headers,
            json=request.json,
            data=request.data,
            idempotency_key=request.idempotency_key,
        )

    def _headers(self, headers: Mapping[str, str] | None) -> dict[str, str]:
        merged = dict(self.headers)
        merged.update(headers or {})
        return merged

    def _url(self, path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        return urljoin(f"{self.base_url.rstrip('/')}/", path.lstrip("/"))

    def _needs_idempotency(self, request: ApiRequest) -> bool:
        return request.method.upper() not in SAFE_METHODS and self.retry_policy.attempts > 1
