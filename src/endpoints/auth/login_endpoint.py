"""Module for defining Login Route"""

from flask.views import MethodView
from flask_smorest import Blueprint
from utils.utils_api.schemas import UserSchema
from controllers.auth.login_controller import LoginController
from flask_jwt_extended import jwt_required

"""
Endpoint for login in application.
Sending request to login controller.
"""

blp = Blueprint("login", __name__, description="login")


@blp.route("/login")
class LoginEndpoint(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    Construtor() -> Initialisation of Login Controller
    post() -> Method to post request method
    """

    def __init__(self):
        self.login_controller = LoginController()

    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        Method to post request which verifies user and generate token
        Parameter -> user_data: UserSchema
        Return Type -> Json
        """
        response = self.login_controller.verify_user(user_data)
        return response
    
@blp.route("/refresh")
class RefreshEndpoint(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    Construtor() -> Initialisation of Login Controller
    post() -> Method to post request method
    """

    def __init__(self):
        self.login_controller = LoginController()

    @jwt_required(refresh=True)
    def post(self):
        """
        Method to post request which verifies user and generate token
        Parameter -> user_data: UserSchema
        Return Type -> Json
        """
        response = self.login_controller.refresh_user()
        return response

@blp.route("/logout")
class LogoutEndpoint(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    Construtor() -> Initialisation of Login Controller
    post() -> Method to post request method
    """

    def __init__(self):
        self.login_controller = LoginController()

    @jwt_required()
    def post(self):
        """
        Method to post request which verifies user and generate token
        Parameter -> user_data: UserSchema
        Return Type -> Json
        """
        response = self.login_controller.logout_user()
        return response
