"""
Video Service Logic -> 
1. History is saved on using service.
2. If banned url and non premium user -> Content not generation response
3. If banned url but premium listed for user -> then summary generated without content checking
4. If fresh url then transcript generated and then checked for the content ->
5. If content checked found bad then Bad Content Response.
6. Otherwise, Summary is given in response.
"""

import logging
from shortuuid import ShortUUID
from datetime import datetime
from service_handler.transcript_handler.transcript_generator import transcriptor
from service_handler.content_checker.content_check import ContentChecker
from service_handler.summary_handler.sum_gen import SummaryGenerator
from utils.custom_exception import BannedUrl, ContentNotGenerated, DBException
from config.config import Config
from config.api_config import ApiConfig
from database.mysql_database import db
from database.database_query import (
    PremiumListingTable,
    HistoryTableQuery,
    BannedUrlTable,
    UserSearchesTableQuery,
    UsersTableQuery,
)


logger = logging.getLogger(__name__)


class VideoService:
    """
    Class for defining VideoService Logic
    ...
    Methods:
    -------
    Constructor() -> fetching current date time and initialising transcriptor, content checker, summary generator
    add_user() -> adding new user in application.
    submit_video() -> Summary and Transcript generation logic and content checking
    content_checker() -> checking content and taking decisions of banning user if user exceeded banned search count
    update_user_search_count() -> updating user search count if url is banned
    """

    def __init__(self, uid) -> None:
        self.uid = uid
        self.transcript_obj = transcriptor()
        self.content_check_obj = ContentChecker()
        self.summary_obj = SummaryGenerator()
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def submit_video(self, user_url: str) -> dict:
        """
        Method generate summary from url and check if content is right to show. Also, if content is bad then check if premiumlisted then show to user.
        Parameter -> user_url: str
        Return Type -> dict
        Exceptions Type -> Internal Server Error
        """
        try:
            hid = "H" + ShortUUID(Config.SHORT_UUID_CONSTRAINTS).random(length=4)
            db.save_data(
                HistoryTableQuery.query_insert_history,
                (hid, self.dt_string, self.uid, user_url),
            )
            self.urlid = self.transcript_obj.extract_video_id(user_url)

            # checking if url is already banned
            is_banned_url = db.fetch_data(
                BannedUrlTable.query_select_ban_url, (user_url,)
            )

            # checking if url is premium listed
            premium_listing = db.fetch_data(
                PremiumListingTable.query_select_premium_url_for_user,
                (
                    user_url,
                    self.uid,
                ),
            )

            """
            if is_banned_url -> banned,
            but premium_listing then gnerate summary
            """

            if is_banned_url:
                if not premium_listing:
                    raise BannedUrl(403, "UnaccessibleResource", ApiConfig.BANNED_URL)

            # transcript generated
            transcript = self.transcript_obj.format_transcript(self.urlid)

            # summary generated from transcript
            summary = self.summary_obj.summary_generator(transcript)

            if transcript and summary:
                # if premium listed then no need of content checking
                if len(premium_listing) == 0:
                    # Content checking using API and categorising
                    content_response = self.content_checker(transcript, user_url)

                    if len(content_response) > 0:
                        return content_response

                return {"transcript": transcript, "summary": summary, "hid": hid}

            else:
                raise ContentNotGenerated(404, ApiConfig.CONTENT_NOT_FETCHED)

        except Exception as err:
            raise DBException(500, Config.VIDEO_NOT_SUPPORTED)

    def content_checker(self, transcript: str, user_url: str) -> dict:
        """
        Method checking content of transcript generated and generating response accordingly
        Parameter -> transcript: str, user_url: str
        Return Type -> dict
        """
        content_check = self.content_check_obj.analyze_text(transcript)

        res = {}
        if content_check:
            for key, value in content_check.items():
                if content_check[key] > 0:
                    res[key] = content_check[key]

                    # banning url
                    bid = "B" + ShortUUID(Config.SHORT_UUID_CONSTRAINTS).random(
                        length=4
                    )
                    db.save_data(
                        BannedUrlTable.query_insert_ban_url, (bid, user_url, key, value)
                    )

                    # checking if ban searches limit exceeded, if yes then instant logout
                    if self.update_user_search_count(3) == False:
                        res["status"] = "ban"
                        return res
                    break
        return res

    def update_user_search_count(self, limit: int) -> bool:
        """
        Method updating user search count if url is banned
        Parameter -> limit: int
        Return Type -> bool
        """
        entry = db.fetch_data(
            UserSearchesTableQuery.query_select_user_search, (self.uid,)
        )
        count = entry[0]["search_count"] + 1
        db.save_data(
            UserSearchesTableQuery.query_update_user_search_count, (count, self.uid)
        )
        if count > limit:
            db.save_data(
                UsersTableQuery.query_update_user_role,
                (Config.BAN_STATUS_FIELD_NAME, self.uid),
            )
            return False
        return True
