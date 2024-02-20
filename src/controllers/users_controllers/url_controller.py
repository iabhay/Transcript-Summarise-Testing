"""
Url Controller
1. banning url
2. unbanning url
3. Viewing particular banned url
4. Viewing all banned urls
"""

import logging
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, get_jwt
from utils.exception_handler import custom_error_handler
from business_logic.url_logic import UrlLogic
from config.api_config import ApiConfig

logger = logging.getLogger(__name__)


# All Url Functionalities
class UrlController:
    """
    Class for defining Url Controller
    ...
    Methods:
    -------
    Constructor() -> Method to Initialisation of Url Logic and fetching query parameters and claims from jwt token
    ban_url() -> Method to ban url
    unban_url() -> Method to unban url
    view_ban_url() -> Method to fetch banned url details
    view_unban_url() -> Method to fetch all banned urls details
    """

    def __init__(self):
        self.ban_url_id = request.args.get("ban_url_id")
        self.identity = get_jwt_identity()
        self.claims = get_jwt()
        self.url_logic = UrlLogic()

    @custom_error_handler
    def ban_url(self, url_input):
        """
        Method to ban url
        Parameter -> url_input: dict
        Return Type -> dict
        """
        url_id = url_input["youtube_url"]
        self.url_logic.ban_url(url_id)
        return {"message": ApiConfig.URL_BANNED}

    @custom_error_handler
    def unban_url(self, url_input):
        """
        Method to unban url
        Parameter -> url_input: dict
        Return Type -> dict
        """
        url_id = url_input["youtube_url"]
        self.url_logic.unban_url(url_id)
        return {"message": ApiConfig.URL_UNBANNED}

    @custom_error_handler
    def view_ban_url(self, url_input):
        """
        Method to view banned url details
        Parameter -> url_input: dict
        Return Type -> dict
        """
        url_id = url_input["youtube_url"]
        response = self.url_logic.view_ban_url(url_id)
        return jsonify(response)

    @custom_error_handler
    def view_all_ban_url(self):
        """
        Method to view all banned urls details
        Parameter -> self
        Return Type -> dict
        """
        response = self.url_logic.view_all_ban_url()
        return jsonify(response)
