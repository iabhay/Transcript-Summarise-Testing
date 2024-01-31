import pytest
from src.database.db_ops.messages_db import MessageDB

@pytest.fixture(autouse=True)
def mock_db_helper(mocker):
    mock_db = mocker.MagicMock()
    mocker.patch('src.database.db_ops.messages_db.DBHelper', mock_db)
    return mock_db

@pytest.fixture(autouse=True)
def mock_date(mocker):
    mock_dt = mocker.MagicMock()
    mocker.patch('src.database.db_ops.messages_db.datetime', mock_dt)
    mock_tm = mocker.MagicMock()
    mock_dt.now.return_value = mock_tm
    mock_tm.strftime.return_value = "01/01/2021 00:00:00"
    return mock_dt

def test_banned_module(mocker, capsys, mock_db_helper, mock_date):
    mocker.patch('builtins.input', return_value='lol')
    mocker.patch.object(MessageDB,'save_message', return_value=True)
    messages_db = MessageDB("U1")
    messages_db.banned_module()
    captured = capsys.readouterr()
    assert "Successfully sent message." in captured.out

def exception_thrower(*args, **kwargs):
    raise ValueError

def test_banned_module_exception(mocker, capsys, mock_db_helper, mock_date):
    mocker.patch('builtins.input', lambda _: "Message not sent successfully.")
    messages_db = MessageDB("U1")
    mocker.patch.object(MessageDB, 'save_message', exception_thrower)
    messages_db.banned_module()
    captured = capsys.readouterr()
    assert "Message not sent successfully." in captured.out

def test_save_message(mocker, mock_db_helper, mock_date):
    mock_short = mocker.MagicMock()
    mocker.patch('src.database.db_ops.messages_db.ShortUUID', mock_short)
    mock_short().random.return_value = "1234"
    mocker.patch('src.database.db_ops.messages_db.MessageTableQuery.query_insert_message', "lol")
    messages_db = MessageDB("U1")
    messages_db.save_message("Description")
    mock_db_helper.save_data.assert_called_once_with("lol", ('M1234', '01/01/2021 00:00:00', 'U1', 'Description'))
    
def test_delete_message_by_admin(mocker, mock_db_helper, mock_date):
    mocker.patch('src.database.db_ops.messages_db.MessageTableQuery.query_delete_message', "lol")
    messages_db = MessageDB("U1")
    messages_db.delete_message_by_admin()
    mock_db_helper.delete_data.assert_called_once_with("lol", ('U1', ))

def test_view_one_message(mocker, mock_db_helper, mock_date):
    mocker.patch('src.database.db_ops.messages_db.MessageTableQuery.query_select_message', "lol")
    messages_db = MessageDB("U1")
    messages_db.view_one_message("U1")
    mock_db_helper.display_data.assert_called_once_with("lol", ['Date', 'Username', 'Description'], ('U1', ))

def test_view_premium_messages(mocker, mock_db_helper, mock_date):
    mocker.patch('src.database.db_ops.messages_db.MessageTableQuery.query_select_premium_message', "lol")
    messages_db = MessageDB("U1")
    messages_db.view_premium_messages()
    mock_db_helper.display_data.assert_called_once_with("lol", ['Date', 'Username', 'Description'])

def test_view_non_premium_messages(mocker, mock_db_helper, mock_date):
    mocker.patch('src.database.db_ops.messages_db.MessageTableQuery.query_select_non_premium_message', "lol")
    messages_db = MessageDB("U1")
    messages_db.view_non_premium_messages()
    mock_db_helper.display_data.assert_called_once_with("lol", ['Date', 'Username', 'Description'])

def test_view_all_messages(mocker, mock_db_helper, mock_date):
    mocker.patch('src.database.db_ops.messages_db.MessageTableQuery.query_select_all_messages', "lol")
    messages_db = MessageDB("U1")
    messages_db.view_all_messages()
    mock_db_helper.display_data.assert_called_once_with("lol", ['Date', 'Username', 'Description'])
    