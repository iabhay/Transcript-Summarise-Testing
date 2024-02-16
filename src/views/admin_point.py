"""Module for views of Admin Functionalities."""

from config.config import Config
from utils.dicts import AdminMap


class Admin:
    """
    Class for using functionalities that admin can perform.
    ...
    Methods:
    -------
    constructor()-> setting user id and initialisation of object of admin_menu clas.
    admin_module() -> method to show menu to user.
    message_handler() -> message menu shown to user.
    """

    def __init__(self, uid: str) -> None:
        """
        Constructor method to set uid and Creating object of Admin Map which contains function mapped dictionary.
        Message menu also setted
        Parameter -> uid: str
        Return Type -> None
        """
        self.uid = uid
        self.adm = AdminMap(self.uid)
        self.adm_menu = self.adm.admin_menu()
        self.message_menu = self.adm.message_menu()

    def adminmodule(self):
        """
        Method for View of admin menu fetched from Admin Map.
        Parameter -> self
        Return Type -> None
        """
        while True:
            try:
                ask_user = int(input(Config.ADMIN_PROMPT))
                if ask_user == int(Config.ADMIN_PROMPT_LENGTH):
                    print(Config.EXITING_PROMPT)
                    break
                # message sub menu module
                elif ask_user == 9:
                    self.messages_handler()
                elif (0 < ask_user <= len(self.adm_menu)) and ask_user != 9:
                    # using dictionary - functionality mapping
                    self.adm_menu[ask_user]()
                else:
                    print(Config.INVALID_INPUT_PROMPT)
            except ValueError:
                print(Config.NUMBERS_ONLY_PROMPT)

    def messages_handler(self):
        """
        Method to views of message
        Parameter -> self
        Return Type -> None
        """
        while True:
            try:
                ask = int(input(Config.MESSAGES_VIEW_PROMPT))
                if ask == int(Config.MESSAGES_VIEW_PROMPT_LENGTH):
                    break
                elif 0 < ask <= len(self.message_menu):
                    self.message_menu[ask]()
                else:
                    print(Config.INVALID_INPUT_PROMPT)
            except ValueError:
                print(Config.NUMBERS_ONLY_PROMPT)
