from typing import Literal

# Third-party Dependencies
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class PodcastEpisodeBase(SQLModel):
    title: str
    description: str
    host: str

class PodcastEpisode(SQLModel, table=True):
    __tablename__ = "podcasts"
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    host: str

class PodcastEpisodeGenerate(BaseModel):
    target: Literal["title", "description"]
    prompt: str

class PodcastEpisodeAlternative(PodcastEpisodeGenerate):
    original_episode: PodcastEpisodeBase
    generated_alternative: str
