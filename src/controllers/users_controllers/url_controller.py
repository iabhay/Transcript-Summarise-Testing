import logging
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, get_jwt
from utils.exception_handler import custom_error_handler
from business_logic.url_logic import UrlLogic

logger = logging.getLogger(__name__)


# All Url Functionalities
class UrlController:
    def __init__(self):
        self.args = request.args()
        self.ban_url_id = self.args.get("ban_url_id")
        self.identity = get_jwt_identity()
        self.claims = get_jwt()
        self.url_logic = UrlLogic()

    @custom_error_handler
    def ban_url(self, url_input):
        url_id = url_input["youtube_url"]
        self.url_logic.ban_url(url_id)
        return {"message": "url banned successfully."}

    @custom_error_handler
    def unban_url(self, url_input):
        url_id = url_input["youtube_url"]
        self.url_logic.unban_url(url_id)
        return {"message": "url unbanned successfully."}

    @custom_error_handler
    def view_ban_url(self, url_input):
        url_id = url_input["youtube_url"]
        response = self.url_logic.view_ban_url(url_id)
        return jsonify(response)

    @custom_error_handler
    def view_all_ban_url(self):
        response = self.url_logic.view_all_ban_url()
        return jsonify(response)
