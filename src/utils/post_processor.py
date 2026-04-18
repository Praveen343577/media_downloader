import os
import glob
import shutil

class PostProcessor:
    @staticmethod
    def relocate_youtube_metadata(channel_dir: str, video_id: str) -> None:
        metadata_dir = os.path.join(channel_dir, "metadata")
        os.makedirs(metadata_dir, exist_ok=True)
        
        search_pattern = os.path.join(channel_dir, f"*{video_id}*")
        associated_files = glob.glob(search_pattern)
        
        for file_path in associated_files:
            if not os.path.isfile(file_path):
                continue
                
            ext = os.path.splitext(file_path)[1].lower()
            if ext in [".json", ".webp", ".jpg", ".jpeg", ".png"]:
                try:
                    shutil.move(file_path, os.path.join(metadata_dir, os.path.basename(file_path)))
                except OSError:
                    pass