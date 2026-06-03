# External APIs Guide

## Intent

External API code should be reliable, testable, and explicit about failure.

## Client Pattern

- Build requests in provider-specific clients.
- Use `ApiClient` for simple external API calls.
- Inject an `HttpTransport` when the HTTP implementation needs to change.
  `UrlopenHttpTransport` is the built-in standard-library transport.
- When injecting a custom `requests`-style session, pass `request_error_types`
  if the provider raises non-standard client exceptions.
- Pass a positive `timeout_seconds` and a concrete retry policy at construction.
- Use idempotency keys for retryable writes.
- Convert provider failures into domain exceptions.

## Retry Rules

Retry only when the request is safe or idempotent. Good candidates:

- GET requests
- POST/PUT/PATCH requests with an idempotency key
- 408, 409, 425, 429, and 5xx responses
- Network timeout or connection errors
