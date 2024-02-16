"""Module for views of Premium User."""

import logging
from config.config import Config
from utils.dicts import PremiumMap
from business_logic.submittedvideo.video_service import VideoService
from config.log_config.log_config import LogStatements

logger = logging.getLogger(__name__)


class PremiumUser:
    """
    Class for showing views of Premium User functionalities.
    ...
    Methods:
    -------
    Constructor() -> Initialisation of object of Premium Map which contains mapping of functionalities of premium user
    """

    def __init__(self, uid):
        """
        Constructor method to create object of Premium Map and object of Video Service
        Parameter -> uid: str
        Return Type -> None
        """
        self.premium_map = PremiumMap(uid)
        self.premium_menu = self.premium_map.premium_menu()
        self.video_obj = VideoService(uid)

    def premium_module(self):
        """
        Method to show views of functionalities of premium user
        Parameter -> self
        """
        print(Config.PREMIUM_USER_INTRO)
        while True:
            try:
                ask = int(input(Config.PREMIUM_PROMPT))
                if ask == int(Config.PREMIUM_PROMPT_LENGTH):
                    print(Config.EXITING_PROMPT)
                    logger.info(LogStatements.premium_user_logout)
                    break
                # using dictionary - functionality mapping
                elif 0 < ask <= len(self.premium_menu):
                    res = self.premium_menu[ask]()
                    if res == False:
                        if ask == 6:
                            logger.info(LogStatements.user_downgraded_to_non_premium)
                            # Role Changing
                            return "premium"
                        break
                    else:
                        continue
                else:
                    print(Config.INVALID_INPUT_PROMPT)
            except ValueError:
                print(Config.NUMBERS_ONLY_PROMPT)
        return None
