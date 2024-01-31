import logging
from mysql.connector import Error
from shortuuid import ShortUUID
from datetime import datetime
from utils_api.utility_functions import extract_video_id
from database.mysql_database import db
from database.database_query import BannedUrlTable
from utils.custom_exception import DBException, DataNotFound

logger = logging.getLogger(__name__)


# All Url Functionalities
class UrlLogic:
    def __init__(self):
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def ban_url(self, url_id):
        try:
            url_id = extract_video_id(url_id)
            category = "banned_by_admin"
            severity = 10
            bid = "B" + ShortUUID("123456789").random(length=4)
            db.save_data(
                BannedUrlTable.query_insert_ban_url, (bid, url_id, category, severity)
            )
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def unban_url(self, url_id):
        try:
            url_id = extract_video_id(url_id)
            db.delete_data(BannedUrlTable.query_unban_url, (url_id,))
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def view_all_ban_url(self):
        try:
            response = db.fetch_data(BannedUrlTable.query_select_all_ban_url)
            if len(response) == 0:
                raise DataNotFound(404, "DataNotFound", "Data doesn't exist.")
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def view_ban_url(self, urlid):
        try:
            response = db.fetch_data(BannedUrlTable.query_select_ban_url, (urlid,))
            if len(response) == 0:
                raise DataNotFound(404, "DataNotFound", "Data doesn't exist.")
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")
