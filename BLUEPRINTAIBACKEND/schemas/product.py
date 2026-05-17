from pydantic import BaseModel, Field


class ProductOut(BaseModel):
    id: int
    shop_id: int
    name: str
    category: str | None = None
    price: float | None = None

    model_config = {"from_attributes": True}


class ProductSyncResponse(BaseModel):
    message: str = "Products synced successfully"
    imported_count: int


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    category: str | None = None
    price: float | None = None
