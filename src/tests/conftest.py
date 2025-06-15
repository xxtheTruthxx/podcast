from typing import AsyncGenerator

# Third-party Dependencies
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
from app.core.config import DB_URL
from app.main import app

TEST_DB = "postgresql+asyncpg://dephhjkssyjfzyblmcan:NzlkNDdkNzk4YTNiNzc0@aws-0-eu-central-1.pooler.supabase.com:5432/postgres"

# # Create a test async engine instance
# test_async_engine = create_async_engine(
#     TEST_DB,
#     # DB_URL,
#     echo=False,
#     poolclass=NullPool
# )

# # Drop all tables after each test
# @pytest_asyncio.fixture(scope="function")
# async def test_async_db_engine():
#     async with test_async_engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)
#     yield test_async_engine
#     async with test_async_engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.drop_all)

# @pytest_asyncio.fixture(scope="function")
# async def test_async_session(test_async_db_engine):
#     test_async_session = async_sessionmaker(
#         test_async_db_engine,
#         class_=AsyncSession,
#         expire_on_commit=False,
#         autocommit=False,
#         autoflush=False
#     )

#     async with test_async_session() as session:
#         async with session.begin():
#             yield session

@pytest_asyncio.fixture(scope="function", autouse=True)
async def test_async_client() -> AsyncGenerator[AsyncClient, None]:
    # async def override_async_session() -> AsyncGenerator[AsyncSession, None]:
        # yield test_async_session

    # app.dependency_overrides[get_async_session] = override_async_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client
# /    app.dependency_overrides.clear()