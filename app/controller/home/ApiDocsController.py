from app import Response, Resource, send_from_directory, Blueprint
import os
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.yaml"

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, 
    API_URL,
    config={"app_name": "TEMPLATE FLASK API"}
)

class ApiDocsResource(Resource):
    
    def get(self):
        """Mengembalikan URL dokumentasi API"""
        return Response().success({
            "docs_url": SWAGGER_URL,
            "swagger_spec": API_URL
        }, "Api Docs")

def serve_swagger_yaml(filename):
    """Route untuk mengakses file YAML statis"""
    static_folder = os.path.join(os.getcwd(), "static")
    return send_from_directory(static_folder, filename)