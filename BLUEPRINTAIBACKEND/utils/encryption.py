import base64
import hashlib


def mask_secret(value: str | None, visible_chars: int = 4) -> str | None:
    if not value:
        return value
    if len(value) <= visible_chars:
        return "*" * len(value)
    return f"{value[:visible_chars]}{'*' * max(4, len(value) - visible_chars)}"


def fingerprint_value(value: str | None) -> str | None:
    if not value:
        return None
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def encode_text(value: str) -> str:
    return base64.b64encode(value.encode("utf-8")).decode("utf-8")


def decode_text(value: str) -> str:
    return base64.b64decode(value.encode("utf-8")).decode("utf-8")
