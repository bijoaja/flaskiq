from flask import render_template
from app.service.landing_service import LandingService


class LandingView:

    @staticmethod
    def index():
        context = LandingService.get_context()
        return render_template("landing/index.html", **context)
