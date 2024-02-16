"""Module for defining Login Route"""

from flask.views import MethodView
from flask_smorest import Blueprint
from utils.utils_api.schemas import UserSchema
from controllers.auth.register_controller import RegisterController

"""
Endpoint for signup in application.
Sending request to register controller.
"""

blp = Blueprint("register", __name__, description="register")


@blp.route("/signup")
class RegisterEndpoint(MethodView):
    """
    Class for defining methods that can request this endpoint
    ...
    Methods:
    -------
    Construtor() -> Initialisation of Register Controller
    post() -> Method to post request method
    """

    def __init__(self):
        self.register_controller = RegisterController()

    @blp.arguments(UserSchema)
    def post(self, user_data):
        """
        Method to post request which registers new user
        Parameter -> user_data: UserSchema
        Return Type -> Json
        """
        response = self.register_controller.add_user(user_data)
        return response, 201
