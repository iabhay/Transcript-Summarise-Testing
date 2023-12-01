import re
from database.database_query import UsersTableQuery, UserSearchesTableQuery, MessageTableQuery,HistoryTableQuery, PremiumListingTable,BannedUrlTable
from database.db_ops.db_helper import DBHelper

def password_validation(password):
    pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,20}$"
    answer = re.match(pattern, password)
    if answer:
        return True
    else:
        return False

def pattern_ret():
    return "^([A-z0-9@_\-\.]{4,20})"

def username_validation(username):
    # pattern = "^([A-z0-9@_\-\.]{4,20})"
    pattern = pattern_ret()
    answer = re.match(pattern, username)
    if answer:
        return True
    else:
        return False

def url_validation(url):
    pattern = "(https:\/\/)?(www.)?youtube.(com)\/watch\?v=[a-zA-Z0-9\-\_]{11}"
    answer = re.match(pattern, url)
    if answer:
        return True
    else:
        return False
