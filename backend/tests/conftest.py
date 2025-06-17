from typing import AsyncGenerator

# Third-party Dependencies
import pytest_asyncio
from sqlmodel import SQLModel
from testcontainers.postgres import PostgresContainer
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# Local Dependencies
from app.main import app
from app.api.dependencies import get_async_session

# Create a postgres instance
@pytest_asyncio.fixture(scope="session")
async def postgres_container() -> AsyncGenerator[PostgresContainer, None]:
    with PostgresContainer("postgres:latest", driver="asyncpg") as postgres:
        yield postgres

@pytest_asyncio.fixture(scope="session")
async def async_session(
    postgres_container: PostgresContainer,
) -> AsyncGenerator[AsyncSession, None]:
    # Create a test async engine instance
    async_engine = create_async_engine(
        url = postgres_container.get_connection_url()
    )

    # Drop all and create tables after each test
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    await async_engine.dispose()

# Create an test async client
@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_client(async_session) -> AsyncGenerator[AsyncClient, None]:
    # Override an app dependencies
    app.dependency_overrides[get_async_session] = lambda: async_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client    
    app.dependency_overrides.clear()