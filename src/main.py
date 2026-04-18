import os
import sys
from src.utils.file_manager import FileManager
from src.utils.logger import Logger
from src.utils.delayer import Delayer
from src.utils import RateLimitAbortException
from src.tracker import Tracker
from src.parser import Parser
from src.router import Router

def main() -> None:
    try:
        fm = FileManager()
    except Exception as e:
        print(f"\nInitialization Error: {e}")
        sys.exit(1)

    tracker = Tracker()
    logger = Logger(fm)
    delayer = Delayer(tracker)
    router = Router(tracker, fm)

    platforms = ["Youtube", "Instagram", "Twitter", "Pinterest"]

    for platform in platforms:
        urls = Parser.get_links(platform)
        if not urls:
            continue

        total = len(urls)
        tracker.reset_queue(total, platform)

        for idx, url in enumerate(urls, 1):
            tracker.update(retry="")
            
            try:
                router.process(url, platform)
                tracker.increment_success(idx, total)
                logger.log_success(platform, url)
                
            except RateLimitAbortException:
                tracker.update(target="[FATAL RATE LIMIT ABORT]")
                logger.log_failure(platform, url, "RateLimitAbortException")
                tracker.increment_fail(idx, total)
                break 
                
            except Exception as e:
                tracker.increment_fail(idx, total)
                logger.log_failure(platform, url, str(e))
                
            if idx < total:
                delayer.delay(platform)

    print("\nExecution Completed.")

if __name__ == "__main__":
    main()