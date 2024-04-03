"""
Premiumlist Controller
1. adding premiumlisting of any url for user can be done by admin only.
2. admin can see particular user premiumlisting or all premiumlisting of all users.
"""

import logging
from flask import jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity
from utils.exception_handler import custom_error_handler
from business_logic.premiumlist_logic import PremiumlistLogic
from config.api_config import ApiConfig
from business_logic.message_logic import MessageLogic

logger = logging.getLogger(__name__)


# All Premiumlist Functionalities
class PremiumlistController:
    """
    Class for defining Message Controller
    ...
    Methods:
    -------
    Constructor() -> Method to Initialisation of PremiumList Logic and fetching query parameters and claims from jwt token
    premium_list() -> Method to add url to premiumlisting for that user
    view_premium_list() -> Method to fetch premiumlisting requests
    """

    def __init__(self):
        self.user_id = request.args.get("user_id")
        self.identity = get_jwt_identity()
        self.claims = get_jwt()
        self.premium_list_logic = PremiumlistLogic()

    @custom_error_handler
    def premium_list(self, url_req):
        """
        Method to add url to premiumlisting for that user
        Parameter -> user_req: dict
        Return Type -> dict
        """
        self.premium_list_logic.premium_list(
            url_req["user_id"], url_req["youtube_url"]
        )
        return jsonify({"message": ApiConfig.URL_PREMIUMLISTED})

    @custom_error_handler
    def view_premium_list(self):
        """
        Method to get premiumlisting for that user or all users
        Parameter -> self
        Return Type -> dict
        """
        if self.claims["role"] == "admin":
            if self.user_id:
                response = self.premium_list_logic.view_premium_list(self.user_id)
                return response
            elif request.args is None:
                response = self.premium_list_logic.view_all_premium_list()
            return {"message": ApiConfig.ACCESS_RESTRICTED}, 403
        else:
            if request.args is None:
                response = self.premium_list_logic.view_premium_list(self.identity)
                return response
            return {"message": ApiConfig.ACCESS_RESTRICTED}, 403
        
    @custom_error_handler
    def premiumlist_request(self, url_req):
        youtube_url = url_req['youtube_url']
        msg_logic = MessageLogic()
        description = "Premiumlist - " + youtube_url
        response = msg_logic.send_message(self.identity, description)
        return jsonify({"message": "Request Sent for premiumlisting"})
        

