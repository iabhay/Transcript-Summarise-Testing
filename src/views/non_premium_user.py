"""Module for views of Non Premium User."""

import logging
from config.config import Config
from utils.dicts import NonPremiumMap
from config.log_config.log_config import LogStatements

logger = logging.getLogger(__name__)


class NonPremiumUser:
    """
    Class for showing views of Non Premium User functionalities.
    ...
    Methods:
    -------
    Constructor() -> Initialisation of object of Non Premium Map which contains mapping of functionalities of non premium user
    """

    def __init__(self, uid: str) -> None:
        """
        Constructor method to create object of Non Premium Map
        Parameter -> uid: str
        Return Type -> None
        """
        self.non_premium_map = NonPremiumMap(uid)
        self.non_premium_menu = self.non_premium_map.non_premium_menu()

    def non_premium_module(self):
        """
        Method to show views of functionalities of non premium user
        Parameter -> self
        """
        print(Config.BASIC_USER_INTRO)
        while True:
            try:
                # using dictionary - functional mapping
                ask = int(input(Config.NON_PREMIUM_PROMPT))
                n = int(Config.NON_PREMIUM_PROMPT_LENGTH)
                if ask == n:
                    logger.info(LogStatements.non_premium_user_logout)
                    print(Config.EXITING_PROMPT)
                    break
                elif 0 < ask <= len(self.non_premium_menu):
                    res = self.non_premium_menu[ask]()
                    if res == None:
                        # Role changing
                        if ask == 2:
                            logger.info(LogStatements.user_upgraded_to_premium)
                            return "nonpremium"
                        break
                    elif res == False:
                        return False
                        break
                    else:
                        continue
                else:
                    print(Config.INVALID_INPUT_PROMPT)
                    continue
            except ValueError:
                print(Config.NUMBERS_ONLY_PROMPT)
        return None
