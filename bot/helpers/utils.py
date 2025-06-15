from typing import Optional
from aiohttp import ClientSession

from .logger import logger

class HTTPRequest:
    def __init__(self, url: str):
        self.url = url 


    async def request(
        self,
        method: str,
    ):
        if not self.session:
            self.session = ClientSession()

        try:
            async with self.session.request(
                method=method,
                url=self.url
            ) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    pass
        except Exception as err:
            logger.error()

    async def get(self):
        return await self.request("GET")

    async def __aenter__(self):
        self.session = ClientSession()
        return self  
    
    async def __aclose__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()