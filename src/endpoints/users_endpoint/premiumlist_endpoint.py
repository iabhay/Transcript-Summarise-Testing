from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils_api.schemas import PremiumListSchema, UrlInputSchema
from utils_api.role_api import role_required
from controllers.users_controllers.premiumlist_controller import PremiumlistController

blp = Blueprint("premiumlist", __name__, description="premiumlist")


@blp.route("/premiumlist")
class PremiumList(MethodView):
    @role_required(["admin"])
    @jwt_required()
    @blp.arguments(PremiumListSchema)
    def post(self, url_req):
        identity = get_jwt_identity()
        self.admin_controller = PremiumlistController(identity)
        response = self.admin_controller.premium_list(url_req)
        return response

    @role_required(["premiumuser", "premium", "admin"])
    @jwt_required()
    def get(self):
        self.premium_controller = PremiumlistController()
        response = self.premium_controller.view_premium_list()


@blp.route("/premiumlist-request")
class PremiumList(MethodView):
    @role_required(["premium", "premiumuser"])
    @jwt_required()
    @blp.arguments(UrlInputSchema)
    def post(self, url_req):
        self.premium_controller = PremiumlistController()
        response = self.premium_controller.premium_list(url_req)
        return response
