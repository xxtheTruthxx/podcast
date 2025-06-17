from httpx import AsyncClient
import pytest

# Local Dependencies


@pytest.mark.asyncio
async def test_get_all_episodes(
    test_async_client: AsyncClient
):
    response = await test_async_client.get("api/v1/podcast/episodes")
    assert response.status_code == 200
    # assert response.json() == 