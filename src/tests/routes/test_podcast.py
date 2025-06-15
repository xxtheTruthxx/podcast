from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
import pytest

from app.core.config import settings

@pytest.mark.asyncio
async def test_get_all_episodes(
    async_session: AsyncSession,
    async_client: AsyncClient
):
    
    response = await async_client.get(f"{settings.API_V1_STR}/podcast/episodes")

    assert response.status_code == 200
    