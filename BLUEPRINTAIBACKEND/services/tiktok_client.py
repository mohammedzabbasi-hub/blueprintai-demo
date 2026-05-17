import hashlib
import hmac
import json
import time
from urllib.parse import urlencode

import requests

from config import settings


class TikTokClient:
    def __init__(self, access_token: str | None = None):
        self.base_url = settings.TIKTOK_API_BASE_URL.rstrip("/")
        self.client_id = settings.TIKTOK_CLIENT_ID
        self.client_secret = settings.TIKTOK_CLIENT_SECRET
        self.access_token = access_token

    def _headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["x-tts-access-token"] = self.access_token
        return headers

    def _build_sign(self, path: str, params: dict) -> str:
        payload = path + "".join(f"{k}{v}" for k, v in sorted(params.items()))
        return hmac.new(
            self.client_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def _request(self, method: str, path: str, params: dict | None = None, data: dict | None = None) -> dict:
        params = params or {}
        params.setdefault("app_key", self.client_id)
        params.setdefault("timestamp", int(time.time()))
        params["sign"] = self._build_sign(path, params)

        url = f"{self.base_url}{path}"
        response = requests.request(
            method=method,
            url=url,
            headers=self._headers(),
            params=params,
            json=data,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def exchange_auth_code(self, auth_code: str) -> dict:
        return self._request(
            "POST",
            "/authorization/202309/token/get",
            data={
                "auth_code": auth_code,
                "grant_type": "authorized_code",
            },
        )

    def refresh_access_token(self, refresh_token: str) -> dict:
        return self._request(
            "POST",
            "/authorization/202309/refresh_token",
            data={"refresh_token": refresh_token},
        )

    def get_authorization_url(self, state: str) -> str:
        query = urlencode(
            {
                "app_key": self.client_id,
                "state": state,
                "redirect_uri": settings.TIKTOK_REDIRECT_URI,
            }
        )
        return f"{self.base_url}/api/v2/platform/oauth/connect/?{query}"

    def get_shop_info(self) -> dict:
        return self._request("GET", "/seller/202309/shops")

    def get_products(self, page_number: int = 1, page_size: int = 50) -> dict:
        return self._request(
            "POST",
            "/product/202309/products/search",
            data={
                "page_number": page_number,
                "page_size": page_size,
            },
        )

    def get_orders(self, page_number: int = 1, page_size: int = 50) -> dict:
        return self._request(
            "POST",
            "/order/202309/orders/search",
            data={
                "page_number": page_number,
                "page_size": page_size,
            },
        )

    def get_mock_creatives(self) -> list[dict]:
        return [
            {
                "product": "GlowPatch",
                "title": "3-second acne fix demo",
                "creator": "Ava Lee",
                "thumbnail": "/static/glowpatch-1.jpg",
                "video_url": "https://www.tiktok.com/@example/video/1000000001",
                "insight": "Strong early hook and fast product payoff.",
                "score": 91,
                "views": 1200000,
                "likes": 54000,
                "shares": 3200,
                "clicks": 18000,
                "orders": 2400,
                "date": "2024-03-10",
            },
            {
                "product": "LuxeGlow",
                "title": "Morning routine tutorial",
                "creator": "Mia Chen",
                "thumbnail": "/static/luxeglow-1.jpg",
                "video_url": "https://www.tiktok.com/@example/video/1000000002",
                "insight": "Tutorial-style content performs well for this product.",
                "score": 86,
                "views": 860000,
                "likes": 41000,
                "shares": 2100,
                "clicks": 12400,
                "orders": 1700,
                "date": "2024-03-14",
            },
        ]
