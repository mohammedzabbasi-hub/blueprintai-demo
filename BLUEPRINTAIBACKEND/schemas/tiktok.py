from datetime import datetime
from pydantic import BaseModel


class TikTokAuthStartOut(BaseModel):
    auth_url: str
    state: str


class TikTokTokenExchangeRequest(BaseModel):
    auth_code: str
    state: str | None = None


class TikTokTokenOut(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None
    access_token_expires_at: datetime | None = None
    refresh_token_expires_at: datetime | None = None


class TikTokSyncResponse(BaseModel):
    shop_id: int
    products_synced: int
    orders_synced: int
    creatives_synced: int
    briefs_generated: int
    recommendations_count: int
    shop_refreshed: bool
