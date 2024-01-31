from flask import jsonify, request
from business_logic.common.common_logic import CommonLogic
from utils.exception_handler import custom_error_handler
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from business_logic.user_info_logic import UserInfoLogic


class UserInfoController:
    def __init__(self) -> None:
        self.user_id = request.args.get("user_id")
        self.identity = get_jwt_identity()
        self.claims = get_jwt()
        self.user_info_logic = UserInfoLogic()

    @custom_error_handler
    def view_user(self):
        if self.user_id:
            if self.claims["role"] == "admin":
                response = self.user_info_logic.view_user(self.user_id)
                return response
            else:
                return {"message": "Access Restricted"}
        else:
            response = self.user_info_logic.view_user(self.identity)
            return response

    @custom_error_handler
    def upgrade_non_premium_user(self):
        if self.user_id:
            if self.claims["role"] == "admin":
                if self.identity != self.user_id:
                    response = self.user_info_logic.upgrade_non_premium_user(
                        self.user_id
                    )
                    return {"message": "User Upgraded."}
                else:
                    return {"message": "Admin Role can't be changed."}
            else:
                return {"message": "Access Restricted"}
        else:
            if self.claims["role"] != "admin":
                response = self.user_info_logic.upgrade_non_premium_user(self.identity)
                return {"message": "User Upgraded."}
            else:
                return {"message": "Admin Role can't be changed."}

    @custom_error_handler
    def downgrade_premium_user(self):
        if self.user_id:
            if self.claims["role"] == "admin":
                if self.identity != self.user_id:
                    response = self.user_info_logic.downgrade_premium_user(self.user_id)
                    return {"message": "User Upgraded."}
                else:
                    return {"message": "Admin Role can't be changed."}
            else:
                return {"message": "Access Restricted"}
        else:
            if self.claims["role"] != "admin":
                response = self.user_info_logic.downgrade_premium_user(self.identity)
                return {"message": "User Upgraded."}
            else:
                return {"message": "Admin Role can't be changed."}

    @custom_error_handler
    def view_all_users(self):
        response = self.user_info_logic.view_all_users()
        return response

    @custom_error_handler
    def ban_user(self):
        if self.user_id is None:
            return {"message": "Restricted Endpoint."}
        self.user_info_logic.ban_user(self.user_id)
        return {"message": "user banned successfully."}

    @custom_error_handler
    def unban_user(self):
        if self.user_id is None:
            return {"message": "Restricted Endpoint."}
        self.user_info_logic.unban_user(self.user_id)
        return {"message": "user unbanned successfully."}
