import os
from typing import Generator

from app.service.agent.base_agent import BaseAgent


class OpenAIAgent(BaseAgent):
    """LLM agent backed by the OpenAI API via LangChain streaming."""

    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def get_generator(self, user_message: str, system_prompt: dict) -> Generator:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import SystemMessage, HumanMessage

        llm = ChatOpenAI(
            model=self.model,
            api_key=os.getenv("AI_KEY", ""),
            streaming=True,
        )
        messages = [
            SystemMessage(content=system_prompt["content"]),
            HumanMessage(content=user_message),
        ]
        return self._stream_chunks(llm.stream(messages))

    @staticmethod
    def _stream_chunks(stream) -> Generator:
        for chunk in stream:
            if chunk.content:
                yield chunk.content
