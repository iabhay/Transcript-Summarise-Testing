import logging
from config.config import Config
from database.db_ops.db_initialise import DBInitialise
from utils.exception_handler import handle_exceptions
from authenticator.login.login import Login
from authenticator.register.register import Register
from config.log_config.log_config import LogStatements


class YTTS:
    def __init__(self):
        register = Register()
        login = Login()
        self.auth_dict = {
            1: register.register_module,
            2: login.login_module
        }
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            level=logging.DEBUG,
            filename=LogStatements.log_file_location
        )
        logger = logging.getLogger('main')
        logger.info(LogStatements.starting_application_log)

    # @handle_exceptions()
    def menu(self):
        print(Config.APP_INTRO)
        while True:
            try:
                ask = int(input(Config.MAIN_PROMPT))
                n = int(Config.MAIN_PROMPT_LENGTH)
                if ask == n:
                    print(Config.APP_OUTRO)
                    break
                elif 0 < ask <= len(self.auth_dict):
                    self.auth_dict[ask]()
                else:
                    print(Config.INVALID_INPUT_PROMPT)
            except ValueError:
                print("Numbers only")


if __name__ == "__main__":
    Config.load()
    LogStatements.load()
    DBInitialise.create_all_tables()
    ytts_obj = YTTS()
    ytts_obj.menu()


