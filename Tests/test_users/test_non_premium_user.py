import pytest
import sys
from src.users.non_premium_user.non_premium_user import NonPremiumUser
def mock_1():
    return True

def mock_2():
    return False

def test_non_premium_user(mocker):
    inps = iter([1, 2])
    
    mock_userdb = mocker.MagicMock()
    mocker.patch('src.users.non_premium_user.non_premium_user.UsersDB', mock_userdb)
    
    mock_premium = mocker.MagicMock()
    mocker.patch('src.users.non_premium_user.non_premium_user.PremiumUser', mock_premium)
    
    mock_video = mocker.MagicMock()
    mocker.patch('src.users.non_premium_user.non_premium_user.VideoService', mock_video)

    mocker.patch('src.users.non_premium_user.non_premium_user.Config.BASIC_USER_INTRO', "Intro")
    
    mocker.patch('builtins.input', lambda _: next(inps))
    
    mocker.patch('src.users.non_premium_user.non_premium_user.Config.NON_PREMIUM_PROMPT_LENGTH', "3")
    
    mock_non_premium_map = mocker.MagicMock()
    mocker.patch('src.users.non_premium_user.non_premium_user.NonPremiumMap', mock_non_premium_map)
    mock_non_premium_map().non_premium_menu.return_value = {1: mock_1, 2: mock_2}
    
    mocker.patch('src.users.non_premium_user.non_premium_user.logger.info', lambda _: None)
    
    non_premium = NonPremiumUser("1234")
    res = non_premium.non_premium_module()
    assert res == "nonpremium"
    
@pytest.mark.parametrize("inp, exp", [ (3, "Exit"), (2, "nonpremium")])    
def test_non_premium_user_invalid(mocker, capsys, inp, exp):
    
    mock_userdb = mocker.MagicMock()
    mocker.patch('src.users.non_premium_user.non_premium_user.UsersDB', mock_userdb)
    
    mock_premium = mocker.MagicMock()
    mocker.patch('src.users.non_premium_user.non_premium_user.PremiumUser', mock_premium)
    
    mock_video = mocker.MagicMock()
    mocker.patch('src.users.non_premium_user.non_premium_user.VideoService', mock_video)

    mocker.patch('src.users.non_premium_user.non_premium_user.Config.BASIC_USER_INTRO', "Intro")
    mocker.patch('builtins.input', lambda _: inp)
    
    mocker.patch('src.users.non_premium_user.non_premium_user.Config.NON_PREMIUM_PROMPT_LENGTH', "3")
    
    mock_non_premium_map = mocker.MagicMock()
    mocker.patch('src.users.non_premium_user.non_premium_user.NonPremiumMap', mock_non_premium_map)
    mock_non_premium_map().non_premium_menu.return_value = {1: mock_1, 2: mock_2}
    
    mocker.patch('src.users.non_premium_user.non_premium_user.logger.info', lambda _: None)
    
    mocker.patch('src.users.non_premium_user.non_premium_user.Config.INVALID_INPUT_PROMPT', "Invalid")
    
    mocker.patch('src.users.non_premium_user.non_premium_user.Config.EXITING_PROMPT', "Exit")
    
    non_premium = NonPremiumUser("1234")
    res = non_premium.non_premium_module()
    captured = capsys.readouterr()
    if res == None:
        assert exp in captured.out
    else:
        assert res == "nonpremium"
    
    
    
    