import logging
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
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
"""
    Response Schema Remaining
    Logout Remaining
    Role field name changing remaining in token 
    Logging remaining at controller and endpoint level   
    Doc needs to be changed according to updates while making endpoints
"""

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    level=logging.DEBUG,
    filename=LogStatements.log_file_location,
)
logger = logging.getLogger(__name__)
logger.info(LogStatements.starting_application_log)
Config.load()
LogStatements.load()
ApiConfig.load()
app = Flask(__name__)
app.config["API_TITLE"] = "Transcript Summariser"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = (
    "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
)
app.config["JWT_SECRET_KEY"] = "abhay"
api = Api(app)
jwt = JWTManager(app)

api.register_blueprint(register_blp)
api.register_blueprint(login_blp)
api.register_blueprint(history_blp)
api.register_blueprint(summary_blp)
api.register_blueprint(message_blp)
api.register_blueprint(premiumlist_blp)
api.register_blueprint(url_blp)
api.register_blueprint(user_info_blp)
db.create_all_table()
app.run(debug=True, port=5000)
