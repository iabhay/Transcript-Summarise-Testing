import logging
from database.db_ops.users_db import UsersDB
from config.config import Config
from utils.dicts import PremiumMap
from users.submittedvideo.video_service import VideoService
from config.log_config.log_config import LogStatements
logger = logging.getLogger('premium_user')


class PremiumUser:
    def __init__(self, uid):
        self.uid = uid
        self.user = UsersDB(self.uid)
        self.premium_map = PremiumMap(uid)
        self.premium_menu = self.premium_map.premium_menu()
        self.video_obj = VideoService(uid)

    def premium_module(self):
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
                print("Numbers only")
        return None

