import os
from app.service.agent.tools.base_tool import BaseTool


class RAGTool(BaseTool):
    """Retrieval tool that loads README.md as the chatbot's knowledge base.

    Extensible: swap `_load` for a vector-store retrieval call when needed.
    """

    name = "rag_search"
    description = "Searches the FlaskIQ knowledge base for relevant context."

    def __init__(self, knowledge_path: str = "README.md"):
        self._knowledge = self._load(knowledge_path)

    def _load(self, path: str) -> str:
        abs_path = os.path.join(os.path.dirname(__file__), "../../../../..", path)
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return "Knowledge base not available."

    def run(self, input: str) -> str:
        return self._knowledge

    def as_system_prompt(self) -> dict:
        return {
            "role": "system",
            "content": (
                "You are FlaskIQ Assistant — a helpful AI embedded in the FlaskIQ template. "
                "Answer questions concisely using the project context below.\n\n"
                f"{self._knowledge}"
            ),
        }
