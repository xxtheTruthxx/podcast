from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel
from sqlmodel import SQLModel
from typing import TypeVar

TypeSQL = TypeVar("TypeSQL", bound=SQLModel)
TypeModel = TypeVar("TypeModel", bound=BaseModel)

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

settings = Settings()