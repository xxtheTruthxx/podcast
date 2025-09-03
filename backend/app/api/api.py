# Third-party Dependencies
from fastapi import APIRouter

# Local Dependencies
from .routes import (
  podcast,
  webhook
)

# Create an APIRouter instance
api_router = APIRouter()

# Include routers
api_router.include_router(podcast.router, prefix="/podcast")
api_router.include_router(webhook.router, prefix="/webhook")