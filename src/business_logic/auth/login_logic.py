"""
Login logic -> 
1. Generate Hashed password from user's given password.
2. Check if user exists using username and hashed password.
3. if exist then valid login -> Success Response Generated.
4. If not exist then raise Invalid Login Response.
5. In success response -> access_token generated for that user with successful login message.
6. In access_token -> role, username, uid, ban_status are also sent as additional claims.
7. Error can be of Resource Not Found.
"""

import hashlib
import logging
from mysql.connector import Error
from flask_jwt_extended import create_access_token
from utils.custom_exception import InvalidLogin
from database.database_query import UsersTableQuery
from utils.custom_exception import DBException
from database.mysql_database import db
from config.api_config import ApiConfig


logger = logging.getLogger(__name__)


class LoginLogic:
    """
    Class for defining Login Logic
    ...
    Methods:
    -------
    login() -> Check if user exist or not.
    """

    def login(self, username: str, password: str) -> dict:
        """
        Method which find entry from db using hashed password and usernameand check if user exists
        Parameter -> username: str, password: str
        Return Type -> dict
        """
        try:
            hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            entry = db.fetch_data(
                UsersTableQuery.query_select_user, (username, hashed_password)
            )

            if not entry:
                raise InvalidLogin(404, ApiConfig.USER_NOT_EXIST)
            else:
                response = self.response_generator(entry)
                return response

        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, ApiConfig.SERVER_NOT_WORKING)

    def response_generator(self, entry: list):
        """
        Method which generate response using token and message
        Parameter -> entry: list
        Return Type -> dict
        """
        response = {
            "message": ApiConfig.LOGIN_SUCCESS,
        }
        response["token"] = self.token_generator(entry)
        return response

    def token_generator(self, entry: list):
        """
        Method which generate token
        Parameter -> entry: list
        Return Type -> str
        """
        access_token = create_access_token(
            identity=entry[0]["uid"],
            additional_claims={
                "role": entry[0]["role"],
                "username": entry[0]["username"],
                "ban_status": entry[0]["ban_status"],
            },
        )
        return access_token
