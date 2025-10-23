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

  feeds = await RssCRUD.fetch_all(
    url=settings.RSS_URL,
  )
  
  for feed in feeds:
    if feed.uuid == uuid:
      return template.TemplateResponse(
        request=request,
        name="components/rss/feed.html",
        context={
          "title": f"{settings.NAME} | {feed.title}",
          "feed": feed
        }       
      )
  else:
    return template.TemplateResponse(
      request=request,
      name="components/notFound.html"
    )

@router.get("/feed/{uuid}/add")
async def load_feed(
  request: Request,
  uuid: str,
  session: AsyncSessionDep
):
  """
  Fetch feed from the RSS Feed.
  """

  feeds = await RssCRUD.fetch_all(
    url=settings.RSS_URL,
  )
  
  for feed in feeds:
    if feed.uuid == uuid:
      episode = PodcastEpisode(
        title=feed.title,
        description=feed.description,
        host=feed.author
      )
      await PodcastCRUD(session).create(episode)
    else:
      return template.TemplateResponse(
        request=request,
        name="components/rss/feeds.html",
        context={
          "feeds": feeds
        }       
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
    feeds = await RssCRUD.fetch_all(
        url=settings.RSS_URL,
        offset=offset,
        limit=limit
    )
    return template.TemplateResponse(
      request=request,
      name="components/rss/feeds.html",
      context={
        "feeds": feeds
      }       
    )