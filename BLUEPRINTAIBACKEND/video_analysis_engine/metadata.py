from pathlib import Path
import cv2
from .schemas import VideoMetadata
from .utils import format_aspect_ratio


def extract_video_metadata(video_path: Path) -> VideoMetadata:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)

    duration_seconds = (frame_count / fps) if fps > 0 else 0.0
    cap.release()

    return VideoMetadata(
        filename=video_path.name,
        path=str(video_path),
        size_bytes=video_path.stat().st_size,
        duration_seconds=round(duration_seconds, 2),
        width=width,
        height=height,
        fps=round(float(fps), 2),
        aspect_ratio=format_aspect_ratio(width, height),
    )
