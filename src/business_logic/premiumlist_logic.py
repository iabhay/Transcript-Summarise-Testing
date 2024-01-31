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

logger = logging.getLogger(__name__)


# All Premiumlist Functionalities
class PremiumlistLogic:
    def __init__(self):
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def premium_list(self, username, urlid):
        try:
            uid = self.uid_generator(username)
            if_user_exist = db.fetch_data(
                UsersTableQuery.query_select_user_by_uid, (uid,)
            )
            # username, role, ban
            if len(if_user_exist) == 0:
                raise UserNotFound(404, "UserNotFound", "User not found.")

            elif if_user_exist[0]["role"] != "premium":
                raise NotPremiumUser(
                    422, "UnprocessibleEntity", "User is not Premium User."
                )

            pid = "P" + ShortUUID("123456789").random(length=4)

            db.save_data(
                PremiumListingTable.query_insert_premium_listing,
                (pid, self.dt_string, uid, urlid),
            )
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def view_all_premium_list(self):
        try:
            response = db.fetch_data(
                PremiumListingTable.query_select_all_premium_listing
            )
            if len(response) == 0:
                raise DataNotFound(404, "DataNotFound", "Data doesn't exist.")
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def view_premium_list(self, uid):
        try:
            response = db.fetch_data(
                PremiumListingTable.query_select_premium_listing, (uid,)
            )
            if len(response) == 0:
                raise DataNotFound(404, "DataNotFound", "Data doesn't exist.")
            return response
        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")
