from typing import List, Optional

# Third-party Dependencies
from fastapi import (
    APIRouter,
    status,
    Request
)

from fastapi.templating import Jinja2Templates

# Local Dependencies
from core.config import settings
from core.models.rss import (
    RssFeed,
)
from crud import RssCRUD 

# Initialize Jinja2 template 
template = Jinja2Templates(directory="templates")

router = APIRouter(tags=["RSS Feed"])

@router.get("/feeds",
    response_model=List[RssFeed],
    status_code=status.HTTP_200_OK)
async def fetch_rss_feed(
    request: Request,
    offset: int = 0,
    limit: Optional[int] = None,
):
    """
    Fetch all episodes from the RSS Feed.      
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