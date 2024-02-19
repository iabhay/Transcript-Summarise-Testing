"""Module for defining History Route"""

from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from utils.utils_api.role_api import role_required
from controllers.users_controllers.history_controller import HistoryController

"""
History Resource Endpoints
1. /history/all [GET] for fetching all users history, can be accessed by admin only.
2. /history [GET] for fetching particular user history based on query parameter.
"""

blp = Blueprint("history", __name__, description="history")


@blp.route("/history/all")
class ViewAllHistory(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    get() -> Method to get history of all users
    """

    @role_required(["admin"])
    @jwt_required()
    def get(self):
        """
        Method to get request which verifies jwt and fetch history of all users
        Roles allowed -> admin
        Parameter -> self
        Return Type -> Json
        """
        self.history_controller = HistoryController()
        response = self.history_controller.view_all_history()
        return response


@blp.route("/history")
class ViewHistory(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    get() -> Method to get history of user
    """

    @role_required(["premiumuser", "admin"])
    @jwt_required()
    def get(self):
        """
        Method to get request which verifies jwt and fetch history of user
        Roles allowed -> admin, premium user
        Parameter -> self
        Return Type -> Json
        """
        self.history_controller = HistoryController()
        response = self.history_controller.view_history()
        return response
