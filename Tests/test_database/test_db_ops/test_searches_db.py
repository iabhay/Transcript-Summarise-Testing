import pytest
from src.database.db_ops.searches_db import SearchesDB

@pytest.fixture(autouse=True)
def mock_db_helper(mocker):
    mock_db = mocker.MagicMock()
    mocker.patch('src.database.db_ops.searches_db.DBHelper', mock_db)
    mock_db.fetch_data.return_value = [[1, '01/01/2021 00:00:00', 0, '02/01/2021 00:00:00']]
    mock_db.save_data.return_value = None
    return mock_db

@pytest.fixture(autouse=True)
def mock_user_db(mocker):
    mock_user = mocker.MagicMock()
    mocker.patch('src.database.db_ops.searches_db.UsersDB', mock_user)
    mock_user().update_user.return_value = None
    return mock_user

@pytest.fixture(autouse=True)
def mock_date(mocker):
    mock_dt = mocker.MagicMock()
    mocker.patch('src.database.db_ops.searches_db.datetime', mock_dt)
    mock_tm = mocker.MagicMock()
    mock_dt.now.return_value = mock_tm
    mock_tm.strftime.return_value = "01/01/2021 00:00:00"
    return mock_dt

def test_view_user_search_count(mocker, mock_db_helper, mock_user_db):
    search_db = SearchesDB("U1")
    res = search_db.view_user_search_count()
    assert res == 0


@pytest.mark.parametrize("limit, expected", [(5, True), (0, False)])
def test_update_user_search_count(mocker, mock_db_helper, mock_user_db, limit, expected):
    mocker.patch.object(SearchesDB, 'view_user_search_count', return_value=0)
    search_db = SearchesDB("U1")
    res = search_db.update_user_search_count(limit)
    assert res == expected