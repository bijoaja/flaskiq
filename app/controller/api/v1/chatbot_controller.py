from flask import request
from flask_restful import Resource

from utils import Response
from app.service.agent.chatbot_service import ChatbotService


class ChatbotResource(Resource):

    def post(self):
        data = request.get_json() or {}
        user_message = data.get("message", "").strip()
        if not user_message:
            return Response().invalid(
                is_success=False, values=None,
                message="Field 'message' is required.",
                code=400,
            )
        try:
            generator = ChatbotService.get_generator(user_message)
            return Response(stream_mode=True).success(chunks=generator, content_type="text/plain")
        except Exception as e:
            return Response().invalid(is_success=False, values=None, message=str(e), code=500)
