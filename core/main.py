from __future__ import annotations

from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from core.config import settings


def create_app() -> FastAPI:
    app_name = settings.APP_NAME
    if not app_name:
        raise RuntimeError("Env variables is not loaded")

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("startup: performing lightweight app checks")
        yield
        print("shutdown: cleaning up")

    app = FastAPI(title=app_name, lifespan=lifespan)

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
