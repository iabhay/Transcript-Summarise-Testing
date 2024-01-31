# from flask import Flask
from flask.views import MethodView
from flask_smorest import Blueprint, abort

# from flask_jwt_extended import jwt_required
# from utils_api.role_api import role_required
from utils_api.schemas import UserSchema
from controllers.auth.register_controller import RegisterController


blp = Blueprint("register", __name__, description="register")


@blp.route("/signup")
class RegisterEndpoint(MethodView):
    def __init__(self):
        self.register_controller = RegisterController()

    @blp.arguments(UserSchema)
    def post(self, user_data):
        response = self.register_controller.add_user(user_data)
        return response
