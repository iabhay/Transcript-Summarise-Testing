import logging
from datetime import datetime
from shortuuid import ShortUUID
from database.database_query import MessageTableQuery
from database.db_ops.db_helper import DBHelper
from config.log_config.log_config import LogStatements
logger = logging.getLogger('messages_db')

class MessageDB:
    def __init__(self, uid):
        self.uid = uid
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def banned_module(self):
        message = input("Send Message to Admin for Unban: ")
        try:
            self.save_message(message)
            print("Successfully sent message.")
        except:
            raise Exception("Message not sent successfully.")

    def save_message(self, description):
        try:
            mid = "M" + ShortUUID("123456789").random(length=4)
            DBHelper.save_data(MessageTableQuery.query_insert_message, (mid, self.dt_string, self.uid, description))
            logger.info(LogStatements.message_sent)
        except Exception as e:
            logger.debug(LogStatements.fail_message_sent)
    def delete_message_by_admin(self):
        try:
            DBHelper.delete_data(MessageTableQuery.query_delete_message, (self.uid,))
            logger.info(LogStatements.message_delete)
        except Exception as e:
            logger.debug(LogStatements.fail_message_delete)
    def view_one_message(self, username):
        try:
            table_schema = ['Date', 'Username', 'Description']
            DBHelper.display_data(MessageTableQuery.query_select_message, table_schema, (username,))
        except Exception as e:
            logger.debug(LogStatements.log_exception_message)

    def view_premium_messages(self):
        try:
            table_schema = ['Date', 'Username', 'Description']
            DBHelper.display_data(MessageTableQuery.query_select_premium_message, table_schema)
        except Exception as e:
            logger.debug(LogStatements.log_exception_message)

    def view_non_premium_messages(self):
        try:
            table_schema = ['Date', 'Username', 'Description']
            DBHelper.display_data(MessageTableQuery.query_select_non_premium_message, table_schema)
        except Exception as e:
            logger.debug(LogStatements.log_exception_message)

    def view_all_messages(self):
        try:
            table_schema = ['Date', 'Username', 'Description']
            DBHelper.display_data(MessageTableQuery.query_select_all_messages, table_schema)
        except Exception as e:
            logger.debug(LogStatements.log_exception_message)