"""Module containing different functions for initializing app."""

import logging
import os
from flask import jsonify, g, Flask
from flask.logging import default_handler
from flask_jwt_extended import JWTManager
from flask_smorest import Api
from config.config import Config
from config.api_config import ApiConfig
from config.log_config.log_config import LogStatements
from database.mysql_database import db
from endpoints.auth.login_endpoint import blp as login_blp
from endpoints.auth.register_endpoint import blp as register_blp
from endpoints.services.summary_endpoint import blp as summary_blp
from endpoints.users_endpoint.history_endpoint import blp as history_blp
from endpoints.users_endpoint.message_endpoint import blp as message_blp
from endpoints.users_endpoint.url_endpoint import blp as url_blp
from endpoints.users_endpoint.premiumlist_endpoint import blp as premiumlist_blp
from endpoints.users_endpoint.user_info_endpoint import blp as user_info_blp
from business_logic.token_logic.access_token_logic import AccessToken

class CustomFormatter(logging.Formatter):
    """
        Custom log formatter to format the logs and add request_id in each log.
        ...
        Methods
        -------
        format(): str -> overriden the parent format method to add request_id field.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
            Method to override the parent format methods.
            Parameters -> record
            Returns -> str
        """
        if hasattr(g, 'request_id'):
            record.request_id = g.request_id
        else:
            record.request_id = "REQdefault"
        return super().format(record)


def logging_configuration(app: Flask) -> None:
    """
        Function to set up logging configurations for app.
        Parameters -> Flask app
        Returns -> None
    """
    app.logger.removeHandler(default_handler)
    formatter = CustomFormatter(
        fmt='%(asctime)s %(levelname)-8s [%(filename)s %(funcName)s:%(lineno)d] %(message)s - [%(request_id)s]'
    )
    handler = logging.FileHandler(ApiConfig.LOG_FILE_PATH)
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)


def app_setup(app: Flask) -> None:
    """
        Function having statements for setting of app and document related configuration.
        Parameters -> Flask app
        Returns -> None
    """
    Config.load()
    LogStatements.load()
    ApiConfig.load()
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Transcript Summariser"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )
    db.create_all_table()
    logging_configuration(app)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")


def jwt_setup(app: Flask) -> None:
    """
        Function for setting of JWT related configurations.
        Parameters -> Flask app
        Returns -> None
    """
    jwt = JWTManager(app)
    token = AccessToken()

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header: dict, jwt_payload: dict) -> tuple:
        """
            Function to check for expired JWT.
            Parameters -> jwt_header: dict, jwt_payload: dict
            Returns -> tuple
        """
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error: str) -> tuple:
        """
            Function to check for invalid JWT.
            Parameters -> error: str
            Returns -> tuple
        """
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error: str) -> tuple:
        """
            Function to check for missing JWT.
            Parameters -> error: str
            Returns -> tuple
        """
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload) -> bool:
        """
            Function to check for revoked JWT.
            Parameters -> jwt_header: dict, jwt_payload: dict
            Returns -> bool
        """
        check_access_token = token.is_token_revoked(jwt_payload["jti"], "access_token")
        check_refresh_token = token.is_token_revoked(jwt_payload["jti"], "refresh_token")
        return check_access_token or check_refresh_token

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header: dict, jwt_payload: dict) -> tuple:
        """
            Function to check for revoked JWT.
            Parameters -> jwt_header: dict, jwt_payload: dict
            Returns -> tuple
        """
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )


def register_blueprint(api: Api) -> None:
    """
        Function for registering various blueprints of API.
        Parameters -> API
        Returns -> None
    """
    api.register_blueprint(register_blp)
    api.register_blueprint(login_blp)
    api.register_blueprint(history_blp)
    api.register_blueprint(summary_blp)
    api.register_blueprint(message_blp)
    api.register_blueprint(premiumlist_blp)
    api.register_blueprint(url_blp)
    api.register_blueprint(user_info_blp)