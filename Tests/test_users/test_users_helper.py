import pytest
from src.users.users_helper import UsersHelper

@pytest.mark.parametrize("inp, expected", [(1, "You are now upgraded to premium."), (2, "Back.."), (3, "Enter valid choice.")])
def test_upgrade_to_premium(mocker, inp, expected, capsys):
    mock_user = mocker.MagicMock()
    mocker.patch('src.users.users_helper.UsersDB',mock_user)
    mocker.patch('builtins.input', lambda _: inp)
    mock_user.update_user.return_value = True
    user_obj = UsersHelper("123")
    user_obj.upgrade_to_premium()
    captured = capsys.readouterr()
    assert expected in captured.out



def test_upgrade_to_premium_exception(mocker, capsys):
    mock_user = mocker.MagicMock()
    mocker.patch('src.users.users_helper.UsersDB',mock_user)
    mocker.patch('builtins.input').side_effect = [ValueError("Enter Numbers only.")]
    mock_user.update_user.return_value = True
    user_obj = UsersHelper("123")
    user_obj.upgrade_to_premium()
    captured = capsys.readouterr()
    assert "Enter Numbers only." in captured.out

@pytest.mark.parametrize("inp, expected", [(1, "You are downgraded!!"), (2, "back.."), (3, "Enter valid choice.")])
def test_downgrade_to_premium(mocker, inp, expected, capsys):
    mock_user = mocker.MagicMock()
    mocker.patch('src.users.users_helper.UsersDB',mock_user)
    mocker.patch('builtins.input', lambda _: inp)
    mock_user.update_user.return_value = True
    user_obj = UsersHelper("123")
    user_obj.downgrade_to_basic()
    captured = capsys.readouterr()
    assert expected in captured.out

def test_downgrade_to_premium_exception(mocker, capsys):
    mock_user = mocker.MagicMock()
    mocker.patch('src.users.users_helper.UsersDB',mock_user)
    mocker.patch('builtins.input').side_effect = [ValueError("Enter Numbers only.")]
    mock_user.update_user.return_value = True
    user_obj = UsersHelper("123")
    user_obj.downgrade_to_basic()
    captured = capsys.readouterr()
    assert "Enter Numbers only." in captured.out