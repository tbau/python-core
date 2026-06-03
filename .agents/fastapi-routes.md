# FastAPI Routes Agent

Use this guide when adding FastAPI support or route modules.

## Checklist

- Keep route handlers thin: validate, call a service, return a response.
- Put business behavior in services that can be tested without FastAPI.
- Register routers through `python_core.fastapi.scaffold.create_app`.
- Use dependency injection for services, database units of work, and API clients.
- Add health routes and exception handlers consistently.

## Route Pattern

```python
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/{item_id}")
async def get_item(item_id: str, service = Depends(...)):
    return await service.get_item(item_id)
```
