from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator
import pytest_asyncio

from unittest.mock import AsyncMock, MagicMock, create_autospec
from sqlmodel.ext.asyncio.session import AsyncSession

from app.main import app

@pytest_asyncio.fixture
async def mock_db_session():
    # Create a mock async session
    session = create_autospec(AsyncSession)
    # Mock async methods
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.exec = MagicMock()
    
    return session

@pytest_asyncio.fixture
async def test_async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client