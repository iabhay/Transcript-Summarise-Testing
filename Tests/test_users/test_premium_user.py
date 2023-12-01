import pytest
import sys
from src.users.premium_user.premium_user import PremiumUser
from src.users.premium_user.premium_user_controller import PremiumUserController
def mock_1():
    return True

def mock_2():
    return False

def mock_3():
    raise ValueError

class TestPremiumUser:

    def test_premium_module(self, mocker):
        inps = iter([1, 2, 3, 4, 5, 6])
        
        mock_userdb = mocker.MagicMock()
        mocker.patch('src.users.premium_user.premium_user.UsersDB', mock_userdb)
        
        mock_video = mocker.MagicMock()
        mocker.patch('src.users.premium_user.premium_user.VideoService', mock_video)

        mocker.patch('src.users.premium_user.premium_user.Config.PREMIUM_USER_INTRO', "Intro")
        
        mocker.patch('builtins.input', lambda _: next(inps))
        
        mocker.patch('src.users.premium_user.premium_user.Config.PREMIUM_PROMPT_LENGTH', "7")
        
        mock_premium_map = mocker.MagicMock()
        mocker.patch('src.users.premium_user.premium_user.PremiumMap', mock_premium_map)
        mock_premium_map().premium_menu.return_value = {1: mock_1, 2: mock_1, 3: mock_1, 4: mock_1, 5: mock_1, 6: mock_2}
        
        mocker.patch('src.users.premium_user.premium_user.logger.info', lambda _: None)
        
        premium = PremiumUser("1234")
        res = premium.premium_module()
        assert res == "premium"
        
    def test_premium_module_invalid(self, mocker, capsys):
        inps = iter([7])
        
        mock_userdb = mocker.MagicMock()
        mocker.patch('src.users.premium_user.premium_user.UsersDB', mock_userdb)
        
        mock_video = mocker.MagicMock()
        mocker.patch('src.users.premium_user.premium_user.VideoService', mock_video)

        mocker.patch('src.users.premium_user.premium_user.Config.PREMIUM_USER_INTRO', "Intro")
        
        mocker.patch('src.users.premium_user.premium_user.Config.INVALID_INPUT_PROMPT', "Invalid")
        
        mocker.patch('src.users.premium_user.premium_user.Config.EXITING_PROMPT', "Exit")
        
        mocker.patch('builtins.input', lambda _: next(inps))
        
        mocker.patch('src.users.premium_user.premium_user.Config.PREMIUM_PROMPT_LENGTH', "7")
        
        mock_premium_map = mocker.MagicMock()
        mocker.patch('src.users.premium_user.premium_user.PremiumMap', mock_premium_map)
        mock_premium_map().premium_menu.return_value = {1: mock_1, 2: mock_1, 3: mock_1, 4: mock_1, 5: mock_1, 6: mock_2}
        
        mocker.patch('src.users.premium_user.premium_user.logger.info', lambda _: None)
        
        premium = PremiumUser("1234")
        res = premium.premium_module()
        captured = capsys.readouterr()

        assert "Exit" in captured.out
        
    def test_premium_module_exception(self, mocker, capsys):
        inps = iter([6, 7])
        
        mock_userdb = mocker.MagicMock()
        mocker.patch('src.users.premium_user.premium_user.UsersDB', mock_userdb)
        
        mock_video = mocker.MagicMock()
        mocker.patch('src.users.premium_user.premium_user.VideoService', mock_video)

        mocker.patch('src.users.premium_user.premium_user.Config.PREMIUM_USER_INTRO', "Intro")
        
        mocker.patch('src.users.premium_user.premium_user.Config.INVALID_INPUT_PROMPT', "Invalid")
        
        mocker.patch('src.users.premium_user.premium_user.Config.EXITING_PROMPT', "Exit")
        
        mocker.patch('builtins.input', lambda _: next(inps))
        
        mocker.patch('src.users.premium_user.premium_user.Config.PREMIUM_PROMPT_LENGTH', "7")
        
        mock_premium_map = mocker.MagicMock()
        mocker.patch('src.users.premium_user.premium_user.PremiumMap', mock_premium_map)
        mock_premium_map().premium_menu.return_value = {1: mock_1, 2: mock_1, 3: mock_1, 4: mock_1, 5: mock_1, 6: mock_3}
        
        mocker.patch('src.users.premium_user.premium_user.logger.info', lambda _: None)
        
        premium = PremiumUser("1234")
        res = premium.premium_module()
        captured = capsys.readouterr()

        assert "Numbers only" in captured.out
        
    def test_premium_module_break(self, mocker, capsys):
        inps = iter([7])
        
        mock_userdb = mocker.MagicMock()
        mocker.patch('src.users.premium_user.premium_user.UsersDB', mock_userdb)
        
        mock_video = mocker.MagicMock()
        mocker.patch('src.users.premium_user.premium_user.VideoService', mock_video)

        mocker.patch('src.users.premium_user.premium_user.Config.PREMIUM_USER_INTRO', "Intro")
        
        mocker.patch('src.users.premium_user.premium_user.Config.INVALID_INPUT_PROMPT', "Invalid")
        
        mocker.patch('src.users.premium_user.premium_user.Config.EXITING_PROMPT', "Exit")
        
        mocker.patch('builtins.input', lambda _: next(inps))
        
        mocker.patch('src.users.premium_user.premium_user.Config.PREMIUM_PROMPT_LENGTH', "7")
        
        mock_premium_map = mocker.MagicMock()
        mocker.patch('src.users.premium_user.premium_user.PremiumMap', mock_premium_map)
        mock_premium_map().premium_menu.return_value = {1: mock_1, 2: mock_1, 3: mock_1, 4: mock_1, 5: mock_1, 6: mock_3}
        
        mocker.patch('src.users.premium_user.premium_user.logger.info', lambda _: None)
        
        premium = PremiumUser("1234")
        res = premium.premium_module()
        assert res == None
    
    
    
    
class TestPremiumController:
    
        def test_init(self, mocker):
            mock_msg = mocker.MagicMock()
            mock_premium = mocker.MagicMock()
            mock_history = mocker.MagicMock()
            
            mocker.patch('src.users.premium_user.premium_user_controller.MessageDB', mock_msg)
            mocker.patch('src.users.premium_user.premium_user_controller.PremiumListingsDB', mock_premium)
            mocker.patch('src.users.premium_user.premium_user_controller.HistoryDB', mock_history)
            
            premium = PremiumUserController("1234")
            
            assert premium.uid == "1234"
            assert premium.msg_obj == mock_msg()
            assert premium.premium_obj == mock_premium()
            assert premium.history_obj == mock_history()
            
        def test_send_message_to_admin(self, mocker, capsys):
            inps = iter(["Message"])
            
            mock_msg = mocker.MagicMock()
            mock_premium = mocker.MagicMock()
            mock_history = mocker.MagicMock()
            
            mocker.patch('src.users.premium_user.premium_user_controller.MessageDB', mock_msg)
            
            
            mocker.patch('builtins.input', lambda _: next(inps))
            
            mock_logger = mocker.MagicMock()
            mocker.patch('src.users.premium_user.premium_user_controller.logger.info', mock_logger)
            mock_msg.save_message.return_value = None
            premium = PremiumUserController("1234")
            premium.send_message_to_admin()
            captured = capsys.readouterr()
            
            assert "Message sent successfully." in captured.out
            
        def test_send_message_to_admin_url(self, mocker, capsys):
            inps = iter(["Message", "Url"])
            
            mock_msg = mocker.MagicMock()
            mock_premium = mocker.MagicMock()
            mock_history = mocker.MagicMock()
            
            mocker.patch('src.users.premium_user.premium_user_controller.MessageDB', mock_msg)
            
            mocker.patch('builtins.input', lambda _: next(inps))
            
            mock_logger = mocker.MagicMock()
            mocker.patch('src.users.premium_user.premium_user.logger', mock_logger)
            
            premium = PremiumUserController("1234")
            premium.send_message_to_admin("https://www.google.com")
            captured = capsys.readouterr()
            
            assert "Message sent successfully." in captured.out
            
        def test_premium_listing(self, mocker, capsys):
            inps = iter(["Message", "Url"])
            mocker.patch('builtins.input', lambda _: next(inps))
            mocker.patch('src.users.premium_user.premium_user_controller.url_validation', lambda _: True)
            mocker.patch.object(PremiumUserController, 'send_message_to_admin', return_value=None)
            premium = PremiumUserController("1234")
            premium.premium_listing_of_banned_url()
            captured = capsys.readouterr()
            res = "Once approved by admin, it'll be added to your premium listing."
            assert res in captured.out
        
        def test_premium_listing_invalid(self, mocker, capsys):
            inps = iter(["Message", "Url"])
            mocker.patch('builtins.input', lambda _: next(inps))
            mocker.patch('src.users.premium_user.premium_user_controller.url_validation', lambda _: False)
            mocker.patch.object(PremiumUserController, 'send_message_to_admin', return_value=None)
            premium = PremiumUserController("1234")
            premium.premium_listing_of_banned_url()
            captured = capsys.readouterr()
            res = "Enter valid url."
            assert res in captured.out
            
        def test_view_my_premium_listing(self, mocker, capsys):
            mock_premium = mocker.MagicMock()
            mocker.patch('src.users.premium_user.premium_user_controller.PremiumListingsDB', mock_premium)
            mock_premium.view_premium_user_listing.return_value = None
            premium = PremiumUserController("1234")
            res = premium.view_my_premium_listing()
            assert res == None
            
        def test_view_my_history(self, mocker, capsys):
            mock_history = mocker.MagicMock()
            mocker.patch('src.users.premium_user.premium_user_controller.HistoryDB', mock_history)
            mock_history.view_one_user_history.return_value = None
            premium = PremiumUserController("1234")
            res = premium.view_my_history()
            assert res == None
            