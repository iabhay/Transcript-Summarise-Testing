"""
Login Controller extracting useful data from request that is required in Login Logic.
username and password passed in Login Logic.
Error handled by custom error decorator.
"""

from business_logic.auth.login_logic import LoginLogic
from utils.exception_handler import custom_error_handler


class LoginController:
    """
    Class for defining Login Controller
    ...
    Methods:
    -------
    Constructor() -> Method to Initialisation of Login Logic
    verify_user() -> Method to Verify user by providing username and password to login logic
    """

    def __init__(self) -> None:
        self.login_logic = LoginLogic()

    @custom_error_handler
    def verify_user(self, user_data):
        """
        Method extracting username and password from request body data and giving it to logic
        Parameter -> user_data: dict
        Return Type -> dict
        """
        response = self.login_logic.login(
            username=user_data["username"], password=user_data["password"]
        )
        return response
