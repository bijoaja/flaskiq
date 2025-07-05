from app import Blueprint, Api
from app.controller.home import HomeResource, ApiDocsResource
from app.controller.home.ApiDocsController import swaggerui_blueprint

main_bp = Blueprint("main", __name__, url_prefix="/api")
api = Api(main_bp)

# MAIN ROUTES
api.add_resource(HomeResource, "/")
main_bp.register_blueprint(swaggerui_blueprint, url_prefix="/docs")

