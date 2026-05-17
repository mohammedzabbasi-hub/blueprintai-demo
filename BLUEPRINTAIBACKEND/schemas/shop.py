from pydantic import BaseModel


class ShopOut(BaseModel):
    id: int
    user_id: int
    shop_name: str
    tiktok_shop_id: str

    model_config = {"from_attributes": True}


class ShopConnectResponse(BaseModel):
    message: str
    shop: ShopOut | None = None
    auth_url: str | None = None
