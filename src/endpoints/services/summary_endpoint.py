"""Module for defining Summary Service Route"""

from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.utils_api.role_api import role_required
from controllers.service_controller.summary_service_controller import SummaryController
from utils.utils_api.schemas import UrlInputSchema

"""
Summary geneneration endpoint
jwt token will be required to get data from this request
according to role and user data will be generated.
"""

blp = Blueprint("summary", __name__, description="summary")


@blp.route("/summary")
class SummaryEndpoint(MethodView):
    

    @role_required(["nonpremiumuser", "premiumuser", "admin"])
    @jwt_required()
    @blp.arguments(UrlInputSchema)
    def post(self, youtube_url):
        """
        Method to get request which verifies jwt and generate summary for the youtube url given
        Roles allowed -> nonpremiumuser
        Parameter -> youtube_url: UrlInputSchema
        Return Type -> Json
        """
        identity = get_jwt_identity()
        self.summary_controller = SummaryController(identity)
        response = self.summary_controller.submit_video(youtube_url)
        return response
