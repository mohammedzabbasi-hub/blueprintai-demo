from urllib.parse import urlparse


def is_valid_url(url: str | None) -> bool:
    if not url:
        return False
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)


def is_tiktok_url(url: str | None) -> bool:
    if not is_valid_url(url):
        return False
    host = urlparse(url).netloc.lower()
    return "tiktok.com" in host
