"""Module to define Custom Exception and it's types"""


class CustomBaseException(Exception):
    """
    Class to define custom exception which has parent class Exception
    ...
    Methods:
    -------
    constructor() -> setting message, error code
    """

    def __init__(self, error_code: int, message: str) -> None:
        """
        Method to set message in Exception class and error code and message
        Parameter -> error_code: int, message: str
        Return Type -> None
        """
        super().__init__(message)
        self.error_code = error_code
        self.message = message


class InvalidLogin(CustomBaseException):
    pass


class InvalidRegister(CustomBaseException):
    pass


class DBException(CustomBaseException):
    pass


class PasswordNotMatch(CustomBaseException):
    pass


class UserNotFound(CustomBaseException):
    pass


class UsernameInvalid(CustomBaseException):
    pass


class BannedUrl(CustomBaseException):
    pass


class ContentNotGenerated(CustomBaseException):
    pass

class AppException(CustomBaseException):
    pass


class BadContent(CustomBaseException):
    pass


class NotPremiumUser(CustomBaseException):
    pass


class DataNotFound(CustomBaseException):
    pass


class PersmissionGrantError(CustomBaseException):
    pass
