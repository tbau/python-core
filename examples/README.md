# Examples

These examples are intended to be copied into new projects and adapted. Most
files avoid side effects at import time so you can read, import, and test them
without writing files or making network calls.

## Good Starting Points

- `production_service_flow.py`: end-to-end use case with validation, repository,
  outbox, message bus, and dependency injection.
- `external_api_client.py`: provider-style API wrapper with timeout, retry,
  idempotency, and an injected fake transport.
- `sqlalchemy_transaction.py`: SQLAlchemy transaction boundary with explicit
  commit and automatic close behavior.
- `dependency_injection.py`: scoped service wiring for request or job flows.
- `auth_jwt_oauth.py`: JWT, role permissions, ownership checks, and OAuth URL
  construction.
- `cache_usage.py`: Redis-style cache adapter with a fake client.
- `custom_spreadsheet_writer.py` and `excel_profile.py`: Excel adapter examples
  that require the `excel` extra when run.
- `fastapi_app/main.py`: optional FastAPI app scaffold that requires the `api`
  extra when run.

## Running

Base examples:

```powershell
python examples\production_service_flow.py
python examples\external_api_client.py
python examples\retry_with_backoff.py
```

Optional adapter examples:

```powershell
python -m pip install -e ".[api,auth,excel]"
python examples\auth_jwt_oauth.py
python examples\custom_spreadsheet_writer.py
```

For a fully pinned environment, install from the root `requirements.txt` first.
