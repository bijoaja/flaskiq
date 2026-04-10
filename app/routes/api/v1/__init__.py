from flask import Blueprint
from flask_restful import Api, Resource
from flask import jsonify

from app.controller.api.v1.auth_controller import AuthRegisterResource, AuthLoginResource
from app.controller.api.v1.chatbot_controller import ChatbotResource
from app.controller.api.v1.cms_controller import CmsListResource, CmsDetailResource
from app.controller.api.v1.docs_controller import ApiDocsResource, swaggerui_blueprint

api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api = Api(api_v1_bp)

# ── Welcome ───────────────────────────────────────────────────────────────────
class WelcomeResource(Resource):
    def get(self):
        return {"success": True, "data": {"name": "FlaskIQ API", "version": "2.0.0"}, "message": "Welcome"}

api.add_resource(WelcomeResource,         "/")
api.add_resource(AuthRegisterResource,    "/auth/register")
api.add_resource(AuthLoginResource,       "/auth/login")
api.add_resource(ChatbotResource,         "/chatbot")
api.add_resource(CmsListResource,         "/cms")
api.add_resource(CmsDetailResource,       "/cms/<int:page_id>")
api.add_resource(ApiDocsResource,         "/docs/info")

api_v1_bp.register_blueprint(swaggerui_blueprint, url_prefix="/docs")
