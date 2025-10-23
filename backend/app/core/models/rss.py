# Third-party Dependencies
from pydantic import BaseModel

class RssFeed(BaseModel):
    image_url: str
    date: str
    title: str
    description: str
    author: str
    origin: str
    uuid: str

class RssFeedPost(BaseModel):
    title: str