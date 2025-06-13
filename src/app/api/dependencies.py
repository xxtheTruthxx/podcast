from fastapi import Depends
from typing import Annotated, AsyncGenerator
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from core.db.database import async_session
from core.logger import logger

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to provice the async session object"""
    async with async_session() as session:
            try:
                yield session
            except SQLAlchemyError as err:
                logger.critical(f"[x] An error occured while processing with database: {err}")
                 
AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]