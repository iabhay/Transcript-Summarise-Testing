"""Module containing logic related to access tokens."""

import pymysql
from flask_jwt_extended import (create_access_token, create_refresh_token, get_jwt, get_jti)
from config.api_config import ApiConfig
from database.database_query import BlocklistQuery
from database.mysql_database import db
from utils.custom_exception import DBException


class AccessToken:
    """
        Class containing logic related creating and handling authorization tokens.
        Methods
        -------
        create_token(): tuple -> Method for creating tokens.
        get_user_claims(): dict -> Method for getting claims.
        save_tokens_to_database(): None -> Method for saving tokens in database.
        revoke_token(): None -> Method for revoking access and refresh tokens.
        is_token_revoked(): bool -> Method for checking if token is revoked or not.
    """

    def create_token(self, fresh_token: bool, identity: str, claims: dict) -> tuple:
        """
            Method for generating tokens.
            Parameters -> fresh_token: bool, identity: str, claims: dict
            Returns -> tuple
        """
        self.revoke_token(identity)
        access_token = create_access_token(identity=identity, fresh=fresh_token, additional_claims=claims)
        access_token_jti = get_jti(access_token)
        refresh_token = create_refresh_token(identity=identity, additional_claims=claims)
        refresh_token_jti = get_jti(refresh_token)
        self.save_tokens_to_database(identity, access_token_jti, refresh_token_jti)
        return access_token, refresh_token

    def get_user_claims(self) -> dict:
        """
            Method to get user claims.
            Parameters -> None
            Returns -> dict
        """
        return get_jwt()

    def save_tokens_to_database(self, identity: str, access_token: str, refresh_token: str) -> None:
        """
            Method to save tokens generated to database.
            Parameters -> access_token: str, refresh_token: str
            Returns -> None
        """
        try:
            db.save_data(BlocklistQuery.INSERT_TOKEN, (identity, access_token, refresh_token))
        except pymysql.Error:
            raise DBException(500, "Internal Server Error", "Something wrong with the server.")

    def revoke_token(self, identity: str) -> None:
        """
            Method responsible for revoking access and refresh tokens.
            Parameters -> access_token: str
            Returns -> None
        """
        try:
            db.save_data(BlocklistQuery.REVOKE_TOKEN, (identity,))
        except pymysql.Error:
            raise DBException(500, "Internal Server Error", "Something wrong with the server.")

    def is_token_revoked(self, token_jti: str, token_type: str) -> bool:
        """
            Method to check whether the token is revoked or not.
            Parameters -> token_jti: str
            Returns -> bool
        """
        try:
            query = BlocklistQuery.FETCH_TOKEN_STATUS.format(token_type)
            data = db.fetch_data(query, (token_jti, ))

            if not data:
                return False

            if data[0]["status"] == ApiConfig.TOKEN_REVOKED:
                return True
            else:
                return False

        except pymysql.Error:
            raise DBException(500, "Internal Server Error", "Something wrong with the server.")