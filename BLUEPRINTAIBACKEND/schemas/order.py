from datetime import datetime
from pydantic import BaseModel


class OrderOut(BaseModel):
    id: int
    shop_id: int
    tiktok_order_id: str
    buyer_name: str | None = None
    order_status: str | None = None
    currency: str | None = None
    total_amount: float | None = None
    raw_payload: str | None = None
    placed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class OrderSyncResponse(BaseModel):
    message: str = "Orders synced successfully"
    imported_count: int
