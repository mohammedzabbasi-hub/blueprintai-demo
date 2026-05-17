import json
from datetime import datetime
from typing import Any


def utc_now_iso() -> str:
    return datetime.utcnow().isoformat()


def safe_json_dumps(value: Any) -> str:
    try:
        return json.dumps(value, default=str)
    except Exception:
        return "{}"


def safe_json_loads(value: str | None, default=None):
    if default is None:
        default = {}
    if not value:
        return default
    try:
        return json.loads(value)
    except Exception:
        return default


def compact_text(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = " ".join(value.split())
    return cleaned.strip() or None


def top_items(counter_like: dict[str, int], limit: int = 5) -> list[tuple[str, int]]:
    return sorted(counter_like.items(), key=lambda item: item[1], reverse=True)[:limit]
