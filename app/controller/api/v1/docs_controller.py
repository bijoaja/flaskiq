from flask_restful import Resource
from flask_swagger_ui import get_swaggerui_blueprint

from utils import Response

SWAGGER_URL = "/api/v1/docs"
API_URL     = "/static/swagger.yaml"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": "FlaskIQ API"},
)


class ApiDocsResource(Resource):

    def get(self):
        return Response().success(
            is_success=True,
            values={"docs_url": SWAGGER_URL, "swagger_spec": API_URL},
            message="API Documentation",
        )
