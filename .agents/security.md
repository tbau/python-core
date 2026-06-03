# Security Agent

Use this guide when touching file paths, external inputs, auth, secrets, or
network calls.

## Checklist

- Never log secrets, tokens, API keys, passwords, or raw authorization headers.
- Keep path operations workspace-bounded when handling user-supplied paths.
- Validate external data at boundaries before passing it deeper into the app.
- Make network timeouts mandatory and retries bounded.
- Require idempotency keys for retryable write operations to external APIs.
- Keep destructive operations explicit and reversible where practical.
- Keep JWT secrets, OAuth client secrets, refresh tokens, and API keys out of
  source code and logs.
- Prefer short-lived access tokens and explicit issuer/audience validation.

## Review Questions

- What untrusted input crosses this boundary?
- What happens on timeout, partial failure, duplicate request, or rollback?
- Can the caller customize the security-sensitive behavior?
