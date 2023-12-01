import pytest
import builtins
import sys
from src.users.admin.admin_point import Admin
from src.users.admin.admincontroller import AdminController
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
    def test_init(self, mocker):
        mock_adm = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.AdminController', mock_adm)
        adm = Admin("1234")
        assert adm.uid == "1234"
        
    def test_view_user_pass(self, mocker):
        inps = iter(["abhay", "agrawal"])
        mocker.patch('src.users.admin.admincontroller.username_validation', return_value=True)
        mocker.patch.object(AdminController,'uid_generator', return_value=["1234", "abhay"])
        
        mock_adm = mocker.MagicMock()
        mocker.patch('src.users.admin.admincontroller.DBHelper', mock_adm)
        mock_adm.display_data.return_value = None
        mocker.patch('builtins.input', lambda _: next(inps))
        adm = AdminController("1234")
        assert adm.view_user() is None
        
#     def test_view_user_fail(self, mocker, capsys):
#         inps = iter([3, 2])
#         mock_adm = mocker.MagicMock()
#         mocker.patch('src.users.admin.admin_point.Admin', mock_adm)
#         mock_adm().view_user.return_value = None
#         mocker.patch('builtins.input', lambda _: next(inps))
#         mocker.patch('src.users.admin.admin_point.Config.USERNAME_PROMPT_LENGTH', "2")
#         mocker.patch('src.users.admin.admin_point.Config.INVALID_INPUT_PROMPT', "Invalid")
#         adm = Admin("1234")
#         adm.view_user()
#         captured = capsys.readouterr()
#         assert "Invalid" in captured.out
        
#     def test_view_all_users_pass(self, mocker):
#         inps = iter([1, 2])
#         mock_adm = mocker.MagicMock()
#         mocker.patch('src.users.admin.admin_point.Admin', mock_adm)
#         mock_adm().view_all_users.return_value = None
#         mocker.patch('builtins.input', lambda _: next(inps))
#         mocker.patch('src.users.admin.admin_point.Config.USERNAME_PROMPT_LENGTH', "2")
#         adm = Admin("1234")
#         assert adm.view_all_users() is None
        
#     def test_view_all_users_fail(self, mocker, capsys):
#         inps = iter([3, 2])
#         mock_adm = mocker.MagicMock()
#         mocker.patch('src.users.admin.admin_point.Admin', mock_adm)
#         mock_adm().view_all_users.return_value = None
#         mocker.patch('builtins.input', lambda _: next(inps))
#         mocker.patch('src.users.admin.admin_point.Config.USERNAME_PROMPT_LENGTH', "2")
#         mocker.patch('src.users.admin.admin_point.Config.INVALID_INPUT_PROMPT', "Invalid")
#         adm = Admin("1234")
#         adm.view_all_users()
#         captured = capsys.readouterr()
#         assert "Invalid