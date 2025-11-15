from typing import Optional, Annotated, List
from pydantic import BaseModel

from fastapi import (
  APIRouter,
  HTTPException,
  status,
  Form,
  Path,
  Query,
  Body,
  Header
)
from fastapi.responses import JSONResponse, Response
from starlette.responses import Response as StarletteResponse

from core.models.podcast import (
  PodcastEpisode,
  PodcastEpisodeBase,
)
from api.dependencies import AsyncSessionDep
from crud import PodcastCRUD

# Request models for PUT and PATCH
class EpisodeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    host: Optional[str] = None

class EpisodeFullUpdate(BaseModel):
    title: str
    description: str
    host: str

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

@router.get("/episodes/{episode_id}",
  response_model=PodcastEpisodeBase,
  status_code=status.HTTP_200_OK)
async def get_episode_by_id(
  episode_id: Annotated[int, Path()],
  session: AsyncSessionDep
):
  """
  Get a single episode by ID.
  """
  episode = await PodcastCRUD(session).read_by_id(episode_id)
  if not episode:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Episode not found."
    )
  return episode

@router.head("/episodes/{episode_id}",
  status_code=status.HTTP_200_OK)
async def head_episode(
  episode_id: Annotated[int, Path()],
  session: AsyncSessionDep
):
  """
  Check if an episode exists (HEAD request).
  Returns 200 if exists, 404 if not.
  """
  episode = await PodcastCRUD(session).read_by_id(episode_id)
  if not episode:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Episode not found."
    )
  return Response(status_code=status.HTTP_200_OK)

@router.put("/episodes/{episode_id}",
  response_model=PodcastEpisodeBase,
  status_code=status.HTTP_200_OK)
async def update_episode_full(
  session: AsyncSessionDep,
  episode_id: Annotated[int, Path()],
  episode_data: EpisodeFullUpdate = Body(...),
):
  """
  Full update of an episode (PUT method).
  All fields are required.
  """
  # Check if episode exists
  existing_episode = await PodcastCRUD(session).read_by_id(episode_id)
  if not existing_episode:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Episode not found."
    )
  
  # Update with all fields
  updated_episode = await PodcastCRUD(session).update(
    episode_id,
    data={
      "title": episode_data.title,
      "description": episode_data.description,
      "host": episode_data.host
    }
  )
  
  if not updated_episode:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Failed to update episode."
    )
  
  return updated_episode

@router.patch("/episodes/{episode_id}",
  response_model=PodcastEpisodeBase,
  status_code=status.HTTP_200_OK)
async def update_episode_partial(
  session: AsyncSessionDep,
  episode_id: Annotated[int, Path()],
  episode_data: EpisodeUpdate = Body(...),
):
  """
  Partial update of an episode (PATCH method).
  Only provided fields will be updated.
  """
  # Check if episode exists
  existing_episode = await PodcastCRUD(session).read_by_id(episode_id)
  if not existing_episode:
    raise HTTPException(
      status_code=status.HTTP_404_NOT_FOUND,
      detail="Episode not found."
    )
  
  # Build update data with only provided fields
  update_data = {}
  if episode_data.title is not None:
    update_data["title"] = episode_data.title
  if episode_data.description is not None:
    update_data["description"] = episode_data.description
  if episode_data.host is not None:
    update_data["host"] = episode_data.host
  
  if not update_data:
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="At least one field must be provided for update."
    )
  
  # Update with partial data
  updated_episode = await PodcastCRUD(session).update(
    episode_id,
    data=update_data
  )
  
  if not updated_episode:
    raise HTTPException(
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      detail="Failed to update episode."
    )
  
  return updated_episode

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