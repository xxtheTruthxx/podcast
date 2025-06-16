# Third-party Dependencies
from pydantic import BaseModel

class RssFeed(BaseModel):
    title: str
    url: str

class RssFeedPost(BaseModel):
    title: str