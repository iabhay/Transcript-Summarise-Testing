import pytest
import sqlite3
from src.database.database_connection import DatabaseConnection

@pytest.fixture
def mock_database_connection(mocker):
    mock_connection = mocker.MagicMock(spec = DatabaseConnection)
    mocker.patch('src.database.database_connection.DatabaseConnection', return_value = mock_connection)
    mock_cursor = mocker.MagicMock()
    mock_connection.__enter__.return_value.cursor.return_value = mock_cursor
    mock_connection.__exit__.return_value = None
    return mock_cursor
 
class TestContextManager:
 
    def test_database_connection(self):
        with DatabaseConnection(":memory:") as conn:
            assert conn is not None
 
    def test_database_connection_class_error(self):
        with pytest.raises(sqlite3.Error):
            with DatabaseConnection(":memory:") as conn:
                raise sqlite3.Error

