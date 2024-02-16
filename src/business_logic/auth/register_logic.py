"""
Logic for register endpoint.
Hashed password generated from user's entered password.
Then two unique ids generated for two table entries.
Data saved to Database if no error occurred.
But, if error occurred then it can be of Integrity error then 
Invalid Register Error Response is raised.
"""

import hashlib
from mysql.connector import Error
from utils.custom_exception import InvalidRegister, DBException
from mysql.connector import IntegrityError
from database.database_query import UsersTableQuery, UserSearchesTableQuery
from database.mysql_database import db
from shortuuid import ShortUUID
from datetime import datetime
from config.api_config import ApiConfig


class RegisterLogic:
    """
    Class for defining Register Logic
    ...
    Methods:
    -------
    Constructor() -> fetching current date time
    add_user() -> adding new user in application.
    """

    def __init__(self) -> None:
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def add_user(self, username: str, password: str) -> None:
        """
        Method add user details to db
        Parameter -> username: str, password: str
        Return Type -> None
        Exceptions Type -> Integrity Error if user exists already
        """
        try:
            hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            self.uid = "U" + ShortUUID(ApiConfig.UID_CONSTRAINTS).random(length=4)
            sid = "S" + ShortUUID(ApiConfig.UID_CONSTRAINTS).random(length=4)
            db.save_data(
                UsersTableQuery.query_insert_user,
                (self.uid, self.dt_string, username, hashed_password),
            )
            db.save_data(
                UserSearchesTableQuery.query_insert_user_search,
                (sid, self.dt_string, self.uid),
            )
        except IntegrityError as err:
            raise InvalidRegister(409, ApiConfig.USER_ALREADY_EXIST)
        except Error as err:
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)
