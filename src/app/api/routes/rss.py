from typing import List, Optional

# Third-party Dependencies
from fastapi import (
    APIRouter,
    status,
    Request
)
from fastapi.templating import Jinja2Templates
from api.dependencies import AsyncSessionDep

# Local Dependencies
from core.config import settings
from core.models.rss import RssFeed
from core.models.podcast import PodcastEpisode
from core.logger import logger
from crud import PodcastCRUD, RssCRUD 

# Initialize Jinja2 template 
template = Jinja2Templates(directory="templates")

router = APIRouter(tags=["RSS Feed"])

@router.get("/feed/{uuid}")
async def load_feed(
  request: Request,
  uuid: str
):
  """
  Fetch feed from the RSS Feed.
  """
  try:
    feeds = await RssCRUD.fetch_all(
      url=settings.RSS_URL,
    )
    
    for feed in feeds:
      if feed.uuid == uuid:
        return template.TemplateResponse(
          request=request,
          status_code=status.HTTP_200_OK,
          name="components/rss/feed.html",
          context={
            "title": f"News RSS",
            "feed": feed
          }       
        )
    
    # Feed not found
    return template.TemplateResponse(
      request=request,
      status_code=status.HTTP_404_NOT_FOUND,
      name="components/notFound.html",
      context={"title": "Feed not found"}
    )
  except Exception as e:
    logger.error(f"Error loading feed {uuid}: {str(e)}")
    return template.TemplateResponse(
      request=request,
      status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
      name="components/notFound.html",
      context={"title": "Error loading feed"}
    )

@router.get("/feed/{uuid}/add")
async def add_feed(
    request: Request,
    uuid: str,
    session: AsyncSessionDep
):
    """
    Add a feed as a podcast episode.
    """
    try:
        feeds = await RssCRUD.fetch_all(url=settings.RSS_URL)
        for feed in feeds:
            if feed.uuid == uuid:
                episode = PodcastEpisode(
                    title=feed.title,
                    description=feed.description,
                    host=feed.author
                )
                await PodcastCRUD(session).create(episode)
                return template.TemplateResponse(
                  request=request,
                  status_code=status.HTTP_200_OK,
                  name="components/successful.html",
                  context={"title": "PodGen."}
                )
        
        # Feed not found
        return template.TemplateResponse(
          request=request,
          status_code=status.HTTP_404_NOT_FOUND,
          name="components/notFound.html",
          context={"title": "Feed not found"}
        )
    except Exception as e:
        logger.error(f"Error adding feed {uuid}: {str(e)}")
        return template.TemplateResponse(
          request=request,
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          name="components/notFound.html",
          context={"title": "Error adding feed"}
        )

@router.get("/feeds",
    response_model=List[RssFeed],
    status_code=status.HTTP_200_OK)
async def fetch_rss_feeds( 
    request: Request,
    offset: int = 0,
    limit: Optional[int] = None,
):
    """
    Fetch all feeds from the RSS Feed.      
    """
    try:
        feeds = await RssCRUD.fetch_all(
            url=settings.RSS_URL,
            offset=offset,
            limit=limit
        )
        return template.TemplateResponse(
          request=request,
          status_code=status.HTTP_200_OK,
          name="components/rss/feeds.html",
          context={
            "title": "News RSS",
            "feeds": feeds if feeds else []
          }       
        )
    except Exception as e:
        logger.error(f"Error fetching RSS feeds: {str(e)}")
        return template.TemplateResponse(
          request=request,
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          name="components/rss/feeds.html",
          context={
            "title": "News RSS",
            "feeds": [],
            "error": "Failed to load feeds. Please try again later."
          }       
        )