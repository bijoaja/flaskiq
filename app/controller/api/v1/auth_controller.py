from flask import request
from flask_restful import Resource

from utils import Response
from app.service.view.auth_service import AuthService


class AuthRegisterResource(Resource):

    def post(self):
        data = request.get_json() or {}
        required = {"username", "email", "password"}
        if not required.issubset(data.keys()):
            return Response().invalid(
                is_success=False, values=None,
                message="Fields 'username', 'email', and 'password' are required.",
                code=400,
            )
        try:
            user = AuthService.register(data["username"], data["email"], data["password"])
            return Response().success(is_success=True, values=user, message="User registered successfully.", code=201)
        except ValueError as e:
            return Response().invalid(is_success=False, values=None, message=str(e), code=409)


class AuthLoginResource(Resource):

    def post(self):
        data = request.get_json() or {}
        if not {"email", "password"}.issubset(data.keys()):
            return Response().invalid(
                is_success=False, values=None,
                message="Fields 'email' and 'password' are required.",
                code=400,
            )
        try:
            token = AuthService.login(data["email"], data["password"])
            return Response().success(is_success=True, values={"token": token}, message="Login successful.")
        except ValueError as e:
            return Response().invalid(is_success=False, values=None, message=str(e), code=401)
