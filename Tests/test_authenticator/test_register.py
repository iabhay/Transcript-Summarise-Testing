import pytest
from src.authenticator.register.register import Register


def test_register(mocker, capsys):
    user_inps = iter(["abhay", "abhay2"])
    pass_inps = iter(["abhaypswd", "abhay2pswd"])
    mock_user = mocker.MagicMock()
    mocker.patch("src.authenticator.register.register.UsersDB", mock_user)
    mocker.patch("src.authenticator.register.register.Config.ENTER_USERNAME_PROMPT")
    mocker.patch("builtins.input", lambda _: next(user_inps))
    a = "Enter"
    mocker.patch(
        "src.authenticator.register.register.pwinput", lambda a, mask: next(pass_inps)
    )
    # mocked_pwinput.return_value = next(pass_inps)
    mocker.patch(
        "src.authenticator.register.register.username_validation", lambda _: True
    )
    mocker.patch(
        "src.authenticator.register.register.password_validation", lambda _: True
    )
    mocker.patch.object(Register, "check_registration", lambda *args: False)
    mock_hash = mocker.MagicMock()
    mocker.patch(
        "src.authenticator.register.register.hashlib.sha256", lambda _: mock_hash
    )
    mock_hash.hexdigest.return_value = "1234"
    mock_user().create_user.return_value = None
    obj = Register()
    obj.register_module()
    captured = capsys.readouterr()
    assert "Registered successfully!!" in captured.out


def test_check_registration_already_exist(mocker):
    mock_user = mocker.MagicMock()
    mocker.patch("src.authenticator.register.register.UsersDB", mock_user)
    mock_user().check_user.return_value = True
    obj = Register()
    assert obj.check_registration("abhay", "abhaypwd") == True


def test_check_registration_non_exist(mocker):
    mock_user = mocker.MagicMock()
    mocker.patch("src.authenticator.register.register.UsersDB", mock_user)
    mock_user().check_user.return_value = False
    obj = Register()
    assert obj.check_registration("abhay", "abhaypwd") == False


def test_register_invalid_username(mocker, capsys):
    user_valid = iter([False, True, True])
    pass_valid = iter([False, True])
    check_valid = iter([False, True])
    mock_user = mocker.MagicMock()
    mocker.patch("src.authenticator.register.register.UsersDB", mock_user)
    mocker.patch("src.authenticator.register.register.Config.ENTER_USERNAME_PROMPT")
    a = "Enter"
    mocker.patch(
        "src.authenticator.register.register.pwinput", lambda a, mask: "abhaypwd"
    )
    mocker.patch("builtins.input", lambda _: "abhay")
    mocker.patch(
        "src.authenticator.register.register.username_validation",
        lambda _: next(user_valid),
    )
    mocker.patch(
        "src.authenticator.register.register.password_validation",
        lambda _: next(pass_valid),
    )
    mocker.patch.object(Register, "check_registration", lambda *args: next(check_valid))
    mock_user.create_user.return_value = None
    obj = Register()
    res = obj.register_module()
    captured = capsys.readouterr()
    assert "Invalid Username!" in captured.out
    assert "Invalid Password!!" in captured.out
    assert "Registered successfully!!" in captured.out
    assert res == None
