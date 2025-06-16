from typing import List, Literal, Optional, Dict, Any
import warnings

# Third-party Dependencies
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
import aiohttp
from bs4 import (
    BeautifulSoup,
    XMLParsedAsHTMLWarning
)

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
    
    @staticmethod
    async def request(
        method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
        url: str,
        params: Optional[Dict[Any, Any]] = None,
        data: Optional[Dict[Any, Any]] = None,
        headers: Optional[Dict[Any, Any]] = None,
        response_type: Literal["text", "json", "bytes", "xml"] = "text",
    ):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    headers=headers
                ) as response:
                    if 200 <= response.status < 300:
                        if response_type == "text":
                            return await response.text()
                        elif response_type == "json":
                            return await response.json()
                        elif response_type == "bytes":
                            return await response.read()
                        elif response_type == "xml":
                            warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
                            markup = await response.text()
                            return BeautifulSoup(markup, "lxml")
                        else:
                            raise aiohttp.ClientError(f"Unsupported response_type: {response_type}")
                    else:
                        raise aiohttp.ClientError(f"Unexpected status code: {response.status}")
            except aiohttp.ClientError as err:
                logger.error(f"HTTP Request failed: {err}")