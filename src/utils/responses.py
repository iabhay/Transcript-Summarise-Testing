"""Module for defining standard Error Response and Success Response"""

from flask import jsonify
from typing import Optional


class ErrorResponse:
    """
    Class for Standard Error Template
    ...
    Methods:
    -------
    jsonify_error() -> set attributes in format
    -------
    Class Properties:
    success: bool -> False, as this is error response class
    """

    success = False

    @staticmethod
    def jsonify_error(custom_error) -> dict:
        """
        Static Method to generate json response in which success and message are set.
        Parameter -> custom_error: CustomBaseException
        Return Type -> dict
        """
        return jsonify(
            {"success": ErrorResponse.success, "message": custom_error.message}
        )


class SuccessResponse:
    """
    Class for Standard Success Template
    ...
    Methods:
    -------
    jsonify_data() -> set attributes in format
    -------
    Class Properties:
    success: bool -> True, as this is success response class
    """

    success = True

    @staticmethod
    def jsonify_data(message, data: Optional[dict] = {}) -> dict:
        """
        Static Method to generate json response in which success and message are set.
        Parameter -> message: str, data: Optional[dict]
        Return Type -> dict
        """
        return jsonify(
            {"success": SuccessResponse.success, "message": message, "data": data}
        )
