from pathlib import Path
from urllib.parse import urlparse

from config import settings


def prepare_video_placeholder(video_url: str) -> dict:
    parsed = urlparse(video_url)
    filename = Path(parsed.path).name or "video.mp4"
    fake_local_path = str(Path(settings.RAW_VIDEO_DIR) / filename)

    return {
        "video_url": video_url,
        "local_video_path": fake_local_path,
        "audio_path": str(Path(settings.AUDIO_DIR) / f"{Path(filename).stem}.mp3"),
        "frame_paths": [
            str(Path(settings.FRAME_DIR) / f"{Path(filename).stem}_frame_{i}.jpg")
            for i in range(1, settings.ANALYSIS_MAX_FRAMES + 1)
        ],
    }
