import logging
from database.db_ops.users_db import UsersDB
from config.config import Config
from utils.dicts import NonPremiumMap
from users.submittedvideo.video_service import VideoService
from users.premium_user.premium_user import PremiumUser

from config.log_config.log_config import LogStatements
logger = logging.getLogger('non_premium_user')


class NonPremiumUser:
    def __init__(self, uid):
        self.uid = uid
        self.user = UsersDB(self.uid)
        self.premium_user = PremiumUser(self.uid)
        self.non_premium_map = NonPremiumMap(uid)
        self.non_premium_menu = self.non_premium_map.non_premium_menu()
        self.video_obj = VideoService(uid)

    # @handle_exceptions
    def non_premium_module(self):
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
                    if res == False:
                        # Role changing
                        if ask == 2:
                            logger.info(LogStatements.user_upgraded_to_premium)
                            return "nonpremium"
                        break
                    else:
                        continue
                else:
                    print(Config.INVALID_INPUT_PROMPT)
                    continue
            except ValueError:
                print("Numbers only")
        return None
