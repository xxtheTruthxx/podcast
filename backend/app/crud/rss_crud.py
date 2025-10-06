from typing import List

# Local Dependencies
from . import BaseCRUD
from core.models.rss import RssFeed
import requests

from bs4 import (
  BeautifulSoup,
  XMLParsedAsHTMLWarning
)
import warnings

class RssCRUD(BaseCRUD):
    def __init__(self, session):
        super().__init__(session)

    @classmethod
    async def fetch_all(
        cls,
        *,
        url: str,
        **kwargs,
    ) -> List[RssFeed]:
        """
        Fetch all RSS feeds from URL.
        """
        offset, limit = kwargs.get("offset"), kwargs.get("limit")
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; MyPodcastFetcher/1.0; +https://example.com"})
        warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
        soup = BeautifulSoup(response.content, "lxml")
        feeds = [
            RssFeed(
                title=item.title.text,
                description=item.description.text
            )
            for item in soup.find_all("item")
        ][offset:]
        return feeds[:limit] if limit else feeds