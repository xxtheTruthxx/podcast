from typing import List

# Third-party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

# Local Dependencies
from core.config import TypeSQL

class BaseCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        obj: type[TypeSQL],
    ) -> TypeSQL:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def read_all(
            self,
            db_obj: type[TypeSQL],
        ) -> List[type[TypeSQL]]:
        statement = select(db_obj)
        result = await self.session.execute(statement)
        return result.scalars().all()