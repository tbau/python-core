# Architecture Agent

Use this guide when changing package structure or adding a new subsystem.

## Checklist

- Keep domain interfaces separate from framework adapters.
- Add shared concepts to `python_core/interfaces` only when two or more
  subsystems need them.
- Put optional integrations in focused packages such as `python_core/db`,
  `python_core/http`, `python_core/files`, and `python_core/fastapi`.
- Prefer composition over inheritance unless the abstraction represents a stable
  contract.
- Keep public constructors simple and pass dependencies in explicitly.

## Acceptance Criteria

- New public APIs are documented in `docs/architecture.md` or the relevant guide.
- Public classes live in class-named modules such as `repository.py`.
- Imports from `python_core` work without optional extras installed.
- No file grows beyond the 300-line target without being split.
