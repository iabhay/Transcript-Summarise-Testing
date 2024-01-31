from business_logic.submittedvideo.video_service import VideoService
from utils.exception_handler import custom_error_handler
from flask import jsonify


class SummaryController:
    def __init__(self, uid) -> None:
        self.video_service = VideoService(uid)

    @custom_error_handler
    def submit_video(self, youtube_url):
        response = self.video_service.submit_video(youtube_url)
        response["youtube_url"] = youtube_url["youtube_url"]
        if "transcript" not in response.keys():
            response["message"] = "Bad Content Found"
        return jsonify(response)
