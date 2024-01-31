import hashlib
from config.config import Config
from utils.custom_exception import InvalidRegister
from database.database_query import UsersTableQuery, UserSearchesTableQuery
from database.mysql_database import db
from shortuuid import ShortUUID
from datetime import datetime


class RegisterLogic:
    def __init__(self) -> None:
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def add_user(self, username, password):
        username = username.strip()
        password = password.strip()
        hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
        if not self.check_registration(username, hashed_password):
            self.uid = "U" + ShortUUID("123456789").random(length=4)
            sid = "S" + ShortUUID("123456789").random(length=4)
            db.save_data(
                UsersTableQuery.query_insert_user,
                (self.uid, self.dt_string, username, hashed_password),
            )
            db.save_data(
                UserSearchesTableQuery.query_insert_user_search,
                (sid, self.dt_string, self.uid),
            )
        else:
            raise InvalidRegister(409, "ConflictError", "User already exixts.")

    def check_registration(self, username, password):
        is_already_registered = db.fetch_data(
            UsersTableQuery.query_select_user, (username, password)
        )
        if len(is_already_registered) > 0:
            return True
        else:
            return False
