import pytest
import builtins
import sys
# from users_controllers.admin.admin_point import Admin
# from users_controllers.admin.admincontroller import AdminController
from src.config.config import Config


def mock_call_1():
    print("mock called 1")
    return "mock called 1"

def mock_call_2():
    print("mock called 2")
    raise ValueError

def mock_call_3():
    print("mock called 3")  

def mock_call_4():
    print("mock called 4")

def mock_call_5():
    print("mock called 5")

class TestAdminPoint:
    def test_adminmodule_pass(self, mocker):
        inps = iter([1,6])
        mock_adm_map = mocker.MagicMock()
        mocker.patch('src.users.admin.admin_point.AdminMap')
        mock_adm_map().admin_menu.return_value = {1: mock_call_1}
        mocker.patch('builtins.input', lambda _: next(inps))
        mocker.patch('src.users.admin.admin_point.Config.ADMIN_PROMPT_LENGTH', "6")
        adm = Admin("1234")
        assert adm.adminmodule() is None
        
    def test_adminmodule_fail(self, mocker, capsys):
        inps = iter([1,6])
        mock_adm_map = mocker.MagicMock()
        mocker.patch('src.users.admin.admin_point.AdminMap', mock_adm_map)
        mock_adm_map().admin_menu.return_value = {1: mock_call_2}
        mocker.patch('builtins.input', lambda _: next(inps))
        mocker.patch('src.users.admin.admin_point.Config.ADMIN_PROMPT_LENGTH', "6")
        adm = Admin("1234")
        adm.adminmodule()
        captured = capsys.readouterr()
        assert "Numbers only" in captured.out
        
    def test_adminmodule_fail_2(self, mocker, capsys):
        inps = iter([7,6])
        mock_adm_map = mocker.MagicMock()
        mocker.patch('src.users.admin.admin_point.AdminMap', mock_adm_map)
        mock_adm_map().admin_menu.return_value = {1: mock_call_3}
        mocker.patch('builtins.input', lambda _: next(inps))
        mocker.patch('src.users.admin.admin_point.Config.ADMIN_PROMPT_LENGTH', "6")
        adm = Admin("1234")
        assert adm.adminmodule() == None
        
    def test_adminmodule_fail_3(self, mocker, capsys):
        inps = iter([6])
        mock_adm_map = mocker.MagicMock()
        mocker.patch('builtins.input', lambda _: next(inps))
        mocker.patch('src.users.admin.admin_point.Config.ADMIN_PROMPT_LENGTH', "6")
        mocker.patch('src.users.admin.admin_point.Config.EXITING_PROMPT', "Exiting")
        adm = Admin("1234")
        adm.adminmodule()
        captured = capsys.readouterr()
        assert "Exiting" in captured.out
        
    def test_messages_handler_pass(self, mocker, capsys):
        inps = iter([9, 6])
        mocker.patch('builtins.input', lambda _: next(inps))
        mocker.patch('src.users.admin.admin_point.Config.ADMIN_PROMPT_LENGTH', "6")
        mocker.patch('src.users.admin.admin_point.Config.EXITING_PROMPT', "Exiting")
        mocker.patch.object(Admin, 'messages_handler', return_value=None)
        adm = Admin("1234")
        adm.adminmodule()
        captured = capsys.readouterr()
        assert "Exiting" in captured.out
        
    def test_message_handler_func(self, mocker):
        inps = iter([1, 2, 3, 5, 4])
        mock_adm_map = mocker.MagicMock()
        mocker.patch('src.users.admin.admin_point.AdminMap', mock_adm_map)
        mock_adm_map().message_menu.return_value = {1: mock_call_1, 2: mock_call_2, 3: mock_call_3, 4: mock_call_4}
        mocker.patch('builtins.input', lambda _: next(inps))
        mocker.patch('src.users.admin.admin_point.Config.MESSAGES_VIEW_PROMPT_LENGTH', "4")
        mocker.patch('src.users.admin.admin_point.Config.EXITING_PROMPT', "Exiting")
        adm = Admin("1234")
        assert adm.messages_handler() is None
        
    def test_message_handler_fucn_fail(self, mocker, capsys):
        inps = iter([5, 4])
        mock_adm_map = mocker.MagicMock()
        mocker.patch('src.users.admin.admin_point.AdminMap', mock_adm_map)
        mock_adm_map().message_menu.return_value = {1: mock_call_1, 2: mock_call_2, 3: mock_call_3, 4: mock_call_4}
        mocker.patch('builtins.input', lambda _: next(inps))
        mocker.patch('src.users.admin.admin_point.Config.MESSAGES_VIEW_PROMPT_LENGTH', "4")
        mocker.patch('src.users.admin.admin_point.Config.EXITING_PROMPT', "Exiting")
        mocker.patch('src.users.admin.admin_point.Config.INVALID_INPUT_PROMPT', "Invalid")
        adm = Admin("1234")
        adm.messages_handler()
        captured = capsys.readouterr()
        assert "Invalid" in captured.out

    def test_message_handler_func_exception(self, mocker, capsys):
        inps = iter([1, 4])
        mock_adm_map = mocker.MagicMock()
        mocker.patch('src.users.admin.admin_point.AdminMap', mock_adm_map)
        mock_adm_map().message_menu.return_value = {1: mock_call_2}
        mocker.patch('builtins.input', lambda _: next(inps))
        mocker.patch('src.users.admin.admin_point.Config.MESSAGES_VIEW_PROMPT_LENGTH', "4")
        adm = Admin("1234")
        adm.messages_handler()
        captured = capsys.readouterr()
        assert "Numbers only" in captured.out
        
class TestAdminController:

    @pytest.fixture(autouse=True)
    def mock_message(self, mocker):
        mock_message = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.MessageDB', mock_message)
        return mock_message
    
    @pytest.fixture(autouse=True)
    def mock_banurl(self, mocker):
        mock_ban = mocker.Mock()
        mocker.patch('src.users.admin.admincontroller.BanUrlDB', mock_ban)
        return mock_ban

    @pytest.fixture(autouse=True)
    def mock_transcriptor(self, mocker):
        mock_transcriptor = mocker.Mock()
        mocker.patch('src.users.admin.admincontroller.transcriptor', mock_transcriptor)
        return mock_transcriptor

    def test_init(self, mocker):
        mock_adm = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.AdminController', mock_adm)
        adm = Admin("1234")
        assert adm.uid == "1234"
        
    @pytest.mark.parametrize("uid, user_valid, expected", [(None, True, "No user found"), (None, False, "Enter Valid Username"), (["1234"], True, None)])
    def test_view_user(self, mocker, capsys, uid, user_valid, expected):
        mocker.patch('src.users.admin.admincontroller.username_validation', return_value= user_valid)
        mocker.patch.object(AdminController,'uid_generator', return_value= uid)
        mock_adm = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.DBHelper', mock_adm)
        mock_adm.display_data.return_value = None
        mocker.patch('builtins.input', lambda _: "abhay")
        mocker.patch('src.users.admin.admincontroller.Config.NO_USER_FOUND', "No user found")
        adm = AdminController("1234")
        res = adm.view_user()
        captured = capsys.readouterr()
        if expected :
            assert expected in captured.out
        else:
            assert res is None


    def test_view_all_users(self, mocker, capsys):
        mock_db = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.DBHelper', mock_db)
        mock_db.display_data.return_value = None
        adm = AdminController("1234")
        res = adm.view_all_users()
        captured = capsys.readouterr()
        assert res is None

    @pytest.mark.parametrize("uid, user_valid, expected", [(False, True, "No user found"), (None, False, "Enter Valid Username"), (["1234"], True, "User downgraded")])
    def test_downgrade_premium_user(self, mocker, capsys, mock_banurl,mock_message,mock_transcriptor, uid, user_valid, expected):
        mocker.patch('builtins.input', lambda _: "abhay")
        mock_user = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.UsersDB', mock_user)
        mocker.patch('src.users.admin.admincontroller.username_validation', return_value= user_valid)
        mocker.patch.object(AdminController,'uid_generator', return_value= uid)
        mocker.patch('src.users.admin.admincontroller.Config.NO_USER_FOUND', "No user found")
        mock_user.update_user.return_value = None
        adm = AdminController("1234")
        res = adm.downgrade_premium_user()
        captured = capsys.readouterr()
        assert expected in captured.out
        assert res is None


    @pytest.mark.parametrize("uid, user_valid, expected", [(False, True, "No user found"), (None, False, "Enter Valid Username"), (["1234"], True, "User banned")])
    def test_ban_user(self, mocker, capsys, mock_banurl,mock_message,mock_transcriptor, uid, user_valid, expected):
        mocker.patch('builtins.input', lambda _: "abhay")
        mock_user = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.UsersDB', mock_user)
        mocker.patch('src.users.admin.admincontroller.username_validation', return_value= user_valid)
        mocker.patch.object(AdminController,'uid_generator', return_value= uid)
        mocker.patch('src.users.admin.admincontroller.Config.NO_USER_FOUND', "No user found")
        mock_user.update_user.return_value = None
        adm = AdminController("1234")
        res = adm.ban_user()
        captured = capsys.readouterr()
        assert expected in captured.out
        assert res is None

    @pytest.mark.parametrize("uid, user_valid, expected", [(False, True, "No user found"), (None, False, "Enter Valid Username"), (["1234"], True, "User unbanned")])
    def test_unban_user(self, mocker, capsys, mock_banurl,mock_message,mock_transcriptor, uid, user_valid, expected):
        mocker.patch('builtins.input', lambda _: "abhay")
        mock_user = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.UsersDB', mock_user)
        mocker.patch('src.users.admin.admincontroller.username_validation', return_value= user_valid)
        mocker.patch.object(AdminController,'uid_generator', return_value= uid)
        mocker.patch('src.users.admin.admincontroller.Config.NO_USER_FOUND', "No user found")
        mock_user.update_user.return_value = None
        adm = AdminController("1234")
        res = adm.unban_user()
        captured = capsys.readouterr()
        assert expected in captured.out
        assert res is None

    @pytest.mark.parametrize("url_valid, expected", [(True, "Url banned"), (False, "Enter valid url")])
    def test_ban_url(self, mocker, capsys, mock_transcriptor, mock_banurl, url_valid, expected):
        mocker.patch('src.users.admin.admincontroller.url_validation', return_value= url_valid)
        mocker.patch('builtins.input', lambda _: "https://www.youtube.com/watch?v=1")
        mock_transcriptor.extract_video_id.return_value = "1234"
        mock_banurl.save_ban_url.return_value = None
        adm = AdminController("1234")
        adm.ban_url()
        captured = capsys.readouterr()
        assert expected in captured.out

    #skip
    @pytest.mark.parametrize("url_valid, entry, expected", [(True, False, "No URL Found"),(True,True, "Url unbanned"), (False,True, "Enter valid url")])
    def test_unban_url(self, mocker, capsys, mock_transcriptor, mock_banurl, url_valid, entry, expected):
        mocker.patch('builtins.input', lambda _: "https://www.youtube.com/watch?v=1")
        mocker.patch('src.users.admin.admincontroller.url_validation', return_value= url_valid)
        mock_transcriptor().extract_video_id.return_value = "1234"
        mock_banurl().check_ban_url.return_value = entry
        mock_banurl().delete_ban_url.return_value = True
        mocker.patch('src.users.admin.admincontroller.Config.NO_URL_FOUND', "No URL Found")
        adm = AdminController("1234")
        adm.unban_url()
        captured = capsys.readouterr()
        assert expected in captured.out

    @pytest.mark.parametrize("url_valid, user_valid, valid, entry, expected", [(True,False,["1234"],[["123", "Hate", 4]], "Enter valid url/username"),(True, True, ["1234"],[["123", "Hate", 7]],"Can't be unbanned.\nReason Category - Hate\nSeverity Level(Greater than 5) - 7"),(True, True, ["1234"],[["123", "Hate", 3]],"Premium Listing done for abhay"),(True, True, ["1234"],False,"No URL Found"),(True,True, False, [["123", "Hate", 4]],"No user found"), (False,True,["1234"],[["123", "Hate", 4]], "Enter valid url/username")])
    def test_unban_url_for_premium_user(self, mocker, capsys, mock_transcriptor, mock_banurl, url_valid, user_valid, valid, entry, expected):
        inps = iter(["https://www.youtube.com/watch?v=1", "abhay"])
        mocker.patch('builtins.input', lambda _: next(inps))
        mocker.patch('src.users.admin.admincontroller.url_validation', return_value= url_valid)
        mocker.patch('src.users.admin.admincontroller.username_validation', return_value= user_valid)
        mocker.patch.object(AdminController,'uid_generator', return_value= valid)
        mocker.patch('src.users.admin.admincontroller.Config.NO_URL_FOUND', "No URL Found")
        mocker.patch('src.users.admin.admincontroller.Config.NO_USER_FOUND', "No user found")
        mock_transcriptor().extract_video_id.return_value = "1234"
        mock_banurl().fetch_ban_url.return_value = entry
        mock_premium = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.PremiumListingsDB', mock_premium)
        mock_premium().save_ban_url.return_value = None
        mock_banurl().delete_ban_url.return_value = True
        adm = AdminController("1234")
        adm.unban_url_for_premium_user()
        captured = capsys.readouterr()
        assert expected in captured.out

    @pytest.mark.parametrize("username_valid, expected", [(True, None), (False, "Enter valid username")])
    def test_message_from_user(self, mocker, capsys, mock_message, username_valid, expected):
        mocker.patch('builtins.input', lambda _: "abhay")
        mock_message().view_one_message.return_value = None
        adm = AdminController("1234")
        res = adm.message_from_user()
        captured = capsys.readouterr()
        if expected is False:
            assert expected in captured.out
        assert res is None

    def test_messages_from_non_premium_users(self, mock_message):
        mock_message().view_non_premium_messages.return_value = None
        adm = AdminController("1234")
        res = adm.messages_from_non_premium_users()
        assert res is None

    def test_messages_from_premium_users(self, mock_message):
        mock_message().view_premium_messages.return_value = None
        adm = AdminController("1234")
        res = adm.messages_from_premium_users()
        assert res is None
    
    def test_view_all_messages(self, mock_message):
        mock_message().view_all_messages.return_value = None
        adm = AdminController("1234")
        res = adm.view_all_messages()
        assert res is None

    @pytest.mark.parametrize("target, expected", [(["1234"], "1234"), (None, None)])
    def test_uid_generator(self, mocker, target, expected):
        mock_db = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.DBHelper', mock_db)
        mock_db.fetch_data.return_value = target
        adm = AdminController("1234")
        res = adm.uid_generator("abhay")
        assert res == expected


    @pytest.mark.parametrize("user_valid, valid, expected", [(True, ["1234"], None),(True, False,"No User Found"), (False,None, "Enter valid username")])
    def test_view_history_of_user(self, mocker, capsys, user_valid, valid, expected):
        mock_history = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.HistoryDB', mock_history)
        # mock_history.display_data.return_value = None
        mocker.patch('builtins.input', lambda _: "abhay")
        mocker.patch('src.users.admin.admincontroller.username_validation', return_value= user_valid)
        mocker.patch.object(AdminController,'uid_generator', return_value= valid)
        mocker.patch('src.users.admin.admincontroller.Config.NO_USER_FOUND', "No User Found")
        adm = AdminController("1234")
        res = adm.view_history_of_user()
        captured = capsys.readouterr()
        if expected is None:
            mock_history().view_one_user_history.assert_called_once()
        else:
            assert expected in captured.out
    
    @pytest.mark.parametrize("user_valid, valid, expected", [(True, ["1234"], None),(True, False,"No User Found"), (False,None, "Enter valid username")])
    def test_view_premium_listing_of_user(self, mocker, capsys, user_valid, valid, expected):
        mock_premium = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.PremiumListingsDB', mock_premium)
        # mock_history.display_data.return_value = None
        mocker.patch('builtins.input', lambda _: "abhay")
        mocker.patch('src.users.admin.admincontroller.username_validation', return_value= user_valid)
        mocker.patch.object(AdminController,'uid_generator', return_value= valid)
        mocker.patch('src.users.admin.admincontroller.Config.NO_USER_FOUND', "No User Found")
        adm = AdminController("1234")
        res = adm.view_premium_listing_of_user()
        captured = capsys.readouterr()
        if expected is None:
            mock_premium().view_premium_user_listing.assert_called_once()
        else:
            assert expected in captured.out

    def test_view_all_history(self, mocker):
        mock_history = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.HistoryDB', mock_history)
        adm = AdminController("1234")
        res = adm.view_all_history()
        mock_history().view_all_history.assert_called_once()

    def test_view_all_premium_listing(self, mocker):
        mock_premium = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.PremiumListingsDB', mock_premium)
        adm = AdminController("1234")
        res = adm.view_all_premium_listings()
        mock_premium().view_all_premium_listings.assert_called_once()

    def test_show_all_ban_urls(self, mocker, mock_banurl):
        adm = AdminController("1234")
        res = adm.show_all_ban_urls()
        mock_banurl().view_all_ban_urls.assert_called_once()

    @pytest.mark.parametrize("url_valid, entry, expected", [(True,True, None), (True, False, "No URL Found"), (False, True, "Enter valid url.")])
    def test_show_ban_url(self, mocker,capsys, mock_banurl, mock_transcriptor, url_valid, entry, expected):
        mocker.patch('builtins.input', lambda _: "https://www.youtube.com/watch?v=1")
        mock_transcriptor().extract_video_id.return_value = "1234"
        mock_banurl().fetch_ban_url.return_value = entry
        mocker.patch('src.users.admin.admincontroller.url_validation', return_value= url_valid)
        mocker.patch('src.users.admin.admincontroller.Config.NO_URL_FOUND', "No URL Found")
        adm = AdminController("1234")
        res = adm.show_ban_url()
        # mock_banurl().fetch_ban_url.assert_called_once()
        # mock_banurl().view_ban_url.assert_called_once()
        captured = capsys.readouterr()
        if expected is not None:
            assert expected in captured.out
        else:
            assert res is None
        