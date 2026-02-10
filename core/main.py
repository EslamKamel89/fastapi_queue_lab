from __future__ import annotations

from contextlib import asynccontextmanager

from dotenv import load_dotenv

from core.database import Database
from core.deps import get_session
from core.models_base import Base

load_dotenv()

from fastapi import FastAPI

from core.config import settings


def create_app() -> FastAPI:
    app_name = settings.APP_NAME
    database_url = settings.DATABASE_URL
    if not app_name or not database_url:
        raise RuntimeError("[FastAPI] Env variables is not loaded")
    database = Database(database_url=database_url, echo=True)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("startup: performing lightweight app checks")
        async with database.engine.begin() as conn:
            from apps.auth.models import User
            from apps.jobs.models import Job

            await conn.run_sync(Base.metadata.create_all)
        yield
        await database.dispose()
        print("shutdown: cleaning up")

    app = FastAPI(title=app_name, lifespan=lifespan)
    app.dependency_overrides[get_session] = database.get_session

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
