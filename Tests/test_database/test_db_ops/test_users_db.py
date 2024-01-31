import pytest
from src.database.db_ops.users_db import UsersDB

@pytest.fixture(autouse=True)
def mock_db_helper(mocker):
    mock_db = mocker.MagicMock()
    mocker.patch('src.database.db_ops.users_db.DBHelper', mock_db)
    return mock_db

@pytest.fixture(autouse=True)
def mock_date(mocker):
    mock_dt = mocker.MagicMock()
    mocker.patch('src.database.db_ops.users_db.datetime', mock_dt)
    mock_tm = mocker.MagicMock()
    mock_dt.now.return_value = mock_tm
    mock_tm.strftime.return_value = "01/01/2021 00:00:00"
    return mock_dt

def test_create_user(mocker, mock_db_helper, mock_date):
    mock_short = mocker.MagicMock()
    mocker.patch('src.database.db_ops.users_db.ShortUUID', mock_short)
    mock_short().random.return_value = "1234"
    mocker.patch('src.database.db_ops.users_db.UsersTableQuery.query_insert_user', "lol")
    mocker.patch('src.database.db_ops.users_db.UserSearchesTableQuery.query_insert_user_search', "lol")
    user_db = UsersDB("U1")
    user_db.create_user("U1", "pass")
    mock_db_helper.save_data.call_count == 2

def test_check_user(mocker, mock_db_helper):
    mock_db_helper.fetch_data.return_value = ["U1"]
    user_db = UsersDB("U1")
    res = user_db.check_user("U1", "pass")
    assert res == ["U1"]

@pytest.mark.parametrize("field, value", [("role", "admin"), ("ban_status", "banned")])
def test_update_user(mocker, mock_db_helper, field, value):
    user_db = UsersDB("U1")
    user_db.update_user(field, value)
    mocker.patch('src.database.db_ops.users_db.UsersTableQuery.query_update_user_role', "lol")
    mocker.patch('src.database.db_ops.users_db.UsersTableQuery.query_update_user_ban_status', "lol")
    mock_db_helper.save_data.call_count == 1

def test_fetch_user_details(mocker, mock_db_helper):
    user_db = UsersDB("U1")
    user_db.fetch_user_details("U1")
    mock_db_helper.fetch_data.assert_called_once()

def test_update_user_role_by_admin(mocker, mock_db_helper):
    user_db = UsersDB("U1")
    user_db.update_user_role_by_admin("U1", "admin")
    # mocker.patch('src.database.db_ops.users_db.UsersTableQuery.query_update_user_role', "lol")
    mock_db_helper.save_data.assert_called_once()

def test_user_history(mocker, mock_db_helper, mock_date):
    mock_short = mocker.MagicMock()
    mocker.patch('src.database.db_ops.users_db.ShortUUID', mock_short)
    mock_short().random.return_value = "1234"
    mocker.patch('src.database.db_ops.users_db.HistoryTableQuery.query_insert_history', "lol")
    user_db = UsersDB("U1")
    user_db.user_history("U1")
    mock_db_helper.save_data.assert_called_once_with("lol", ('H1234', '01/01/2021 00:00:00', 'U1', 'U1'))