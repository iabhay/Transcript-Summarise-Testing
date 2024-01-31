import pytest
from src.database.db_ops.db_helper import DBHelper
from src.database.database_connection import DatabaseConnection
@pytest.fixture
def mock_cursor(mocker):
    '''Test Fixture to mock db connection'''

    mock_database_connection = mocker.MagicMock(spec=DatabaseConnection)
    mocker.patch('src.database.db_ops.db_helper.DatabaseConnection', mock_database_connection)

    mock_connection = mocker.MagicMock()
    mock_database_connection().__enter__.return_value = mock_connection

    mock_cursor = mocker.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    
    # mock_execute = mocker.Mock()
    # mock_cursor.execute = mock_execute

    return mock_cursor

def test_save_data(mocker, mock_cursor):
    '''Test save data method'''
    DBHelper.save_data("query", (1,2))
    mock_cursor.execute.assert_called_once_with("query", (1,2))


@pytest.mark.parametrize("query, tup", [("query", (1,2)), ("query", (1,2)), ("query", (False,))])
def test_fetch_data(mock_cursor,  query, tup):
    '''Test fetch data method'''
    DBHelper.fetch_data("query", (1,2))
    
    if tup == False:
        mock_cursor.execute.assert_called_once_with(query)
    elif tup == True:
        mock_cursor.execute.assert_called_once_with(query, (1,2))
    mock_cursor.fetchall.assert_called_once()


@pytest.mark.parametrize("query, table_schema, value", [("query", ['Date', 'Url'], ('U1',)), ("query", ['Date', 'Url'], None), ("query", ['Date', 'Url'], ('U1',))])
def test_display_data(mocker, mock_cursor, query, table_schema, value):
    '''Test display data method'''
    mock_table = mocker.MagicMock()
    mocker.patch('src.database.db_ops.db_helper.PrettyTable', mock_table)
    mock_table().add_row.return_value = True
    mock_cursor.fetchall.return_value = [1,1,1,1,1,1,1]
    DBHelper.display_data(query, table_schema, value)
    if value is not None:
        mock_cursor.execute.assert_called_once_with(query, value)
    elif value is None:
        mock_cursor.execute.assert_called_once_with("query")


@pytest.mark.parametrize("query, value", [("query", (1,2))])
def test_delete_data(mocker, mock_cursor, query, value):
    '''Test delete data method'''
    DBHelper.delete_data(query, value)
    mock_cursor.execute.assert_called_once_with(query, value)
    

