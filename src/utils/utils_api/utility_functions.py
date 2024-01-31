def extract_video_id(self, video_url):
    # a youtube video id is 11 characters long
    # if the video id is longer than that, then it's a url
    if len(video_url) > 11:
        # it's a url
        # the video id is the last 11 characters
        return video_url[-11:]
    else:
        # it's a video id
        return video_url
