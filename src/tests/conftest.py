from collections.abc import AsyncGenerator, Generator
from typing import Literal

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from app.main import app
from app.api.dependencies import  get_async_session
# from app.models import Base

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase, AsyncAttrs):
    pass

@pytest.fixture(scope='session')
def anyio_backend() -> Literal['asyncio']:
    return 'asyncio'

@pytest.fixture(scope='session')
def postgres_container(
    anyio_backend: Literal['asyncio'],
) -> Generator[PostgresContainer, None, None]:
    with PostgresContainer('postgres:16', driver='asyncpg') as postgres:
        yield postgres

@pytest.fixture
async def async_session(
    postgres_container: PostgresContainer,
) -> AsyncGenerator[AsyncSession, None]:
    db_url = postgres_container.get_connection_url()
    async_engine = create_async_engine(db_url)

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(
        bind=async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with async_session() as session:
        yield session

    await async_engine.dispose()


@pytest.fixture
async def async_client(
    async_session: AsyncSession,
) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_session] = lambda: async_session
    _transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=_transport, base_url='http://test', follow_redirects=True
    ) as client:
        yield client

    app.dependency_overrides.clear()


# from typing import AsyncGenerator

# import pytest_asyncio
# from httpx import ASGITransport, AsyncClient
# from sqlalchemy.ext.asyncio import (
#     AsyncSession,
#     async_sessionmaker,
#     create_async_engine
# )

# from sqlalchemy.pool import NullPool
# from sqlmodel import SQLModel

# # Local Dependencies    
# from app.api.dependencies import get_async_session
# from app.core.config import settings, DB_URL
# from app.main import app

# # Create a test async engine instance
# test_async_engine = create_async_engine(
#     url=f"postgresql+asyncpg://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@localhost:{settings.DB_PORT}",
#     echo=False,
#     poolclass=NullPool
# )

# # Drop all tables after each test
# @pytest_asyncio.fixture(scope="function")
# async def async_db_engine():
#     async with test_async_engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)
    
#     yield test_async_engine

#     async with test_async_engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.drop_all)

# @pytest_asyncio.fixture(scope="function")
# async def async_session(async_db_engine):
#     test_async_session = async_sessionmaker(
#         bind=async_db_engine,
#         class_=AsyncSession,
#         expire_on_commit=False,
#         autocommit=False,
#         autoflush=False,
#     )

#     async with test_async_session() as session:
#         await session.begin()
#         yield session
#         await session.rollback()

# @pytest_asyncio.fixture(scope="function", autouse=True)
# async def async_client(async_session) -> AsyncGenerator[AsyncClient, None]:
#     def override_async_session():
#         yield async_session

#     app.dependency_overrides[get_async_session] = override_async_session
#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as async_client:
#         yield async_client
#     app.dependency_overrides.clear()