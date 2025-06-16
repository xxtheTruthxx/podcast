from typing import List, Optional, Annotated

# Third-party Dependencies
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Body
)

# Local Dependencies
from core.config import settings
from core.models.rss import (
    RssFeed,
    RssFeedPost
)
from core.models.podcast import (
    PodcastEpisodeBase,
    PodcastEpisode
)
from api.dependencies import AsyncSessionDep
from crud import RssCRUD 

router = APIRouter(tags=["RSS Feed"])

@router.get("/fetch",
    response_model=List[RssFeed],
    status_code=status.HTTP_200_OK)
async def fetch_rss_feed(
    length: Optional[int] = None
):
    """
    Fetch all episodes from the RSS Feed.      
    """
    feeds = await RssCRUD.get_all(
        url=settings.RSS_URL,
        length=length
    )
    return feeds

@router.post("/post",
    response_model=PodcastEpisodeBase,
    status_code=status.HTTP_201_CREATED)
async def post_rss_feed(
    episode: Annotated[RssFeedPost, Body()],
    session: AsyncSessionDep
):
    """
    Post an episode from the RSS Feed.
    """
    rss = await RssCRUD._fetch_rss(
        url=settings.RSS_URL,
    )
    feed = rss.find("title", string=episode.title).find_parent()
    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Episode not found."
        )
    episode = PodcastEpisode(
        title=feed.find("title").text,
        description=feed.find("description").text,
        host=rss.title.text
    )
    return PodcastEpisodeBase.model_validate(
        await RssCRUD(session).create(episode)
    )