import os
import json
import requests
from app.service.prompts import HomePrompts


class ChatbotService:

    @staticmethod
    def get_generator(user_message: str):
        """Returns a generator that streams Ollama response chunks."""
        prompt = HomePrompts()
        system_prompt = prompt.home_prompt()

        ollama_response = requests.post(
            os.getenv("OLLAMA_HOST"),
            json={
                "model": "mistral",
                "messages": [
                    system_prompt,
                    {"role": "user", "content": user_message}
                ],
                "stream": True
            },
            stream=True
        )

        return ChatbotService._stream_chunks(ollama_response)

    @staticmethod
    def _stream_chunks(response):
        for chunk in response.iter_lines():
            if chunk:
                try:
                    result = json.loads(chunk.decode('utf-8'))
                    content = result.get('message', {}).get('content')
                    if content:
                        yield content
                except json.JSONDecodeError:
                    continue
