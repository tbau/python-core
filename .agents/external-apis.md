# External APIs Agent

Use this guide when adding clients for third-party APIs.

## Checklist

- Use `ApiClient`, a concrete retry policy, and idempotency helpers.
- Use `ExternalApiClient` only when a service needs a protocol boundary.
- Keep provider-specific auth and request signing in small classes.
- Keep request building and response parsing obvious at the call site.
- Include correlation IDs and safe metadata in logs.
- Do not retry unsafe write operations unless an idempotency key is present.

## Failure Handling

- Convert provider errors into `ExternalApiError`.
- Treat timeouts and rate limits as expected failure modes.
- Surface enough context for callers to decide whether to retry later.
