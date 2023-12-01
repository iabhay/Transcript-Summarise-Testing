import logging
from database.db_ops.messages_db import MessageDB
from database.db_ops.premium_listing_db import PremiumListingsDB
from database.db_ops.history_db import HistoryDB
from utils.input_validator import url_validation
from config.log_config.log_config import LogStatements
logger = logging.getLogger('non_premium_user')


class PremiumUserController:
    def __init__(self, uid):
        self.uid = uid
        self.msg_obj = MessageDB(uid)
        self.premium_obj = PremiumListingsDB(uid)
        self.history_obj = HistoryDB(uid)

    def send_message_to_admin(self, url=""):
        ask = input("Enter Message for admin: ")
        ask = ask.strip()
        # if url is given that means premium listing message
        if len(url) > 0:
            ask = ask + ", Url for premium listing -> " + url
            self.msg_obj.save_message(ask)
            logger.info(LogStatements.premium_user_premium_listing_request)
            print("Message sent successfully.")
        elif len(ask) > 0:
            self.msg_obj.save_message(ask)
            logger.info(LogStatements.premium_user_language_request)
            print("Message sent successfully.")
        return None

    def premium_listing_of_banned_url(self):
        url = input("Enter URL for premium listing: ")
        url = url.strip()
        if url_validation(url):
            self.send_message_to_admin(url)
            print("Once approved by admin, it'll be added to your premium listing.")
            return None
        else:
            print("Enter valid url.")

    def view_my_premium_listing(self):
        self.premium_obj.view_premium_user_listing()
        return None

    def view_my_history(self):
        self.history_obj.view_one_user_history()
        return None