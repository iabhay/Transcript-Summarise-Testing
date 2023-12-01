import logging
from shortuuid import ShortUUID
from datetime import datetime
from database.db_ops.db_helper import DBHelper
from database.database_query import PremiumListingTable
from config.log_config.log_config import LogStatements
logger = logging.getLogger('premium_listing_db')

class PremiumListingsDB:
    def __init__(self, uid):
        self.uid = uid
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def save_premium_url(self, urlid):
        if not self.check_premium_list_url(urlid):
            pid = "P" + ShortUUID("123456789").random(length=4)
            try:
                DBHelper.save_data(PremiumListingTable.query_insert_premium_listing, (pid, self.dt_string, self.uid, urlid))
                logger.info(LogStatements.premium_listing_of_url)
            except Exception as e:
                logger.debug(LogStatements.fail_premium_listing_of_url)

    def check_premium_list_url(self, urlid):
        try:
            return DBHelper.fetch_data(PremiumListingTable.query_select_premium_url_for_user, (urlid, self.uid))
        except Exception as e:
            logger.debug(LogStatements.log_exception_message)

    def view_premium_user_listing(self):
        try:
            table_schema = ['Date', 'Username', 'Url']
            DBHelper.display_data(PremiumListingTable.query_select_premium_listing, table_schema, (self.uid, ))
        except Exception as e:
            logger.debug(LogStatements.log_exception_message)
    def view_all_premium_listings(self):
        try:
            table_schema = ['Date', 'Username', 'Url']
            DBHelper.display_data(PremiumListingTable.query_select_all_premium_listing, table_schema)
        except Exception as e:
            logger.debug(LogStatements.log_exception_message)

    def remove_premium_listing(self, uid):
        try:
            DBHelper.delete_data(PremiumListingTable.query_delete_premium_listing, (uid, ))
            logger.info(LogStatements.premium_unlisting_of_url)
        except Exception as e:
            logger.debug(LogStatements.fail_premium_unlisting_of_url)