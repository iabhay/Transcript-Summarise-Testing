import os
import yaml
current_directory = os.path.dirname(__file__)
FPATH = os.path.join(current_directory, 'log_statements.yml')


class LogStatements:
    """
    Maintains all the config variables of the logger
    """

    log_file_location = None

    # authentication logs
    invalid_login_log = None
    starting_application_log = None
    user_exited = None

    # admin
    log_user_downgraded_by_admin = None
    log_user_banned_by_admin = None
    log_user_unbanned_by_admin = None
    log_url_banned_by_admin = None
    log_url_unbanned_by_admin = None
    log_url_premium_listed_by_admin = None

    # database
    log_error_connecting_database = None
    log_connection_to_database = None
    log_exception_message = None

    # non-premium
    url_submitted_by_non_premium = None
    user_upgraded_to_premium = None
    non_premium_user_logout = None

    # premium
    url_submitted_by_premium = None
    user_downgraded_to_non_premium = None
    premium_user_logout = None
    premium_user_language_request = None
    premium_user_premium_listing_request = None

    # submitted-videp
    summary_generated = None
    transcript_generated = None

    # db-ops success
    tables_created = None
    # users
    user_created = None
    user_updated = None
    # searches
    search_count_daily_reset = None
    search_count_updated = None
    # premium_list
    premium_listing_of_url = None
    premium_unlisting_of_url = None
    # messages
    message_sent = None
    message_delete = None
    # history
    user_history_saved = None
    # ban_url
    url_banned = None
    url_unbanned = None

    # db-ops failure
    fail_tables_created = None
    # users
    fail_user_created = None
    fail_user_updated = None
    # searches
    fail_search_count_daily_reset = None
    fail_search_count_updated = None
    # premium_list
    fail_premium_listing_of_url = None
    fail_premium_unlisting_of_url = None
    # messages
    fail_message_sent = None
    fail_message_delete = None
    # history
    fail_user_history_saved = None
    # ban_url
    fail_url_banned = None
    fail_url_unbanned = None

    @classmethod
    def load(cls):
        with open(FPATH, "r") as f:
            data = yaml.safe_load(f)

            cls.log_file_location = data["log_file_location"]

            # authentication logs
            cls.invalid_login_log = data["invalid_login_log"]
            cls.starting_application_log = data["starting_application_log"]
            cls.user_exited = data["user_exited"]

            # admin
            cls.log_user_downgraded_by_admin = data["log_user_downgraded_by_admin"]
            cls.log_user_banned_by_admin = data["log_user_banned_by_admin"]
            cls.log_user_unbanned_by_admin = data["log_user_unbanned_by_admin"]
            cls.log_url_banned_by_admin = data["log_url_banned_by_admin"]
            cls.log_url_unbanned_by_admin = data["log_url_unbanned_by_admin"]
            cls.log_url_premium_listed_by_admin = data[
                "log_url_premium_listed_by_admin"
            ]

            # database
            cls.log_error_connecting_database = data["log_error_connecting_database"]
            cls.log_connection_to_database = data["log_connection_to_database"]
            cls.log_exception_message = data["log_exception_message"]

            # non-premium
            cls.url_submitted_by_non_premium = data["url_submitted_by_non_premium"]
            cls.user_upgraded_to_premium = data["user_upgraded_to_premium"]
            cls.non_premium_user_logout = data["non_premium_user_logout"]

            # premium
            cls.url_submitted_by_premium = data["url_submitted_by_premium"]
            cls.user_downgraded_to_non_premium = data["user_downgraded_to_non_premium"]
            cls.premium_user_logout = data["premium_user_logout"]
            cls.premium_user_language_request = data["premium_user_language_request"]
            cls.premium_user_premium_listing_request = data[
                "premium_user_premium_listing_request"
            ]

            # submitted-videp
            cls.summary_generated = data["summary_generated"]
            cls.transcript_generated = data["transcript_generated"]

            # db-ops success
            cls.tables_created = data["tables_created"]
            # users
            cls.user_created = data["user_created"]
            cls.user_updated = data["user_updated"]
            # searches
            cls.search_count_daily_reset = data["search_count_daily_reset"]
            cls.search_count_updated = data["search_count_updated"]
            # premium_list
            cls.premium_listing_of_url = data["premium_listing_of_url"]
            cls.premium_unlisting_of_url = data["premium_unlisting_of_url"]
            # messages
            cls.message_sent = data["message_sent"]
            cls.message_delete = data["message_delete"]
            # history
            cls.user_history_saved = data["user_history_saved"]
            # ban_url
            cls.url_banned = data["url_banned"]
            cls.url_unbanned = data["url_unbanned"]

            # db-ops failure
            cls.fail_tables_created = data["fail_tables_created"]
            # users
            cls.fail_user_created = data["fail_user_created"]
            cls.fail_user_updated = data["fail_user_updated"]
            # searches
            cls.fail_search_count_daily_reset = data["fail_search_count_daily_reset"]
            cls.fail_search_count_updated = data["fail_search_count_updated"]
            # premium_list
            cls.fail_premium_listing_of_url = data["fail_premium_listing_of_url"]
            cls.fail_premium_unlisting_of_url = data["fail_premium_unlisting_of_url"]
            # messages
            cls.fail_message_sent = data["fail_message_sent"]
            cls.fail_message_delete = data["fail_message_delete"]
            # history
            cls.fail_user_history_saved = data["fail_user_history_saved"]
            # ban_url
            cls.fail_url_banned = data["fail_url_banned"]
            cls.fail_url_unbanned = data["fail_url_unbanned"]
