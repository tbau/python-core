from python_core.exceptions import ConfigurationError, ExternalApiError, IdempotencyRequiredError
from python_core.external_api.api_client import ApiClient
from python_core.external_api.api_request import ApiRequest
from python_core.external_api.api_response import ApiResponse
from python_core.external_api.requests_http_transport import RequestsHttpTransport
from python_core.external_api.urlopen_http_transport import UrlopenHttpTransport
from python_core.reliability.exponential_backoff_retry_policy import ExponentialBackoffRetryPolicy
from python_core.reliability.idempotency_key import IdempotencyKey


class RecordingTransport:
    def __init__(self, response: ApiResponse | None = None) -> None:
        self.response = response or ApiResponse(status_code=200, headers={}, text="")
        self.requests: list[ApiRequest] = []
        self.timeout_seconds: list[float] = []

    def send(self, request: ApiRequest, *, timeout_seconds: float) -> ApiResponse:
        self.requests.append(request)
        self.timeout_seconds.append(timeout_seconds)
        return self.response


class FakeRequestsResponse:
    status_code = 201
    headers = {"Content-Type": "application/json"}
    text = '{"id": "item-1"}'

    def json(self) -> dict[str, str]:
        return {"id": "item-1"}


class FakeRequestsSession:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def request(self, **kwargs: object) -> FakeRequestsResponse:
        self.calls.append(kwargs)
        return FakeRequestsResponse()


class FailingRequestsSession:
    def __init__(self, error: BaseException) -> None:
        self.error = error

    def request(self, **_kwargs: object) -> FakeRequestsResponse:
        raise self.error


class ProviderError(Exception):
    """Provider-specific request failure used by transport tests."""


def test_api_client_requires_idempotency_for_retryable_post() -> None:
    client = ApiClient(
        retry_policy=ExponentialBackoffRetryPolicy(attempts=2, base_delay=0, jitter=0)
    )

    try:
        client.post("https://example.com/items", json={"name": "desk"})
    except IdempotencyRequiredError:
        return

    raise AssertionError("expected IdempotencyRequiredError")


def test_api_client_adds_idempotency_header() -> None:
    transport = RecordingTransport()
    client = ApiClient(transport=transport)
    key = IdempotencyKey.generate(prefix="item")
    request = ApiRequest(method="POST", url="https://example.com/items", idempotency_key=key)

    client.send(request)

    assert transport.requests[0].headers["Idempotency-Key"] == key.value
    assert "Idempotency-Key" not in request.headers


def test_api_client_normalizes_direct_request_method() -> None:
    transport = RecordingTransport()
    client = ApiClient(
        transport=transport,
        retry_policy=ExponentialBackoffRetryPolicy(attempts=2, base_delay=0, jitter=0),
    )
    request = ApiRequest(method="get", url="https://example.com/items")

    client.send(request)

    assert transport.requests[0].method == "GET"


def test_api_client_passes_timeout_to_transport() -> None:
    transport = RecordingTransport()
    client = ApiClient(timeout_seconds=7.5, transport=transport)

    client.get("https://example.com/items")

    assert transport.timeout_seconds == [7.5]


def test_api_client_rejects_non_positive_timeout() -> None:
    for timeout_seconds in (0, -1):
        try:
            ApiClient(timeout_seconds=timeout_seconds)
        except ConfigurationError:
            continue
        raise AssertionError("expected ConfigurationError")


def test_urlopen_transport_encodes_json_body() -> None:
    request = ApiRequest(method="POST", url="https://example.com/items", json={"name": "desk"})

    body, headers = UrlopenHttpTransport()._body_and_headers(request)

    assert body == b'{"name": "desk"}'
    assert headers["Content-Type"] == "application/json"


def test_requests_transport_uses_session_and_timeout() -> None:
    session = FakeRequestsSession()
    transport = RequestsHttpTransport(session=session)
    request = ApiRequest(
        method="POST",
        url="https://example.com/items",
        headers={"Authorization": "Bearer token"},
        json={"name": "desk"},
    )

    response = transport.send(request, timeout_seconds=4.0)

    assert response.status_code == 201
    assert response.json_data == {"id": "item-1"}
    assert session.calls == [
        {
            "method": "POST",
            "url": "https://example.com/items",
            "headers": {"Authorization": "Bearer token"},
            "json": {"name": "desk"},
            "data": None,
            "timeout": 4.0,
        }
    ]


def test_requests_transport_ignores_data_when_json_is_present() -> None:
    session = FakeRequestsSession()
    transport = RequestsHttpTransport(session=session)

    transport.send(
        ApiRequest(
            method="POST",
            url="https://example.com/items",
            json={"name": "desk"},
            data={"name": "ignored"},
        ),
        timeout_seconds=4.0,
    )

    assert session.calls[0]["data"] is None


def test_requests_transport_maps_injected_session_os_error() -> None:
    transport = RequestsHttpTransport(session=FailingRequestsSession(OSError("network down")))

    try:
        transport.send(ApiRequest(method="GET", url="https://example.com"), timeout_seconds=4.0)
    except ExternalApiError as exc:
        assert isinstance(exc.__cause__, OSError)
        return

    raise AssertionError("expected ExternalApiError")


def test_requests_transport_uses_custom_request_error_types() -> None:
    transport = RequestsHttpTransport(
        session=FailingRequestsSession(ProviderError("provider down")),
        request_error_types=(ProviderError,),
    )

    try:
        transport.send(ApiRequest(method="GET", url="https://example.com"), timeout_seconds=4.0)
    except ExternalApiError as exc:
        assert isinstance(exc.__cause__, ProviderError)
        return

    raise AssertionError("expected ExternalApiError")
