import os

class Logger:
    def __init__(self, file_manager) -> None:
        self.fm = file_manager

    def log_success(self, platform: str, url: str) -> None:
        self._write_log(platform, "@downloadedLinks.txt", url)

    def log_failure(self, platform: str, url: str, reason: str = "") -> None:
        entry = f"{url} | {reason}" if reason else url
        self._write_log(platform, "@failedLinks.txt", entry)

    def _write_log(self, platform: str, filename: str, content: str) -> None:
        base_path = self.fm.get_platform_base_path(platform)
        if platform != "Youtube":
            base_path = os.path.dirname(base_path)
            
        log_file = os.path.join(base_path, filename)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{content}\n")