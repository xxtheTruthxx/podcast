from httpx import AsyncClient
import pytest

# Local Dependencies
from app.core.config import settings

@pytest.mark.asyncio
async def test_create_episode(
    async_client: AsyncClient
):
    episode = {
        "title": "Building a Startup",
        "description": "Tips and lessons learned from successful founders on building your own tech company from scratch.",
        "host": "Alex Smith"
    }

    response = await async_client.post(f"{settings.API_V1_STR}/podcast/episodes", json=episode)
    assert response.status_code == 201
    content = response.json()
    assert content["title"] == episode["title"]
    assert content["description"] == episode["description"]
    assert content["host"] == episode["host"]

@pytest.mark.asyncio
async def test_get_all_episodes(
    async_client: AsyncClient
):
    response = await async_client.get(f"{settings.API_V1_STR}/podcast/episodes")
    assert response.status_code == 200