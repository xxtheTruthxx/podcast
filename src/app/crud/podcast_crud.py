from sqlmodel import select

from .base import BaseCRUD

from core.models.podcast import (
    PodcastEpisodeBase,
    PodcastEpisode
)

class PodcastCRUD(BaseCRUD):
    def __init__(self, session):
        super().__init__(session)

    async def get_by_id(self, id: int) -> PodcastEpisodeBase:
       statement = select(PodcastEpisode).where(PodcastEpisode.id == id)
       result = await self.session.execute(statement)
       return result.scalar_one_or_none()
        