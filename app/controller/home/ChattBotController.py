from app import request, Response
from app.service.prompts import HomePrompts
import requests
import os
import json

class ChattBot:
    
    @staticmethod
    def generator_with_stream(response):
        for chunk in response.iter_lines():
            if chunk:
                try:
                    result = json.loads(chunk.decode('utf-8'))
                    if result.get('message') and result.get('message').get('content'):
                        yield result.get('message').get('content')
                except json.JSONDecodeError:
                    continue

    @staticmethod
    def chatbot():
        prompt = HomePrompts()
        system_prompt = prompt.home_prompt()

        data = request.get_json()
        user_message = data.get("message")
        try:
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
            return Response(stream_mode=True).success(
                chunks=ChattBot.generator_with_stream(response=ollama_response),
                content_type="text/plain"
            )

        except Exception as e:
            return Response().invalid(is_success=False, values=None, message=f"Terjadi Kesalahan: {str(e)}")