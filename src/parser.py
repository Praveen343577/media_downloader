import os

class Parser:
    @staticmethod
    def get_links(platform: str) -> list[str]:
        path = os.path.join("input_links", f"{platform}.txt")
        if not os.path.exists(path):
            return []
            
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        return lines