# Uncommon Tasks Agent

Use this guide for less frequent but high-impact work.

## Checklist

- Packaging: keep optional dependencies in extras and protect imports.
- Migrations: document upgrade steps and compatibility assumptions.
- Observability: add structured events without leaking secrets.
- Performance: measure before optimizing and preserve simple APIs.
- Concurrency: make ownership, cancellation, and cleanup explicit.
- Backward compatibility: prefer additive changes until a breaking change is
  clearly justified.

## Stop And Recheck

- The change introduces global state.
- The change adds a required framework dependency.
- The change makes retries, transactions, or cleanup implicit.
