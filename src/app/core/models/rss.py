from pydantic import BaseModel

class RSSFeed(BaseModel):
    title: str
    url: str