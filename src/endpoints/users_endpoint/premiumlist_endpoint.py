"""Module for defining Premiumlist Route"""

from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.utils_api.schemas import PremiumListSchema, UrlInputSchema
from utils.utils_api.role_api import role_required
from controllers.users_controllers.premiumlist_controller import PremiumlistController

"""
Premiumlist Resource Endpoints
1. /premiumlist [POST] for premium listing any url for any user, can be done by admin only.
2. /premiumlist [GET] for fetching all premium listings of any user, can be done by admin and premium user only.
3. /premiumlist-request [POST] for request of premium listing of url to admin, can be accessed by premium user only.
"""

blp = Blueprint("premiumlist", __name__, description="premiumlist")


@blp.route("/premiumlist")
class PremiumList(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    get() -> Method to get premium listings of url method
    post() -> Method to add premiumlisting of url for user
    """

    @role_required(["admin"])
    @jwt_required()
    @blp.arguments(PremiumListSchema)
    def post(self, url_req):
        """
        Method to post request which verifies jwt and add url for premium listing to any premiumuser
        Roles allowed -> admin
        Parameter -> url_req: PremiumListSchema
        Return Type -> Json
        """
        identity = get_jwt_identity()
        self.admin_controller = PremiumlistController()
        response = self.admin_controller.premium_list(url_req)
        return response

    @role_required(["premiumuser", "admin"])
    @jwt_required()
    def get(self):
        """
        Method to get request which verifies jwt and fetch premium listed urls of specific user or users
        Roles allowed -> premiumuser, admin
        Parameter -> self
        Return Type -> Json
        """
        self.premium_controller = PremiumlistController()
        response = self.premium_controller.view_premium_list()
        return response


@blp.route("/premiumlist-request")
class PremiumList(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    post() -> Method to prequest for premiumlisting of url by user
    """

    @role_required(["premiumuser"])
    @jwt_required()
    @blp.arguments(UrlInputSchema)
    def post(self, url_req):
        """
        Method to post request which verifies jwt and send request for premiumlisting of url to admin
        Roles allowed -> premiumuser
        Parameter -> url_req: UrlInputSchema
        Return Type -> Json
        """
        self.premium_controller = PremiumlistController()
        response = self.premium_controller.premiumlist_request(url_req)
        return response
