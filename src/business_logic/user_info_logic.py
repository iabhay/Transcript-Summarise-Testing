"""User Info Logic -> user related logic like adding, banning, unbanning, upgrading, downgrading, view details"""

import logging
from flask import request
from mysql.connector import Error
from database.database_query import UsersTableQuery, AdminQueries
from database.mysql_database import db
from utils.custom_exception import UserNotFound, DBException
from config.api_config import ApiConfig
from flask_jwt_extended import get_jwt, get_jwt_identity
from business_logic.auth.login_logic import LoginLogic

logger = logging.getLogger(__name__)


class UserInfoLogic:
    """
    Class for defining User Info Logic
    ...
    Methods:
    -------
    view_user() -> fetching details of user
    upgrade_non_premium_user() -> changing role of user
    downgrade_premium_user() -> changing role of user
    view_all_users() -> view all users details
    ban_user() -> banning user
    unban_user() -> unbanning user
    """

    def view_user(self, target_uid):
        """
        Method for viewing user details
        Parameter -> target_uid: str
        Return Type -> list
        Exception Type -> SQLError, UserNotFound
        """
        try:
            target = db.fetch_data(
                UsersTableQuery.query_select_user_by_uid, (target_uid,)
            )
            if not target:
                raise UserNotFound(404, ApiConfig.USER_NOT_EXIST)
            else:
                table = db.fetch_data(AdminQueries.query_view_user, (target_uid,))
                return table[0]
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def upgrade_non_premium_user(self, target_uid):
        try:
            target = db.fetch_data(
                UsersTableQuery.query_select_user_by_uid, (target_uid,)
            )
            if not target:
                raise UserNotFound(404, ApiConfig.USER_NOT_EXIST)
            if target[0]["role"] == "premiumuser":
                return {"message": ApiConfig.ALREADYPREMIUM}, 409
            db.save_data(
                UsersTableQuery.query_update_user_role, ("premiumuser", target_uid)
            )
            
            claims = get_jwt()
            identity = target_uid
            access_jti = claims["jti"]
            role = "premiumuser"
            ban_status = claims["ban_status"]
            token_update = LoginLogic()
            response = token_update.update_token(access_jti, identity, role, ban_status)
            response["message"] = ApiConfig.USER_DOWNGRADED
            return response, 200
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def downgrade_premium_user(self, target_uid):
        try:
            target = db.fetch_data(
                UsersTableQuery.query_select_user_by_uid, (target_uid,)
            )
            if not target:
                raise UserNotFound(404, "User doesn't exist.")
            if target[0]["role"] == "nonpremiumuser":
                return {"message": ApiConfig.ALREADY_NONPREMIUML}, 409
            
            db.save_data(
                UsersTableQuery.query_update_user_role,
                ("nonpremiumuser", target_uid),
            )
            claims = get_jwt()
            identity = target_uid
            access_jti = claims["jti"]
            role = "nonpremiumuser"
            ban_status = claims["ban_status"]
            token_update = LoginLogic()
            response = token_update.update_token(access_jti, identity, role, ban_status)
            response["message"] = ApiConfig.USER_DOWNGRADED
            return response, 200
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def view_all_users(self):
        response = db.fetch_data(AdminQueries.query_view_all_users)
        if response is None:
            raise UserNotFound(404, ApiConfig.DATA_NOT_EXIST)
        else:
            return response

    def ban_user(self, uid):
        try:
            target = db.fetch_data(UsersTableQuery.query_select_user_by_uid, (uid,))
            if not target:
                raise UserNotFound(404, ApiConfig.USER_NOT_EXIST)
            db.save_data(
                UsersTableQuery.query_update_user_ban_status, ("banned", uid)
            )
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def unban_user(self, uid):
        try:
            target = db.fetch_data(UsersTableQuery.query_select_user_by_uid, (uid,))
            if not target:
                raise UserNotFound(404, ApiConfig.USER_NOT_EXIST)
            db.save_data(
                UsersTableQuery.query_update_user_ban_status, ("unbanned", uid)
            )
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)
