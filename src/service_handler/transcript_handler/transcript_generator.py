"""Module for generating transcript."""

import logging
from youtube_transcript_api import YouTubeTranscriptApi
import textwrap

logger = logging.getLogger(__name__)


class transcriptor:
    """
    Class for extracting video id from youtube url and Genrating transcript from YouTubeTranscriptApi Library.
    ...
    Methods:
    -------
    extract_video_id() -> Extract unique video id from youtube url
    get_transcript() -> Transcript generator from YouTubeTranscriptApi
    format_transcript() -> Formatting Transcript generated using TextWrap
    """

    def extract_video_id(self, video_url):
        """
        Method to extract Unique Url id from Youtube link
        a youtube video id is 11 characters long
        Parameter -> video_url: str
        Return Type -> str
        """
        if len(video_url) > 11:
            # the video id is the last 11 characters
            return video_url[-11:]
        else:
            # it's a video id
            return video_url

    def get_transcript(self, video_id):
        """
        Method to generate transcript
        Parameter -> video_id: str
        Return Type -> str
        """
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript
        except Exception as e:
            return None

    def format_transcript(self, video_id):
        """
        Method to format generated transcript
        Parameter -> video_id: str
        Return Type -> str
        """
        res = []
        transcript = self.get_transcript(video_id)
        if transcript:
            formatted_transcript = ""
            wrapper = textwrap.TextWrapper(width=300)
            for entry in transcript:
                wrapped_text = wrapper.fill(text=entry["text"])
                res.append(wrapped_text)
                formatted_transcript += wrapped_text + "\n"
            return formatted_transcript
        return None
