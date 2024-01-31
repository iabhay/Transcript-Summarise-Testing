import pytest
from src.database.db_ops.history_db import HistoryDB

@pytest.fixture(autouse=True)
def mock_db_helper(mocker):
    mock_db = mocker.MagicMock()
    mocker.patch('src.database.db_ops.history_db.DBHelper', mock_db)
    return mock_db

@pytest.fixture(autouse=True)
def mock_date(mocker):
    mock_dt = mocker.MagicMock()
    mocker.patch('src.database.db_ops.history_db.datetime', mock_dt)
    mock_tm = mocker.MagicMock()
    mock_dt.now.return_value = mock_tm
    mock_tm.strftime.return_value = "01/01/2021 00:00:00"
    return mock_dt

def test_save_history(mocker, mock_db_helper, mock_date):
    mock_short = mocker.MagicMock()
    mocker.patch('src.database.db_ops.history_db.ShortUUID', mock_short)
    mock_short().random.return_value = "1234"
    mocker.patch('src.database.db_ops.history_db.HistoryTableQuery.query_insert_history', "lol")
    history_db = HistoryDB("U1")
    res = history_db.save_history("U1")
    mock_db_helper.save_data.assert_called_once_with("lol", ('H1234', '01/01/2021 00:00:00', 'U1', 'U1'))
    assert res == "H1234" 

def test_save_history_fail(mocker, mock_db_helper, mock_date):
    mock_short = mocker.MagicMock()
    mocker.patch('src.database.db_ops.history_db.ShortUUID', mock_short)
    mock_short().random.return_value = "1234"
    mocker.patch('src.database.db_ops.history_db.HistoryTableQuery.query_insert_history', "lol")
    mock_db_helper.save_data.side_effect = Exception
    history_db = HistoryDB("U1")
    res = history_db.save_history("U1")
    mock_db_helper.save_data.assert_called_once_with("lol", ('H1234', '01/01/2021 00:00:00', 'U1', 'U1'))
    assert res == None

def test_view_one_user_history(mocker, mock_db_helper):
    mocker.patch('src.database.db_ops.history_db.HistoryTableQuery.query_select_history', "lol")
    history_db = HistoryDB("U1")
    history_db.view_one_user_history()
    mock_db_helper.display_data.assert_called_once_with("lol", ['Date', 'Url'], ('U1',))

def test_view_one_user_history_fail(mocker, mock_db_helper):
    mocker.patch('src.database.db_ops.history_db.HistoryTableQuery.query_select_history', "lol")
    mock_db_helper().display_data.side_effect = Exception
    history_db = HistoryDB("U1")
    history_db.view_one_user_history()
    mock_db_helper.display_data.assert_called_once_with("lol", ['Date', 'Url'], ('U1',))

def test_view_all_history(mocker, mock_db_helper):
    mocker.patch('src.database.db_ops.history_db.HistoryTableQuery.query_select_all_history', "lol")
    history_db = HistoryDB("U1")
    history_db.view_all_history()
    mock_db_helper.display_data.assert_called_once_with("lol", ['Date','Username', 'URL'])
    
