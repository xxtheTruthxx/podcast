# Third-party Dependencies
from fastapi import APIRouter

# Local Dependencies
from .routes import (
    podcast   
)

# Create an APIRouter instance
api_router = APIRouter()

# Include routers
api_router.include_router(podcast.router, prefix="/podcast")