from pydantic import BaseModel


class RecommendationOut(BaseModel):
    id: int | None = None
    category: str
    rec_type: str | None = None
    name: str
    reason: str | None = None
    confidence: int | None = None

    model_config = {"from_attributes": True}
