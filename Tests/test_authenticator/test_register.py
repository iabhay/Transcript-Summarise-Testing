import pytest
from src.authenticator.register.register import Register

def test_register(mocker, capsys):
    user_inps = iter(["abhay", "abhay2"])
    pass_inps = iter(["abhaypswd", "abhay2pswd"])
    mock_user = mocker.MagicMock()
    mocker.patch('src.authenticator.register.register.UsersDB', mock_user)
    mocker.patch('src.authenticator.register.register.Config.ENTER_USERNAME_PROMPT')
    mocker.patch('builtins.input', lambda _: next(user_inps))
    a = "Enter"
    mocker.patch('src.authenticator.register.register.pwinput', lambda a, mask: next(pass_inps))
    # mocked_pwinput.return_value = next(pass_inps)
    mocker.patch('src.authenticator.register.register.username_validation', lambda _: True)
    mocker.patch('src.authenticator.register.register.password_validation', lambda _: True)
    mocker.patch.object(Register,'check_registration', lambda *args: False)
    mock_hash = mocker.MagicMock()
    mocker.patch('src.authenticator.register.register.hashlib.sha256', lambda _: mock_hash)
    mock_hash.hexdigest.return_value = "1234"
    mock_user().create_user.return_value = None
    obj = Register()
    obj.register_module()
    captured = capsys.readouterr()
    assert "Registered successfully!!" in captured.out


# def test_register_user_valid_fail(mocker, capsys):
#     inps =iter([("abhay","abhaypwd", False,True,True, "Invalid Username!"), ("abhay","abhaypwd", True,False,True,"Invalid Password!!"),("abhay", "abhaypwd",True,True,True,None),("abhay", "abhaypwd", True,True,False, "Registered successfully!!")])
#     a = "Enter"
#     mocker.patch('src.authenticator.register.register.pwinput', lambda a, mask:next(inps[1]))
#     mocker.patch('src.authenticator.register.register.Config.SECURE_USERNAME_PROMPT')
#     mocker.patch('src.authenticator.register.register.Config.SECURE_PASSWORD_PROMPT')
#     mock_user = mocker.MagicMock()
#     mocker.patch('src.authenticator.register.register.UsersDB', mock_user)
#     mocker.patch('builtins.input', lambda _: next(inps[0]))
#     mocker.patch('src.authenticator.register.register.username_validation', lambda _: next(inps[2]))
#     mocker.patch('src.authenticator.register.register.password_validation', lambda _: next(inps[3]))
#     mocker.patch.object(Register,'check_registration', lambda *args: next(inps[4]))
#     obj = Register()
#     obj.register_module()
#     captured = capsys.readouterr()
#     assert next(inps[5]) in captured.out

# def test_register_pass_valid_fail(mocker, capsys):
#     user_inps, pass_inps, user_valid, pass_valid, check_reg,expected =("abhay","abhaypwd", True,False,True,"Invalid Password!!")
#     a = "Enter"
#     mocker.patch('src.authenticator.register.register.pwinput', lambda a, mask: pass_inps)
#     mocker.patch('src.authenticator.register.register.Config.SECURE_USERNAME_PROMPT')
#     mocker.patch('src.authenticator.register.register.Config.SECURE_PASSWORD_PROMPT')
#     mock_user = mocker.MagicMock()
#     mocker.patch('src.authenticator.register.register.UsersDB', mock_user)
#     mocker.patch('builtins.input', lambda _: user_inps)
#     mocker.patch('src.authenticator.register.register.username_validation', lambda _: user_valid)
#     mocker.patch('src.authenticator.register.register.password_validation', lambda _: pass_valid)
#     mocker.patch.object(Register,'check_registration', lambda *args: check_reg)
#     obj = Register()
#     if check_reg is not None:    
#         captured = capsys.readouterr()
#         obj.register_module()
#         assert expected in captured.out
#     else:
#         assert obj.register_module() == None

# def test_register_already_registered(mocker, capsys):
#     user_inps, pass_inps, user_valid, pass_valid, check_reg,expected =("abhay","abhaypwd", True,True,True,None)
#     a = "Enter"
#     mocker.patch('src.authenticator.register.register.pwinput', lambda a, mask: pass_inps)
#     mocker.patch('src.authenticator.register.register.Config.SECURE_USERNAME_PROMPT')
#     mocker.patch('src.authenticator.register.register.Config.SECURE_PASSWORD_PROMPT')
#     mock_user = mocker.MagicMock()
#     mocker.patch('src.authenticator.register.register.UsersDB', mock_user)
#     mocker.patch('builtins.input', lambda _: user_inps)
#     mocker.patch('src.authenticator.register.register.username_validation', lambda _: user_valid)
#     mocker.patch('src.authenticator.register.register.password_validation', lambda _: pass_valid)
#     mocker.patch.object(Register,'check_registration', lambda *args: check_reg)
#     obj = Register()
#     if check_reg is not None:    
#         captured = capsys.readouterr()
#         obj.register_module()
#         assert expected in captured.out
#     else:
#         assert obj.register_module() == None

# def test_register_already_registered_successfully(mocker, capsys):
#     user_inps, pass_inps, user_valid, pass_valid, check_reg,expected =("abhay","abhaypwd",True,True,False, "Registered successfully!!")
#     a = "Enter"
#     mocker.patch('src.authenticator.register.register.pwinput', lambda a, mask: pass_inps)
#     mocker.patch('src.authenticator.register.register.Config.SECURE_USERNAME_PROMPT')
#     mocker.patch('src.authenticator.register.register.Config.SECURE_PASSWORD_PROMPT')
#     mock_user = mocker.MagicMock()
#     mocker.patch('src.authenticator.register.register.UsersDB', mock_user)
#     mocker.patch('builtins.input', lambda _: user_inps)
#     mocker.patch('src.authenticator.register.register.username_validation', lambda _: user_valid)
#     mocker.patch('src.authenticator.register.register.password_validation', lambda _: pass_valid)
#     mocker.patch.object(Register,'check_registration', lambda *args: check_reg)
#     obj = Register()
#     if check_reg is not None:    
#         captured = capsys.readouterr()
#         obj.register_module()
#         assert expected in captured.out
#     else:
#         assert obj.register_module() == None




