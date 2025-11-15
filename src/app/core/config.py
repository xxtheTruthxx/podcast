from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import SQLModel
from typing import TypeVar

# Define a generic type variable
TypeSQL = TypeVar("TypeSQL", bound=SQLModel)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    NAME: str
    DESCRIPTION: str
    VERSION: str
    API_V1_STR: str = "/api/v1"

    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    GROQ_API_KEY: str
    GROQ_MODEL_TEMPLATE: str
    GROQ_MODEL: str

    RSS_URL: str

    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

settings = Settings()

DB_URL = f"postgresql+asyncpg://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"