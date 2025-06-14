from contextlib import asynccontextmanager

# Third-party Dependencies
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI

# Local Dependencies
from core.config import settings
from api.api import api_router
from core.db.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

# Initilize an application
app = FastAPI(
    title=settings.NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix=settings.API_V1_STR)