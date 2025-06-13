from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class PodcastEpisodeBase(SQLModel):
    title: str
    description: str
    host: str

class PodcastEpisode(PodcastEpisodeBase, table=True):
    __tablename__ = "podcasts"
    id: int | None = Field(default=None, primary_key=True)

class PodcastEpisodeCreate(PodcastEpisodeBase):
    pass

class PodcastEpisodeGenerate(BaseModel):
    title: str
    prompt: str

class PodcastEpisodeAlternative(PodcastEpisodeGenerate):
    original_episode: PodcastEpisodeBase
    generated_alternative: str
