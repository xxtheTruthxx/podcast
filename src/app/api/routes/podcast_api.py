from typing import Optional, Annotated, List

from fastapi import (
  APIRouter,
  HTTPException,
  status,
  Form,
  Path,
  Query
)
from fastapi.responses import JSONResponse

from core.models.podcast import (
  PodcastEpisode,
  PodcastEpisodeBase,
)
from api.dependencies import AsyncSessionDep
from crud import PodcastCRUD

router = APIRouter(tags=["Podcast API"])

@router.get(f"/episodes/all",
  response_model=List[PodcastEpisodeBase],
  status_code=status.HTTP_200_OK)
async def get_episodes_via_api(
  session: AsyncSessionDep,
  offset: int = 0,
  limit: Optional[Annotated[int, Query()]] = None
):
  """
  Get list of episodes
  """
  return await PodcastCRUD(session).read_all(PodcastEpisode, offset=offset, limit=limit)

@router.post(f"/episodes/create",
  response_model=PodcastEpisode,
  status_code=status.HTTP_201_CREATED)
async def create_episode_via_api(
  title: Annotated[str, Form()],
  description: Annotated[str, Form()],
  host: Annotated[str, Form()],
  session: AsyncSessionDep
):
    """
    Create an episode.
    """
    await PodcastCRUD(session).create(
      PodcastEpisode(
        title=title,
        description=description,
        host=host
      )
    )

    return JSONResponse(
      status_code=status.HTTP_201_CREATED,
      content={"message": "Episode has been created successfully."}
    )

@router.delete("/episodes/{episode_id}/delete",
  status_code=status.HTTP_200_OK,
  name="delete_episode")
async def delete_episode(
  episode_id: Annotated[int, Path()],
  session: AsyncSessionDep
):
  """
  Deletes episode using `id`,
  """
  if not await PodcastCRUD(session).remove_by_id(episode_id):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Episode not found."
      )

  return {"message": "Episode has been removed successfully."}