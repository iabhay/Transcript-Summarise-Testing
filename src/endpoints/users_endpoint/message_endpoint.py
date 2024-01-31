from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required
from utils_api.role_api import role_required
from utils_api.schemas import UserMessageSchema
from controllers.users_controllers.message_controller import MessageController

blp = Blueprint("message", __name__, description="message")


@blp.route("/messages")
class ViewAllMessage(MethodView):
    @role_required(["admin"])
    @jwt_required()
    def get(self):
        self.message_controller = MessageController()
        response = self.message_controller.view_message()
        return response


@blp.route("/message")
class SendMessage(MethodView):
    @role_required(["premium", "premiumuser"])
    @jwt_required()
    @blp.arguments(UserMessageSchema)
    def post(self, user_data):
        self.message_controller = MessageController()
        response = self.message_controller.send_message(user_data)
        return response
