import logging
from config.config import Config
from config.log_config.log_config import LogStatements

logger = logging.getLogger(__name__)


class UsersHelper:
    def __init__(self, uid):
        self.uid = uid

    def upgrade_to_premium(self):
        try:
            ask = int(input(Config.UPGRADE_TO_PREMIUM_PROMPT))
            if 0 < ask < 3:
                if ask == 1:
                    self.user.update_user("role", "premiumuser")
                    logger.info(LogStatements.user_upgraded_to_premium)
                    print(Config.UPGRADED_PREMIUM)
                    return None
                elif ask == 2:
                    print(Config.BACK)
            else:
                print(Config.ENTER_VALID_CHOICE)
        except ValueError:
            print(Config.NUMBERS_ONLY_PROMPT)
        return True

    def downgrade_to_basic(self):
        try:
            ask = int(input(Config.CONFIRM_PROMPT))
            if 0 < ask < 3:
                if ask == 1:
                    self.user.update_user("role", "nonpremiumuser")
                    logger.info(LogStatements.user_downgraded_to_non_premium)
                    print(Config.DOWNGRADED_PREMIUM)
                    return False
                elif ask == 2:
                    print(Config.BACK)
            else:
                print(Config.ENTER_VALID_CHOICE)
        except ValueError:
            print(Config.NUMBERS_ONLY_PROMPT)
        return None
