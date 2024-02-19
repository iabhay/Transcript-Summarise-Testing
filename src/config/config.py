import os
import yaml
current_directory = os.path.dirname(__file__)
FPATH = os.path.join(current_directory, 'config.yml')


class Config:
    """
    Maintains all the config variables of the app
    """

    MAIN_PROMPT = None
    MAIN_PROMPT_LENGTH = None
    ADMIN_PROMPT = None
    ADMIN_PROMPT_LENGTH = None
    MESSAGES_VIEW_PROMPT = None
    MESSAGES_VIEW_PROMPT_LENGTH = None
    MESSAGES_FILTER = None
    MESSAGES_FILTER_LENGTH = None
    NON_PREMIUM_PROMPT = None
    NON_PREMIUM_PROMPT_LENGTH = None
    LANGUAGE_PROMPT = None
    SECURE_PASSWORD_PROMPT = None
    SUBMIT_VIDEO_PROMPT = None
    AFTER_SUBMITTING_URL_PROMPT = None
    AFTER_SUBMITTING_URL_PROMPT_LENGTH = None
    UPGRADE_TO_PREMIUM_PROMPT = None
    UPGRADE_TO_PREMIUM_PROMPT_LENGTH = None
    PREMIUM_PROMPT = None
    PREMIUM_PROMPT_LENGTH = None
    CONFIRM_PROMPT = None
    CONFIRM_PROMPT_LENGTH = None
    ADMIN_USERNAME = None
    ADMIN_PASSWORD = None
    PREMIUM_USER_INTRO = None
    BASIC_USER_INTRO = None
    INVALID_INPUT_PROMPT = None
    EXITING_PROMPT = None
    APP_INTRO = None
    APP_OUTRO = None
    ENTER_USERNAME_PROMPT = None
    ENTER_PASSWORD_PROMPT = None
    ENTER_URL = None
    NO_USER_FOUND = None
    NO_URL_FOUND = None
    PROCESSING_PROMPT = None
    SECURE_USERNAME_PROMPT = None
    NUMBERS_ONLY_PROMPT = None
    INVALID_USERNAME_PROMPT = None
    INVALID_PASSWORD_PROMPT = None
    REGISTRATION_SUCCESS = None
    ALREADY_EXIST = None
    VALID_URL = None
    ALREADY_BANNED_URL = None
    VIDEO_NOT_SUPPORTED = None
    EXHAUSTED_BAN = None
    BANNED_CONTENT = None
    UPGRADED_PREMIUM = None
    DOWNGRADED_PREMIUM = None
    ENTER_VALID_CHOICE = None
    BACK = None
    ANALYSE_TEXT_FAILED = None
    SUMMARY_GENERATION_FAILED = None
    USER_BANNED = None
    USER_UNBANNED = None
    URL_BANNED = None
    URL_UNBANNED = None
    PREMIUM_LISTING_DONE = None
    ENTER_MESSAGE = None
    MESSAGE_SENT = None
    ENTER_URL_FOR_PREMIUMLISTING = None
    ACKNOWLEDGEMENT = None
    NO_DATA_EXIST = None
    MESSAGE_TO_ADMIN_FOR_UNBAN = None
    MESSAGE_NOT_SENT = None
    SHORT_UUID_CONSTRAINTS = None

    @classmethod
    def load(cls):
        with open(FPATH, "r") as f:
            data = yaml.safe_load(f)
            cls.MAIN_PROMPT = data["MAIN_PROMPT"]
            cls.MAIN_PROMPT_LENGTH = data["MAIN_PROMPT_LENGTH"]
            cls.ADMIN_PROMPT = data["ADMIN_PROMPT"]
            cls.ADMIN_PROMPT_LENGTH = data["ADMIN_PROMPT_LENGTH"]
            cls.NON_PREMIUM_PROMPT = data["NON_PREMIUM_PROMPT"]
            cls.NON_PREMIUM_PROMPT_LENGTH = data["NON_PREMIUM_PROMPT_LENGTH"]
            cls.MESSAGES_VIEW_PROMPT = data["MESSAGES_VIEW_PROMPT"]
            cls.MESSAGES_VIEW_PROMPT_LENGTH = data["MESSAGES_VIEW_PROMPT_LENGTH"]
            cls.SECURE_PASSWORD_PROMPT = data["SECURE_PASSWORD_PROMPT"]
            cls.SUBMIT_VIDEO_PROMPT = data["SUBMIT_VIDEO_PROMPT"]
            cls.UPGRADE_TO_PREMIUM_PROMPT = data["UPGRADE_TO_PREMIUM_PROMPT"]
            cls.UPGRADE_TO_PREMIUM_PROMPT_LENGTH = data[
                "UPGRADE_TO_PREMIUM_PROMPT_LENGTH"
            ]
            cls.MESSAGES_FILTER = data["MESSAGES_FILTER"]
            cls.MESSAGES_FILTER_LENGTH = data["MESSAGES_FILTER_LENGTH"]
            cls.LANGUAGE_PROMPT = data["LANGUAGE_PROMPT"]
            cls.AFTER_SUBMITTING_URL_PROMPT = data["AFTER_SUBMITTING_URL"]
            cls.AFTER_SUBMITTING_URL_PROMPT_LENGTH = data["AFTER_SUBMITTING_URL_LENGTH"]
            cls.PREMIUM_PROMPT = data["PREMIUM_PROMPT"]
            cls.PREMIUM_PROMPT_LENGTH = data["PREMIUM_PROMPT_LENGTH"]
            cls.CONFIRM_PROMPT = data["CONFIRM_PROMPT"]
            cls.CONFIRM_PROMPT_LENGTH = data["CONFIRM_PROMPT_LENGTH"]
            cls.ADMIN_USERNAME = data["ADMIN_USERNAME"]
            cls.ADMIN_PASSWORD = data["ADMIN_PASSWORD"]
            cls.PREMIUM_USER_INTRO = data["PREMIUM_USER_INTRO"]
            cls.BASIC_USER_INTRO = data["BASIC_USER_INTRO"]
            cls.INVALID_INPUT_PROMPT = data["INVALID_INPUT_PROMPT"]
            cls.EXITING_PROMPT = data["EXITING_PROMPT"]
            cls.APP_INTRO = data["APP_INTRO"]
            cls.APP_OUTRO = data["APP_OUTRO"]
            cls.ENTER_USERNAME_PROMPT = data["ENTER_USERNAME_PROMPT"]
            cls.ENTER_PASSWORD_PROMPT = data["ENTER_PASSWORD_PROMPT"]
            cls.ENTER_URL = data["ENTER_URL"]
            cls.NO_USER_FOUND = data["NO_USER_FOUND"]
            cls.NO_URL_FOUND = data["NO_URL_FOUND"]
            cls.PROCESSING_PROMPT = data["PROCESSING_PROMPT"]
            cls.SECURE_USERNAME_PROMPT = data["SECURE_USERNAME_PROMPT"]
            cls.NUMBERS_ONLY_PROMPT = data["NUMBERS_ONLY_PROMPT"]
            cls.INVALID_USERNAME_PROMPT = data["INVALID_USERNAME_PROMPT"]
            cls.INVALID_PASSWORD_PROMPT = data["INVALID_PASSWORD_PROMPT"]
            cls.REGISTRATION_SUCCESS = data["REGISTRATION_SUCCESS"]
            cls.ALREADY_EXIST = data["ALREADY_EXIST"]
            cls.VALID_URL = data["VALID_URL"]
            cls.ALREADY_BANNED_URL = data["ALREADY_BANNED_URL"]
            cls.VIDEO_NOT_SUPPORTED = data["VIDEO_NOT_SUPPORTED"]
            cls.EXHAUSTED_BAN = data["EXHAUSTED_BAN"]
            cls.BANNED_CONTENT = data["BANNED_CONTENT"]
            cls.UPGRADED_PREMIUM = data["UPGRADED_PREMIUM"]
            cls.DOWNGRADED_PREMIUM = data["DOWNGRADED_PREMIUM"]
            cls.ENTER_VALID_CHOICE = data["ENTER_VALID_CHOICE"]
            cls.BACK = data["BACK"]
            cls.ANALYSE_TEXT_FAILED = data["ANALYSE_TEXT_FAILED"]
            cls.SUMMARY_GENERATION_FAILED = data["SUMMARY_GENERATION_FAILED"]
            cls.USER_BANNED = data["USER_BANNED"]
            cls.USER_UNBANNED = data["USER_UNBANNED"]
            cls.URL_BANNED = data["URL_BANNED"]
            cls.URL_UNBANNED = data["URL_UNBANNED"]
            cls.PREMIUM_LISTING_DONE = data["PREMIUM_LISTING_DONE"]
            cls.ENTER_MESSAGE = data["ENTER_MESSAGE"]
            cls.MESSAGE_SENT = data["MESSAGE_SENT"]
            cls.ENTER_URL_FOR_PREMIUMLISTING = data["ENTER_URL_FOR_PREMIUMLISTING"]
            cls.ACKNOWLEDGEMENT = data["ACKNOWLEDGEMENT"]
            cls.NO_DATA_EXIST = data["NO_DATA_EXIST"]
            cls.MESSAGE_TO_ADMIN_FOR_UNBAN = data["MESSAGE_TO_ADMIN_FOR_UNBAN"]
            cls.MESSAGE_NOT_SENT = data["MESSAGE_NOT_SENT"]
            cls.SHORT_UUID_CONSTRAINTS = data["SHORT_UUID_CONSTRAINTS"]
