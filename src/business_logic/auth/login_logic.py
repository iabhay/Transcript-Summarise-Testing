import hashlib
import logging
from mysql.connector import Error
from flask_jwt_extended import create_access_token
from utils.custom_exception import InvalidLogin
from database.database_query import UsersTableQuery, UserSearchesTableQuery
from utils.custom_exception import DBException
from database.mysql_database import db

logger = logging.getLogger(__name__)


class LoginLogic:
    def login(self, username, password):
        try:
            hashed_password = hashlib.sha256(password.encode("utf-8")).hexdigest()
            entry = db.fetch_data(
                UsersTableQuery.query_select_user, (username, hashed_password)
            )

            if not entry:
                raise InvalidLogin(404, "NotFound", "User Not Exists")
            else:
                response = self.response_generator(entry)
                return response

        except Error as e:
            logger.error(f"Error in SQL {e}")
            raise DBException(500, "InternalServerError", "Server not responding.")

    def response_generator(self, entry):
        response = {
            "message": "Logged in Successfully.",
        }
        response["token"] = self.token_generator(entry)
        return response

    def token_generator(self, entry):
        access_token = create_access_token(
            identity=entry[0]["uid"],
            additional_claims={
                "role": entry[0]["role"],
                "username": entry[0]["username"],
                "ban_status": entry[0]["ban_status"],
            },
        )
        return access_token
