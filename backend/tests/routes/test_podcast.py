from httpx import AsyncClient
import pytest

# from app.core.config import settings

@pytest.mark.asyncio
async def test_get_all_episodes(
    test_async_client: AsyncClient
):
    
    response = await test_async_client.get(f"api/v1/podcast/episodes")
    assert response.status_code == 200