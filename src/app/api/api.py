# Third-party Dependencies
from fastapi import APIRouter

# Local Dependencies
from core.config import settings
from .routes import (
  podcast,
  podcast_api,
  rss,
  admin
)

# Create an APIRouter instance
api_router = APIRouter()

# Include routers
api_router.include_router(podcast.router, prefix="/podcast")
api_router.include_router(podcast_api.router, prefix=f"{settings.API_V1_STR}/podcast")
api_router.include_router(rss.router, prefix="/rss")
api_router.include_router(admin.router)