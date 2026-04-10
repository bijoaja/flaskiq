from abc import ABC, abstractmethod


class BaseTool(ABC):
    name: str = ""
    description: str = ""

    @abstractmethod
    def run(self, input: str) -> str:
        """Execute the tool with the given input and return a result string."""
        ...
