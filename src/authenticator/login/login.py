import hashlib
import logging
from pwinput import pwinput
from database.db_ops.users_db import UsersDB
from users.premium_user.premium_user import PremiumUser
from users.admin.admin_point import Admin
from users.non_premium_user.non_premium_user import NonPremiumUser
from database.db_ops.messages_db import MessageDB
from utils.exception_handler import handle_exceptions
from config.config import Config

from config.log_config.log_config import LogStatements
logger = logging.getLogger('login')


class Login:
    def __init__(self):
        self.uid = ""
        self.res = ""

    # @handle_exceptions
    def login_module(self):
        while True:
            # If role changed then self.res will be already filled, and checking for returning role from module which
            # it is coming
            if self.res and self.uid and (self.res == "nonpremium" or self.res == "premium"):
                if self.res == "premium":
                    non_premium_user = NonPremiumUser(self.uid)  # self.uid will be already filled once user loggedin
                    self.res = non_premium_user.non_premium_module()
                elif self.res == "nonpremium":
                    premium_user = PremiumUser(self.uid)
                    self.res = premium_user.premium_module()

            # Just checking returning values from diff methods accordingly
            elif self.res == True or self.res == False or self.res == "":
                username = input(Config.ENTER_USERNAME_PROMPT)
                username = username.strip()
                password = pwinput(prompt=Config.ENTER_PASSWORD_PROMPT, mask="*")
                password = password.strip()
                # Direct redirect to admin module
                if username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
                    admin = Admin("")
                    admin.adminmodule()
                    break
                else:
                    # Authenticating user
                    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                    user = UsersDB("")
                    # entry is basically all details about that user column wise
                    entry = user.check_user(username, hashed_password)
                    if not entry:
                        logger.info(LogStatements.invalid_login_log)
                        print("Invalid Credentials!!")
                        return
                    uid = entry[0][0]  # this is unique id for that user that'll be used for all functions
                    self.uid = uid
                    m_obj = MessageDB(uid)
                    non_premium_user = NonPremiumUser(uid)
                    premium_user = PremiumUser(uid)
                    admin = Admin(uid)
                    print("You are logged in!!")
                    # checking if user banned then redirecting to banned module
                    if entry[0][5] == "banned":
                        m_obj.banned_module()
                    elif entry[0][4] == "nonpremiumuser" and entry[0][5] == "unbanned":
                        self.res = non_premium_user.non_premium_module()
                        self.login_module()
                    elif entry[0][4] == "premiumuser" and entry[0][5] == "unbanned":
                        self.res = premium_user.premium_module()
                        self.login_module()
                        # for multiple admins (future purpose only)
                    elif entry[0][4] == "admin":
                        admin.adminmodule()
                        break
                    else:
                        print("Wrong role was filled!")
                    return True

            # resetting as it's exiting
            elif not self.res:
                logger.info(LogStatements.user_exited)
                self.uid = ""
                self.res = ""
                break




