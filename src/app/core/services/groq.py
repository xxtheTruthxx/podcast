from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from typing import Any, Optional

from core.logger import logger
from core.config import settings

class GroqClient:
    def __init__(
            self,
            model: str,
            temperature: float = 0.6,
            max_retries: int = 2,
        ):
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            temperature=temperature,
            max_retries=max_retries,
            model=model
        )
        self.template: Optional[ChatPromptTemplate] = None

    def create_template(self, prompt: str) -> 'GroqClient':
        try:
            self.template = ChatPromptTemplate.from_messages(
                [
                    SystemMessage(
                        content=prompt
                    ),
                    ("user", "{input}")
                ]
            )
            return self
        except Exception as err:
            logger.error(err)

    async def ask(self, prompt: Any):
        chain = self.template | self.llm
        try:
            response = await chain.ainvoke(
                {"input": prompt}
            )
            return response.content
        except Exception as err:
            logger.error(err)