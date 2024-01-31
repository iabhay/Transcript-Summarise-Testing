from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from utils_api.role_api import role_required
from controllers.service_controller.summary_service_controller import SummaryController
from utils_api.schemas import UrlInputSchema

blp = Blueprint("summary", __name__, description="summary")


@blp.route("/summary")
class SummaryEndpoint(MethodView):
    @role_required(["nonpremiumuser", "premiumuser", "admin", "nonpremium"])
    @jwt_required()
    @blp.arguments(UrlInputSchema)
    def get(self, youtube_url):
        identity = get_jwt_identity()
        self.summary_controller = SummaryController(identity)
        response = self.summary_controller.submit_video(youtube_url)
        return response
        # return {}
