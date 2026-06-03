# Refactor Agent

Use this guide for cleanup and restructuring.

## Checklist

- Preserve public behavior unless the task explicitly changes it.
- Move code in small steps and keep imports working.
- Add tests before risky behavior changes.
- Prefer deleting dead abstractions over adding compatibility layers.
- Update docs when a pattern changes.

## Stop Conditions

- A file is shorter but less readable.
- A generic abstraction hides important failure behavior.
- A framework dependency leaks into the core package import path.
