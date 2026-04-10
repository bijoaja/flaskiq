from flask import render_template
from app.service import HomeService


class HomeView:
    @staticmethod
    def home():
        context = HomeService.get_context()
        return render_template("home/index.html", **context)
