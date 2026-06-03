"""Provider-style external API client with an injected transport."""

from __future__ import annotations

from dataclasses import dataclass

from python_core.external_api.api_client import ApiClient
from python_core.external_api.api_request import ApiRequest
from python_core.external_api.api_response import ApiResponse
from python_core.reliability.exponential_backoff_retry_policy import ExponentialBackoffRetryPolicy
from python_core.reliability.idempotency_key import IdempotencyKey


@dataclass(frozen=True)
class RemoteItem:
    """Domain model returned by the provider client."""

    id: str
    name: str


class FakeTransport:
    """Transport for examples and tests that avoids real network calls."""

    def __init__(self) -> None:
        self.requests: list[ApiRequest] = []

    def send(self, request: ApiRequest, *, timeout_seconds: float) -> ApiResponse:
        """Record a request and return a provider-like response."""
        self.requests.append(request)
        return ApiResponse(
            status_code=201,
            headers={"Content-Type": "application/json"},
            text='{"id": "item_123", "name": "Desk"}',
            json_data={"id": "item_123", "name": "Desk"},
        )


class InventoryApi:
    """Small provider client that hides HTTP details from application code."""

    def __init__(self, client: ApiClient) -> None:
        self._client = client

    def create_item(self, name: str) -> RemoteItem:
        """Create one item with retry-safe idempotency."""
        response = self._client.post(
            "/items",
            json={"name": name},
            idempotency_key=IdempotencyKey.generate(prefix="item"),
        )
        data = response.json()
        return RemoteItem(id=data["id"], name=data["name"])


def build_inventory_api(transport: FakeTransport) -> InventoryApi:
    """Configure the provider client with explicit timeout and retry settings."""
    client = ApiClient(
        base_url="https://inventory.example.test",
        timeout_seconds=5.0,
        retry_policy=ExponentialBackoffRetryPolicy(attempts=3, base_delay=0.1, jitter=0),
        transport=transport,
    )
    return InventoryApi(client)


def main() -> None:
    """Run the example without making a network request."""
    transport = FakeTransport()
    api = build_inventory_api(transport)
    item = api.create_item("Desk")

    print(item)
    print(transport.requests[0].headers["Idempotency-Key"])


if __name__ == "__main__":
    main()
