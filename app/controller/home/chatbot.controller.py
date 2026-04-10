from flask import request
from utils import Response
from app.service.api.v1 import ChatbotService


class ChatbotView:
    @staticmethod
    def chatbot():
        data = request.get_json()
        user_message = data.get("message")
        try:
            generator = ChatbotService.get_generator(user_message)
            return Response(stream_mode=True).success(
                chunks=generator,
                content_type="text/plain"
            )
        except Exception as e:
            return Response().invalid(
                is_success=False, values=None,
                message=f"Terjadi Kesalahan: {str(e)}"
            )
