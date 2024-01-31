from business_logic.auth.login_logic import LoginLogic
from utils.exception_handler import custom_error_handler


class LoginController:
    def __init__(self) -> None:
        self.login_logic = LoginLogic()

    @custom_error_handler
    def verify_user(self, user_data):
        response = self.login_logic.login(
            username=user_data["username"], password=user_data["password"]
        )
        return response
