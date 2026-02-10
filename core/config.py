import os

from pydantic import BaseModel


class Settings(BaseModel):

    APP_NAME: str | None = os.getenv("APP_NAME")
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")


settings = Settings()
