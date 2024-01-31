from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from utils_api.schemas import UrlInputSchema
from utils_api.role_api import role_required
from controllers.users_controllers.url_controller import UrlController

blp = Blueprint("admin", __name__, description="admin")


# ban
@blp.route("/url/ban")
class BanUrl(MethodView):
    @role_required(["admin"])
    @jwt_required()
    @blp.arguments(UrlInputSchema)
    def post(self, url_input):
        self.url_controller = UrlController(url_input)
        response = self.url_controller.ban_url(url_input)
        return response

    @role_required(["admin"])
    @jwt_required()
    @blp.arguments(UrlInputSchema)
    def get(self, url_input):
        self.url_controller = UrlController(url_input)
        response = self.url_controller.view_ban_url(url_input)
        return response


@blp.route("/url/unban")
class UnbanUrl(MethodView):
    @role_required(["admin"])
    @jwt_required()
    @blp.arguments(UrlInputSchema)
    def delete(self, url_input):
        self.url_controller = UrlController(url_input)
        response = self.url_controller.unban_url(url_input)
        return response


@blp.route("/urls")
class ViewBanUrl(MethodView):
    @role_required(["admin"])
    @jwt_required()
    @blp.arguments(UrlInputSchema)
    def get(self, url_input):
        self.url_controller = UrlController(url_input)
        response = self.url_controller.view_all_ban_url(url_input)
        return response
