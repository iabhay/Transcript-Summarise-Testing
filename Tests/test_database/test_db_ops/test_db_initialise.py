import pytest
import sqlite3
from src.database.db_ops.db_initialise import DBInitialise
from src.database.database_connection import DatabaseConnection

@pytest.fixture
def mock_cursor(mocker):
    '''Test Fixture to mock db connection'''

    mock_database_connection = mocker.MagicMock(spec=DatabaseConnection)
    mocker.patch('src.database.db_ops.db_initialise.DatabaseConnection', mock_database_connection)

    mock_connection = mocker.MagicMock()
    mock_database_connection().__enter__.return_value = mock_connection

    mock_cursor = mocker.MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    
    # mock_execute = mocker.Mock()
    # mock_cursor.execute = mock_execute

    return mock_cursor

def test_create_all_tables(mocker, mock_cursor):
    '''Test create all tables method'''
    DBInitialise.create_all_tables()
    assert mock_cursor.execute.call_count == 6

def exception_thrower(*args, **kwargs):
    raise ValueError

# @pytest.mark.skip
def test_create_all_tables_exception(mocker, mock_cursor, caplog):
    '''Test create all tables method'''
    mocker.patch('src.database.db_ops.db_initialise.LogStatements.fail_tables_created', 'fail_tables_created')

    mock_cursor.execute = Exception()
    DBInitialise.create_all_tables()
    assert "fail_tables_created" in caplog.text
