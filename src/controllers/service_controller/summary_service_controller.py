"""
Summary controller extracts useful data from request and sent to video service logic.
If transcript not generated then Bad Content error response is sent to user.
"""

from business_logic.submittedvideo.video_service import VideoService
from utils.exception_handler import custom_error_handler
from flask import jsonify
from config.api_config import ApiConfig


class SummaryController:
    """
    Class for defining Login Controller
    ...
    Methods:
    -------
    Constructor() -> Method to Initialisation of Video Service Logic
    verify_user() -> Method to give video url to logic for generating summary
    """

    def __init__(self, uid) -> None:
        self.video_service = VideoService(uid)

    @custom_error_handler
    def submit_video(self, youtube_url):
        """
        Method extracting youtube_url from request body data and giving it to logic
        Parameter -> youtube_url: dict
        Return Type -> json
        """
        yt_url = youtube_url["youtube_url"]
        response = self.video_service.submit_video(yt_url)
        response["youtube_url"] = yt_url
        if "transcript" not in response.keys():
            response["message"] = ApiConfig.BAD_CONTENT_FOUND
        return jsonify(response)
