from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from utils_api.role_api import role_required
from controllers.users_controllers.history_controller import HistoryController

blp = Blueprint("history", __name__, description="history")


@blp.route("/history/all")
class ViewAllHistory(MethodView):
    @role_required(["admin"])
    @jwt_required()
    def get(self):
        self.history_controller = HistoryController()
        response = self.admin_controller.view_all_history()
        return response


@blp.route("/history")
class ViewHistory(MethodView):
    @role_required(["premiumuser", "premium", "admin"])
    @jwt_required()
    def get(self):
        self.history_controller = HistoryController()
        response = self.history_controller.view_history()
        return response
