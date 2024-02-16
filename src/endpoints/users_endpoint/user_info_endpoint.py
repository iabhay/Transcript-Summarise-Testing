"""Module for User Related Route"""

from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from utils.utils_api.role_api import role_required
from controllers.users_controllers.user_info_controller import UserInfoController

"""
All endpoints related to user are here. (To access all these jwt is required.)
1. /user/profile endpoint for showing profile for the user.
2. /upgrade used for upgrading the role of user from non premium to premium.
3. /downgrade used for downgrading the role of user from premium to nonpremium.
4. /users to get data of all users, can be accessed by only admin.
5. /user/ban for banning user, can be accessed by admin.
6. /user/unban for unbanning user, can be accessed by admin.
Each endpoint can generate different response according to the role of user who hitted the endpoint.
This behaviour is handled in User info Logic.
"""

blp = Blueprint("user", __name__, description="user endpoints")


@blp.route("/user/profile")
class UserViewEndpoint(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    get() -> Method to get user details
    """

    @jwt_required()
    def get(self):
        """
        Method to get request which verifies jwt and get user details
        Roles allowed -> anyone
        Parameter -> self
        Return Type -> Json
        """
        self.user_info_controller = UserInfoController()
        response = self.user_info_controller.view_user()
        return response


@blp.route("/upgrade")
class UpgradeUser(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    put() -> Method to upgrade user
    """

    @jwt_required()
    def put(self):
        """
        Method to put request which verifies jwt and upgrade user role
        Roles allowed -> anyone
        Parameter -> self
        Return Type -> Json
        """
        self.user_info_controller = UserInfoController()
        response = self.user_info_controller.upgrade_non_premium_user()
        return response


@blp.route("/downgrade")
class DowngradeUser(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    put() -> Method to downgrade user
    """

    @jwt_required()
    def put(self):
        """
        Method to put request which verifies jwt and downgrade user role
        Roles allowed -> anyone
        Parameter -> self
        Return Type -> Json
        """
        self.user_info_controller = UserInfoController()
        response = self.user_info_controller.downgrade_premium_user()
        return response


@blp.route("/users")
class AdminAllUsersViewEndpoint(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    get() -> Method to get all users details
    """

    @role_required(["admin"])
    @jwt_required()
    def get(self):
        """
        Method to get request which verifies jwt and get all users details
        Roles allowed -> admin
        Parameter -> self
        Return Type -> Json
        """
        self.admin_controller = UserInfoController()
        response = self.admin_controller.view_all_users()
        return response


@blp.route("/user/ban")
class BanUser(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    put() -> Method to ban user
    """

    @role_required(["admin"])
    @jwt_required()
    def put(self):
        """
        Method to put request which verifies jwt and ban user
        Roles allowed -> admin
        Parameter -> self
        Return Type -> Json
        """
        self.user_info_controller = UserInfoController()
        response = self.user_info_controller.ban_user()
        return response


@blp.route("/user/unban")
class UnbanUser(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    put() -> Method to unban user
    """

    @role_required(["admin"])
    @jwt_required()
    def put(self):
        """
        Method to put request which verifies jwt and unban user
        Roles allowed -> admin
        Parameter -> self
        Return Type -> Json
        """
        self.user_info_controller = UserInfoController()
        response = self.user_info_controller.unban_user()
        return response
