from abc import ABC, abstractmethod
from typing import Generator


class BaseAgent(ABC):
    """Abstract base for all LLM provider agents."""

    @abstractmethod
    def get_generator(self, user_message: str, system_prompt: dict) -> Generator:
        """Return a generator that yields response text chunks."""
        ...
