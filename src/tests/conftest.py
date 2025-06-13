from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator
import pytest_asyncio 

from unittest.mock import AsyncMock, MagicMock, create_autospec
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.dependencies import get_async_session
from app.main import app

@pytest_asyncio.fixture
async def test_async_client(mock_db_session) -> AsyncGenerator[AsyncClient, None]:
    # Override database dependency
    app.dependency_overrides[get_async_session] = lambda: mock_db_session
    
    # Initialize an async client
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client
    
    # Cleanup overrides
    app.dependency_overrides.clear()