from typing import Annotated

# Third-party Dependencies
from fastapi import (
    APIRouter,
    status,
    Body
)
from fastapi.responses import JSONResponse
from core.models.podcast import (
    PodcastEpisode,
    PodcastEpisodeBase
)

# Local Dependencies
from api.dependencies import AsyncSessionDep
from crud import PodcastCRUD

router = APIRouter(tags=["Webhook"])

@router.post("/event",
    status_code=status.HTTP_200_OK)
async def webhook_event(
    episode: Annotated[PodcastEpisodeBase, Body],
    session: AsyncSessionDep
):
    """Send a webhook event."""
    db_obj = PodcastEpisode.model_validate(episode)
    await PodcastCRUD(session).create(db_obj)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "Episode added."}
    )