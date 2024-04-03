"""
    Response Schema Remaining
    Logout Remaining
    Role field name changing remaining in token 
    Logging remaining at controller and endpoint level   
    Doc needs to be changed according to updates while making endpoints
"""

"""Module for initializing app."""

import logging
from flask import Flask, g
from flask_smorest import Api
from flask_cors import CORS
import shortuuid
from database.mysql_database import db
from utils.api_setup import app_setup, jwt_setup, register_blueprint, logging_configuration

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """
        Function which will be invoked on starting of application.
        Parameters -> None
        Returns -> Flask application
    """
    app = Flask(__name__)
    CORS(app)
    app_setup(app)
    api = Api(app)
    jwt_setup(app)
    register_blueprint(api)

    @app.before_request
    def get_request_id() -> None:
        """
            Function that will be invoked before every request to reset request id.
            Parameters -> None
            Returns -> None
        """
        g.request_id = "REQ" + shortuuid.ShortUUID().random(length=4)
    return app


app = create_app()