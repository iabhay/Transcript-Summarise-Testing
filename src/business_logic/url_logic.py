import logging
import pymysql
from shortuuid import ShortUUID
from datetime import datetime
from utils.utils_api.utility_functions import extract_video_id
from database.mysql_database import db
from database.database_query import BannedUrlTable
from utils.custom_exception import DBException, DataNotFound
from config.api_config import ApiConfig

logger = logging.getLogger(__name__)


# All Url Functionalities
class UrlLogic:
    def __init__(self):
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def ban_url(self, url_id):
        try:
            category = "banned_by_admin"
            severity = 10
            bid = "B" + ShortUUID(ApiConfig.UID_CONSTRAINTS).random(length=4)
            db.save_data(
                BannedUrlTable.query_insert_ban_url, (bid, url_id, category, severity)
            )
        except pymysql.IntegrityError:
            return None
        except pymysql.Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def unban_url(self, url_id):
        try:
            db.delete_data(BannedUrlTable.query_unban_url, (url_id,))
        except pymysql.Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def view_all_ban_url(self):
        try:
            response = db.fetch_data(BannedUrlTable.query_select_all_ban_url)
            print(response)
            if not response:
                raise DataNotFound(404, ApiConfig.DATA_NOT_EXIST)
            return response
        except pymysql.Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def view_ban_url(self, urlid):
        try:
            response = db.fetch_data(BannedUrlTable.query_select_ban_url, (urlid,))
            if not response:
                raise DataNotFound(404, ApiConfig.DATA_NOT_EXIST)
            return response
        except pymysql.Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)
