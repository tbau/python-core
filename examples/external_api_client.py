"""Example external API call with timeout, retry, and idempotency settings."""

from python_core.external_api.api_client import ApiClient
from python_core.reliability.exponential_backoff_retry_policy import ExponentialBackoffRetryPolicy
from python_core.reliability.idempotency_key import IdempotencyKey


def create_remote_item(url: str, payload: dict[str, object]) -> object:
    client = ApiClient(timeout_seconds=10, retry_policy=ExponentialBackoffRetryPolicy(attempts=3))
    response = client.post(
        url,
        json=payload,
        idempotency_key=IdempotencyKey.generate(prefix="item"),
    )
    return response.json_data or response.text
