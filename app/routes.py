from app import Blueprint, Api
from app.controller.home import HomeResource, ApiDocsResource, ViewHome, ChattBot
from app.controller.home.ApiDocsController import swaggerui_blueprint

# MAIN ROUTES API
api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

# ADD ROUTES API
api.add_resource(HomeResource, "/")
api_bp.register_blueprint(swaggerui_blueprint, url_prefix="/docs")

# MAIN ROUTES VIEW
view_bp = Blueprint("view", __name__, url_prefix="/")

# ADD ROUTES VIEW
view_bp.add_url_rule("/", view_func=ViewHome.home)
view_bp.add_url_rule("/chatbot", view_func=ChattBot.chatbot, methods=["POST"], endpoint="chatbot")