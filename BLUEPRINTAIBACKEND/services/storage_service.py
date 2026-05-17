import os
from pathlib import Path

from config import settings


def ensure_upload_dir() -> Path:
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir


def save_uploaded_file(filename: str, content: bytes) -> str:
    upload_dir = ensure_upload_dir()
    file_path = upload_dir / filename

    with open(file_path, "wb") as f:
        f.write(content)

    return str(file_path)


def delete_file(path: str) -> bool:
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
