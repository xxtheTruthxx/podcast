from typing import List

# Local Dependencies
from . import BaseCRUD
from core.models.rss import RssFeed
import aiohttp

from bs4 import (
  BeautifulSoup,
  XMLParsedAsHTMLWarning
)
import warnings

class RssCRUD(BaseCRUD):
    def __init__(self, session):
        super().__init__(session)

    @classmethod
    def safe_extract(cls, item, tag_name:str, default=""):
       tag = item.find(tag_name)
       return tag.get_text(strip=True) if tag else default

    @classmethod
    async def extract_soup(cls, url:str) -> BeautifulSoup:
      headers = {"User-Agent": "Mozilla/5.0 (compatible; MyPodcastFetcher/1.0; +https://example.com"}

      async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
          content = await response.text()

      warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
      soup = BeautifulSoup(content, "lxml-xml")
      return soup

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
        offset = kwargs.get("offset", 0)
        limit = kwargs.get("limit", None)


        # Extract from xml
        soup = await cls.extract_soup(url)

        feeds = []
        author_elem = soup.find("itunes:author")
        author = author_elem.text.strip()
        for item in soup.find_all("item"):
          title = cls.safe_extract(item, "title")
          description = cls.safe_extract(item, "description")
          pub_date = cls.safe_extract(item, "pubDate")
          origin = cls.safe_extract(item, "link")
          uuid = cls.safe_extract(item, "guid")

          image_url = ""
          itunes_img = item.find("itunes:image")
          if itunes_img and itunes_img.get("href"):
            image_url = itunes_img["href"]
          else:
            media_thumb = item.find("media:thumbnail")
            if media_thumb and media_thumb.get("url"):
              image_url = media_thumb["url"]

          if title:
             feeds.append(
                RssFeed(
                   image_url=image_url,
                   title=title,
                   description=description,
                   author=author,
                   date=pub_date,
                   origin=origin,
                   uuid=uuid
                )
             )
              
        feeds = feeds[offset:]
        return feeds[:limit] if limit else feeds