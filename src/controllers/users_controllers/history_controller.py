"""
History Controller
1. Extracting id, role, ban_status from jwt
2. Fetching all users or particular user history according to request and role of user.
"""

import logging
from flask import request
from flask_jwt_extended import get_jwt, get_jwt_identity
from utils.exception_handler import custom_error_handler
from business_logic.history_logic import HistoryLogic
from config.api_config import ApiConfig


logger = logging.getLogger(__name__)


class HistoryController:
    """
    Class for defining History Controller
    ...
    Methods:
    -------
    Constructor() -> Method to Initialisation of History Logic and fetching query parameters and claims from jwt token
    view_all_history() -> Method to get all history
    view_history() -> Method to get history of user
    """

    def __init__(self):
        self.user_id = request.args.get("user_id")
        self.identity = get_jwt_identity()
        self.claims = get_jwt()
        self.history_logic = HistoryLogic(self.identity)

    @custom_error_handler
    def view_all_history(self):
        """
        Method fetching all history of all users
        Parameter -> self
        Return Type -> list
        """
        response = self.history_logic.view_all_history()
        return response

    @custom_error_handler
    def view_history(self):
        """
        Method fetching history of user according to role functionality
        if user hitting endpoint then personal history of that user but if admin sending request to get data of particular user then admin will get data of that user
        Parameter -> self
        Return Type -> list
        """
        if self.user_id:
            if self.claims["role"] == "admin":
                response = self.history_logic.view_history(self.user_id)
                return response
            else:
                return {"message": ApiConfig.ACCESS_RESTRICTED}
        else:
            response = self.history_logic.view_history(self.identity)
            return response
