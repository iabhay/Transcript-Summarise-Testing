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
from flask import current_app as app
from flask_jwt_extended import get_jwt
import hashlib
from mysql.connector import Error
from utils.custom_exception import InvalidLogin
from database.database_query import UsersTableQuery
from utils.custom_exception import DBException
from database.mysql_database import db
from config.api_config import ApiConfig
from business_logic.token_logic.access_token_logic import AccessToken
from business_logic.token_logic.refresh_token_logic import RefreshToken


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
            app.logger.error(f"Error in SQL {e}")
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
        token_gen = AccessToken()
        tokens = token_gen.create_token(True, entry[0]["uid"], {"role": entry[0]["role"], "ban_status": entry[0]["ban_status"]})
        response["access_token"] = tokens[0]
        response["refresh_token"] = tokens[1]
        return response
    
    def logout(self) -> tuple:
        """Method responsible for calling business logic for logging out the system for user..
           Parameters -> None
           Returns -> tuple
        """
        token_claims = get_jwt()
        identity = token_claims["sub"]
        auth_token_business = AccessToken()
        auth_token_business.revoke_token(identity)
        app.logger.info("User Logged Out!")
        return {"message": ApiConfig.LOGOUT_SUCCESS}, 200
    
    def refresh_user(self, refresh_jti: str, identity: str, role: str, ban_status: str) -> tuple:
        """Method responsible for calling business logic for creating new access and refresh token.
           Parameters -> refresh_jti: str, username: str, role: str, p_type: str
           Returns -> tuple
        """
        token = AccessToken()
        refresh_token_business = RefreshToken()
        data = refresh_token_business.generate_new_token(refresh_jti, identity, role, ban_status)
        access_token = data[0]["access_token"]
        refresh_token = data[0]["refresh_token"]
        return {"message": "New tokens generated successfully.",
                "access_token": access_token,
                "refresh_token":refresh_token}, 200
    
    def update_token(self, access_jti: str, identity: str, role: str, ban_status: str) -> tuple:
        """Method responsible for calling business logic for creating new access and refresh token.
           Parameters -> refresh_jti: str, username: str, role: str, p_type: str
           Returns -> tuple
        """
        token = AccessToken()
        refresh_token_business = RefreshToken()
        token.revoke_token(identity)
        tokens = token.create_token(False, identity, {"role": role, "ban_status": ban_status})
        access_token = tokens[0]
        refresh_token = tokens[1]
        return {"message": "New tokens generated successfully.",
                "access_token": access_token,
                "refresh_token":refresh_token}
