"""Minimal FastAPI app using python-core scaffolding."""

from fastapi import APIRouter

from python_core.fastapi import AppSettings, create_app

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/{item_id}")
async def get_item(item_id: str) -> dict[str, str]:
    return {"item_id": item_id}


app = create_app(
    settings=AppSettings(title="Example API", version="0.1.0"),
    routers=[router],
)
