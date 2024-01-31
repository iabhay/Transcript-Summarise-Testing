import logging
from shortuuid import ShortUUID
from datetime import datetime
from service_handler.transcript_handler.transcript_generator import transcriptor
from service_handler.content_checker.content_check import ContentChecker
from service_handler.summary_handler.sum_gen import SummaryGenerator
from utils.custom_exception import BannedUrl, ContentNotGenerated
from config.config import Config
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
    def __init__(self, uid):
        self.uid = uid
        self.transcript_obj = transcriptor()
        self.content_check_obj = ContentChecker()
        self.summary_obj = SummaryGenerator()
        tm = datetime.now()
        self.dt_string = tm.strftime("%d/%m/%Y %H:%M:%S")

    def submit_video(self, user_url):
        user_url = user_url["youtube_url"]
        hid = "H" + ShortUUID(Config.SHORT_UUID_CONSTRAINTS).random(length=4)
        db.save_data(
            HistoryTableQuery.query_insert_history,
            (hid, self.dt_string, self.uid, user_url),
        )
        self.urlid = self.transcript_obj.extract_video_id(user_url)

        # checking if url is already banned
        is_banned_url = db.fetch_data(BannedUrlTable.query_select_ban_url, (user_url,))

        # checking if url is premium listed
        premium_listing = db.fetch_data(
            PremiumListingTable.query_select_premium_url_for_user,
            (
                user_url,
                self.uid,
            ),
        )
        # if is_banned_url -> banned,
        # but premium_listing then gnerate summary
        if len(is_banned_url) > 0:
            if len(premium_listing) == 0:
                raise BannedUrl(403, "UnaccessibleResource", "Already Banned URL.")
                # return None

        # transcript generated
        transcript = self.transcript_obj.format_transcript(self.urlid)
        # summary generated from transcript
        summary = self.summary_obj.summary_generator(transcript)
        if transcript and summary:
            # if premium listed then no need of content checking
            if len(premium_listing) == 0:
                # Content checking using API and categorising
                print(user_url)
                content_response = self.content_checker(transcript, user_url)
                if len(content_response) > 0:
                    # raise BadContent(403, "BadContent", "Content generated but can't be shown.")
                    return content_response
            return {"transcript": transcript, "summary": summary, "hid": hid}
        else:
            raise ContentNotGenerated(
                500, "ContentNotGenerated", "Content not fetched from internal service."
            )
            return False

    def content_checker(self, transcript, user_url):
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

    def update_user_search_count(self, limit):
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
