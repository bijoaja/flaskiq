from flask import render_template


class AuthView:

    @staticmethod
    def login_page():
        return render_template("auth/login.html")

    @staticmethod
    def register_page():
        return render_template("auth/register.html")
