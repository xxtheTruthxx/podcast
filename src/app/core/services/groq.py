from typing import Any, Optional

# Third-party Dependencies
from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage

# Local Dependencies
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
        """
        Create a prompt template for the chat model.
        """
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
            logger.error(
                {"msg": "An error occured while creating prompt template.",
                 "error": err
                })

    async def ask(self, prompt: Any):
        """
        Provide a prompt for the chat model.
        """
        chain = self.template | self.llm
        try:
            response = await chain.ainvoke(
                {"input": prompt}
            )
            return response.content
        except Exception as err:
            logger.error(
                {"msg": "An error occurred while chatting with chat model.",
                 "error": err
                })