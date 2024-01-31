import pytest
from src.database.db_ops.premium_listing_db import PremiumListingsDB

@pytest.fixture(autouse=True)
def mock_db_helper(mocker):
    mock_db = mocker.MagicMock()
    mocker.patch('src.database.db_ops.premium_listing_db.DBHelper', mock_db)
    # mock_db.save_data.return_value = True
    # mock_db.fetch_data.return_value = False
    # mock_db.delete_data.return_value = True
    # mock_db.display_data.return_value = True
    return mock_db

@pytest.fixture(autouse=True)
def mock_date(mocker):
    mock_dt = mocker.MagicMock()
    mocker.patch('src.database.db_ops.premium_listing_db.datetime', mock_dt)
    mock_tm = mocker.MagicMock()
    mock_dt.now.return_value = mock_tm
    mock_tm.strftime.return_value = "01/01/2021 00:00:00"
    return mock_dt

def test_save_premium_url(mocker, mock_db_helper):
    mock_short_uuid = mocker.MagicMock()
    mocker.patch('src.database.db_ops.premium_listing_db.ShortUUID', mock_short_uuid)
    mocker.patch('src.database.db_ops.premium_listing_db.PremiumListingTable.query_insert_premium_listing', "lol")
    mock_short_uuid().random.return_value = '1234'
    mocker.patch.object(PremiumListingsDB, 'check_premium_list_url', return_value=False)
    premium_listing_db = PremiumListingsDB("U1")
    premium_listing_db.save_premium_url("U1")
    mock_db_helper.save_data.assert_called_once_with("lol", ('P1234', '01/01/2021 00:00:00', 'U1', 'U1'))

def test_check_premium_list_url(mocker, mock_db_helper):
    mocker.patch('src.database.db_ops.premium_listing_db.PremiumListingTable.query_select_premium_url_for_user', "lol")
    premium_listing_db = PremiumListingsDB("U1")
    premium_listing_db.check_premium_list_url("U1")
    mock_db_helper.fetch_data.assert_called_once_with("lol", ('U1', 'U1'))

def test_view_premium_user_listing(mocker, mock_db_helper):
    mocker.patch('src.database.db_ops.premium_listing_db.PremiumListingTable.query_select_premium_listing', "lol")
    premium_listing_db = PremiumListingsDB("U1")
    premium_listing_db.view_premium_user_listing()
    mock_db_helper.display_data.assert_called_once_with("lol", ['Date', 'Username', 'Url'], ('U1', ))

def test_view_all_premium_listings(mocker, mock_db_helper):
    mocker.patch('src.database.db_ops.premium_listing_db.PremiumListingTable.query_select_all_premium_listing', "lol")
    premium_listing_db = PremiumListingsDB("U1")
    premium_listing_db.view_all_premium_listings()
    mock_db_helper.display_data.assert_called_once_with("lol", ['Date', 'Username', 'Url'])

def test_remove_premium_listing(mocker, mock_db_helper):
    mocker.patch('src.database.db_ops.premium_listing_db.PremiumListingTable.query_delete_premium_listing', "lol")
    premium_listing_db = PremiumListingsDB("U1")
    premium_listing_db.remove_premium_listing("U1")
    mock_db_helper.delete_data.assert_called_once_with("lol", ('U1', ))