from typing import Annotated, List, Optional

from fastapi import (
  APIRouter,
  HTTPException,
  status,
  Path,
  Query
)

from api.dependencies import AsyncSessionDep

from core.config import settings
from core.models.rss import RssFeed
from core.models.podcast import PodcastEpisode
from core.logger import logger
from crud import PodcastCRUD, RssCRUD 

router = APIRouter(tags=["RSS Feed API"])

@router.get("/feeds",
  response_model=List[RssFeed],
  status_code=status.HTTP_200_OK)
async def fetch_rss_feeds_via_api( 
  offset: Annotated[int, Query()] = 0,
  limit: Optional[int] = None,
):
    """
    Fetch all feeds from the RSS Feed.      
    """
    try:
      return await RssCRUD.fetch_all(
        url=settings.RSS_URL,
        offset=offset,
        limit=limit
      )
    except Exception as e:
      logger.error(f"Error fetching RSS feeds: {str(e)}")
      raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to load feeds. Please try again later."
      )

@router.get("/feed/{uuid}")
async def load_feed_via_api(
  uuid: Annotated[str, Path()]
):
  """
  Fetch feed from the RSS Feed via API.
  """
  feeds = await RssCRUD.fetch_all(
    url=settings.RSS_URL,
  )
  for feed in feeds:
    if feed.uuid == uuid:
      return feed
  raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Feed not found."
  )
  
@router.post("/feed/{uuid}/add")
async def add_feed_via_api(
  uuid: Annotated[str, Path()],
  session: AsyncSessionDep
):
  """
  Add a feed as a podcast episode via API.
  """
  feeds = await RssCRUD.fetch_all(url=settings.RSS_URL)
  for feed in feeds:
    if feed.uuid == uuid:
      await PodcastCRUD(session).create(
        PodcastEpisode(
          title=feed.title,
          description=feed.description,
          host=feed.author
        )
      )
      raise HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail="Feed has been added successfully."
      )
    
  raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Feed not found."
  )