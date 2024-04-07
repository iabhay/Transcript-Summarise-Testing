"""
Message Controller
1. Admin can access Messages according to filter provided in query paramters(?user_type or ?user_id) -> (particular user, premium, nonpremium, all).
2. If premium user then it's own messages
3. If non premium user then access denied.
"""

import logging
from flask import request
from flask_jwt_extended import get_jwt_identity, get_jwt
from utils.exception_handler import custom_error_handler
from business_logic.message_logic import MessageLogic
from config.api_config import ApiConfig

logger = logging.getLogger(__name__)


# All Message Functionalities
class MessageController:
    """
    Class for defining Message Controller
    ...
    Methods:
    -------
    Constructor() -> Method to Initialisation of Message Logic and fetching query parameters and claims from jwt token
    view_message() -> Method to get message
    send_message() -> Method to send message from user to admin
    """

    def __init__(self):
        self.user_id = request.args.get("user_id")
        self.user_type = request.args.get("user_type")
        self.identity = get_jwt_identity()
        self.claims = get_jwt()
        self.message_logic = MessageLogic()

    @custom_error_handler
    def view_message(self):
        """
        Method fetching message of user according to role functionality
        if admin providing user_type or user_id then messages of that user_type or user_id will be served
        Parameter -> self
        Return Type -> list
        """
        if self.claims["role"] == "admin":
            if self.user_id:
                response = self.message_logic.view_user_message(self.user_id)
                return response
            if self.user_type:
                if self.user_type == "premiumuser":
                    response = self.message_logic.view_premium_message(self.user_id)
                    return response
                elif self.user_type == "nonpremiumuser":
                    response = self.message_logic.view_nonpremium_message(self.user_id)
                    return response
            response = self.message_logic.view_all_message()
            return response
        return {"message": ApiConfig.ACCESS_RESTRICTED}, 403

    @custom_error_handler
    def send_message(self, user_data):
        """
        Method sending message of user to admin
        Parameter -> user_data: dict
        Return Type -> dict
        """
        if self.claims["role"] == "premiumuser" or self.claims["ban_status"] == "banned":
            self.message_logic.send_message(self.identity, user_data["description"])
            return {"message": ApiConfig.SENT_TO_ADMIN}, 200
        else:
            return {"message": ApiConfig.ACCESS_RESTRICTED}, 403