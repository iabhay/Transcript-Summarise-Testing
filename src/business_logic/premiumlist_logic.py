"""Premiumlist Logic -> Fetching premiumlisting, adding url for premiumlisting logic"""

import logging
from mysql.connector import Error
from shortuuid import ShortUUID
from datetime import datetime
from database.mysql_database import db
from database.database_query import UsersTableQuery, PremiumListingTable
from utils.custom_exception import (
    UserNotFound,
    DBException,
    NotPremiumUser,
    DataNotFound,
)
from config.api_config import ApiConfig

logger = logging.getLogger(__name__)


class PremiumlistLogic:
    """
    Class for defining History Logic
    ...
    Methods:
    -------
    Constructor() -> fetching current date time
    premium_list() -> adding url for premiumlisting
    view_all_premium_list() -> Fetching all users premium listings
    view_premium_list() -> Fetching premiumlistings of particular user
    """

    def __init__(self):
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def premium_list(self, uid: str, url_id: str):
        """
        Method for premiumlisting of url for any user
        Parameter -> username: str, url_id: str
        Return Type -> None
        Exception Type -> SQLError, UserNotFound, NotPremiumUser
        """
        try:
            if_user_exist = db.fetch_data(
                UsersTableQuery.query_select_user_by_uid, (uid,)
            )
            # username, role, ban
            if not if_user_exist:
                raise UserNotFound(404, ApiConfig.USER_NOT_EXIST)

            elif if_user_exist[0]["role"] != "premiumuser":
                raise NotPremiumUser(422, ApiConfig.USER_IS_NONPREMIUM)

            pid = "P" + ShortUUID("123456789").random(length=4)

            db.save_data(
                PremiumListingTable.query_insert_premium_listing,
                (pid, self.dt_string, uid, url_id),
            )
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def view_all_premium_list(self) -> list:
        """
        Method for viewing premiumlisting of urls of all users
        Parameter -> self
        Return Type -> list
        Exception Type -> SQLError, DataNotFound
        """
        try:
            response = db.fetch_data(
                PremiumListingTable.query_select_all_premium_listing
            )
            if not response:
                raise DataNotFound(404, ApiConfig.DATA_NOT_EXIST)
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def view_premium_list(self, uid: str) -> list:
        """
        Method for viewing premiumlisting of urls of any user
        Parameter -> uid: str
        Return Type -> list
        Exception Type -> SQLError, DataNotFound
        """
        try:
            response = db.fetch_data(
                PremiumListingTable.query_select_premium_listing, (uid,)
            )
            if not response:
                raise DataNotFound(404, ApiConfig.DATA_NOT_EXIST)
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)
