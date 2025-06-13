from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from typing import List

from core.models.base import TypeSQL

class BaseCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            create_obj: TypeSQL,
            return_obj: TypeSQL
        ) -> TypeSQL:
        self.session.add(create_obj)
        await self.session.commit()
        await self.session.refresh(create_obj)
        result = return_obj(**create_obj.model_dump())
        return result
    
    async def read_all(
            self,
            db_obj: TypeSQL
        ) -> List[TypeSQL]:
        statement = select(db_obj)
        result = await self.session.execute(statement)
        return result.scalars().all()