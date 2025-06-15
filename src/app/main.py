from contextlib import asynccontextmanager

# Third-party Dependencies
from starlette.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from fastapi import FastAPI

# Local Dependencies
from core.config import settings
from api.api import api_router
from core.db.database import async_engine

# delete this

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database tables
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await async_engine.dispose()

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