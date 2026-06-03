# Security Guide

## Defaults

- Treat external input as untrusted.
- Keep file access explicit and caller-controlled.
- Do not log secrets or raw credentials.
- Use bounded retries and mandatory timeouts for network calls.
- Use idempotency keys for retryable writes.
- Keep transaction boundaries visible.

## Sensitive Data

Redact these values before logging:

- Authorization headers
- API keys and bearer tokens
- Passwords and connection strings
- Session cookies
- Personally identifiable data unless the caller opted in

## Path Safety

When adding path helpers, resolve paths before use and keep destructive
operations scoped to an expected root. Prefer returning planned actions before
executing deletions or overwrites.

## Security Helpers

- Use `python_core.utils.security_utils` for secure token generation,
  constant-time comparisons, HMAC-SHA256 helpers, and redaction.
- Use `python_core.utils.encryption_utils.FernetEncryption` when data must be
  encrypted and authenticated with a symmetric key.
- Install `python-core[security]` before using encryption helpers.
- Do not add custom encryption algorithms. Wrap reviewed recipes and keep key
  handling explicit at call sites.
