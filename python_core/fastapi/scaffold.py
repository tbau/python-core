"""FastAPI app and route scaffolding."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from python_core.exceptions import ConfigurationError, PythonCoreError


@dataclass(frozen=True)
class AppSettings:
    """Minimal settings for creating a FastAPI app."""

    title: str = "Python Core API"
    version: str = "0.1.0"
    debug: bool = False


def create_app(
    *,
    settings: AppSettings | None = None,
    routers: Iterable[Any] = (),
) -> Any:
    """Create a FastAPI app and register standard behavior."""

    fastapi = _fastapi()
    app_settings = settings or AppSettings()
    app = fastapi.FastAPI(
        title=app_settings.title,
        version=app_settings.version,
        debug=app_settings.debug,
    )
    app.include_router(health_router())
    for router in routers:
        app.include_router(router)

    @app.exception_handler(PythonCoreError)
    async def python_core_error_handler(_request: Any, exc: PythonCoreError) -> Any:
        """Convert library exceptions into a simple JSON error response."""

        return fastapi.responses.JSONResponse(
            status_code=400,
            content={"error": exc.__class__.__name__, "message": str(exc)},
        )

    return app


def health_router() -> Any:
    """Return a standard health router."""

    fastapi = _fastapi()
    router = fastapi.APIRouter(tags=["health"])

    @router.get("/health")
    async def health() -> dict[str, str]:
        """Return a simple liveness response."""

        return {"status": "ok"}

    return router


def _fastapi() -> Any:
    try:
        import fastapi
        import fastapi.responses
    except ImportError as exc:
        raise ConfigurationError("Install python-core[api] to use FastAPI scaffolding") from exc
    return fastapi
