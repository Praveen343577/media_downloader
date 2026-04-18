import yt_dlp
import os
import re
from typing import Any
from src.utils import RateLimitAbortException
from src.utils.post_processor import PostProcessor

class YTDLPApi:
    def __init__(self, tracker: Any, file_manager: Any) -> None:
        self.tracker = tracker
        self.fm = file_manager
        self.cookie_path = self.fm.get_cookie_path()

    def progress_hook(self, d: dict) -> None:
        if d['status'] == 'downloading':
            speed = d.get('speed', 0)
            if speed:
                self.tracker.update(speed=f"[{speed / 1024 / 1024:.1f} MiB/s]")
                
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            if total_bytes:
                self.tracker.update(active_size=f"[{total_bytes / 1024 / 1024:.1f} MB]")

        elif d['status'] == 'finished':
            total_bytes = d.get('total_bytes', 0)
            if total_bytes:
                self.tracker.add_payload(total_bytes / 1024 / 1024)

    def _truncate_title(self, title: str) -> str:
        if len(title) <= 100:
            return title
        trunc = title[:100]
        last_space = trunc.rfind(' ')
        return trunc[:last_space] if last_space != -1 else trunc

    def download(self, url: str) -> None:
        base_path = self.fm.get_platform_base_path("Youtube")
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mkv',
            'writethumbnail': True,
            'writeinfojson': True,
            'cookiefile': self.cookie_path,
            'outtmpl': os.path.join(base_path, '%(uploader)s', '%(title).100s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'no_warnings': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info:
                    raise Exception("Failed to extract info")
                
                clean_title = self._truncate_title(info.get('title', 'Unknown'))
                self.tracker.update(target=f"[{clean_title[:38]}]")
                
                ydl.download([url])
                
                channel = info.get('uploader', 'Unknown')
                video_id = info.get('id', '')
                channel_path = os.path.join(base_path, channel)
                PostProcessor.relocate_youtube_metadata(channel_path, video_id)
                
        except yt_dlp.utils.DownloadError as e:
            err_msg = str(e).lower()
            if any(code in err_msg for code in ["429", "401", "403", "rate-limit"]):
                raise RateLimitAbortException("YouTube Rate Limit / Auth Error")
            raise Exception(str(e))