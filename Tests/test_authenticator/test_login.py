import pytest
from src.authenticator.login.login import Login


def test_login_module_admin(mocker):
    mocker.patch("builtins.input", lambda _: "admin")
    prompt = "Enter"
    mocker.patch("src.authenticator.login.login.pwinput", lambda prompt, mask: "admin")
    mocker.patch("src.authenticator.login.login.Config.ADMIN_USERNAME", "admin")
    mocker.patch("src.authenticator.login.login.Config.ADMIN_PASSWORD", "admin")
    mock_admin = mocker.Mock()
    mocker.patch("src.authenticator.login.login.Admin", lambda _: mock_admin)
    login = Login()
    login.login_module()
    mock_admin.adminmodule.assert_called_once()


def test_login_module_new_login_invalid(mocker, capsys):
    mocker.patch("builtins.input", lambda _: "newuser")
    prompt = "Enter"
    mocker.patch(
        "src.authenticator.login.login.pwinput", lambda prompt, mask: "newuser"
    )
    mocker.patch("src.authenticator.login.login.Config.ADMIN_USERNAME", "admin")
    mocker.patch("src.authenticator.login.login.Config.ADMIN_PASSWORD", "admin")
    mock_user = mocker.Mock()
    mocker.patch("src.authenticator.login.login.UsersDB", lambda _: mock_user)
    mock_user.check_user.return_value = None
    login = Login()
    login.login_module()
    captured = capsys.readouterr()
    assert "Invalid Credentials!!" in captured.out


# @pytest.mark.skip
def test_login_module_new_login_valid_banned(mocker, capsys):
    mocker.patch("builtins.input", lambda _: "newuser")
    prompt = "Enter"
    mocker.patch(
        "src.authenticator.login.login.pwinput", lambda prompt, mask: "newuser"
    )
    mocker.patch("src.authenticator.login.login.Config.ADMIN_USERNAME", "admin")
    mocker.patch("src.authenticator.login.login.Config.ADMIN_PASSWORD", "admin")
    mock_user = mocker.Mock()
    mocker.patch("src.authenticator.login.login.UsersDB", lambda _: mock_user)
    mock_user.check_user.return_value = [
        [1, "newuser", "newuser", "date", "nonpremium", "banned"]
    ]
    mock_message = mocker.Mock()
    mocker.patch("src.authenticator.login.login.MessageDB", lambda _: mock_message)
    mock_nonpremium = mocker.Mock()
    mocker.patch(
        "src.authenticator.login.login.NonPremiumUser", lambda _: mock_nonpremium
    )
    mock_premium = mocker.Mock()
    mocker.patch("src.authenticator.login.login.PremiumUser", lambda _: mock_premium)
    mock_admin = mocker.Mock()
    mocker.patch("src.authenticator.login.login.Admin", lambda _: mock_admin)
    login = Login()
    res = login.login_module()
    mock_message.banned_module.assert_called_once()
    assert res == True


def test_login_module_new_login_valid_unbanned(mocker, capsys):
    mocker.patch("builtins.input", lambda _: "newuser")
    prompt = "Enter"
    mocker.patch(
        "src.authenticator.login.login.pwinput", lambda prompt, mask: "newuser"
    )
    mocker.patch("src.authenticator.login.login.Config.ADMIN_USERNAME", "admin")
    mocker.patch("src.authenticator.login.login.Config.ADMIN_PASSWORD", "admin")
    mock_user = mocker.Mock()
    mocker.patch("src.authenticator.login.login.UsersDB", lambda _: mock_user)
    mock_user.check_user.return_value = [
        [1, "newuser", "newuser", "date", "nonpremiumuser", "unbanned"]
    ]
    mock_message = mocker.Mock()
    mocker.patch("src.authenticator.login.login.MessageDB", lambda _: mock_message)
    mock_nonpremium = mocker.Mock()
    mocker.patch(
        "src.authenticator.login.login.NonPremiumUser", lambda _: mock_nonpremium
    )
    mock_premium = mocker.Mock()
    mocker.patch("src.authenticator.login.login.PremiumUser", lambda _: mock_premium)
    mock_admin = mocker.Mock()
    mocker.patch("src.authenticator.login.login.Admin", lambda _: mock_admin)
    mock_nonpremium.non_premium_module.return_value = None
    login = Login()
    res = login.login_module()
    mock_nonpremium.non_premium_module.assert_called_once()
    # assert res == True


def test_login_module_new_login_valid_unbanned_premium(mocker, capsys):
    mocker.patch("builtins.input", lambda _: "newuser")
    prompt = "Enter"
    mocker.patch(
        "src.authenticator.login.login.pwinput", lambda prompt, mask: "newuser"
    )
    mocker.patch("src.authenticator.login.login.Config.ADMIN_USERNAME", "admin")
    mocker.patch("src.authenticator.login.login.Config.ADMIN_PASSWORD", "admin")
    mock_user = mocker.Mock()
    mocker.patch("src.authenticator.login.login.UsersDB", lambda _: mock_user)
    mock_user.check_user.return_value = [
        [1, "newuser", "newuser", "date", "premiumuser", "unbanned"]
    ]
    mock_message = mocker.Mock()
    mocker.patch("src.authenticator.login.login.MessageDB", lambda _: mock_message)
    mock_nonpremium = mocker.Mock()
    mocker.patch(
        "src.authenticator.login.login.NonPremiumUser", lambda _: mock_nonpremium
    )
    mock_premium = mocker.Mock()
    mocker.patch("src.authenticator.login.login.PremiumUser", lambda _: mock_premium)
    mock_admin = mocker.Mock()
    mocker.patch("src.authenticator.login.login.Admin", lambda _: mock_admin)
    login = Login()
    mock_premium.premium_module.return_value = None
    res = login.login_module()
    mock_premium.premium_module.assert_called_once()
    # assert res == True


def test_login_module_role_change_premium(mocker, capsys):
    mocker.patch("builtins.input", lambda _: "newuser")
    prompt = "Enter"
    mocker.patch(
        "src.authenticator.login.login.pwinput", lambda prompt, mask: "newuser"
    )
    mocker.patch("src.authenticator.login.login.Config.ADMIN_USERNAME", "admin")
    mocker.patch("src.authenticator.login.login.Config.ADMIN_PASSWORD", "admin")
    mock_user = mocker.Mock()
    mocker.patch("src.authenticator.login.login.UsersDB", lambda _: mock_user)
    mock_user.check_user.return_value = [
        [1, "newuser", "newuser", "date", "nonpremiumuser", "unbanned"]
    ]
    mock_message = mocker.Mock()
    mocker.patch("src.authenticator.login.login.MessageDB", lambda _: mock_message)
    mock_nonpremium = mocker.Mock()
    mocker.patch(
        "src.authenticator.login.login.NonPremiumUser", lambda _: mock_nonpremium
    )
    mock_premium = mocker.Mock()
    mocker.patch("src.authenticator.login.login.PremiumUser", lambda _: mock_premium)
    mock_admin = mocker.Mock()
    mocker.patch("src.authenticator.login.login.Admin", lambda _: mock_admin)

    mock_nonpremium.non_premium_module.return_value = "nonpremium"
    mock_premium.premium_module.return_value = None
    login = Login()
    res = login.login_module()
    mock_premium.premium_module.assert_called_once()
    assert res == None


def test_login_module_role_change_non_premium(mocker, capsys):
    mocker.patch("builtins.input", lambda _: "newuser")
    prompt = "Enter"
    mocker.patch(
        "src.authenticator.login.login.pwinput", lambda prompt, mask: "newuser"
    )
    mocker.patch("src.authenticator.login.login.Config.ADMIN_USERNAME", "admin")
    mocker.patch("src.authenticator.login.login.Config.ADMIN_PASSWORD", "admin")
    mock_user = mocker.Mock()
    mocker.patch("src.authenticator.login.login.UsersDB", lambda _: mock_user)
    mock_user.check_user.return_value = [
        [1, "newuser", "newuser", "date", "premiumuser", "unbanned"]
    ]
    mock_message = mocker.Mock()
    mocker.patch("src.authenticator.login.login.MessageDB", lambda _: mock_message)
    mock_nonpremium = mocker.Mock()
    mocker.patch(
        "src.authenticator.login.login.NonPremiumUser", lambda _: mock_nonpremium
    )
    mock_premium = mocker.Mock()
    mocker.patch("src.authenticator.login.login.PremiumUser", lambda _: mock_premium)
    mock_admin = mocker.Mock()
    mocker.patch("src.authenticator.login.login.Admin", lambda _: mock_admin)

    mock_premium.premium_module.return_value = "premium"
    mock_nonpremium.non_premium_module.return_value = None
    login = Login()
    res = login.login_module()
    mock_nonpremium.non_premium_module.assert_called_once()
    assert res == None


def test_login_module_admin(mocker, capsys):
    mocker.patch("builtins.input", lambda _: "newuser")
    prompt = "Enter"
    mocker.patch(
        "src.authenticator.login.login.pwinput", lambda prompt, mask: "newuser"
    )
    mocker.patch("src.authenticator.login.login.Config.ADMIN_USERNAME", "admin")
    mocker.patch("src.authenticator.login.login.Config.ADMIN_PASSWORD", "admin")
    mock_user = mocker.Mock()
    mocker.patch("src.authenticator.login.login.UsersDB", lambda _: mock_user)
    mock_user.check_user.return_value = [
        [1, "newuser", "newuser", "date", "admin", "unbanned"]
    ]
    mock_message = mocker.Mock()
    mocker.patch("src.authenticator.login.login.MessageDB", lambda _: mock_message)
    mock_nonpremium = mocker.Mock()
    mocker.patch(
        "src.authenticator.login.login.NonPremiumUser", lambda _: mock_nonpremium
    )
    mock_premium = mocker.Mock()
    mocker.patch("src.authenticator.login.login.PremiumUser", lambda _: mock_premium)
    mock_admin = mocker.Mock()
    mocker.patch("src.authenticator.login.login.Admin", lambda _: mock_admin)
    login = Login()
    res = login.login_module()
    mock_admin.adminmodule.assert_called_once()
    assert res == None
