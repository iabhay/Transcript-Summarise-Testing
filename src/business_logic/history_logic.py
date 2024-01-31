import logging
from mysql.connector import Error
from flask import request
from service_handler.transcript_handler.transcript_generator import transcriptor
from shortuuid import ShortUUID
from datetime import datetime
from database.mysql_database import db
from database.database_query import HistoryTableQuery
from utils.custom_exception import DBException, DataNotFound
from config.config import Config
from config.log_config.log_config import LogStatements

logger = logging.getLogger(__name__)


# All Admin Functionalities
class HistoryLogic:
    def __init__(self, uid):
        self.uid = uid
        self.trancriptor = transcriptor()
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def view_all_history(self):
        try:
            response = db.fetch_data(HistoryTableQuery.query_select_all_history)
            if len(response) == 0:
                raise DataNotFound(404, "DataNotFound", "Data doesn't exist.")
            return response

        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def view_history(self, uid):
        try:
            response = db.fetch_data(HistoryTableQuery.query_select_history, (uid,))
            if len(response) == 0:
                raise DataNotFound(404, "DataNotFound", "Data doesn't exist.")
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")
