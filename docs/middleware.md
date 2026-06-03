# Middleware Guide

## Intent

Middleware handles cross-cutting request concerns without mixing them into
services.

## Good Uses

- Request IDs
- Authentication and authorization
- Idempotency checks
- Logging context
- Feature flags
- Metrics

## Rule

Middleware should enrich or reject context. Business behavior belongs in
services and facades.
