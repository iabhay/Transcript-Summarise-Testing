import logging
from datetime import datetime
from shortuuid import ShortUUID
from database.database_query import HistoryTableQuery
from database.db_ops.db_helper import DBHelper
from config.log_config.log_config import LogStatements
logger = logging.getLogger('history_db')

class HistoryDB:
    def __init__(self, uid):
        self.uid = uid
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def save_history(self, urlid):
        try:
            hid = "H" + ShortUUID("123456789").random(length=4)
            DBHelper.save_data(HistoryTableQuery.query_insert_history, (hid, self.dt_string, self.uid, urlid))
            logger.info(LogStatements.user_history_saved)
        except Exception as e:
            logger.debug(LogStatements.fail_user_history_saved)
        else:
            return hid

    def view_one_user_history(self):
        try:
            table_schema = ['Date', 'Url']
            DBHelper.display_data(HistoryTableQuery.query_select_history, table_schema, (self.uid,))
        except Exception as e:
            logger.debug(LogStatements.log_exception_message)

    def view_all_history(self):
        try:
            table_schema = ['Date','Username', 'URL']
            DBHelper.display_data(HistoryTableQuery.query_select_all_history, table_schema)
        except Exception as e:
            logger.debug(LogStatements.log_exception_message)