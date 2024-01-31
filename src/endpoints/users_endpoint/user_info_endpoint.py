from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from utils_api.schemas import PremiumListSchema, UrlInputSchema
from utils_api.role_api import role_required

from controllers.users_controllers.user_info_controller import UserInfoController


blp = Blueprint("user", __name__, description="user endpoints")


@blp.route("/user/profile")
class UserViewEndpoint(MethodView):
    @jwt_required()
    def get(self):
        self.user_info_controller = UserInfoController()
        response = self.user_info_controller.view_user()
        return response


@blp.route("/upgrade")
class UpgradeUser(MethodView):
    @jwt_required()
    def put(self):
        self.user_info_controller = UserInfoController()
        response = self.user_info_controller.upgrade_non_premium_user()
        return response


@blp.route("/downgrade")
class DowngradeUser(MethodView):
    @jwt_required()
    def put(self):
        self.user_info_controller = UserInfoController()
        response = self.user_info_controller.downgrade_premium_user()
        return response


@blp.route("/users")
class AdminAllUsersViewEndpoint(MethodView):
    @role_required(["admin"])
    @jwt_required()
    def get(self):
        self.admin_controller = UserInfoController()
        response = self.admin_controller.view_all_users()
        return response


@blp.route("/user/ban")
class BanUser(MethodView):
    @role_required(["admin"])
    @jwt_required()
    def put(self):
        self.user_info_controller = UserInfoController()
        response = self.user_info_controller.ban_user()
        return response


@blp.route("/user/unban")
class UnbanUser(MethodView):
    @role_required(["admin"])
    @jwt_required()
    def put(self):
        self.user_info_controller = UserInfoController()
        response = self.user_info_controller.unban_user()
        return response
