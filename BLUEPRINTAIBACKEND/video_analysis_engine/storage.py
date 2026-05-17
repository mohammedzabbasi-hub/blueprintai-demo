from pathlib import Path
from .config import UPLOAD_DIR, validate_video_extension
from .utils import safe_filename


def save_uploaded_file(file_bytes: bytes, original_filename: str) -> Path:
    if not validate_video_extension(original_filename):
        raise ValueError(f"Unsupported video extension: {original_filename}")

    filename = safe_filename(original_filename)
    output_path = UPLOAD_DIR / filename

    with open(output_path, "wb") as f:
        f.write(file_bytes)

    return output_path
