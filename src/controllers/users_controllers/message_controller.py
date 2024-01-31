import logging
from flask import request
from flask_jwt_extended import get_jwt_identity, get_jwt
from utils.exception_handler import custom_error_handler
from business_logic.message_logic import MessageLogic

logger = logging.getLogger(__name__)


# All Message Functionalities
class MessageController:
    def __init__(self):
        self.args = request.args()
        self.user_id = self.args.get("user_id")
        self.user_type = request.args.get("user_type")
        self.identity = get_jwt_identity()
        self.claims = get_jwt()
        self.message_logic = MessageLogic()

    @custom_error_handler
    def view_message(self):
        if self.claims["role"] == "admin":
            if self.user_id and self.user_type:
                return {"message": "Restricted Endpoint."}
            if self.user_id:
                response = self.message_logic.view_user_message(self.user_id)
                return response
            if self.user_type:
                if self.user_type == "premium":
                    response = self.message_logic.view_premium_message(self.user_id)
                    return response
                elif self.user_type == "nonpremium":
                    response = self.message_logic.view_nonpremium_message(self.user_id)
                    return response
            if self.args is None:
                response = self.message_logic.view_all_message()
                return response
        return {"message": "Access Restricted"}

    @custom_error_handler
    def send_message(self, user_data):
        self.message_logic.send_message(user_data["description"])
        return {"message": "Your request for unban successfully sent to admin."}
