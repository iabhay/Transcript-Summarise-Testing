class CustomBaseException(Exception):
    def __init__(self, error_code, error, message):
        super().__init__(message)
        self.error_code = error_code
        self.error = error
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


class BadContent(CustomBaseException):
    pass


class NotPremiumUser(CustomBaseException):
    pass


class DataNotFound(CustomBaseException):
    pass


class PersmissionGrantError(CustomBaseException):
    pass
