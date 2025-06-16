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
from core.config import settings
from api.dependencies import AsyncSessionDep
from crud import PodcastCRUD

router = APIRouter(tags=["Webhook"])

@router.post("/event",
    status_code=status.HTTP_200_OK)
async def webhook_event(
    episode: Annotated[PodcastEpisodeBase, Body()],
    session: AsyncSessionDep
):
    """
    Send a webhook event.
    """
    episode = PodcastEpisode.model_validate(episode)
    await PodcastCRUD(session).create(episode)

    # Send a message to the Telegram Bot
    await PodcastCRUD.request(
        method="POST", url=f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage",
        params={
            "chat_id": settings.TELEGRAM_CHAT_ID,
            "text": f"New episode added: {episode.title}"
        })
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "Episode added."}
    )