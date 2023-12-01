import logging
import functools
import sqlite3
from config.log_config.log_config import LogStatements
logger = logging.getLogger('exception_handler')


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
                    # print(f"Exception occurred: {e}")
                    logger.debug(default_response)
                except Exception as e:
                    # Handle the exception and provide the default response
                    print(default_response)
                    logger.debug(f"Exception occurred: {e}")
        return wrapper
    return decorator


def db_exception(default_success_response="", default_failure_response=LogStatements.log_exception_message):
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

# def error_handler(func):
#     """
#         Method which acts as decorator for handling all types of exception
#         Parameter = function
#         Return type = function
#     """
#     @functools.wraps(func)
#     def wrapper(*args : tuple,**kwargs : dict) -> None:
#         """
#             Method which handles exception
#             Parameter = *args, **kwargs
#             Return type = None
#         """
#         try:
#             return func(*args,**kwargs)
#         except sqlite3.IntegrityError as err:
#             logger.exception(err)
#             print(PromptConfig.DB_INTEGRITY_ERROR)
#         except sqlite3.OperationalError as err:
#             logger.exception(err)
#             print(PromptConfig.DB_ERROR_MESSAGE)
#         except sqlite3.ProgrammingError as err:
#             logger.exception(err)
#             print(PromptConfig.DB_ERROR_MESSAGE)
#         except sqlite3.Error as err:
#             logger.exception(err)
#             print(PromptConfig.DB_GENERAL_ERROR)
#         except ValueError as err:
#             logger.exception(err)
#             print(PromptConfig.INVALID_INPUT_ERROR)
#         except TypeError as err:
#             logger.exception(err)
#             print(PromptConfig.INVALID_INPUT_ERROR)
#         except Exception as err:
#             logger.exception(err)
#             print(PromptConfig.GENERAL_EXCEPTION_MSG)
#     return wrapper
