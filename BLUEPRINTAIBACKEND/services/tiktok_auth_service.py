import secrets
from datetime import datetime, timedelta, UTC

from services.tiktok_client import TikTokClient


def get_tiktok_oauth_url() -> tuple[str, str]:
    state = secrets.token_urlsafe(24)
    client = TikTokClient()
    return client.get_authorization_url(state), state


def exchange_code_for_tokens(auth_code: str) -> dict:
    client = TikTokClient()
    token_data = client.exchange_auth_code(auth_code)

    data = token_data.get("data", {})
    return {
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token"),
        "access_token_expires_at": datetime.now(UTC) + timedelta(seconds=int(data.get("access_token_expire_in", 0) or 0)),
        "refresh_token_expires_at": datetime.now(UTC) + timedelta(seconds=int(data.get("refresh_token_expire_in", 0) or 0)),
        "raw": token_data,
    }


def refresh_tokens(refresh_token: str) -> dict:
    client = TikTokClient()
    token_data = client.refresh_access_token(refresh_token)

    data = token_data.get("data", {})
    return {
        "access_token": data.get("access_token"),
        "refresh_token": data.get("refresh_token", refresh_token),
        "access_token_expires_at": datetime.now(UTC) + timedelta(seconds=int(data.get("access_token_expire_in", 0) or 0)),
        "refresh_token_expires_at": datetime.now(UTC) + timedelta(seconds=int(data.get("refresh_token_expire_in", 0) or 0)),
        "raw": token_data,
    }
