from pathlib import Path
import cv2
from .config import FRAMES_DIR, DEFAULT_FRAME_INTERVAL_SECONDS, DEFAULT_MAX_FRAMES
from .schemas import FrameData


def extract_key_frames(
    video_path: Path,
    interval_seconds: int = DEFAULT_FRAME_INTERVAL_SECONDS,
    max_frames: int = DEFAULT_MAX_FRAMES,
) -> list[FrameData]:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Could not open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 0.0
    if fps <= 0:
        cap.release()
        raise ValueError("Invalid FPS; cannot extract frames.")

    frame_step = int(fps * interval_seconds)
    if frame_step <= 0:
        frame_step = 1

    output_dir = FRAMES_DIR / video_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    frames: list[FrameData] = []
    current_frame = 0
    saved_count = 0

    while cap.isOpened() and saved_count < max_frames:
        success, frame = cap.read()
        if not success:
            break

        if current_frame % frame_step == 0:
            timestamp = current_frame / fps
            image_path = output_dir / f"frame_{saved_count:03d}.jpg"
            cv2.imwrite(str(image_path), frame)

            frames.append(
                FrameData(
                    timestamp_seconds=round(timestamp, 2),
                    image_path=str(image_path),
                )
            )
            saved_count += 1

        current_frame += 1

    cap.release()
    return frames
