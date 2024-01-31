import pytest
from src.database.db_ops.ban_url_db import BanUrlDB


@pytest.fixture(autouse=True)
def mock_db_helper(mocker):
    mock_db = mocker.MagicMock()
    mocker.patch("src.database.db_ops.ban_url_db.DBHelper", mock_db)
    # mock_db.save_data.return_value = True
    # mock_db.fetch_data.return_value = False
    # mock_db.delete_data.return_value = True
    # mock_db.display_data.return_value = True
    return mock_db


def test_save_ban_url(mocker, mock_db_helper):
    mock_short_uuid = mocker.MagicMock()
    mocker.patch("src.database.db_ops.ban_url_db.ShortUUID", mock_short_uuid)
    mocker.patch(
        "src.database.db_ops.ban_url_db.BannedUrlTable.query_insert_ban_url", "lol"
    )
    mock_short_uuid().random.return_value = "1234"
    mocker.patch.object(BanUrlDB, "fetch_ban_url", return_value=False)
    ban_url_db = BanUrlDB()
    ban_url_db.save_ban_url("U1", "Malware", "High")
    mock_db_helper.save_data.assert_called_once_with(
        "lol", ("B1234", "U1", "Malware", "High")
    )


def test_fetch_ban_url(mocker, mock_db_helper):
    mock_db_helper.fetch_data.return_value = True
    ban_url_db = BanUrlDB()
    res = ban_url_db.fetch_ban_url("U1")
    assert res == True


def test_delete_ban_url(mocker, mock_db_helper):
    # mock_db_helper.delete_data.return_value = True
    mocker.patch("src.database.db_ops.ban_url_db.BannedUrlTable.query_unban_url", "lol")
    ban_url_db = BanUrlDB()
    res = ban_url_db.delete_ban_url("U1")
    mock_db_helper.delete_data.assert_called_once_with("lol", ("U1",))


def test_view_ban_url(mocker, mock_db_helper):
    # mock_db_helper.delete_data.return_value = True
    mocker.patch(
        "src.database.db_ops.ban_url_db.BannedUrlTable.query_select_ban_url", "lol"
    )
    ban_url_db = BanUrlDB()
    res = ban_url_db.view_ban_url("U1")
    mock_db_helper.display_data.assert_called_once_with(
        "lol", ["URL ID", "Category", "Severity"], ("U1",)
    )


def test_check_ban_url(mocker, mock_db_helper):
    mock_db_helper.fetch_data.return_value = True
    ban_url_db = BanUrlDB()
    res = ban_url_db.check_ban_url("U1")
    assert res == True


def test_view_all_ban_urls(mocker, mock_db_helper):
    # mock_db_helper.delete_data.return_value = True
    mocker.patch(
        "src.database.db_ops.ban_url_db.BannedUrlTable.query_select_all_ban_url", "lol"
    )
    ban_url_db = BanUrlDB()
    ban_url_db.view_all_ban_urls()
    mock_db_helper.display_data.assert_called_once_with(
        "lol", ["URL ID", "Category", "Severity"]
    )
