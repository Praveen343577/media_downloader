import re
from typing import Any
from src.downloaders.ytdlp_api import YTDLPApi
from src.downloaders.gallerydl_sub import GalleryDLSub
from src.utils import RateLimitAbortException

class Router:
    def __init__(self, tracker: Any, file_manager: Any) -> None:
        self.ytdlp = YTDLPApi(tracker, file_manager)
        self.gallerydl = GalleryDLSub(tracker, file_manager)
        
        self.regexes = {
            "Youtube": re.compile(r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.*"),
            "Instagram": re.compile(r"^(https?://)?(www\.)?instagram\.com/.*"),
            "Twitter": re.compile(r"^(https?://)?(www\.)?(twitter\.com|x\.com)/.*"),
            "Pinterest": re.compile(r"^(https?://)?(www\.)?pinterest\.com/.*")
        }

    def process(self, url: str, platform: str) -> None:
        if not self.regexes[platform].match(url):
            raise Exception("Domain Regex Validation Failed")

        if platform == "Youtube":
            self.ytdlp.download(url)
        else:
            self.gallerydl.download(url, platform)