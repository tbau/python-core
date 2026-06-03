from python_core.exceptions import IdempotencyRequiredError
from python_core.external_api.api_client import ApiClient
from python_core.external_api.api_request import ApiRequest
from python_core.reliability.exponential_backoff_retry_policy import ExponentialBackoffRetryPolicy
from python_core.reliability.idempotency_key import IdempotencyKey


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
    client = ApiClient()
    key = IdempotencyKey.generate(prefix="item")
    request = ApiRequest(method="POST", url="https://example.com/items", idempotency_key=key)

    _body, headers = client._body_and_headers(request)

    assert headers["Idempotency-Key"] == key.value
