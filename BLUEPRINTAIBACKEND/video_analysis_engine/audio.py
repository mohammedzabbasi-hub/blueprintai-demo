from pathlib import Path
import subprocess
from .config import AUDIO_DIR


def extract_audio(video_path: Path) -> Path:
    output_dir = AUDIO_DIR / video_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_path = output_dir / f"{video_path.stem}.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(audio_path),
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        no_audio_markers = [
            "Output file does not contain any stream",
            "Stream map 'a' matches no streams",
            "does not contain any stream",
        ]
        if any(marker in result.stderr for marker in no_audio_markers):
            return audio_path

        raise RuntimeError(f"FFmpeg audio extraction failed: {result.stderr}")

    return audio_path
