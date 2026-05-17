from pathlib import Path
import uuid


def generate_id() -> str:
    return uuid.uuid4().hex


def safe_filename(filename: str) -> str:
    path = Path(filename)
    stem = "".join(c for c in path.stem if c.isalnum() or c in ("-", "_")).strip()
    ext = path.suffix.lower()
    if not stem:
        stem = "video"
    return f"{stem}_{generate_id()}{ext}"


def format_aspect_ratio(width: int, height: int) -> str:
    if height == 0:
        return "unknown"
    return f"{width}:{height}"


def chunk_list(items, size):
    for i in range(0, len(items), size):
        yield items[i:i + size]
