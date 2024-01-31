import pytest
from src.main import YTTS

@pytest.fixture(autouse=True)
def mock_main(mocker):
    mock_reg = mocker.MagicMock()
    mocker.patch('src.main.Register', mock_reg)

    mock_login = mocker.MagicMock()
    mocker.patch('src.main.Login', mock_login)

    mock_reg.register_module.return_value = True
    mock_login.login_module.return_value = True

def exception_thrower(mocker):
    raise ValueError


@pytest.mark.skip
def test_main(mocker, mock_main, capsys):
    inps = iter([1, 2,4, 3])
    mocker.patch('builtins.input', next(inps))
    mocker.patch('src.main.Config.MAIN_PROMPT_LENGTH', 3)
    mocker.patch('src.main.Config.INVALID_INPUT_PROMPT', 'invalid')
    mocker.patch('src.main.Config.APP_INTRO', 'intro')
    mocker.patch('src.main.Config.APP_OUTRO', 'outro')
    ytts = YTTS()
    ytts.menu()
    captured = capsys.readouterr()
    # assert "Numbers only" in captured.out
    assert "invalid" in captured.out
    assert "intro" in captured.out
    assert "outro" in captured.out