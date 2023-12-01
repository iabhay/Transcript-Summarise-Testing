import logging
from utils.input_validator import url_validation
from service_handler.transcript_handler.transcript_generator import transcriptor
from service_handler.content_checker.content_check import ContentChecker
from database.db_ops.ban_url_db import BanUrlDB
from database.db_ops.searches_db import SearchesDB
from database.db_ops.history_db import HistoryDB
from database.db_ops.premium_listing_db import PremiumListingsDB
from service_handler.summary_handler.sum_gen import SummaryGenerator
from config.config import Config
# from utils.dicts import SubmittedVideo
from config.log_config.log_config import LogStatements
logger = logging.getLogger('video_service')


class VideoService:
    def __init__(self, uid):
        self.uid = uid
        self.transcript_obj = transcriptor()
        self.content_check_obj = ContentChecker()
        self.ban_url_obj = BanUrlDB()
        self.search_count_db = SearchesDB(self.uid)
        self.summary = ""
        self.summary_obj = SummaryGenerator()
        self.urlid = ""
        self.history_obj = HistoryDB(self.uid)
        self.transcript = ""
        # self.submit_obj = SubmittedVideo(uid)
        # self.submit_menu = self.submit_obj.submit_menu()

    def submit_video(self):
        ask = input(Config.SUBMIT_VIDEO_PROMPT)
        ask = ask.strip()
        # saving this search to history of that user
        if ask != "1":
            if url_validation(ask):
                hid = self.history_obj.save_history(ask)
                print(Config.PROCESSING_PROMPT)
                self.urlid = self.transcript_obj.extract_video_id(ask)

                # checking if url is already banned
                valid = self.ban_url_obj.fetch_ban_url(self.urlid)

                # checking if url is premium listed
                premium_list_obj = PremiumListingsDB(self.uid)
                check_premium_lisiting = premium_list_obj.check_premium_list_url(self.urlid)

                if valid and (len(check_premium_lisiting) == 0):
                    print("Already Banned Url")
                

                else:
                    # transcript generated
                    transcript = self.transcript_obj.format_transcript(self.urlid)
                    # summary generated from transcript
                    summary = self.summary_obj.summary_generator(transcript)
                    if transcript and summary:
                        # if premium listed then no need of content checking
                        if len(check_premium_lisiting) == 0:
                            # Content checking using API and categorising
                            content_check = self.content_check_obj.analyze_text(transcript)
                            if content_check:
                                for key, value in content_check.items():
                                    if content_check[key] > 0:
                                        print("Url is banned.")
                                        # banning url
                                        self.ban_url_obj.save_ban_url(self.urlid, key, value)

                                        # checking if ban searches limit exceeded, if yes then instant logout
                                        if self.search_count_db.update_user_search_count(3) == False:
                                            print("You have exhausted ban search limits in a day.\nYOU ARE BANNED. "
                                                  "PLEASE CONTACT ADMIN!!")
                                            return False
                                        return True
                        self.submitted_video_module(transcript, summary, hid)
                    else:
                        print("This video is not supported. Please try other videos.")
            else:
                print("Enter valid url")
        return True

    def submitted_video_module(self, transcript, summary, hid):
        while True:
            try:
                ask = int(input(Config.AFTER_SUBMITTING_URL_PROMPT))
                if ask == int(Config.AFTER_SUBMITTING_URL_PROMPT_LENGTH):
                    print(Config.EXITING_PROMPT)
                    break
                if ask == 1:
                    self.save_summary(summary, hid)
                elif ask == 2:
                    self.save_transcript(transcript, hid)
                elif ask == 3:
                    self.show_video_details(transcript, summary, hid)
                else:
                    print(Config.INVALID_INPUT_PROMPT)
            except ValueError:
                print("Enter Numbers only")

    def save_summary(self, summary, hid):
        with open(f"downloadable_results/summary_outputs/{hid}_summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)
        logger.info(LogStatements.summary_generated)
        print(f"Summary File Generated with id - {hid}")

    def save_transcript(self, transcript, hid):
        with open(f"downloadable_results/transcript_outputs/{hid}_transcript.txt", "w", encoding="utf-8") as f:
            f.write(transcript)
        logger.info(LogStatements.transcript_generated)
        print(f"Transcript File Generated with id - {hid}")

    def show_video_details(self, transcript, summary, hid):
        read_transcript = transcript
        read_summary = summary
        transcript_word = read_transcript.split()
        summary_word = read_summary.split()
        print(f"Video URLID - {hid}\nTranscript Length - {len(transcript_word)}\nSummary Length - {len(summary_word)}")