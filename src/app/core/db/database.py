# Third-party Dependencies
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

# Local Dependencies
from core.config import DB_URL

# Create an async engine instance
async_engine = create_async_engine(DB_URL, echo=True, pool_pre_ping=True)

# Create a reusable Session class for consistent database interactions 
async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# async def init_db():
    # """
    # Create the database tables.
    # """
    # async with async_engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.create_all)