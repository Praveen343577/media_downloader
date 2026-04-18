import json
import time
import random
from typing import Any

class Delayer:
    def __init__(self, tracker: Any) -> None:
        self.tracker = tracker
        self.counters: dict[str, int] = {"Youtube": 0, "Instagram": 0, "Twitter": 0, "Pinterest": 0}
        with open("config/settings.json", "r") as f:
            self.settings = json.load(f)["delays"]

    def delay(self, platform: str) -> None:
        self.counters[platform] += 1
        cfg = self.settings[platform]
        
        if self.counters[platform] % cfg["macro_interval"] == 0:
            duration = random.uniform(cfg["macro_min"], cfg["macro_max"])
        else:
            duration = random.uniform(cfg["micro_min"], cfg["micro_max"])
            
        self._sleep_with_countdown(duration)

    def _sleep_with_countdown(self, seconds: float) -> None:
        end_time = time.time() + seconds
        while True:
            remaining = end_time - time.time()
            if remaining <= 0:
                self.tracker.update(cooldown="[00:00]")
                break
            mins, secs = divmod(int(remaining), 60)
            self.tracker.update(cooldown=f"[{mins:02d}:{secs:02d}]")
            time.sleep(1)