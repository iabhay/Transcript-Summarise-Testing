class CreateTablesQuery:
    query_create_user = "CREATE TABLE IF NOT EXISTS USERS (uid VARCHAR(10) PRIMARY KEY, created_at VARCHAR(30), username VARCHAR(50) UNIQUE, password VARCHAR(150), role VARCHAR(30) DEFAULT 'nonpremiumuser', ban_status VARCHAR(40) DEFAULT 'unbanned')"
    query_create_user_search = "CREATE TABLE IF NOT EXISTS SEARCHES (sid VARCHAR(10) PRIMARY KEY, date_time VARCHAR(30), uid VARCHAR(10) , search_count INTEGER DEFAULT 0, FOREIGN KEY(uid) REFERENCES USERS(uid) ON DELETE CASCADE)"
    query_create_message = "CREATE TABLE IF NOT EXISTS MESSAGES (mid VARCHAR(10) PRIMARY KEY, date_time VARCHAR(30), uid VARCHAR(10), description VARCHAR(256), FOREIGN KEY(uid) REFERENCES USERS(uid) ON DELETE CASCADE)"
    query_create_history = "CREATE TABLE IF NOT EXISTS HISTORY (hid VARCHAR(10) PRIMARY KEY, date_time VARCHAR(30), uid VARCHAR(10), url_id VARCHAR(70), FOREIGN KEY(uid) REFERENCES USERS(uid) ON DELETE CASCADE)"
    query_create_premium_listing = "CREATE TABLE IF NOT EXISTS PREMIUMLISTINGS (pid VARCHAR(10) PRIMARY KEY, date_time VARCHAR(30), uid VARCHAR(10), url_id VARCHAR(70), FOREIGN KEY(uid) REFERENCES USERS(uid) ON DELETE CASCADE)"
    query_create_ban_url = "CREATE TABLE IF NOT EXISTS BANNEDURL (bid VARCHAR(10) PRIMARY KEY, url_id VARCHAR(70) UNIQUE, category VARCHAR(40), severity_level INTEGER)"
    query_create_blocklist = "CREATE TABLE IF NOT EXISTS BLOCKLIST (access_token VARCHAR(600) PRIMARY KEY, refresh_token VARCHAR(600) NOT NULL, uid VARCHAR(15), status VARCHAR(20) DEFAULT 'issued', FOREIGN KEY(uid) REFERENCES USERS(uid) ON DELETE CASCADE)"

class BlocklistQuery:
    INSERT_TOKEN = "INSERT INTO BLOCKLIST(uid, access_token, refresh_token) VALUES(%s, %s, %s)"
    REVOKE_TOKEN = "UPDATE BLOCKLIST SET status = 'revoked' WHERE uid = %s"
    FETCH_TOKEN_STATUS = "SELECT status FROM BLOCKLIST WHERE {} = %s"
    FETCH_REFRESH_TOKEN = "SELECT refresh_token FROM BLOCKLIST WHERE uid = %s and status = %s"
    FETCH_ACCESS_TOKEN = "SELECT access_token FROM BLOCKLIST WHERE uid = %s and status = %s"

class UsersTableQuery:
    query_insert_user = "INSERT INTO USERS (uid, created_at, username, password) VALUES (%s, %s, %s, %s)"
    query_select_user = "SELECT * FROM USERS WHERE username=%s AND password=%s"
    query_select_user_by_admin = "SELECT * FROM USERS WHERE username=%s"
    query_select_all_user = "SELECT * FROM USERS"
    query_update_user_role = "UPDATE USERS SET role=%s where uid=%s"
    query_update_user_ban_status = "UPDATE USERS SET ban_status=%s where uid=%s"
    query_select_user_by_uid = (
        "SELECT username, role, ban_status from USERS WHERE uid=%s"
    )


class UserSearchesTableQuery:
    query_update_user_search_count = "UPDATE SEARCHES SET search_count=%s WHERE uid=%s "
    query_insert_user_search = (
        "INSERT INTO SEARCHES (sid, date_time, uid) VALUES (%s, %s, %s)"
    )
    query_select_user_search = (
        "SELECT USERS.created_at, USERS.username, SEARCHES.search_count, SEARCHES.date_time, "
        "USERS.ban_status FROM USERS INNER JOIN SEARCHES ON USERS.uid = SEARCHES.uid WHERE "
        "USERS.uid=%s"
    )
    query_update_day_wise = (
        "UPDATE SEARCHES SET (date_time, search_count) VALUES = (%s, %s)"
    )
    quer_select_all_user_search = (
        "SELECT USERS.created_at, USERS.username, SEARCHES.search_count, "
        "SEARCHES.date_time, USERS.ban_status FROM USERS INNER JOIN SEARCHES ON USERS.uid"
        " = SEARCHES.uid"
    )


class MessageTableQuery:
    query_insert_message = "INSERT INTO MESSAGES (mid, date_time, uid, description) VALUES (%s, %s , %s , %s)"
    query_select_message = "SELECT MESSAGES.mid, MESSAGES.date_time, USERS.username, MESSAGES.description FROM USERS INNER JOIN MESSAGES ON USERS.uid = MESSAGES.uid WHERE USERS.uid=%s"
    query_delete_message = "DELETE FROM MESSAGES INNER JOIN USERS ON USERS.uid=MESSAGES.uid WHERE USERS.uid=%s"
    query_select_premium_message = 'SELECT MESSAGES.mid, MESSAGES.date_time, USERS.username, MESSAGES.description FROM USERS INNER JOIN MESSAGES ON USERS.uid = MESSAGES.uid WHERE USERS.role="premiumuser"'
    query_select_non_premium_message = 'SELECT MESSAGES.mid, MESSAGES.date_time, USERS.username, MESSAGES.description FROM USERS INNER JOIN MESSAGES ON USERS.uid = MESSAGES.uid WHERE USERS.role="nonpremiumuser"'
    query_select_all_messages = "SELECT MESSAGES.mid, MESSAGES.date_time, USERS.username, MESSAGES.description FROM USERS INNER JOIN MESSAGES ON USERS.uid = MESSAGES.uid"


class HistoryTableQuery:
    query_insert_history = (
        "INSERT INTO HISTORY (hid, date_time, uid, url_id) VALUES (%s, %s, %s, %s)"
    )
    query_select_history = "SELECT hid, date_time, url_id FROM HISTORY WHERE uid=%s"
    query_select_all_history = "SELECT HISTORY.hid, HISTORY.date_time, USERS.username, HISTORY.url_id FROM HISTORY INNER JOIN USERS ON USERS.uid=HISTORY.uid"


class PremiumListingTable:
    query_insert_premium_listing = "INSERT INTO PREMIUMLISTINGS (pid, date_time, uid, url_id) VALUES (%s, %s, %s, %s)"
    query_select_premium_listing = "SELECT PREMIUMLISTINGS.pid, PREMIUMLISTINGS.date_time, USERS.username, PREMIUMLISTINGS.url_id FROM USERS INNER JOIN PREMIUMLISTINGS ON USERS.uid = PREMIUMLISTINGS.uid WHERE USERS.uid=%s"
    query_select_premium_listing_by_admin = "SELECT PREMIUMLISTINGS.pid, PREMIUMLISTINGS.date_time, USERS.username, PREMIUMLISTINGS.url_id FROM USERS INNER JOIN PREMIUMLISTINGS ON USERS.uid = PREMIUMLISTINGS.uid WHERE USERS.uid=%s"
    query_delete_premium_listing = "DELETE FROM PREMIUMLISTINGS WHERE uid=%s"
    query_select_all_premium_listing = "SELECT PREMIUMLISTINGS.pid, PREMIUMLISTINGS.date_time, USERS.username, PREMIUMLISTINGS.url_id FROM PREMIUMLISTINGS INNER JOIN USERS ON USERS.uid=PREMIUMLISTINGS.uid"
    query_select_premium_url_for_user = (
        "SELECT * FROM PREMIUMLISTINGS WHERE url_id=%s and uid=%s"
    )


class BannedUrlTable:
    query_insert_ban_url = "INSERT INTO BANNEDURL (bid, url_id, category, severity_level) VALUES (%s, %s, %s, %s)"
    query_unban_url = "DELETE FROM BANNEDURL WHERE url_id=%s"
    query_select_ban_url = (
        "SELECT bid, url_id, category, severity_level FROM BANNEDURL WHERE url_id=%s"
    )
    query_select_all_ban_url = (
        "SELECT bid, url_id, category, severity_level FROM BANNEDURL"
    )


class AdminQueries:
    query_view_user = "SELECT USERS.uid,USERS.username, USERS.created_at, USERS.role, USERS.ban_status, SEARCHES.date_time, SEARCHES.search_count FROM USERS INNER JOIN SEARCHES ON USERS.uid=SEARCHES.uid WHERE USERS.uid=%s"
    query_view_all_users = "SELECT USERS.uid,USERS.username, USERS.created_at, USERS.role, USERS.ban_status, SEARCHES.date_time, SEARCHES.search_count FROM USERS INNER JOIN SEARCHES ON USERS.uid = SEARCHES.uid"
