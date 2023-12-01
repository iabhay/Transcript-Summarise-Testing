
class CreateTablesQuery:
    query_create_user = 'CREATE TABLE IF NOT EXISTS USERS (uid text PRIMARY KEY, created_at text, username text UNIQUE, password TEXT, role text DEFAULT "nonpremiumuser", ban_status text DEFAULT "unbanned")'
    query_create_user_search = 'CREATE TABLE IF NOT EXISTS SEARCHES (sid text PRIMARY KEY, date_time text, uid text , search_count integer DEFAULT 0, FOREIGN KEY(uid) REFERENCES USERS(uid))'
    query_create_message = 'CREATE TABLE IF NOT EXISTS MESSAGES (mid text PRIMARY KEY, date_time text, uid text, description text, FOREIGN KEY(uid) REFERENCES USERS(uid))'
    query_create_history = 'CREATE TABLE IF NOT EXISTS HISTORY (hid text PRIMARY KEY, date_time text, uid text, url_id text, FOREIGN KEY(uid) REFERENCES USERS(uid))'
    query_create_premium_listing = 'CREATE TABLE IF NOT EXISTS PREMIUMLISTINGS (pid text PRIMARY KEY, date_time text, uid text, url_id text, FOREIGN KEY(uid) REFERENCES USERS(uid))'
    query_create_ban_url = 'CREATE TABLE IF NOT EXISTS BANNEDURL (bid text PRIMARY KEY, url_id text UNIQUE, category text, severity_level integer)'

class UsersTableQuery:
    query_insert_user = 'INSERT INTO USERS (uid, created_at, username, password) VALUES (?, ?, ?, ?)'
    query_select_user = 'SELECT * FROM USERS WHERE username=? AND password=?'
    query_select_user_by_admin = 'SELECT * FROM USERS WHERE username=?'
    query_select_all_user = 'SELECT * FROM USERS'
    query_update_user_role = 'UPDATE USERS SET role=? where uid=?'
    query_update_user_ban_status = 'UPDATE USERS SET ban_status=? where uid=?'
    query_select_user_by_uid = 'SELECT username, role, ban_status from USERS WHERE uid=?'


class UserSearchesTableQuery:
    query_update_user_search_count = 'UPDATE SEARCHES SET search_count=? WHERE uid=? '
    query_insert_user_search = 'INSERT INTO SEARCHES (sid, date_time, uid) VALUES (?, ?, ?)'
    query_select_user_search = ('SELECT USERS.created_at, USERS.username, SEARCHES.search_count, SEARCHES.date_time, '
                                'USERS.ban_status FROM USERS INNER JOIN SEARCHES ON USERS.uid = SEARCHES.uid WHERE '
                                'USERS.uid=?')
    query_update_day_wise = 'UPDATE SEARCHES SET (date_time, search_count) VALUES = (?, ?)'
    quer_select_all_user_search = ('SELECT USERS.created_at, USERS.username, SEARCHES.search_count, '
                                   'SEARCHES.date_time, USERS.ban_status FROM USERS INNER JOIN SEARCHES ON USERS.uid'
                                   ' = SEARCHES.uid')

class MessageTableQuery:
    query_insert_message = 'INSERT INTO MESSAGES (mid, date_time, uid, description) VALUES (?, ? , ? , ?)'
    query_select_message = 'SELECT MESSAGES.date_time, USERS.username, MESSAGES.description FROM USERS INNER JOIN MESSAGES ON USERS.uid = MESSAGES.uid WHERE USERS.uid=?'
    query_delete_message = 'DELETE FROM MESSAGES INNER JOIN USERS ON USERS.uid=MESSAGES.uid WHERE USERS.uid=?'
    query_select_premium_message = 'SELECT MESSAGES.date_time, USERS.username, MESSAGES.description FROM USERS INNER JOIN MESSAGES ON USERS.uid = MESSAGES.uid WHERE USERS.role="premiumuser"'
    query_select_non_premium_message = 'SELECT MESSAGES.date_time, USERS.username, MESSAGES.description FROM USERS INNER JOIN MESSAGES ON USERS.uid = MESSAGES.uid WHERE USERS.role="nonpremiumuser"'
    query_select_all_messages = 'SELECT MESSAGES.date_time, USERS.username, MESSAGES.description FROM USERS INNER JOIN MESSAGES ON USERS.uid = MESSAGES.uid'

class HistoryTableQuery:
    query_insert_history = 'INSERT INTO HISTORY (hid, date_time, uid, url_id) VALUES (?, ?, ?, ?)'
    query_select_history = 'SELECT date_time, url_id FROM HISTORY WHERE uid=?'
    query_select_all_history = 'SELECT HISTORY.date_time, USERS.username, HISTORY.url_id FROM HISTORY INNER JOIN USERS ON USERS.uid=HISTORY.uid'


class PremiumListingTable:
    query_insert_premium_listing = 'INSERT INTO PREMIUMLISTINGS (pid, date_time, uid, url_id) VALUES (?, ?, ?, ?)'
    query_select_premium_listing = 'SELECT PREMIUMLISTINGS.date_time, USERS.username, PREMIUMLISTINGS.url_id FROM USERS INNER JOIN PREMIUMLISTINGS ON USERS.uid = PREMIUMLISTINGS.uid WHERE USERS.uid=?'
    query_select_premium_listing_by_admin = 'SELECT PREMIUMLISTINGS.date_time, USERS.username, PREMIUMLISTINGS.url_id FROM USERS INNER JOIN PREMIUMLISTINGS ON USERS.uid = PREMIUMLISTINGS.uid WHERE USERS.uid=?'
    query_delete_premium_listing = 'DELETE FROM PREMIUMLISTINGS WHERE uid=?'
    query_select_all_premium_listing = 'SELECT PREMIUMLISTINGS.date_time, USERS.username, PREMIUMLISTINGS.url_id FROM PREMIUMLISTINGS INNER JOIN USERS ON USERS.uid=PREMIUMLISTINGS.uid'
    query_select_premium_url_for_user = 'SELECT * FROM PREMIUMLISTINGS WHERE url_id=? and uid=?'

class BannedUrlTable:
    query_insert_ban_url = 'INSERT INTO BANNEDURL (bid, url_id, category, severity_level) VALUES (?, ?, ?, ?)'
    query_unban_url = 'DELETE FROM BANNEDURL WHERE url_id=?'
    query_select_ban_url = 'SELECT url_id, category, severity_level FROM BANNEDURL WHERE url_id=?'
    query_select_all_ban_url = 'SELECT url_id, category, severity_level FROM BANNEDURL'

class AdminQueries:
    query_view_user = 'SELECT USERS.uid,USERS.username, USERS.created_at, USERS.role, USERS.ban_status, SEARCHES.date_time, SEARCHES.search_count FROM USERS INNER JOIN SEARCHES ON USERS.uid=SEARCHES.uid WHERE USERS.uid=?'
    query_view_all_users = 'SELECT USERS.uid,USERS.username, USERS.created_at, USERS.role, USERS.ban_status, SEARCHES.date_time, SEARCHES.search_count FROM USERS INNER JOIN SEARCHES ON USERS.uid = SEARCHES.uid'


