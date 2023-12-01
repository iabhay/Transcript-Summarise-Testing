import yaml

FPATH = r'src/config/config.yml'

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
    LANGUAGES = None
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

    @classmethod
    def load(cls):
        with open(FPATH, 'r') as f:
            data = yaml.safe_load(f)
            cls.MAIN_PROMPT = data['MAIN_PROMPT']
            cls.MAIN_PROMPT_LENGTH = data['MAIN_PROMPT_LENGTH']
            cls.ADMIN_PROMPT = data['ADMIN_PROMPT']
            cls.ADMIN_PROMPT_LENGTH = data['ADMIN_PROMPT_LENGTH']
            cls.NON_PREMIUM_PROMPT = data['NON_PREMIUM_PROMPT']
            cls.NON_PREMIUM_PROMPT_LENGTH = data['NON_PREMIUM_PROMPT_LENGTH']
            cls.MESSAGES_VIEW_PROMPT = data['MESSAGES_VIEW_PROMPT']
            cls.MESSAGES_VIEW_PROMPT_LENGTH = data['MESSAGES_VIEW_PROMPT_LENGTH']
            cls.SECURE_PASSWORD_PROMPT = data['SECURE_PASSWORD_PROMPT']
            cls.SUBMIT_VIDEO_PROMPT = data['SUBMIT_VIDEO_PROMPT']
            cls.UPGRADE_TO_PREMIUM_PROMPT = data['UPGRADE_TO_PREMIUM_PROMPT']
            cls.UPGRADE_TO_PREMIUM_PROMPT_LENGTH = data['UPGRADE_TO_PREMIUM_PROMPT_LENGTH']
            cls.MESSAGES_FILTER = data['MESSAGES_FILTER']
            cls.MESSAGES_FILTER_LENGTH = data['MESSAGES_FILTER_LENGTH']
            cls.LANGUAGE_PROMPT = data['LANGUAGE_PROMPT']
            cls.AFTER_SUBMITTING_URL_PROMPT = data['AFTER_SUBMITTING_URL']
            cls.AFTER_SUBMITTING_URL_PROMPT_LENGTH = data['AFTER_SUBMITTING_URL_LENGTH']
            cls.PREMIUM_PROMPT = data['PREMIUM_PROMPT']
            cls.PREMIUM_PROMPT_LENGTH = data['PREMIUM_PROMPT_LENGTH']
            cls.LANGUAGES = data['LANGUAGES']
            cls.CONFIRM_PROMPT = data['CONFIRM_PROMPT']
            cls.CONFIRM_PROMPT_LENGTH = data['CONFIRM_PROMPT_LENGTH']
            cls.ADMIN_USERNAME = data['ADMIN_USERNAME']
            cls.ADMIN_PASSWORD = data['ADMIN_PASSWORD']
            cls.PREMIUM_USER_INTRO = data['PREMIUM_USER_INTRO']
            cls.BASIC_USER_INTRO = data['BASIC_USER_INTRO']
            cls.INVALID_INPUT_PROMPT = data['INVALID_INPUT_PROMPT']
            cls.EXITING_PROMPT = data['EXITING_PROMPT']
            cls.APP_INTRO = data['APP_INTRO']
            cls.APP_OUTRO = data['APP_OUTRO']
            cls.ENTER_USERNAME_PROMPT = data['ENTER_USERNAME_PROMPT']
            cls.ENTER_PASSWORD_PROMPT = data['ENTER_PASSWORD_PROMPT']
            cls.ENTER_URL = data['ENTER_URL']
            cls.NO_USER_FOUND = data['NO_USER_FOUND']
            cls.NO_URL_FOUND = data['NO_URL_FOUND']
            cls.PROCESSING_PROMPT = data['PROCESSING_PROMPT']
            cls.SECURE_USERNAME_PROMPT = data['SECURE_USERNAME_PROMPT']