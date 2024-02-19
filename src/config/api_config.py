import os
import yaml
current_directory = os.path.dirname(__file__)
FPATH = os.path.join(current_directory, 'api_config.yml')


class ApiConfig:
    
    """
    Maintain all configs for api.
    """

    USER_NOT_EXIST = None
    SERVER_NOT_WORKING = None
    LOGIN_SUCCESS = None
    UID_CONSTRAINTS = None
    USER_ALREADY_EXIST =None
    BANNED_URL= None
    CONTENT_NOT_FETCHED = None
    DATA_NOT_EXIST = None
    USER_IS_PREMIUM = None
    USER_IS_NONPREMIUM = None
    USER_PROFILE_UNAVAILABLE = None
    ALREADY_NONPREMIUML = None
    ALREADYPREMIUM = None
    USER_REGISTER_SUCCESS = None
    BAD_CONTENT_FOUND = None
    ACCESS_RESTRICTED = None
    SENT_TO_ADMIN = None
    URL_PREMIUMLISTED = None
    URL_BANNED = None
    URL_UNBANNED = None
    USER_UPGRADED = None
    USER_DOWNGRADED = None
    ADMIN_ROLE_UNCHANGEABLE = None
    USER_BANNED = None
    USER_UNBANNED = None
    PERMISSION_NOT_GRANTED = None
    TOKEN_ISSUED = None
    TOKEN_REVOKED = None
    LOG_FILE_PATH = None
    LOGOUT_SUCCESS = None

    @classmethod
    def load(cls):
        with open(FPATH, "r") as f:
            data = yaml.safe_load(f)
            cls.LOGIN_SUCCESS = data['LOGIN_SUCCESS']
            cls.SERVER_NOT_WORKING = data['SERVER_NOT_WORKING']
            cls.USER_NOT_EXIST = data['USER_NOT_EXIST']
            cls.UID_CONSTRAINTS = data['UID_CONSTRAINTS']
            cls.USER_ALREADY_EXIST = data['USER_ALREADY_EXIST']
            cls.BANNED_URL= data['BANNED_URL']
            cls.CONTENT_NOT_FETCHED = data['CONTENT_NOT_FETCHED']
            cls.DATA_NOT_EXIST = data['DATA_NOT_EXIST']
            cls.USER_IS_PREMIUM = data['USER_IS_PREMIUM']
            cls.USER_IS_NONPREMIUM = data['USER_IS_NONPREMIUM']
            cls.USER_PROFILE_UNAVAILABLE = data['USER_PROFILE_UNAVAILABLE']
            cls.ALREADY_NONPREMIUML = data['ALREADY_NONPREMIUML']
            cls.ALREADYPREMIUM = data['ALREADYPREMIUM']
            cls.USER_REGISTER_SUCCESS = data['USER_REGISTER_SUCCESS']
            cls.BAD_CONTENT_FOUND = data['BAD_CONTENT_FOUND']
            cls.ACCESS_RESTRICTED = data['ACCESS_RESTRICTED']
            cls.SENT_TO_ADMIN = data['SENT_TO_ADMIN']
            cls.URL_PREMIUMLISTED = data['URL_PREMIUMLISTED']
            cls.URL_BANNED = data['URL_BANNED']
            cls.URL_UNBANNED = data['URL_UNBANNED']
            cls.USER_UPGRADED = data['USER_UPGRADED']
            cls.USER_DOWNGRADED = data['USER_DOWNGRADED']
            cls.ADMIN_ROLE_UNCHANGEABLE = data['ADMIN_ROLE_UNCHANGEABLE']
            cls.USER_BANNED = data['USER_BANNED']
            cls.USER_UNBANNED = data['USER_UNBANNED']
            cls.PERMISSION_NOT_GRANTED = data['PERMISSION_NOT_GRANTED']
            cls.TOKEN_ISSUED = data['TOKEN_ISSUED']
            cls.TOKEN_REVOKED = data['TOKEN_REVOKED']
            cls.LOG_FILE_PATH = data['LOG_FILE_PATH']
            cls.LOGOUT_SUCCESS = data['LOGOUT_SUCCESS']
