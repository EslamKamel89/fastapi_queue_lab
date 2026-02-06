from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    raise RuntimeError("Database is not initialized")
