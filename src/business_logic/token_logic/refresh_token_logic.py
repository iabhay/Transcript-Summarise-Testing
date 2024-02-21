"""
    Module containing business logic related to the creation of new access token(fresh=False)
    and refresh token.
"""

import pymysql

from config.api_config import ApiConfig
from database.database_query import BlocklistQuery 
from database.mysql_database import db
from utils.custom_exception import AppException, DBException
from business_logic.token_logic.access_token_logic import AccessToken

class RefreshToken:
    """
        Class containing business logic related to access and refresh token generation.
    """

    def __init__(self) -> None:
        self.token = AccessToken()

    def generate_new_token(self, refresh_jti: str, identity: str, role: str, ban_status: str) -> list:
        """
            Method to generate new access and refresh tokens.
            Parameters -> refresh_jti: str, user_identity: str, role: str, p_type: int
            Returns -> list
        """
        try:
            data = db.fetch_data(BlocklistQuery.FETCH_REFRESH_TOKEN, (identity, ApiConfig.TOKEN_ISSUED))
            if not data:
                raise AppException(401, "Unauthorized")

            get_token_jti = data[0]["refresh_token"]
            if refresh_jti != get_token_jti:
                raise AppException(401, "Unauthorized")

            self.token.revoke_token(identity)
            tokens = self.token.create_token(False, identity,
                                             {"role": role, "ban_status": ban_status})
            access_token = tokens[0]
            refresh_token = tokens[1]
            return [{
                "access_token": access_token,
                "refresh_token": refresh_token
            }]
        except pymysql.Error:
            raise DBException(500, "Internal Server Error")