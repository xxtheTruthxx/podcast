from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Body
)
from core.models.podcast import (
    PodcastEpisodeBase,
    PodcastEpisode,
    PodcastEpisodeCreate
)

from typing import List, Annotated

from api.dependencies import AsyncSessionDep
from crud import PodcastCRUD

router = APIRouter(tags=["Podcast"])

@router.get("/episodes",
    response_model=List[PodcastEpisodeBase],
    status_code=status.HTTP_200_OK)
async def get_all_episodes(
    session: AsyncSessionDep
):
    """Get all podcast episodes."""
    result = await PodcastCRUD(session).read_all(
        db_obj=PodcastEpisode
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episodes not found."
        )
    return result

@router.post("/episodes",
    response_model=PodcastEpisodeBase,
    status_code=status.HTTP_201_CREATED)
async def create_episode(
    episode: Annotated[PodcastEpisodeBase, Body],
    session: AsyncSessionDep
):
    """Create a podcast episode."""
    db_obj = PodcastEpisodeCreate.model_validate(episode)
    result = await PodcastCRUD(session).create(
        create_obj=PodcastEpisode(**db_obj.model_dump()),
        return_obj=PodcastEpisodeBase
    )
    return result