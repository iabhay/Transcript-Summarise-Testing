from business_logic.auth.register_logic import RegisterLogic
from utils.exception_handler import custom_error_handler


class RegisterController:
    def __init__(self) -> None:
        self.register_logic = RegisterLogic()

    @custom_error_handler
    def add_user(self, user_data):
        self.register_logic.add_user(
            username=user_data["username"], password=user_data["password"]
        )
        return {"message": "User registered successfully."}
