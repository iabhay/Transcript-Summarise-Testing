"""Module containing decorators for handling exceptions, errors"""

import logging
from config.log_config.log_config import LogStatements
from functools import wraps
from typing import Callable
from utils.custom_exception import CustomBaseException
from utils.responses import ErrorResponse

logger = logging.getLogger(__name__)


def handle_exceptions(default_response="Enter Carefully."):
    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    # Call the original function
                    return func(*args, **kwargs)
                except ValueError as e:
                    print("Enter Numbers only.")
                    print(f"Exception occurred: {e}")
                    logger.debug(default_response)
                except TypeError as e:
                    print("Type Error.")
                    logger.debug(default_response)
                except Exception as e:
                    # Handle the exception and provide the default response
                    print(default_response)
                    logger.debug(f"Exception occurred: {e}")

        return wrapper

    return decorator


def db_exception(
    default_success_response="",
    default_failure_response=LogStatements.log_exception_message,
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    # Call the original function
                    logger.info(default_success_response)
                    return func(*args, **kwargs)
                except ValueError:
                    print("Enter Numbers only.")
                except Exception as e:
                    # Handle the exception and provide the default response
                    print(f"Exception occurred: {e}")
                    print(default_failure_response)
                    logger.debug(default_failure_response)

        return wrapper

    return decorator


def custom_error_handler(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: tuple, **kwargs: dict) -> None:
        try:
            return func(*args, **kwargs)
        except CustomBaseException as custom_error:
            return ErrorResponse.jsonify_error(custom_error), custom_error.error_code

    return wrapper
