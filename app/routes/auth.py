from flask import Blueprint
from app.controller.auth.auth_controller import AuthView

auth_view_bp = Blueprint("auth", __name__)

auth_view_bp.add_url_rule("/login",    view_func=AuthView.login_page,    endpoint="login",    methods=["GET"])
auth_view_bp.add_url_rule("/register", view_func=AuthView.register_page, endpoint="register", methods=["GET"])
