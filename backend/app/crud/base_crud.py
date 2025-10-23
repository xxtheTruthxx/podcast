from typing import List
import warnings

# Third-party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

# Local Dependencies
from core.config import TypeSQL
from core.logger import logger

class BaseCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        obj: type[TypeSQL],
    ) -> TypeSQL:
        """
        Create an object.
        """
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def read_all(
            self,
            obj: type[TypeSQL],
            **kwargs,
        ) -> List[type[TypeSQL]]:
        """
        Read all objects from the table.
        """
        offset, limit = kwargs.get("offset"), kwargs.get("limit")
        statement = select(obj).offset(offset).limit(limit)
        result = await self.session.execute(statement)
        return result.scalars().all()