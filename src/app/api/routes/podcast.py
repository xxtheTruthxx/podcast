from typing import List, Annotated
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Path,
    Body
)
from core.models.podcast import (
    PodcastEpisode,
    PodcastEpisodeBase,
    PodcastEpisodeGenerate,
    PodcastEpisodeAlternative
)

from core.services.groq import GroqClient

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
    episodes = await PodcastCRUD(session).read_all(
        db_obj=PodcastEpisode
    )
    if not episodes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Episodes not found."}
        )
    return episodes

@router.post("/episodes",
    response_model=PodcastEpisodeBase,
    status_code=status.HTTP_201_CREATED)
async def create_episode(
    episode: Annotated[PodcastEpisodeBase, Body],
    session: AsyncSessionDep
):
    """Create a podcast episode."""
    db_obj = PodcastEpisode.model_validate(episode)
    result = await PodcastCRUD(session).create(
        obj=db_obj
    )
    episode = PodcastEpisodeBase.model_validate(result)
    return episode

@router.post("/episodes/{episode_id}/generate_alternative",
    response_model=PodcastEpisodeAlternative,
    status_code=status.HTTP_200_OK)
async def get_alternative_episode(
    episode_id: Annotated[int, Path],
    message: Annotated[PodcastEpisodeGenerate, Body],
    session: AsyncSessionDep
):
    """Get alternative episode."""
    result = await PodcastCRUD(session).get_by_id(id=episode_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Episode not found."}
        )
    origional_episode = PodcastEpisodeBase.model_validate(result)

    groq = GroqClient(
        model="llama-3.1-8b-instant",
    ).create_template(
        prompt=message.prompt
    )
    target = getattr(origional_episode, message.target)
    generated_alternative = await groq.ask(target)
    
    return PodcastEpisodeAlternative(
        target=message.target,
        prompt=message.prompt,
        original_episode=origional_episode,
        generated_alternative=generated_alternative
    )