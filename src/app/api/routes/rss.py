from typing import List, Optional
import warnings

# Third-party Dependencies
from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Body
)
from bs4 import (
    BeautifulSoup,
    XMLParsedAsHTMLWarning
)
import aiohttp

# Local Dependencies
from core.logger import logger
from core.config import settings
from core.models.rss import RSSFeed

router = APIRouter(tags=["RSS Feed"])

@router.get("/",
    response_model=List[RSSFeed],
    status_code=status.HTTP_200_OK)
async def fetch_rss_feed(
    length: Optional[int] = None
):
    async with aiohttp.ClientSession() as http:
        try:
            async with http.get(settings.RSS_ENDPOINT) as response:
                if response.status == 200:
                    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
                    markup = await response.text()
                    soup = BeautifulSoup(markup, "lxml")                
                    
                    episodes = []
                    for item in soup.find_all("item"):
                        episode = RSSFeed(
                            title=item.title.text,
                            url=item.link.next_sibling.strip()
                        )
                        episodes.append(episode)
                    return episodes[:length] if length else episodes
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid status code."
                    )
        except aiohttp.ClientError as err:
            logger.error(f"HTTP Request failed: {err}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="An error occured while requesting to the resource."
            )
        
# Optionally, allow adding an RSS episode as a new episode in your app.