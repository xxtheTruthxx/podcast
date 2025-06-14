from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

# Local Dependencies    
from app.api.dependencies import get_async_session
from app.core.config import settings, DB_URL
from app.main import app

# Create a test async engine instance
test_async_engine = create_async_engine(
    url=f"postgresql+asyncpg://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@localhost:{settings.DB_PORT}",
    echo=False,
    poolclass=NullPool
)

# Drop all tables after each test
@pytest_asyncio.fixture(scope="function")
async def async_db_engine():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    yield test_async_engine

    async with test_async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def async_session(async_db_engine):
    test_async_session = async_sessionmaker(
        bind=async_db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with test_async_session() as session:
        await session.begin()
        yield session
        await session.rollback()

@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_client(async_session) -> AsyncGenerator[AsyncClient, None]:
    def override_async_session():
        yield async_session

    app.dependency_overrides[get_async_session] = override_async_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client
    app.dependency_overrides.clear()