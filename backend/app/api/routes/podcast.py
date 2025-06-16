from typing import List, Optional, Annotated

# Third-party Dependencies
from fastapi import (
    APIRouter,
    status,
    Path,
    Query,
    Body
)
from fastapi.responses import JSONResponse

# Local Dependencies
from core.models.podcast import (
    PodcastEpisode,
    PodcastEpisodeBase,
    PodcastEpisodeGenerate,
    PodcastEpisodeAlternative
)
from core.services import GroqClient
from api.dependencies import AsyncSessionDep
from crud import PodcastCRUD

router = APIRouter(tags=["Podcast"])

@router.get("/episodes",
    response_model=List[PodcastEpisodeBase],
    status_code=status.HTTP_200_OK)
async def get_episodes(
    session: AsyncSessionDep,
    offset: int = 0,
    limit: Optional[Annotated[int, Query()]] = None
):
    """
    Get all episodes.
    """
    episodes = await PodcastCRUD(session).read_all(
        PodcastEpisode, 
        offset=offset,
        limit=limit
    )
    if not episodes:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Episodes not found."}
        )
    return episodes

@router.post("/episodes",
    response_model=PodcastEpisodeBase,
    status_code=status.HTTP_201_CREATED)
async def create_episode(
    episode: Annotated[PodcastEpisodeBase, Body()],
    session: AsyncSessionDep
):
    """
    Create an episode.
    """
    result = await PodcastCRUD(session).create(
        PodcastEpisode.model_validate(episode)
    )
    return PodcastEpisodeBase.model_validate(result)

@router.post("/episodes/{episode_id}/generate_alternative",
    response_model=PodcastEpisodeAlternative,
    status_code=status.HTTP_200_OK)
async def get_alternative_episode(
    episode_id: Annotated[int, Path()],
    message: Annotated[PodcastEpisodeGenerate, Body()],
    session: AsyncSessionDep
):
    """
    Generate an alternative version of the episode.
    """
    result = await PodcastCRUD(session).get_by_id(episode_id)
    if not result:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": "Episode not found."}
        )
    origional_episode = PodcastEpisodeBase.model_validate(result)

    groq = GroqClient(
        model="gemma2-9b-it",
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
