# Built-in Dependencies
from typing import Annotated, AsyncGenerator

# Third-party Dependencies
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

# Local Dependencies
from core.db.database import async_session
from core.logger import logger

# Define an async function to get the database session
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to provice the async session object"""
    async with async_session() as session:
            yield session
              
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]