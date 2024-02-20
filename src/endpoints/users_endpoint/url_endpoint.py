"""Module for Url Related Route"""

from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from utils.utils_api.schemas import UrlInputSchema
from utils.utils_api.role_api import role_required
from controllers.users_controllers.url_controller import UrlController

"""
URL Resource endpoints
1. /url/ban [POST] for banning url, can be done by admin only.
2. /url/ban [GET] for getting details of already banned url, can be done by admin only.
3. /url/unban [POST] for unbanning url, can be accessed by admin.
4. /urls [] for gettinf details of all banned urls, can be accessed by admin.
"""

blp = Blueprint("admin", __name__, description="admin")


@blp.route("/url/ban")
class BanUrl(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    get() -> Method to get banned url details
    post() -> Method to add any url into banned
    """

    @role_required(["admin"])
    @jwt_required()
    @blp.arguments(UrlInputSchema)
    def post(self, url_input):
        """
        Method to post request which verifies jwt and ban the given url
        Roles allowed -> admin
        Parameter -> url_input: UrlInputSchema
        Return Type -> Json
        """
        self.url_controller = UrlController(url_input)
        response = self.url_controller.ban_url(url_input)
        return response

    @role_required(["admin"])
    @jwt_required()
    @blp.arguments(UrlInputSchema)
    def get(self, url_input):
        """
        Method to get request which verifies jwt and get the banned url details
        Roles allowed -> admin
        Parameter -> url_input: UrlInputSchema
        Return Type -> Json
        """
        self.url_controller = UrlController()
        response = self.url_controller.view_ban_url(url_input)
        return response


@blp.route("/url/unban")
class UnbanUrl(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    delete() -> Method to unban url
    """

    @role_required(["admin"])
    @jwt_required()
    @blp.arguments(UrlInputSchema)
    def delete(self, url_input):
        """
        Method to delete request which verifies jwt and unban the given url
        Roles allowed -> admin
        Parameter -> url_input: UrlInputSchema
        Return Type -> Json
        """
        self.url_controller = UrlController()
        response = self.url_controller.unban_url(url_input)
        return response


@blp.route("/urls")
class ViewBanUrl(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    get() -> Method to get all banned urls details
    """

    @role_required(["admin"])
    @jwt_required()
    def get(self):
        """
        Method to get request which verifies jwt and get the all banned url details
        Roles allowed -> admin
        Parameter -> self
        Return Type -> Json
        """
        self.url_controller = UrlController()
        response = self.url_controller.view_all_ban_url()
        return response
