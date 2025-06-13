from unittest.mock import AsyncMock, MagicMock
from httpx import AsyncClient
import pytest 

from app.core.models.podcast import PodcastEpisode
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.models.podcast import (
    PodcastEpisodeCreate,
    PodcastEpisodeBase,
    PodcastEpisode
)

@pytest.mark.asyncio
async def test_get_all_episodes(
    test_async_client: AsyncClient,
    mock_db_session: AsyncSession
):
    episode_data = {
        "title": "The Future of AI",
        "description": "We discuss upcoming trends in artificial intelligence.",
        "host": "Joe Rogan"
    }

    episode = PodcastEpisode(**episode_data, id=1)

    # Mock session methods
    mock_db_session.add.return_value = None
    mock_db_session.commit = AsyncMock()
    mock_db_session.refresh = AsyncMock(return_value=episode)

    response = await test_async_client.post("/podcast/episodes", json=episode_data)

    assert response.status_code == 201

    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(episode)