from flask_restful import Resource
from flask_swagger_ui import get_swaggerui_blueprint
from utils import Response
from app.service.api.v1 import DocsApiService

SWAGGER_URL = "/api/v1/docs"
API_URL     = "/static/swagger.yaml"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "TEMPLATE FLASK API"}
)


class ApiDocsResource(Resource):
    def get(self):
        info = DocsApiService.get_info()
        return Response().success(values=info, message="Api Docs")
