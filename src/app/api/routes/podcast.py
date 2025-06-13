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
    PodcastEpisodeCreate,
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
            detail="Episode not found."
        )
    episode = PodcastEpisodeBase(**result.model_dump())
    
    response = await GroqClient("llama3-70b-8192").chat(
        message=[
            {
                "role": "user",
                "context": episode.description 
            }
        ]
    )

    # disc = GroqClient.chat(result.description).choices[0].message.content
    # print(disc)
    result = PodcastEpisodeAlternative(
        title=message.title, prompt=message.prompt, original_episode=episode, generated_alternative=response)
    return result