# FastAPI Guide

## Intent

FastAPI support should make route creation consistent without forcing every
project to use FastAPI.

## Structure

- App creation belongs in `python_core.fastapi.scaffold`.
- Domain services should not import FastAPI.
- Route modules should be thin and depend on injected services.
- Exception handlers should convert domain exceptions into predictable responses.

## Adding Routes

1. Create an `APIRouter` in the app project.
2. Inject services, repositories, or clients through dependencies.
3. Register the router with `create_app`.
4. Add tests for route status codes and service calls.

See `examples/fastapi_app/main.py`.
