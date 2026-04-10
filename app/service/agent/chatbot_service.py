import os
from typing import Generator

from app.service.agent.tools.rag_tool import RAGTool


class ChatbotService:
    """Provider-agnostic chatbot service.

    Reads AI_PROVIDER env var ("ollama" or "openai") and dispatches to the
    correct agent. Adding a new provider requires only a new BaseAgent subclass
    and an extra branch here.
    """

    @staticmethod
    def get_generator(user_message: str) -> Generator:
        provider = os.getenv("AI_PROVIDER", "ollama").lower()
        system_prompt = RAGTool().as_system_prompt()

        if provider == "openai":
            from app.service.agent.openai.openai_agent import OpenAIAgent
            agent = OpenAIAgent()
        else:
            from app.service.agent.ollama.ollama_agent import OllamaAgent
            agent = OllamaAgent()

        return agent.get_generator(user_message, system_prompt)
