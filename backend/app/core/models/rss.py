# Third-party Dependencies
from pydantic import BaseModel

class RssFeed(BaseModel):
    title: str
    description: str
    
class RssFeedPost(BaseModel):
    title: str