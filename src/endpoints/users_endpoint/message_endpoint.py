"""Module for definingMessage Route"""

"""
Message Resource Endpoints
1. /messages[GET] for fetching all messages received from all users based on filter if any. Admin can access.
2. /message [POST] for sending any message to admin. Can be used by premium only.
"""

from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from utils.utils_api.role_api import role_required
from utils.utils_api.schemas import UserMessageSchema
from controllers.users_controllers.message_controller import MessageController

blp = Blueprint("message", __name__, description="message")


@blp.route("/messages")
class ViewAllMessage(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    get() -> Method to get all messages method
    """

    @role_required(["admin"])
    @jwt_required()
    def get(self):
        """
        Method to get request which verifies jwt and fetch all messages of users
        Roles allowed -> admin
        Parameter -> self
        Return Type -> Json
        """
        self.message_controller = MessageController()
        response = self.message_controller.view_message()
        return response


@blp.route("/message")
class SendMessage(MethodView):
    @jwt_required()
    @blp.arguments(UserMessageSchema)
    def post(self, user_data):
        """
        Method to post request which verifies jwt and send message to admin
        Roles allowed -> premiumuser
        Parameter -> user_data: UserMessageSchema
        Return Type -> Json
        """
        self.message_controller = MessageController()
        response = self.message_controller.send_message(user_data)
        return response
