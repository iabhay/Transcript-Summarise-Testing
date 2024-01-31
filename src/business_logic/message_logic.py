import logging
from mysql.connector import Error
from shortuuid import ShortUUID
from datetime import datetime
from database.mysql_database import db
from database.database_query import UsersTableQuery, MessageTableQuery
from utils.custom_exception import UserNotFound, DBException, DataNotFound

logger = logging.getLogger(__name__)


# All Message Functionalities
class MessageLogic:
    def __init__(self):
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def view_premium_message(self):
        try:
            response = db.fetch_data(MessageTableQuery.query_select_premium_message)
            if len(response) == 0:
                raise DataNotFound(404, "DataNotFound", "Data doesn't exist.")
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def view_nonpremium_message(self):
        try:
            response = db.fetch_data(MessageTableQuery.query_select_non_premium_message)
            if len(response) == 0:
                raise DataNotFound(404, "DataNotFound", "Data doesn't exist.")
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def view_all_message(self):
        try:
            response = db.fetch_data(MessageTableQuery.query_select_all_messages)
            if len(response) == 0:
                raise DataNotFound(404, "DataNotFound", "Data doesn't exist.")
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def view_user_message(self, uid):
        try:
            target = db.fetch_data(UsersTableQuery.query_select_user_by_uid, (uid,))
            if len(target) == 0:
                raise UserNotFound(404, "UserNotFound", "User not found.")
            response = db.fetch_data(MessageTableQuery.query_select_all_messages)
            if len(response) == 0:
                raise DataNotFound(404, "DataNotFound", "Data doesn't exist.")
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def send_message(self, description):
        try:
            mid = "M" + ShortUUID("123456789").random(length=4)
            db.save_data(
                MessageTableQuery.query_insert_message,
                (mid, self.dt_string, self.uid, description),
            )
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")
