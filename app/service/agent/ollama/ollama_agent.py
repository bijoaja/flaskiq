import os
import json
import requests
from typing import Generator

from app.service.agent.base_agent import BaseAgent


class OllamaAgent(BaseAgent):
    """LLM agent backed by a local Ollama server."""

    def __init__(self, model: str | None = None, host: str | None = None):
        self.model = model or os.getenv("OLLAMA_MODEL", "mistral")
        self.host  = host  or os.getenv("OLLAMA_HOST", "http://localhost:11434")

    def get_generator(self, user_message: str, system_prompt: dict) -> Generator:
        response = requests.post(
            f"{self.host}/api/chat",
            json={
                "model":    self.model,
                "messages": [system_prompt, {"role": "user", "content": user_message}],
                "stream":   True,
            },
            stream=True,
            timeout=60,
        )
        return self._stream_chunks(response)

    @staticmethod
    def _stream_chunks(response) -> Generator:
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    content = data.get("message", {}).get("content")
                    if content:
                        yield content
                except (json.JSONDecodeError, UnicodeDecodeError):
                    continue
