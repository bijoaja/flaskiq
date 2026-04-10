from flask import Blueprint
from app.controller.landing.landing_controller import LandingView

landing_bp = Blueprint("landing", __name__)

landing_bp.add_url_rule("/", view_func=LandingView.index, endpoint="home", methods=["GET"])
