from pydantic import BaseModel


class CreativeOut(BaseModel):
    id: int
    shop_id: int
    product_id: int | None = None

    product: str
    title: str
    creator: str

    creator_type: str | None = None
    creator_archetype: str | None = None
    ad_type: str | None = None
    hook_type: str | None = None
    speaking_style: str | None = None
    demo_style: str | None = None
    cta_style: str | None = None

    thumbnail: str | None = None
    insight: str | None = None

    score: int | None = None
    views: int = 0
    likes: int = 0
    shares: int = 0
    clicks: int = 0
    orders: int = 0
    date: str | None = None

    model_config = {"from_attributes": True}


class CreativeSyncResponse(BaseModel):
    message: str
    imported_count: int
