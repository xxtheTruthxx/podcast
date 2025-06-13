from sqlmodel import SQLModel, Field

class PodcastEpisodeBase(SQLModel):
    title: str
    description: str
    host: str

class PodcastEpisode(PodcastEpisodeBase, table=True):
    __tablename__ = "podcasts"
    id: int | None = Field(default=None, primary_key=True)

class PodcastEpisodeCreate(PodcastEpisodeBase):
    pass