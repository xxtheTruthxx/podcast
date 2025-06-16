from typing import List

# Local Dependencies
from . import BaseCRUD
from core.models.rss import RssFeed

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
        offset, limit = kwargs.get("offset"), kwargs.get("limit")
        soup = await BaseCRUD.request("GET", url, response_type="xml")
        feeds = [
            RssFeed(
                title=item.title.text,
                url=item.link.next_sibling.strip()
            )
            for item in soup.find_all("item")
        ][offset:]
        return feeds[:limit] if limit else feeds