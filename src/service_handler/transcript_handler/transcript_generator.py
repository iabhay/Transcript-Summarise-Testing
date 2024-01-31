import logging
from youtube_transcript_api import YouTubeTranscriptApi
import textwrap

logger = logging.getLogger(__name__)


class transcriptor:
    def extract_video_id(self, video_url):
        """
        a youtube video id is 11 characters long
        if the video id is longer than that, then it's a url
        """
        if len(video_url) > 11:
            """
            it's a url
            the video id is the last 11 characters
            """
            return video_url[-11:]
        else:
            # it's a video id
            return video_url

    def get_transcript(self, video_id):
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            return transcript
        except Exception as e:
            return None

    def format_transcript(self, video_id):
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
