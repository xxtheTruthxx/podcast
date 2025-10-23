from sqlmodel import select

# Local Dependencies
from .base_crud import BaseCRUD
from core.models.podcast import (
    PodcastEpisodeBase,
    PodcastEpisode
)

class PodcastCRUD(BaseCRUD):
    def __init__(self, session):
        super().__init__(session)

    async def read_by_id(self, id: int) -> PodcastEpisodeBase:
       """
       Fetch the podcast using its `id`.
       """
       statement = select(PodcastEpisode).where(PodcastEpisode.id == id)
       result = await self.session.execute(statement)
       return result.scalar_one_or_none()
    
    async def update(self, id: int, data: dict) -> PodcastEpisodeBase:
        """
        Update a podcast episode by id.
        """
        result = await self.session.execute(select(PodcastEpisode).where(PodcastEpisode.id == id))
        episode = result.scalar_one_or_none()
        if not episode: 
            return None
        for key, value in data.items():
            if hasattr(episode, key):
                setattr(episode, key, value)
        self.session.add(episode)
        await self.session.commit()
        await self.session.refresh(episode)

        return episode

    async def remove_by_id(self, id: int):
      """
      Delete a podcast episode by id.
      """
      statement = select(PodcastEpisode).where(PodcastEpisode.id == id)
      result = await self.session.execute(statement)
      instance = result.scalar_one_or_none()
      if instance:
        await self.session.delete(instance)
        await self.session.commit()
      else:
        return None