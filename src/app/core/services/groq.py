from litellm import acompletion
# from groq import Groq

from core.logger import logger
from core.config import settings 

class GroqClient:
    def __init__(self, model: str):
        self.model = model
    
    async def chat(self, message):
        try:
            response = await acompletion(
                model=f"groq/{self.model}",
                messages=message,
                stream=True
            )
        except Exception as err:
            logger.error(err)
            pass
        print(response)
        return response    