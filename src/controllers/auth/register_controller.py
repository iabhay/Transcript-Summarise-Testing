"""
Register Controller Gives required data from request received from Router to Register Logic.
Error handled here can be of User already exist raised in register logic.
Custom error template is returned if any error occured during fetching or saving data to db.
"""

from business_logic.auth.register_logic import RegisterLogic
from utils.exception_handler import custom_error_handler
from config.api_config import ApiConfig


class RegisterController:
    """
    Class for defining Login Controller
    ...
    Methods:
    -------
    Constructor() -> Method to Initialisation of Register Logic
    verify_user() -> Method to add user by providing username and password to register logic
    """

    def __init__(self) -> None:
        self.register_logic = RegisterLogic()

    @custom_error_handler
    def add_user(self, user_data):
        """
        Method extracting username and password from request body data and giving it to logic
        Parameter -> user_data: dict
        Return Type -> dict
        """
        self.register_logic.add_user(
            username=user_data['username'], password=user_data['password']
        )
        response = {"username": user_data['username'],
                    "message": ApiConfig.USER_REGISTER_SUCCESS}
        return response
