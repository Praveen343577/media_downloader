import subprocess
import os
import re
from typing import Any
from src.utils import RateLimitAbortException

class GalleryDLSub:
    def __init__(self, tracker: Any, file_manager: Any) -> None:
        self.tracker = tracker
        self.fm = file_manager
        self.cookie_path = self.fm.get_cookie_path()

    def download(self, url: str, platform: str) -> None:
        self.tracker.update(target=f"[{url[:38]}]", speed="[N/A]", active_size="[N/A]")
        base_path = self.fm.get_platform_base_path(platform)
        
        cmd = [
            "gallery-dl",
            "--cookies", self.cookie_path,
            "-d", base_path,
            "--write-metadata",
            "--directory-depth", "0"
        ]

        if platform == "Twitter":
            cmd.extend(["-o", "twitter:videos=true", "-o", "twitter:images=true"])
            
        cmd.append(url)

        try:
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8"
            )

            file_count = 0
            for line in iter(process.stdout.readline, ''):
                line_lower = line.lower()
                if any(err in line_lower for err in ["http error 429", "http error 403", "http error 401"]):
                    process.kill()
                    raise RateLimitAbortException(f"{platform} Rate Limit / Auth Error")
                
                if line.startswith("#"):
                    file_count += 1
                    self.tracker.update(speed=f"[Files: {file_count}]")

            process.wait()
            if process.returncode != 0 and process.returncode != 1:
                raise Exception(f"Gallery-dl exited with code {process.returncode}")

        except RateLimitAbortException:
            raise
        except Exception as e:
            raise Exception(str(e))