from flask import request
from mysql.connector import Error
from database.database_query import UsersTableQuery, AdminQueries
from database.mysql_database import db
from utils.custom_exception import UserNotFound, DBException, PersmissionGrantError
import logging

logger = logging.getLogger(__name__)


class UserInfoLogic:
    def view_user(self, target_uid):
        try:
            target = db.fetch_data(
                UsersTableQuery.query_select_user_by_uid, (target_uid,)
            )
            if len(target) == 0:
                raise UserNotFound(404, "UserNotFound", "User Profile not available.")
            else:
                table = db.fetch_data(AdminQueries.query_view_user, (target_uid,))
                return table
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def upgrade_non_premium_user(self, target_uid):
        try:
            target = db.fetch_data(
                UsersTableQuery.query_select_user_by_uid, (target_uid,)
            )

            if len(target) == 0:
                raise UserNotFound(404, "ResourceNotFound", "User doesn't exist.")

            db.save_data(
                UsersTableQuery.query_update_user_role, ("premium", target_uid)
            )
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def downgrade_premium_user(self, target_uid):
        try:
            target = db.fetch_data(
                UsersTableQuery.query_select_user_by_uid, (target_uid,)
            )

            if len(target) == 0:
                raise UserNotFound(404, "ResourceNotFound", "User doesn't exist.")
            db.save_data(
                UsersTableQuery.query_update_user_role, ("nonpremium", target_uid)
            )
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def view_all_users(self):
        response = db.fetch_data(AdminQueries.query_view_all_users)
        if response is None:
            raise UserNotFound(404, "DataNotFound", "Data Not Found.")
        else:
            return response

    def ban_user(self, uid):
        try:
            target = db.fetch_data(UsersTableQuery.query_select_user_by_uid, (uid,))
            if len(target) == 0:
                raise UserNotFound(404, "UserNotFound", "User not found.")
            db.save_data(
                UsersTableQuery.query_update_user_ban_status, ("banned", self.uid)
            )
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def unban_user(self, uid):
        try:
            target = db.fetch_data(UsersTableQuery.query_select_user_by_uid, (uid,))
            if len(target) == 0:
                raise UserNotFound(404, "UserNotFound", "User not found.")
            db.save_data(
                UsersTableQuery.query_update_user_ban_status, ("unbanned", self.uid)
            )
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")
