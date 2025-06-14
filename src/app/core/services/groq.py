from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
import json 

from typing import Any, Optional

from core.logger import logger
from core.config import settings, TypeModel

class GroqClient:
    def __init__(
            self,
            model: str,
            temperature: float,
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
        self.template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=prompt
                ),
                ("user", "{input}")
            ]
        )
        return self

    async def ask(self, prompt: Any):
        chain = self.template | self.llm
        try:
            response = await chain.ainvoke(
                {"input": prompt}
            )
            return response.content
        except Exception as err:
            logger.error(err)