import logging
from database.db_ops.messages_db import MessageDB
from database.database_query import AdminQueries
from database.db_ops.users_db import UsersDB
from database.db_ops.ban_url_db import BanUrlDB
from service_handler.transcript_handler.transcript_generator import transcriptor
from database.db_ops.premium_listing_db import PremiumListingsDB
from database.db_ops.db_helper import DBHelper
from database.database_query import UsersTableQuery
from database.db_ops.history_db import HistoryDB
from utils.input_validator import username_validation, url_validation
from config.config import Config
from config.log_config.log_config import LogStatements
logger = logging.getLogger('admincontroller')


# All Admin Functionalities
class AdminController:
    def __init__(self, uid):
        self.uid = uid
        self.msg_obj = MessageDB(self.uid)
        self.ban_url_obj = BanUrlDB()
        self.trancriptor = transcriptor()

    def view_user(self):
        username = input(Config.ENTER_USERNAME_PROMPT)
        username = username.strip()
        if username_validation(username):
            valid = self.uid_generator(username)
            if not valid:
                print(Config.NO_USER_FOUND)
            else:
                target_uid = valid[0]
                table_schema = ['Uid', 'Username', 'Registered on', 'Role', 'Ban Status', 'Date of banned searches', 'Today Banned Search Count']
                DBHelper.display_data(AdminQueries.query_view_user, table_schema, (target_uid,))
        else:
            print("Enter Valid Username")
            
    def view_all_users(self):
        table_schema = ['Uid', 'Username', 'Registered on', 'Role', 'Ban Status', 'Date of banned searches', 'Today banned Search Count']
        DBHelper.display_data(AdminQueries.query_view_all_users, table_schema)

    def downgrade_premium_user(self):
        username = input(Config.ENTER_USERNAME_PROMPT)
        username = username.strip()
        if username_validation(username):
            valid = self.uid_generator(username)
            if not valid:
                print(Config.NO_USER_FOUND)
            else:
                target_uid = valid[0]
                user_obj = UsersDB(target_uid)
                user_obj.update_user("role", "nonpremiumuser")
                logger.info(LogStatements.log_user_downgraded_by_admin)
                print("User downgraded")
        else:
            print("Enter Valid Username")

    def ban_user(self):
        username = input(Config.ENTER_USERNAME_PROMPT)
        username = username.strip()
        if username_validation(username):
            valid = self.uid_generator(username)
            if not valid:
                print(Config.NO_USER_FOUND)
            else:
                target_uid = valid[0]
                user_obj = UsersDB(target_uid)
                user_obj.update_user("ban_status", "banned")
                logger.info(LogStatements.log_user_banned_by_admin)
                print("User banned")
        else:
            print("Enter Valid Username")

    def unban_user(self):
        username = input(Config.ENTER_USERNAME_PROMPT)
        username = username.strip()
        if username_validation(username):
            valid = self.uid_generator(username)
            if not valid:
                print(Config.NO_USER_FOUND)
            else:
                target_uid = valid[0]
                user_obj = UsersDB(target_uid)
                user_obj.update_user("ban_status", "unbanned")
                logger.info(LogStatements.log_user_unbanned_by_admin)
                print("User unbanned")
        else:
            print("Enter Valid Username")

    def ban_url(self):
        ask = input(Config.ENTER_URL)
        ask = ask.strip()
        if url_validation(ask):
            urlid = self.trancriptor.extract_video_id(ask)
            self.ban_url_obj.save_ban_url(urlid, "Admin", "5")
            logger.info(LogStatements.log_url_banned_by_admin)
            print("Url banned")
        else:
            print("Enter valid url")

    def unban_url(self):
        ask = input(Config.ENTER_URL)
        ask = ask.strip()
        if url_validation(ask):
            urlid = self.trancriptor.extract_video_id(ask)
            entry = self.ban_url_obj.check_ban_url(urlid)
            if entry:
                self.ban_url_obj.delete_ban_url(urlid)
                logger.info(LogStatements.log_url_unbanned_by_admin)
                print("Url unbanned")
            else:
                print(Config.NO_URL_FOUND)
        else:
            print("Enter valid url")

    def unban_url_for_premium_user(self):
        ask = input(Config.ENTER_URL)
        ask = ask.strip()
        username = input(Config.ENTER_USERNAME_PROMPT)
        username = username.strip()
        if url_validation(ask) and username_validation(username):
            valid = self.uid_generator(username)
            if valid:
                target_uid = valid[0]
                urlid = self.trancriptor.extract_video_id(ask)
                entry = self.ban_url_obj.fetch_ban_url(urlid)
                premium_listing_obj = PremiumListingsDB(target_uid)
                if entry:
                    # If severity level is too much then admin gets message for why he can't unban
                    if entry[0][2] > 5:
                        print(f"Can't be unbanned.\nReason Category - {entry[0][1]}\nSeverity Level(Greater than 5) - {entry[0][2]}")
                    else:
                        premium_listing_obj.save_premium_url(ask)
                        logger.info(LogStatements.log_url_premium_listed_by_admin)
                        print(f"Premium Listing done for {username}")
                else:
                    print(Config.NO_URL_FOUND)
            else:
                print(Config.NO_USER_FOUND)
        else:
            print("Enter valid url/username")

    def message_from_user(self):
        username = input(Config.ENTER_USERNAME_PROMPT)
        username = username.strip()
        if username_validation(username):
            self.msg_obj.view_one_message(username)
        else:
            print("Enter valid username")

    def messages_from_non_premium_users(self):
        self.msg_obj.view_non_premium_messages()

    def messages_from_premium_users(self):
        self.msg_obj.view_premium_messages()

    def view_all_messages(self):
        self.msg_obj.view_all_messages()

    def uid_generator(self, username):
        target = DBHelper.fetch_data(UsersTableQuery.query_select_user_by_admin, (username,))
        if target:
            return target[0]
        return

    def view_history_of_user(self):
        username = input(Config.ENTER_USERNAME_PROMPT)
        username = username.strip()
        if username_validation(username):
            valid = self.uid_generator(username)
            if not valid:
                print(Config.NO_USER_FOUND)
            else:
                target_uid = valid[0]
                history_obj = HistoryDB(target_uid)
                history_obj.view_one_user_history()
        else:
            print("Enter valid username")
    def view_premium_listing_of_user(self):
        username = input(Config.ENTER_USERNAME_PROMPT)
        username = username.strip()
        if username_validation(username):
            valid = self.uid_generator(username)
            if not valid:
                print(Config.NO_USER_FOUND)
            else:
                target_uid = valid[0]
                premium_listing_obj = PremiumListingsDB(target_uid)
                premium_listing_obj.view_premium_user_listing()
        else:
            print("Enter valid username")

    def view_all_history(self):
        history_obj = HistoryDB(self.uid)
        history_obj.view_all_history()

    def view_all_premium_listings(self):
        premium_listing_obj = PremiumListingsDB(self.uid)
        premium_listing_obj.view_all_premium_listings()

    def show_all_ban_urls(self):
        self.ban_url_obj.view_all_ban_urls()

    def show_ban_url(self):
        ask = input(Config.ENTER_URL)
        ask = ask.strip()
        if url_validation(ask):
            urlid = self.trancriptor.extract_video_id(ask)
            entry = self.ban_url_obj.view_ban_url(urlid)
            entry_fetch = self.ban_url_obj.fetch_ban_url(urlid)
            if not entry_fetch:
                print(Config.NO_URL_FOUND)
        else:
            print("Enter valid url.")
