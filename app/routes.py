from app import Blueprint, Api
from app.controller.home import HomeView, ChatbotView
from app.controller.cms import CmsView
from app.controller.api.v1 import (
    HomeResource, ChatbotResource, ApiDocsResource,
    CmsListResource, CmsDetailResource, swaggerui_blueprint
)

# ── API v1 Blueprint ─────────────────────────────────────────────────────────
api_v1_bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")
api = Api(api_v1_bp)

api.add_resource(HomeResource,      "/")
api.add_resource(ChatbotResource,   "/chatbot")
api.add_resource(ApiDocsResource,   "/docs/info")
api.add_resource(CmsListResource,   "/cms")
api.add_resource(CmsDetailResource, "/cms/<int:page_id>")

api_v1_bp.register_blueprint(swaggerui_blueprint, url_prefix="/docs")

# ── View Blueprint ────────────────────────────────────────────────────────────
# Blueprint name kept as "view" so url_for('view.home') in templates still works
view_bp = Blueprint("view", __name__, url_prefix="/")

view_bp.add_url_rule("/",                view_func=HomeView.home,          endpoint="home")
view_bp.add_url_rule("/chatbot",         view_func=ChatbotView.chatbot,    methods=["POST"], endpoint="chatbot")
view_bp.add_url_rule("/cms",             view_func=CmsView.index,          endpoint="cms_index")
view_bp.add_url_rule("/cms/page/<slug>", view_func=CmsView.page_detail,    endpoint="cms_detail")
