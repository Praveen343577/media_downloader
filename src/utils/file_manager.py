import os
import datetime
from dotenv import load_dotenv

load_dotenv()

class FileManager:
    def __init__(self) -> None:
        self.target_dir: str = os.getenv("TARGET_DOWNLOAD_DIR", "./downloads")
        self.platforms: list[str] = ["Youtube", "Instagram", "Twitter", "Pinterest"]
        self._ensure_base_dirs()

    def _ensure_base_dirs(self) -> None:
        for platform in self.platforms:
            os.makedirs(os.path.join(self.target_dir, platform), exist_ok=True)

    def get_platform_base_path(self, platform: str) -> str:
        if platform not in self.platforms:
            raise ValueError(f"Invalid platform: {platform}")
        
        if platform == "Youtube":
            return os.path.join(self.target_dir, platform)
            
        date_str = datetime.datetime.now().strftime("%Y_%m_%d")
        path = os.path.join(self.target_dir, platform, date_str)
        os.makedirs(path, exist_ok=True)
        return path

    def get_cookie_path(self) -> str:
        cookie_path = os.path.abspath(os.path.join("config", "cookies.txt"))
        if not os.path.exists(cookie_path):
            raise FileNotFoundError(f"Missing strictly required cookies at: {cookie_path}")
        return cookie_path