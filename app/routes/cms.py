from flask import Blueprint
from app.controller.cms.cms_controller import CmsView

cms_bp = Blueprint("cms", __name__, url_prefix="/cms")

cms_bp.add_url_rule("/",            view_func=CmsView.index,       endpoint="cms_index", methods=["GET"])
cms_bp.add_url_rule("/page/<slug>", view_func=CmsView.page_detail, endpoint="cms_detail", methods=["GET"])
