# from flask import Flask
from flask.views import MethodView
from flask_smorest import Blueprint, abort

# from flask_jwt_extended import jwt_required
# from utils_api.role_api import role_required
from utils_api.schemas import UserSchema
from controllers.auth.login_controller import LoginController


blp = Blueprint("login", __name__, description="login")


@blp.route("/login")
class LoginEndpoint(MethodView):
    def __init__(self):
        self.login_controller = LoginController()

    @blp.arguments(UserSchema)
    def post(self, user_data):
        response = self.login_controller.verify_user(user_data)
        return response
