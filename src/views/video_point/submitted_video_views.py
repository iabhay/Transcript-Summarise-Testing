"""Module for views of Video Service functionalities."""

from business_logic.submittedvideo.video_service import VideoService
from config.config import Config
from utils.input_validator import url_validation


class VideoView:
    """
    Class for showing views of Video Service functionalities.
    ...
    Methods:
    -------
    Constructor() -> Setting Uid and Reation of object of Video Service.
    submit_video() -> method for showing menu of bideo service functionalities.
    submitted_video_module() -> method for showing views of post summary generation of fucntionalities.
    """

    def __init__(self, uid: str) -> None:
        """
        Constructor method to create object of Video Service
        Parameter -> uid: str
        Return Type -> None
        """
        self.uid = uid
        self.video_service = VideoService(uid)

    def submit_video(self):
        """
        Method to show views of functionalities of video service
        Parameter -> self
        Return Type -> bool
        """
        user_url = input(Config.SUBMIT_VIDEO_PROMPT)
        user_url = user_url.strip()
        if user_url == "1":
            return True
        if url_validation(user_url):
            print(Config.PROCESSING_PROMPT)
            res = self.video_service.submit_video(user_url)
            if res is None:
                print(Config.ALREADY_BANNED_URL)
                return True
            elif res is False:
                print(Config.VIDEO_NOT_SUPPORTED)
                return True
            elif res:
                if type(res) is not tuple:
                    if res["status"] == "ban":
                        print(Config.EXHAUSTED_BAN)
                        return False
                    else:
                        print(Config.BANNED_CONTENT)
                        return True
                else:
                    self.submitted_video_module(res[0], res[1], res[2])
                    return True
        else:
            print(Config.VALID_URL)
            return True

    def submitted_video_module(self, transcript, summary, hid):
        """
        Method to show views of functionalities of post summary generation feature
        Parameter -> transcript: str, summary: str, hid: str
        Return Type -> None
        """
        while True:
            try:
                ask = int(input(Config.AFTER_SUBMITTING_URL_PROMPT))
                if ask == int(Config.AFTER_SUBMITTING_URL_PROMPT_LENGTH):
                    print(Config.EXITING_PROMPT)
                    break
                if ask == 1:
                    self.video_service.save_summary(summary, hid)
                elif ask == 2:
                    self.video_service.save_transcript(transcript, hid)
                elif ask == 3:
                    self.video_service.show_video_details(transcript, summary, hid)
                else:
                    print(Config.INVALID_INPUT_PROMPT)
            except ValueError:
                print(Config.NUMBERS_ONLY_PROMPT)
