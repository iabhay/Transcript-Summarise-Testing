"""
User Info Controller
1. particular user can see his own profile or admin can see any user's profile.
2. upgrading user by admin. Admin role can't be changed.
3. upgrading user itself. Admin role can't be changed.
4. downgrading user by admin. Admin role can't be changed.
5. downgrading user itself. Admin role can't be changed.
6. all user can be seen by admin only.
7. ban or unban user by admin only.
"""

from flask import jsonify, request
from utils.exception_handler import custom_error_handler
from flask_jwt_extended import get_jwt, get_jwt_identity
from business_logic.user_info_logic import UserInfoLogic
from config.api_config import ApiConfig
from business_logic.auth.login_logic import LoginLogic

class UserInfoController:
    def __init__(self) -> None:
        """
        Class for defining User Info Controller
        ...
        Methods:
        -------
        Constructor() -> Method to Initialisation of User info Logic and fetching query parameters and claims from jwt token

        """
        self.user_id = request.args.get("user_id")
        self.identity = get_jwt_identity()
        self.claims = get_jwt()
        self.user_info_logic = UserInfoLogic()

    @custom_error_handler
    def view_user(self) -> list:
        """
        Method to view user
        Parameter -> self
        Return Type -> list
        """
        if self.user_id:
            if self.claims["role"] == "admin":
                response = self.user_info_logic.view_user(self.user_id)
                return response
            else:
                return {"message": ApiConfig.ACCESS_RESTRICTED}, 403
        else:
            response = self.user_info_logic.view_user(self.identity)
            return response

    @custom_error_handler
    def upgrade_non_premium_user(self):
        """
        Method to upgrade non premium user
        Parameter -> self
        Return Type -> dict
        """
        if self.user_id:
            if self.claims["role"] == "admin":
                if self.identity != self.user_id:
                    response = self.user_info_logic.upgrade_non_premium_user(
                        self.user_id
                    )
                    return {"message": ApiConfig.USER_UPGRADED}
                else:
                    return {"message": ApiConfig.ADMIN_ROLE_UNCHANGEABLE}
            else:
                return {"message": ApiConfig.ACCESS_RESTRICTED}, 403
        else:
            if self.claims["role"] != "admin":
                response = self.user_info_logic.upgrade_non_premium_user(self.identity)
                return response
            else:
                return {"message": ApiConfig.ADMIN_ROLE_UNCHANGEABLE}

    @custom_error_handler
    def downgrade_premium_user(self):
        """
        Method to downgrade premium user
        Parameter -> self
        Return Type -> dict
        """
        if self.user_id:
            if self.claims["role"] == "admin":
                if self.identity != self.user_id:
                    response = self.user_info_logic.downgrade_premium_user(self.user_id)
                    return (
                        {"message": ApiConfig.USER_DOWNGRADED}
                        if not response
                        else response
                    )
                else:
                    return {"message": ApiConfig.ADMIN_ROLE_UNCHANGEABLE}
            else:
                return {"message": ApiConfig.ACCESS_RESTRICTED}, 403
        else:
            if self.claims["role"] != "admin":
                response = self.user_info_logic.downgrade_premium_user(self.identity)
                return response
            else:
                return {"message": ApiConfig.ADMIN_ROLE_UNCHANGEABLE}

    @custom_error_handler
    def view_all_users(self):
        """
        Method to view all users
        Parameter -> self
        Return Type -> list
        """
        response = self.user_info_logic.view_all_users()
        return response

    @custom_error_handler
    def ban_user(self):
        """
        Method to ban user
        Parameter -> self
        Return Type -> dict
        """
        if self.user_id:
            if self.claims["role"] == "admin":
                if self.identity != self.user_id:
                    response = self.user_info_logic.ban_user(
                        self.user_id
                    )
                    return {"message": ApiConfig.USER_BANNED}
                else:
                    return {"message": ApiConfig.ADMIN_ROLE_UNCHANGEABLE}
            
        return {"message": ApiConfig.ACCESS_RESTRICTED}, 403

    @custom_error_handler
    def unban_user(self):
        """
        Method to unban user
        Parameter -> self
        Return Type -> dict
        """
        if self.user_id:
            if self.claims["role"] == "admin":
                if self.identity != self.user_id:
                    response = self.user_info_logic.unban_user(
                        self.user_id
                    )
                    return {"message": ApiConfig.USER_UNBANNED}
                else:
                    return {"message": ApiConfig.ADMIN_ROLE_UNCHANGEABLE}
        return {"message": ApiConfig.ACCESS_RESTRICTED}, 403
