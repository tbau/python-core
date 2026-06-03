# Logging Guide

## Intent

Logging should provide useful operational context without tying services to one
logging framework.

## Pattern

- Services depend on the `EventLogger` interface.
- Default local code can use `StandardEventLogger`.
- Logs should use event names plus structured fields.
- Sensitive values must be redacted before logging.

## Event Names

Use names that describe what happened:

- `api.request.started`
- `api.request.failed`
- `db.transaction.rolled_back`
- `excel.parse.missing_column`

Avoid embedding secrets, raw payloads, or long free-form messages in event names.
