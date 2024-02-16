"""History Logic -> Fetching history of specific user or all users"""

import logging
from mysql.connector import Error
from service_handler.transcript_handler.transcript_generator import transcriptor
from datetime import datetime
from database.mysql_database import db
from database.database_query import HistoryTableQuery
from utils.custom_exception import DBException, DataNotFound
from config.api_config import ApiConfig

logger = logging.getLogger(__name__)


class HistoryLogic:
    """
    Class for defining History Logic
    ...
    Methods:
    -------
    Constructor() -> fetching current date time and initialising transcriptor
    view_all_history() -> Fetching all users history
    view_history() -> Fetching history of particular user
    """

    def __init__(self, uid):
        self.uid = uid
        self.trancriptor = transcriptor()
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def view_all_history(self):
        """
        Method fetching history of all users
        Return Type -> list
        Exception Type -> SQLError, DataNotFound
        """
        try:
            response = db.fetch_data(HistoryTableQuery.query_select_all_history)
            if len(response) == 0:
                raise DataNotFound(404, ApiConfig.DATA_NOT_EXIST)
            return response

        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def view_history(self, uid: str):
        """
        Method fetching history of user
        Parameter -> uid: str
        Return Type -> list
        Exception Type -> SQLError, DataNotFound
        """
        try:
            response = db.fetch_data(HistoryTableQuery.query_select_history, (uid,))
            if len(response) == 0:
                raise DataNotFound(404, ApiConfig.DATA_NOT_EXIST)
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)
