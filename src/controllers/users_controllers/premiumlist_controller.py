import logging
from flask import jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity
from utils.exception_handler import custom_error_handler
from business_logic.premiumlist_logic import PremiumlistLogic
from config.config import Config
from config.log_config.log_config import LogStatements

logger = logging.getLogger(__name__)


# All Premiumlist Functionalities
class PremiumlistController:
    def __init__(self):
        self.args = request.args()
        self.user_id = self.args.get("user_id")
        self.identity = get_jwt_identity()
        self.claims = get_jwt()
        self.premium_list_logic = PremiumlistLogic()

    @custom_error_handler
    def premium_list(self, url_req):
        self.premium_list_logic.premium_list(
            url_req["username"], url_req["youtube_url"]
        )
        return jsonify({"message": "URL Premiumlisted for user."})

    @custom_error_handler
    def view_premium_list(self):
        if self.claims["role"] == "admin":
            if self.user_id:
                response = self.premium_list_logic.view_premium_list(self.user_id)
                return response
            elif self.args is None:
                response = self.premium_list_logic.view_all_premium_list()
            return {"message": "Access Restricted"}
        else:
            response = self.premium_list_logic.view_premium_list(self.identity)
            return response
