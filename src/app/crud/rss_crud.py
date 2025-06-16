from typing import Optional, List
import warnings

# Third-party Dependencies
from bs4 import (
    BeautifulSoup,
    XMLParsedAsHTMLWarning
)
import aiohttp

# Local Dependencies
from . import BaseCRUD
from core.logger import logger
from core.models.rss import RssFeed

class RssCRUD(BaseCRUD):
    def __init__(self, session):
        super().__init__(session)


    @classmethod
    async def get_all(
        cls,
        *,
        url: str,
        length: Optional[int] = None
    ) -> List[RssFeed]:
        soup = await cls._fetch_rss(url=url)
        feeds = [
            RssFeed(
                title=item.title.text,
                url=item.link.next_sibling.strip()
            )
            for item in soup.find_all("item")
        ]
        return feeds[:length] if length else feeds
            
    @classmethod
    async def _fetch_rss(cls, url: str) -> BeautifulSoup:
        async with aiohttp.ClientSession() as http:
            try:
                async with http.get(url=url) as response:
                    if response.status == 200:
                        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
                        markup = await response.text()
                        return BeautifulSoup(markup, "lxml") 
                    else:
                        raise aiohttp.ClientError(f"Unexpected status code: {response.status}")
            except aiohttp.ClientError as err:
                logger.error(f"HTTP Request failed: {err}")