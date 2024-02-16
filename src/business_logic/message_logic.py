"""Message Logic -> adding message, fetching all messages, premium user messages, non premium messages, particular user message"""

import logging
from mysql.connector import Error
from shortuuid import ShortUUID
from datetime import datetime
from database.mysql_database import db
from database.database_query import UsersTableQuery, MessageTableQuery
from utils.custom_exception import UserNotFound, DBException, DataNotFound
from config.api_config import ApiConfig

logger = logging.getLogger(__name__)


class MessageLogic:
    """
    Class for defining Message Logic
    ...
    Methods:
    -------
    Constructor() -> fetching current date time
    view_premium_message() -> fetching all premium users messages
    view_nonpremium_message() -> fetching all non premium user messages
    view_all_message() -> fetching all users messages
    view_user_message() -> fetching particular user message
    send_message() -> adding message from any user for admin
    """

    def __init__(self):
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def view_premium_message(self):
        """
        Method fetching messages of premium users
        Parameter -> self
        Return Type -> list
        Exception Type -> SQLError, DataNotFound
        """
        try:
            response = db.fetch_data(MessageTableQuery.query_select_premium_message)
            if len(response) == 0:
                raise DataNotFound(404, ApiConfig.DATA_NOT_FOUND)
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def view_nonpremium_message(self):
        """
        Method fetching messages of non premium users
        Parameter -> self
        Return Type -> list
        Exception Type -> SQLError, DataNotFound
        """
        try:
            response = db.fetch_data(MessageTableQuery.query_select_non_premium_message)
            if len(response) == 0:
                raise DataNotFound(404, ApiConfig.DATA_NOT_FOUND)
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def view_all_message(self):
        """
        Method fetching messages of all users
        Parameter -> self
        Return Type -> list
        Exception Type -> SQLError, DataNotFound
        """
        try:
            response = db.fetch_data(MessageTableQuery.query_select_all_messages)
            if len(response) == 0:
                raise DataNotFound(404, ApiConfig.DATA_NOT_FOUND)
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def view_user_message(self, uid: str) -> list:
        """
        Method fetching message of particular user
        Parameter -> uid: str
        Return Type -> list
        Exception Type -> UserNotFound, SQLError, DataNotFound
        """
        try:
            target = db.fetch_data(UsersTableQuery.query_select_user_by_uid, (uid,))
            if len(target) == 0:
                raise UserNotFound(404, ApiConfig.USER_NOT_EXIST)
            response = db.fetch_data(MessageTableQuery.query_select_all_messages)
            if len(response) == 0:
                raise DataNotFound(404, ApiConfig.DATA_NOT_FOUND)
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def send_message(self, uid, description):
        """
        Method for adding message of particular user
        Parameter -> description: str
        Return Type -> None
        Exception Type -> SQLError
        """
        try:
            mid = "M" + ShortUUID("123456789").random(length=4)
            db.save_data(
                MessageTableQuery.query_insert_message,
                (mid, self.dt_string, uid, description),
            )
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)
