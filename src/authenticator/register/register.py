import hashlib
from pwinput import pwinput
import logging
from config.config import Config
from utils.input_validator import password_validation, username_validation
from database.db_ops.users_db import UsersDB
from config.log_config.log_config import LogStatements
from utils.exception_handler import handle_exceptions
logger = logging.getLogger('register')


class Register:
    def __init__(self):
        self.user = UsersDB("")

    # @handle_exceptions
    def register_module(self):
        while True:
            print(Config.SECURE_USERNAME_PROMPT)
            username = input(Config.ENTER_USERNAME_PROMPT)
            username = username.strip()
            if not username_validation(username):
                print("Invalid Username!")
            else:
                print(Config.SECURE_PASSWORD_PROMPT)
                password = pwinput(Config.ENTER_PASSWORD_PROMPT, mask="*")
                password = password.strip()
                # Checking for regex validation
                if not password_validation(password):
                    print("Invalid Password!!")
                else:
                    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                    # checking if already registered with username
                    if not self.check_registration(username, hashed_password):
                        self.user.create_user(username, hashed_password)
                        print("Registered successfully!!")
                        break

    def check_registration(self, name, password):
        is_already_registered = self.user.check_user(name, password)
        if is_already_registered:
            print("Already registered!!\nTry login!!")
            return True
        else:
            return False
