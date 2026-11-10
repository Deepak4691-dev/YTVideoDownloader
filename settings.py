import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
THUMBNAILS_DIR = os.path.join(BASE_DIR, "thumbnails")
DATABASE_FILE = os.path.join(DATA_DIR, "ytvideod.db")
DEFAULT_DOWNLOAD_FOLDER = DOWNLOADS_DIR
DEFAULT_QUALITY = "Best Available"
QUALITY_OPTIONS = [
    "Best Available", "2160p", "1440p", "1080p",
    "720p", "480p", "360p"
]

def create_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    os.makedirs(THUMBNAILS_DIR, exist_ok=True)

create_directories()
