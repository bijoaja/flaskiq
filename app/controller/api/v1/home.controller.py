from flask_restful import Resource
from utils import Response
from app.service.api.v1 import HomeApiService


class HomeResource(Resource):
    def get(self):
        message = HomeApiService.welcome_message()
        return Response().success(values=None, message=message)
