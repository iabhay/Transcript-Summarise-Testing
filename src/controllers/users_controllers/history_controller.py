import logging
from flask import request
from flask_jwt_extended import get_jwt, get_jwt_identity
from utils.exception_handler import custom_error_handler
from business_logic.history_logic import HistoryLogic
from config.config import Config
from config.log_config.log_config import LogStatements

logger = logging.getLogger(__name__)


# All History Functionalities
class HistoryController:
    def __init__(self):
        self.user_id = request.args.get("user_id")
        self.identity = get_jwt_identity()
        self.claims = get_jwt()
        self.history_logic = HistoryLogic(self.identity)

    @custom_error_handler
    def view_all_history(self):
        response = self.history_logic.view_all_history()
        return response

    @custom_error_handler
    def view_history(self):
        if self.user_id:
            if self.claims["role"] == "admin":
                response = self.history_logic.view_history(self.user_id)
                return response
            else:
                return {"message": "Access Restricted"}
        else:
            response = self.user_info_logic.view_user(self.identity)
            return response
